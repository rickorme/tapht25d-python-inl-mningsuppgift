from src import debug


class Player:
    
    marker = "🤤"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    # Move the player. "dx" and "dy" are the differences in x and y coordinates, respectively.
    def move(self, dx, dy, grid):
        """Move the player.\n
        dx = horizontal movement, from left to right\n
        dy = vertical movement, from top to bottom"""
        self.pos_x += dx
        self.pos_y += dy
        return self.get_item(grid)

    def can_move(self, x, y, grid):
        return not grid.is_obstruction(self.pos_x + x, self.pos_y + y)
        
    def can_jump(self, x, y, grid):
        """Allow the player to jump 2 spaces if there is no obstruction in the way
        and they are within the bounds of the grid."""
        debug.debug_print(f"Checking if player can jump to ({self.pos_x + 2*x}, {self.pos_y + 2*y})")
        if (
            grid.coordinates_within_bounds(self.pos_x + 2*x, self.pos_y + 2*y) \
            and not grid.is_obstruction(self.pos_x + 2*x, self.pos_y + 2*y) 
            ):            
            return True, 2
        elif self.can_move(x, y, grid):
            return True, 1
        else:
            return False, 0

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
        
    def jump_right(self, grid):
        x=1
        y=0
        can_jump, jump_distance = self.can_jump(x, y, grid)
        if can_jump:
            collected_item = self.move(jump_distance*x, jump_distance*y, grid)
            return collected_item
        
    def jump_left(self, grid):
        x=-1
        y=0
        can_jump, jump_distance = self.can_jump(x, y, grid)
        if can_jump:
            collected_item = self.move(jump_distance*x, jump_distance*y, grid)
            return collected_item
        
    def jump_up(self, grid):    
        x=0
        y=-1
        can_jump, jump_distance = self.can_jump(x, y, grid)
        if can_jump:
            collected_item = self.move(jump_distance*x, jump_distance*y, grid)
            return collected_item
        
    def jump_down(self, grid):
        x=0
        y=1
        can_jump, jump_distance = self.can_jump(x, y, grid)
        if can_jump:
            collected_item = self.move(jump_distance*x, jump_distance*y, grid)
            return collected_item

    def get_item(self, grid):
        return grid.get(self.pos_x, self.pos_y)   