from .grid import Grid
from .player import Player
from . import pickups



player = Player(2, 1)
score = 0
inventory = []

g = Grid()
g.set_player(player)
g.make_walls()
pickups.randomize(g)


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)


command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]

    if command == "d":
        maybe_item = player.move_right(g)

    elif command == "a":
        maybe_item = player.move_left(g)
    
    elif command == "w":
        maybe_item = player.move_up(g)
        
    elif command == "s":
        maybe_item = player.move_down(g)

    if isinstance(maybe_item, pickups.Item):
        # we found something
        score += maybe_item.value
        print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
        #g.set(player.pos_x, player.pos_y, g.empty)
        g.clear(player.pos_x, player.pos_y)


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
