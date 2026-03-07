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

def set_turd_traps(grid):
    for i in range(turd_trap.count):
        while True:
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, turd_trap)
                break