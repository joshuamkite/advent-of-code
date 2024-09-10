
import heapq


class GridProcessor:
    def __init__(self, input_file):
        self.grid = self.read_input(input_file)
        self.start, self.end = self.find_start_end(self.grid)
        self.elevation_grid = self.map_elevations(self.grid)

    def read_input(self, input_file):
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # convert to list of lists
        grid = [list(line.strip()) for line in lines]

        return grid

    def find_start_end(self, grid):
        start = None
        end = None

        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 'S':
                    start = (i, j)
                elif val == 'E':
                    end = (i, j)
        return start, end

    def find_lows(self):
        lows = []
        for i, row in enumerate(self.elevation_grid):
            for j, val in enumerate(row):
                if val == 0:
                    lows.append([i, j])
        return lows

    def map_elevations(self, grid):
        """
        create a dictionary where the keys are the lowercase letters 'a' to 'z', and the values are their corresponding integer elevations 0 to 25 with the ord() function, which gives the Unicode (ASCII) value of a character:
        chr(i) converts the integer i back to its corresponding character.
        ord('a') gives the ASCII value of 'a', and subtracting it from other letters gives the correct range (i.e., a = 0, b = 1, ..., z = 25).
        """
        elevation_map = {chr(i): i - ord('a') for i in range(ord('a'), ord('z') + 1)}

        # Override 'S' and 'E' values to their respective elevations
        elevation_map['S'] = elevation_map['a']  # 'S' is treated as 'a', so its elevation is 0
        elevation_map['E'] = elevation_map['z']  # 'E' is treated as 'z', so its elevation is 25

        # convert grid to elevation grid using elevation_map
        elevation_grid = [[elevation_map[val] for val in row] for row in grid]

        return elevation_grid

    def find_path_part_1(self):
        return self.find_path(self.start)

    def find_path_part_2(self):
        hiking_distance = []
        for low in self.find_lows():
            distance = self.find_path(low)
            if distance is not None:
                hiking_distance.append(distance)
        return min(list(set(hiking_distance)))

    def find_path(self, starting_point):
        """Use Dijkstra's algorithm:

        Initialization: Set the starting node’s distance to 0 and all other nodes' distances to infinity.
        Priority Queue: Use a priority queue (min-heap) to explore the least costly nodes first.
        Distance Updates: For each neighboring node, update its distance if you can reach it with a smaller cost.
        Termination: The algorithm finishes when you reach the end node or when the queue is empty."""

        # Step 1: Initialization

        # Get the size of the grid
        rows, cols = len(self.elevation_grid), len(self.elevation_grid[0])

        # Initialize distance map to infinity
        distances = [[float('inf')] * cols for _ in range(rows)]

        # Set the distance of the start node to 0
        start_row, start_col = starting_point
        distances[start_row][start_col] = 0

        # Priority queue (min-heap): store (distance, row, col)
        pq = [(0, start_row, start_col)]

        # Step 2: Exploration and Distance Updates

        # Directions for moving (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Process nodes in the priority queue
        while pq:
            current_distance, row, col = heapq.heappop(pq)

            # If we reached the end node, stop
            if (row, col) == self.end:
                return current_distance

            # Explore neighbors
            for row_offset, col_offset in directions:
                new_row, new_col = row + row_offset, col + col_offset

                # Check if new position is within bounds
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    # Check if we can move based on elevation constraint
                    current_elevation = self.elevation_grid[row][col]
                    new_elevation = self.elevation_grid[new_row][new_col]

                    if new_elevation <= current_elevation + 1:
                        # Calculate new distance
                        new_distance = current_distance + 1

                        # Update distance if a shorter path is found
                        if new_distance < distances[new_row][new_col]:
                            distances[new_row][new_col] = new_distance
                            heapq.heappush(pq, (new_distance, new_row, new_col))


def main():
    # print(GridProcessor('./input.txt').find_path())
    # print(GridProcessor('./input.txt').find_lows())
    print("Part 1:", GridProcessor('./input.txt').find_path_part_1())
    print("Part 2:", GridProcessor('./input.txt').find_path_part_2())


if __name__ == "__main__":
    main()
