
class Item:
    """Represents things you can pick up."""
    def __init__(self, name, value=10, symbol="🥝", count=1):
        self.name = name
        self.value = value
        self.symbol = symbol
        self.count = count

    def __str__(self):
        return self.symbol


pickups = [Item("carrot", value=15,symbol="🥕",count=3), 
           Item("apple", value=20, symbol="🍎", count=2), 
           Item("strawberry", value=50, symbol="🍓", count=1), 
           Item("cherry", value=40, symbol="🍒", count=1), 
           Item("watermelon", value=20, symbol="🍉", count=2), 
           Item("kiwi", value=20, symbol="🥝", count=2), 
           Item("cucumber", value=15, symbol="🥒", count=3), 
           Item("doughnut", value=10, symbol="🍔", count=6)
        ]

def randomize(grid):
    for item in pickups:

        for i in range(item.count):
            while True:
                # randomise a position till we find one that is empty
                x = grid.get_random_x()
                y = grid.get_random_y()
                if grid.is_empty(x, y):
                    grid.set(x, y, item)
                    break  # break the while loop, continue with the next iteration of the for loop