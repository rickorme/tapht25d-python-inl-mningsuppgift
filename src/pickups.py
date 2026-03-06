
class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="🥝"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


pickups = [Item("carrot", value=20,symbol="🥕"), 
           Item("apple", value=20, symbol="🍎"), 
           Item("strawberry", value=20, symbol="🍓"), 
           Item("cherry", value=20, symbol="🍒"), 
           Item("watermelon", value=20, symbol="🍉"), 
           Item("kiwi", value=20, symbol="🥝"), 
           Item("cucumber", value=20, symbol="🥒"), 
           Item("doughnut", value=10, symbol="🍩")
        ]

def randomize(grid):
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen