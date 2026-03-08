import random

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 30
    height = 22
    empty = "⚫"  # Tecken för en tom ruta
    wall = "🧱"   # Tecken för en ogenomtränglig vägg

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]
        self.player = None
        self.enemies = []

    def is_obstruction(self, x, y):
        """Returnerar True om det inte går att gå på den aktuella rutan"""
        return self.get(x, y) == self.wall
    
    def is_enemy(self, x, y):
        """Return True if there is an enemy on the current tile"""
        for enemy in self.enemies:
            if enemy.pos_x == x and enemy.pos_y == y:
                return True
        return False

    def get(self, x, y):
        """Hämta det som finns på en viss position"""
        return self.data[y][x]

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        self.player = player

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)

    def get_random_center_pos(self, percentage=30):
        """
        Returns a random (x, y) coordinate near the center of the grid.
        percentage: Defines how large the central area is, as a percentage of the total grid size.
        For example, if percentage=30, the central area will be 30% of the grid's width and height.
        """
        # 1. Calculate the dimensions of the inner "spawn" box
        # We use max(1, ...) to ensure the box is always at least 1x1
        box_width = max(1, int(self.width * (percentage/100)))
        box_height = max(1, int(self.height * (percentage/100)))
        
        # 2. Calculate the top-left starting point of this box
        min_x = (self.width - box_width) // 2
        min_y = (self.height - box_height) // 2
        
        # 3. Calculate the bottom-right ending point
        max_x = min_x + box_width - 1
        max_y = min_y + box_height - 1
        
        # 4. Pick a random coordinate within these limits
        # Check to ensure we get an empty position
        empty_pos = False
        while not empty_pos:
            spawn_x = random.randint(min_x, max_x)
            spawn_y = random.randint(min_y, max_y)
            empty_pos = self.is_empty(spawn_x, spawn_y)

        return spawn_x, spawn_y

    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += self.player.marker
                
                else: 
                    # Check for enemies on this tile
                    enemy_here = False
                    for enemy in self.enemies:
                        if x == enemy.pos_x and y == enemy.pos_y:
                            xs += enemy.marker
                            enemy_here = True
                            break
                    if not enemy_here:
                        xs += str(row[x])
            xs += "\n"
        return xs


    def make_walls(self):
        """Creates walls around the edges of the grid."""
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

    def get_valid_turn(self, possible_moves, current_direction, cw_count, ccw_count, DIRECTIONS):
        """
        Evaluates possible moves, prevents excessive turning, 
        and returns the new direction and updated turn counters.
        """
        # Make a copy of the list so we can safely remove options from it
        options = list(possible_moves)

        while options:
            # Step 1: Randomly select a move
            chosen_move = random.choice(options)

            # Step 2: Determine the direction of rotation
            current_idx = DIRECTIONS.index(current_direction)
            new_idx = DIRECTIONS.index(chosen_move)

            # The Modulo (%) operator is the secret to circular array math!
            is_straight = (new_idx == current_idx)
            is_cw = (new_idx == (current_idx + 1) % 4)
            is_ccw = (new_idx == (current_idx - 1) % 4)

            # Step 3: Check if rotation should NOT be allowed
            if is_cw and cw_count >= 2:
                options.remove(chosen_move)
                continue  # Jump back up to the start of the while loop
                
            if is_ccw and ccw_count >= 2:
                options.remove(chosen_move)
                continue

            # Step 4: Rotation is allowed! Update counters and return
            if is_cw:
                return chosen_move, cw_count + 1, 0
            elif is_ccw:
                return chosen_move, 0, ccw_count + 1
            elif is_straight:
                return chosen_move, 0, 0  # Going straight resets the boxing-in counters

        # UNLESS: There are no more valid moves left in the options list
        return None, cw_count, ccw_count

    def make_inner_walls(self):
        """Create random inner walls on the grid, with logic to prevent boxing in areas."""
        # generate a random number of walls to create, between 3 and 8
        num_of_walls = random.randint(3, 8)
        print(f"Creating {num_of_walls} inner walls...")
        
        # Named tuples for better readability when checking directions
        no_direction = (0, 0)
        up = (0, -1)
        right = (1, 0)
        down = (0, 1)
        left = (-1, 0)

        # Directions strictly in CLOCKWISE order, to help with the logic of preventing boxing in
        DIRECTIONS = [up, right, down, left]

        # generate a random length for each wall, between 1 and 15
        for wall in range(num_of_walls):
            wall_length =random.randint(1,15)

            # Find an empty position to start the wall
            wall_started = False
            while not wall_started:
                start_x = self.get_random_x()
                start_y = self.get_random_y()
                if self.is_empty(start_x, start_y):
                    self.set(start_x, start_y, self.wall)
                    # print(f"Starting wall {wall+1} at ({start_x}, {start_y}) with length {wall_length}.")
                    wall_started = True
                    x, y = start_x, start_y

            # Trackers to prevent boxing in
            consecutive_clockwise = 0
            consecutive_anticlockwise = 0    
            current_direction = no_direction                

            for i in range(wall_length):
                # check all available moves from the current position
                possible_moves = []

                for dx, dy in DIRECTIONS:
                    check_x = x + dx
                    check_y = y + dy
                    # print(f"Checking position ({check_x}, {check_y}) for wall placement.")
                    if self.is_empty(check_x, check_y):
                        possible_moves.append((dx, dy))

                if not possible_moves:
                    # print("No more possible moves for this wall. Final length: ", i)
                    break  # no more moves available, stop building this wall
                else:

                    if current_direction == no_direction:
                        # if this is the first move, just pick a random direction
                        current_direction = random.choice(possible_moves)
                        new_direction = current_direction
                        # print(f"First move for wall {wall+1}: {new_direction}")
                    else:
                        # print(f"Possible moves for wall {wall+1}: {possible_moves}, current direction: {current_direction}, CW count: {consecutive_clockwise}, CCW count: {consecutive_anticlockwise}")
                        # first check if we can continue in the same direction
                        can_continue_straight = current_direction in possible_moves
                        # then check if we can turn (but only allow turning if it doesn't lead to excessive turning in the same direction)
                        can_turn = (can_continue_straight and len(possible_moves) > 1) or (can_continue_straight == False)

                        if can_continue_straight and not can_turn:
                            new_direction = current_direction
                            consecutive_clockwise = 0
                            consecutive_anticlockwise = 0
                        elif can_turn and not can_continue_straight:
                            
                            new_direction, consecutive_clockwise, consecutive_anticlockwise = self.get_valid_turn(
                                possible_moves, 
                                current_direction, 
                                consecutive_clockwise, 
                                consecutive_anticlockwise, 
                                DIRECTIONS
                            )

                            # Check if a valid move was actually found
                            if new_direction is None:
                                break  # Wall is trapped, stop building it
                        else:
                            
                            # 90% chance to go straight, IF straight is actually an option
                            if random.randint(1, 10) <= 9:
                                new_direction = current_direction
                            else:
                                new_direction, consecutive_clockwise, consecutive_anticlockwise = self.get_valid_turn(
                                    possible_moves, 
                                    current_direction, 
                                    consecutive_clockwise, 
                                    consecutive_anticlockwise, 
                                    DIRECTIONS
                                )

                                # Check if a valid move was actually found
                                if new_direction is None:
                                    break  # Wall is trapped, stop building it

                    # Move in the chosen direction and place the wall segment
                    x += new_direction[0]
                    y += new_direction[1]
                    self.set(x, y, self.wall)
                    current_direction = new_direction
                    # print(f"Placed wall segment at ({x}, {y}), new direction: {current_direction}, CW count: {consecutive_clockwise}, CCW count: {consecutive_anticlockwise}")
                         


    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""
        return self.get(x, y) == self.empty

