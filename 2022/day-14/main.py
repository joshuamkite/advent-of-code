def parse_input(file_path):
    """
    Parses the input file and returns a list of unique rock paths.
    Each path is a list of (x, y) tuples.
    """
    paths = []
    unique_paths = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Convert each path to a tuple of tuples for immutability
            path = tuple(tuple(map(int, segment.split(","))) for segment in line.strip().split(" -> "))
            if path not in unique_paths:
                unique_paths.add(path)
                paths.append(list(path))
    return paths


def determine_grid_size(paths, source_x=500, source_y=0):
    """
    Determines the minimum and maximum x and y values to set grid boundaries.
    """
    min_x = min(min(x for x, y in path) for path in paths)
    max_x = max(max(x for x, y in path) for path in paths)
    min_y = min(min(y for x, y in path) for path in paths)
    max_y = max(max(y for x, y in path) for path in paths)

    # Ensure the grid includes the sand source
    min_x = min(min_x, source_x)
    max_x = max(max_x, source_x)
    min_y = min(min_y, source_y)
    max_y = max(max_y, source_y)

    return min_x, max_x, min_y, max_y


def initialize_grid(min_x, max_x, min_y, max_y):
    """
    Initializes the grid based on determined boundaries without adding walls.
    """
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return [['.' for _ in range(width)] for _ in range(height)]


def place_source(grid, source_x, source_y, min_x, min_y):
    """
    Places the sand source '+' in the grid.
    """
    adjusted_x = source_x - min_x
    adjusted_y = source_y - min_y
    grid[adjusted_y][adjusted_x] = '+'


def draw_rocks(grid, paths, min_x, min_y):
    """
    Draws rocks '#' on the grid based on the provided paths.
    """
    for path in paths:
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            if start[0] == end[0]:  # Vertical line
                x = start[0] - min_x
                for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    grid[y - min_y][x] = '#'
            elif start[1] == end[1]:  # Horizontal line
                y = start[1] - min_y
                for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    grid[y][x - min_x] = '#'


def print_grid(grid):
    """
    Prints the grid to the console.
    """
    for row in grid:
        print("".join(row))


def simulate_sand_falling(cave, source_x, source_y, min_x, min_y):
    """
    Simulates sand falling until a unit falls into the abyss.
    Returns the number of sand units that come to rest.
    """
    width = len(cave[0])
    height = len(cave)
    sand_count = 0

    while True:
        # Start sand at the source
        x, y = source_x - min_x, source_y - min_y

        # Check if the source is already blocked
        if cave[y][x] != '+' and cave[y][x] != '.':
            # Source is blocked; simulation ends
            return sand_count

        while True:
            # Stop the simulation if sand falls out of bounds (into the abyss)
            if y + 1 >= height:
                return sand_count

            # Check if the space directly below is empty
            if cave[y + 1][x] == '.':
                y += 1  # Move down
            else:
                moved = False

                # Attempt to move down-left
                if x - 1 < 0:
                    # Sand flows into the abyss to the left
                    return sand_count
                elif cave[y + 1][x - 1] == '.':
                    y += 1
                    x -= 1  # Move down-left
                    moved = True

                # Attempt to move down-right
                if not moved:
                    if x + 1 >= width:
                        # Sand flows into the abyss to the right
                        return sand_count
                    elif cave[y + 1][x + 1] == '.':
                        y += 1
                        x += 1  # Move down-right
                        moved = True

                if not moved:
                    # Sand comes to rest when all three options are blocked
                    cave[y][x] = 'o'
                    sand_count += 1
                    break  # Start simulating the next unit of sand


def simulate_sand_in_cave(cave, min_x, min_y):
    """
    Simulates the sand falling process and returns the count of sand units at rest.
    """
    # Assuming the sand source is at (500, 0)
    source_x = 500
    source_y = 0

    # Simulate sand falling and return the number of units that come to rest
    return simulate_sand_falling(cave, source_x, source_y, min_x, min_y)


def main():
    file_path = 'input.txt'  # Path to the input file
    paths = parse_input(file_path)

    # Step 1: Determine grid size based on paths and source
    min_x, max_x, min_y, max_y = determine_grid_size(paths)

    # Step 2: Initialize an empty grid without adding walls
    grid = initialize_grid(min_x, max_x, min_y, max_y)

    # Step 3: Place the sand source at (500, 0) adjusted for the grid
    place_source(grid, 500, 0, min_x, min_y)

    # Step 4: Draw rocks based on the paths
    draw_rocks(grid, paths, min_x, min_y)

    # Step 5: Simulate sand falling and count how many units come to rest
    sand_units = simulate_sand_in_cave(grid, min_x, min_y)
    print(f"Number of units of sand that come to rest: {sand_units}")

    # Optionally, print the grid after sand has settled
    # Note: For large inputs, printing the grid can be impractical
    print_grid(grid)


if __name__ == "__main__":
    main()
