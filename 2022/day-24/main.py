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

    def bfs(self, start, goal, start_time):
        """ Perform the BFS-like search to find the shortest time from start to goal """
        current = [start]
        time = start_time

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

            # If we reached the goal, return the time (no need to add 1)
            if goal in current:
                return time  # Return the current minute without adding 1

            time += 1

    def solve_part_1(self):
        """ Solve Part 1 by finding the shortest path from start to goal """
        return self.bfs(self.start, self.end, 0)

    def solve_part_2(self):
        """ Solve Part 2 by going to the goal, back to start, then to the goal again """
        # First trip: from start to goal
        time_to_goal = self.bfs(self.start, self.end, 0)

        # Second trip: from goal back to start
        time_back_to_start = self.bfs(self.end, self.start, time_to_goal)

        # Third trip: from start to goal again
        final_time_to_goal = self.bfs(self.start, self.end, time_back_to_start)

        # Total time is the sum of all three trips
        return final_time_to_goal


if __name__ == "__main__":
    file_name = 'input.txt'
    valley = Valley(file_name)

    # Solve Part 1
    minutes_part_1 = valley.solve_part_1()
    print(f"Fewest number of minutes to reach the exit (Part 1): {minutes_part_1}")

    # Solve Part 2
    total_minutes_part_2 = valley.solve_part_2()
    print(f"Fewest number of minutes to complete all trips (Part 2): {total_minutes_part_2}")
