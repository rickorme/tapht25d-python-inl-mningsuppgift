import re


class Player:
    marker = "🤤"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy, grid):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy
        return self.get_item(grid)

    def can_move(self, x, y, grid):
        return not grid.is_obstruction(self.pos_x + x, self.pos_y + y)

    def move_right(self, grid):
        x=1
        y=0
        if self.can_move(x, y, grid):
            collected_item = self.move(x, y, grid)
            return collected_item

    def move_left(self, grid):
        x=-1
        y=0
        if self.can_move(x, y, grid):
            collected_item = self.move(x, y, grid)
            return collected_item

    def move_up(self, grid):    
        x=0
        y=-1
        if self.can_move(x, y, grid):
            collected_item = self.move(x, y, grid)
            return collected_item

    def move_down(self, grid):
        x=0
        y=1
        if self.can_move(x, y, grid):
            collected_item = self.move(x, y, grid)
            return collected_item

    def get_item(self, grid):
        return grid.get(self.pos_x, self.pos_y)   


