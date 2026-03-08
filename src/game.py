from .grid import Grid
from .player import Player
from .enemy import spawn_enemies
from . import debug
from . import pickups
from . import specials


score = 0
inventory = []
show_inventory = False
grace_period = 0

g = Grid()
g.make_walls()
g.make_inner_walls()
specials.set_turd_traps(g)
specials.set_exit(g)
player = Player(*g.get_random_center_pos()) # "splat" the tuple into x and y
g.set_player(player)
spawn_enemies(g)
pickups.randomize(g)


# TODO: move this to a separate file
def print_status(game_grid):
    """Show the game status and other information."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)
    if show_inventory:
        print(f"Inventory: {inventory}")
    if debug.debug_on:
        print("DEBUG MODE ON")
        
command = "a"
# Loop until the user presses Q or X.
while not command.casefold() in ["q", "x"]:
    print_status(g)
    player.marker = "🤤"
    command = input("Use WASD to move, I to toggle inventory, T to cleanup a turd,\n" \
                    "DBG to enable debug mode, Q/X to quit. ")
    command = command.casefold()

    if command in ["w", "a", "s", "d", "jw", "ja", "js", "jd"]:

        if command == "w":
            maybe_item = player.move_up(g)
        elif command == "a":
            maybe_item = player.move_left(g)            
        elif command == "s":
            maybe_item = player.move_down(g)
        elif command == "d":
            maybe_item = player.move_right(g)
        elif command == 'jw':
            maybe_item = player.jump_up(g)
        elif command == 'ja':
            maybe_item = player.jump_left(g)
        elif command == 'js':
            maybe_item = player.jump_down(g)
        elif command == 'jd':
            maybe_item = player.jump_right(g)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            score += maybe_item.value
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            inventory.append(maybe_item.symbol)
            g.clear(player.pos_x, player.pos_y)
            # set the grace period to 5 turns, during which the player won't lose points 
            grace_period = 6 # we set it to 6 because the first turn will immediately reduce it to 5
        
        elif maybe_item == specials.turd_trap:
            print(f"{maybe_item.symbol} You stepped on a turd trap! {maybe_item.value} points.")
            score += maybe_item.value
            player.marker = "🤮"

        elif maybe_item == specials.exit:
            # If the player has collected all the pickups, they can win by stepping on the exit 
            if len(inventory) == sum(item.count for item in pickups.pickups):
                print(f"{maybe_item.symbol} You found the exit! You win!")
                break

        """ Don't reduce the player's score for moving if they are in the grace period after collecting an item. 
        This gives them a few turns to move around and collect more items without losing points. """
        if grace_period > 0:
            grace_period -= 1
        else:
            score = max(0, score - 1)  # take away 1 point for each move, but don't go below 0  

        ''' Enemy movement should happen after the player has moved, but before we print the status again.
        This way, the player can see the consequences of their move (like stepping on a trap or picking up an item) before the enemies move. '''
        for enemy in g.enemies:
            enemy.hone_in_on_player(player, g)
            if enemy.pos_x == player.pos_x and enemy.pos_y == player.pos_y:
                print(f"{enemy.marker} An enemy got you! {enemy.harm} points.")
                score += enemy.harm
                player.marker = "🤕"
                # remove the enemy from the grid            
                g.remove_enemy(enemy)

    elif command == "i":
        show_inventory= not show_inventory

    elif command == "dbg":
        debug.toggle_debug()

    elif command == "t":
        # Check if there is a trap in the adjacent cells, if so disarm it and remove it from the grid
        objects = g.get_objects_around_player()
        for obj in objects:
            if obj[0] == specials.turd_trap:
                print(f"You cleaned up a turd trap!")
                g.clear(obj[1], obj[2])  # obj[1] is x, obj[2] is y
                g.set(obj[1], obj[2], "🧻")  # Clear the trap from the grid
                break


# This is where we end up when the while loop ends.
print("Thank you for playing!")
