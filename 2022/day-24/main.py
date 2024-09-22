from collections import deque

# Directions: up, down, left, right
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]  # Adding wait (0, 0)


class Valley:
    def __init__(self, file_name):
        """ Initialize the Valley object by parsing the input file """
        self.rows, self.cols, self.width, self.height, self.start, self.end = self.parse_input(file_name)

    def parse_input(self, file_name):
        """ Parse the input file to get the grid, blizzards, start, and exit points """
        with open(file_name, 'r') as file:
            rows = [list(line.strip()) for line in file]

        width = len(rows[0])
        height = len(rows)

        # Columns for easy blizzard checking
        cols = [[rows[y][x] for y in range(height)] for x in range(width)]

        # Start and end points (where '.' is in the first and last rows)
        start = [(i, 0) for i, val in enumerate(rows[0]) if val == '.'][0]  # Find start
        end = [(i, height - 1) for i, val in enumerate(rows[-1]) if val == '.'][0]  # Find end

        return rows, cols, width, height, start, end

    def wrapped(self, n, maxn):
        """ Wrap the position for blizzard movement """
        return (n - 1) % (maxn - 2) + 1

    def bfs(self):
        """ Perform the BFS-like search to find the shortest time """
        current = [self.start]
        time = 0

        while True:
            next_positions = []
            for pos in current:
                for dx, dy in DIRECTIONS:
                    x, y = pos[0] + dx, pos[1] + dy

                    # Filter positions that are out of bounds or hit walls
                    if y < 0 or y >= self.height or self.cols[x][y] == '#':
                        continue

                    # Check horizontal blizzards '<' and '>'
                    if self.rows[y][self.wrapped(x + time, self.width)] == '<' or \
                       self.rows[y][self.wrapped(x - time, self.width)] == '>':
                        continue

                    # Check vertical blizzards '^' and 'v'
                    if self.cols[x][self.wrapped(y + time, self.height)] == '^' or \
                       self.cols[x][self.wrapped(y - time, self.height)] == 'v':
                        continue

                    next_positions.append((x, y))

            # Sort and remove duplicates
            current = sorted(set(next_positions))

            # If we reached the end, return the time
            if self.end in current:
                return time

            time += 1


if __name__ == "__main__":
    file_name = 'input.txt'
    valley = Valley(file_name)
    minutes = valley.bfs()
    print(f"Fewest number of minutes to reach the exit: {minutes}")
