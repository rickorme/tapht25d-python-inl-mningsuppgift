from .grid import Grid
from .player import Player
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
player = Player(*g.get_random_center_pos()) # "splat" the tuple into x and y
g.set_player(player)
pickups.randomize(g)


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)
    if show_inventory:
        print(f"Inventory: {inventory}")


command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, i to toggle inventory, Q/X to quit. ")
    command = command.casefold()[:1]

    if command in ["w", "a", "s", "d"]:

        if command == "w":
            maybe_item = player.move_up(g)
        elif command == "a":
            maybe_item = player.move_left(g)            
        elif command == "s":
            maybe_item = player.move_down(g)
        elif command == "d":
            maybe_item = player.move_right(g)

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

        if grace_period > 0:
            grace_period -= 1
        else:
            score = max(0, score - 1)  # straffa spelaren genom att ta bort poäng     

    elif command == "i":
        show_inventory= not show_inventory


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
