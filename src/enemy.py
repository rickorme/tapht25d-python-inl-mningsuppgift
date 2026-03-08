import random
from tkinter import ALL


no_direction = (0, 0)
up = (0, -1)
right = (1, 0)
down = (0, 1)
left = (-1, 0)

ALL_DIRECTIONS = [up, right, down, left]

class Enemy:
    marker = "👹"
    movement_chance_percent = 50
    harm = -20

    def __init__(self, x, y, marker="👹", movement_chance_percent=50, harm=-20):
        self.pos_x = x
        self.pos_y = y
        self.marker = marker
        self.movement_chance_percent = movement_chance_percent
        self.harm = harm

    # Move enemy in a given direction, if possible
    def move(self, dx, dy, grid):
        """Move the enemy.\n
        dx = horizontal movement, from left to right\n
        dy = vertical movement, from top to bottom"""
        if self.can_move(dx, dy, grid):
            self.pos_x += dx
            self.pos_y += dy

    def can_move(self, x, y, grid):
        return not grid.is_obstruction(self.pos_x + x, self.pos_y + y) and not grid.is_enemy(self.pos_x + x, self.pos_y + y)

    def move_right(self, grid):
        x=1
        y=0
        self.move(x, y, grid)

    def move_left(self, grid):
        x=-1
        y=0
        self.move(x, y, grid)

    def move_up(self, grid):    
        x=0
        y=-1
        self.move(x, y, grid)

    def move_down(self, grid):
        x=0
        y=1
        self.move(x, y, grid)

    def move_randomly(self, grid):  
        if random.randint(0, 100) < self.movement_chance_percent:
            direction = random.choice(["up", "down", "left", "right"])
            if direction == "up":
                self.move_up(grid)
            elif direction == "down":
                self.move_down(grid)
            elif direction == "left":
                self.move_left(grid)
            elif direction == "right":
                self.move_right(grid)

    def hone_in_on_player(self, player, grid):
        """Move towards the player if possible, otherwise move randomly. 
        The chance of moving is determined by movement_chance_percent."""
        honing_moves = []
        non_honing_moves = ALL_DIRECTIONS.copy()
        
        # Decide whether to move this turn based on movement_chance_percent
        if random.randint(0, 100) >= self.movement_chance_percent:
            return  # Skip movement this turn
        else:
            # Compare the position to the player's position and move in a 
            # direction that brings it closer to the player. 

            if player.pos_x < self.pos_x and self.can_move(-1, 0, grid):
                # Add the left move to the honing moves and remove it from the non-honing moves
                honing_moves.append(left)
                non_honing_moves.remove(left)
            elif player.pos_x > self.pos_x and self.can_move(1, 0, grid):
                # Add the right move to the honing moves and remove it from the non-honing moves
                honing_moves.append(right)
                non_honing_moves.remove(right)
            elif player.pos_y < self.pos_y and self.can_move(0, -1, grid):
                # Add the up move to the honing moves and remove it from the non-honing moves
                honing_moves.append(up)
                non_honing_moves.remove(up)
            elif player.pos_y > self.pos_y and self.can_move(0, 1, grid):
                # Add the down move to the honing moves and remove it from the non-honing moves
                honing_moves.append(down)
                non_honing_moves.remove(down)

            for move in honing_moves:
                # Check if the move is possible, if not remove it from the honing moves
                if not self.can_move(*move, grid):
                    honing_moves.remove(move)

            if honing_moves:
                # randomly choose one of the honing moves
                direction = random.choice(honing_moves)
            else:
                # If there are no honing moves available, randomly choose one of the non-honing moves that are still possible
                for move in non_honing_moves:
                    if not self.can_move(*move, grid):
                        non_honing_moves.remove(move)
                if non_honing_moves:
                    direction = random.choice(non_honing_moves)

            if direction == up:
                self.move_up(grid)
            elif direction == down:
                self.move_down(grid)
            elif direction == left:
                self.move_left(grid)
            elif direction == right:
                self.move_right(grid)
        

enemies = [Enemy(0, 0, marker="👹", movement_chance_percent=60, harm=-50),
           Enemy(0, 0, marker="💀", movement_chance_percent=80, harm=-10),
           Enemy(0, 0, marker="👻", movement_chance_percent=60, harm=-20)]      

def spawn_enemies(grid):
    for enemy in enemies:
    
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                enemy.pos_x = x
                enemy.pos_y = y
                grid.add_enemy(enemy)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen
