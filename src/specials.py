class Special:
    """Represent special objects that can be placed on the grid"""
    def __init__(self, name, symbol, value=0, count=0):
        self.name = name
        self.symbol = symbol
        self.value = value
        self.count = count

    def __str__(self):
        return self.symbol

turd_trap = Special("trap", "💩", value=-10, count=5)

exit = Special("exit", "🚪", value=0, count=1)   

def set_special(grid, special):
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, special)
            break


def set_turd_traps(grid):
    for turd in range(turd_trap.count):
        print(f"turd: {turd}")
        set_special(grid, turd_trap)

def set_exit(grid):
    set_special(grid, exit)