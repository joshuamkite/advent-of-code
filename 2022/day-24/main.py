from collections import deque

# Directions: up, down, left, right
DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


class Valley:
    def __init__(self, file_name):
        """ Initialize the Valley object by parsing the input file """
        grid, blizzards, start, exit = self.parse_input(file_name)
        self.grid = grid  # The grid map (list of lists)
        self.blizzards = blizzards  # List of blizzards [(x, y, direction)]
        self.start = start  # Start position (entry point)
        self.exit = exit  # Exit position (goal)
        self.max_x = len(grid)
        self.max_y = len(grid[0])

    def get_neighbors(self, position):
        """ Get all neighboring positions (up, down, left, right, wait) """
        x, y = position
        possible_moves = [(x + dx, y + dy) for dx, dy in DIRECTIONS.values()]
        possible_moves.append((x, y))  # Include the option to wait in place
        return possible_moves

    def is_valid_move(self, position, minute):
        """ Check if the move to 'position' is valid at 'minute' """
        x, y = position

        # Ensure position is within bounds and not a wall
        if not (0 <= x < self.max_x and 0 <= y < self.max_y):
            return False
        if self.grid[x][y] == '#':  # Wall check
            return False

        # Check if blizzards are at this position at this minute
        for blizzard_x, blizzard_y, direction in self.blizzards:
            if self.get_blizzard_position((blizzard_x, blizzard_y, direction), minute) == position:
                return False

        return True

    def get_blizzard_position(self, blizzard, minute):
        """ Calculate the position of a blizzard at a given minute """
        x, y, direction = blizzard
        dx, dy = DIRECTIONS[direction]

        # Move blizzard according to its direction
        if direction in ['<', '>']:
            # Wrap horizontally, skipping walls
            new_y = (y + dy * minute - 1) % (self.max_y - 2) + 1  # Wrapping between 1 and max_y - 2 (skipping walls)
            new_x = x  # Horizontal movement doesn't affect the row
        elif direction in ['^', 'v']:
            # Wrap vertically, skipping walls
            new_x = (x + dx * minute - 1) % (self.max_x - 2) + 1  # Wrapping between 1 and max_x - 2 (skipping walls)
            new_y = y  # Vertical movement doesn't affect the column

        return (new_x, new_y)

    def print_grid(self, player_position, minute):
        """ Print the grid with blizzard positions and the player's position for debugging without modifying the actual grid """

        # Create a deep copy of the grid to modify with blizzards and player for debugging purposes
        grid_copy = [row[:] for row in self.grid]

        # Dictionary to track how many blizzards are at each position
        blizzard_count = {}

        # Count blizzards at each position based on the current minute
        for blizzard_x, blizzard_y, direction in self.blizzards:
            bx, by = self.get_blizzard_position((blizzard_x, blizzard_y, direction), minute)
            if (bx, by) in blizzard_count:
                blizzard_count[(bx, by)] += 1
            else:
                blizzard_count[(bx, by)] = 1

        # Add blizzards to the grid copy for debugging
        for (bx, by), count in blizzard_count.items():
            if count == 1:
                # Only one blizzard at this position, show the direction
                for blizzard_x, blizzard_y, direction in self.blizzards:
                    if self.get_blizzard_position((blizzard_x, blizzard_y, direction), minute) == (bx, by):
                        grid_copy[bx][by] = direction
                        break
            else:
                # More than one blizzard, show the number of blizzards
                grid_copy[bx][by] = str(count)

        # Add the player's position to the grid for debugging
        px, py = player_position
        grid_copy[px][py] = 'E'  # 'E' for the player's position

        # Print the grid row by row for debugging
        print(f"Minute {minute}:")
        for row in grid_copy:
            print(''.join(row))
        print()  # Add a blank line for better readability

    def bfs(self):
        """ Perform BFS to find the shortest path from start to exit """
        queue = deque()
        visited = set()
        current_minute_printed = -1  # To ensure we only print once per minute

        # Start BFS with the initial position and minute 0
        queue.append((self.start, 0))  # (position, minute)
        visited.add((self.start, 0))   # (position, minute)

        while queue:
            current_position, current_minute = queue.popleft()

            # Only print the grid when we move to a new minute
            if current_minute != current_minute_printed:
                self.print_grid(current_position, current_minute)  # Debugging print
                current_minute_printed = current_minute  # Update to prevent duplicate prints

            # If we reached the exit, return the number of minutes
            if current_position == self.exit:
                print(f"Reached the exit in {current_minute} minutes")
                return current_minute

            # Get all possible moves (neighbors + wait)
            neighbors = self.get_neighbors(current_position)
            next_minute = current_minute + 1

            can_wait = True  # Track whether waiting is needed

            # Try moving to neighbors
            for neighbor in neighbors:
                # Ensure the move is valid at the next minute
                if self.is_valid_move(neighbor, next_minute):
                    can_wait = False  # If a valid move exists, no need to wait
                    if (neighbor, next_minute) not in visited:
                        queue.append((neighbor, next_minute))
                        visited.add((neighbor, next_minute))

            # If no valid moves exist, stay in place (wait)
            if can_wait and (current_position, next_minute) not in visited:
                queue.append((current_position, next_minute))  # Stay in the same position
                visited.add((current_position, next_minute))

        # If we exhaust the queue without finding a path, return failure
        print("No valid path found")
        return -1

    def parse_input(self, file_name):
        """ Parse the input file to get the grid, blizzards, start, and exit points """
        grid = []
        blizzards = []
        start = None
        exit = None

        with open(file_name, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                grid.append(list(line))

                # Find blizzards and their directions
                for j, char in enumerate(line):
                    if char in DIRECTIONS:
                        blizzards.append((i, j, char))

                # Identify entry and exit points (non-wall in top and bottom rows)
                if i == 0:  # Top row
                    for j, char in enumerate(line):
                        if char == '.':
                            start = (i, j)
                elif i == len(lines) - 1:  # Bottom row
                    for j, char in enumerate(line):
                        if char == '.':
                            exit = (i, j)

        return grid, blizzards, start, exit


if __name__ == "__main__":
    # Parse the input file to get the grid, blizzards, and start/exit points
    file_name = 'test.txt'

    # Create the Valley object (parse input happens inside __init__)
    valley = Valley(file_name)

    # Run the BFS to find the shortest path
    minutes = valley.bfs()
    print(f"Fewest number of minutes to reach the exit: {minutes}")
