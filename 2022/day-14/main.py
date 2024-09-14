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


def determine_grid_size(paths, source_x=500, source_y=0, add_floor=False):
    """
    Determines the minimum and maximum x and y values to set grid boundaries.
    If add_floor is True, extends the grid to include the floor.
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

    if add_floor:
        # Floor is at y = max_y + 2
        floor_y = max_y + 2
        max_y = floor_y  # Extend the grid to include the floor

        # To prevent sand from overflowing left/right, add buffer based on floor_y
        # Since floor is infinite, sand can spread outwards as much as needed
        # We'll add a buffer proportional to floor_y to accommodate spread
        buffer = floor_y * 2  # Adjust as necessary
        min_x -= buffer
        max_x += buffer

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


def draw_floor(grid, min_x, min_y, floor_y):
    """
    Draws the floor '#' on the grid at the specified floor_y.
    """
    y = floor_y - min_y
    if y >= len(grid):
        raise IndexError(f"Floor y-coordinate {floor_y} is outside the grid height {len(grid)}.")
    for x in range(len(grid[y])):
        grid[y][x] = '#'


def print_grid(grid):
    """
    Prints the grid to the console.
    """
    for row in grid:
        print("".join(row))


def simulate_sand_falling_part1(cave, source_x, source_y, min_x, min_y):
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
            # Source is blocked; simulation ends (Not applicable for Part 1)
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


def simulate_sand_falling_part2(cave, source_x, source_y, min_x, min_y, floor_y):
    """
    Simulates sand falling with a floor until the source is blocked.
    Returns the number of sand units that come to rest.
    """
    width = len(cave[0])
    height = len(cave)
    sand_count = 0

    while True:
        # Start sand at the source
        x, y = source_x - min_x, source_y - min_y

        # Check if the source is already blocked
        if cave[y][x] == 'o':
            # Source is blocked; simulation ends
            return sand_count

        while True:
            # If y + 1 is the floor level, sand comes to rest
            if y + 1 == floor_y - min_y:
                cave[y][x] = 'o'
                sand_count += 1
                break

            # Check if the space directly below is empty
            if cave[y + 1][x] == '.':
                y += 1  # Move down
            else:
                moved = False

                # Attempt to move down-left
                if x - 1 >= 0 and cave[y + 1][x - 1] == '.':
                    y += 1
                    x -= 1  # Move down-left
                    moved = True

                # Attempt to move down-right
                if not moved and x + 1 < width and cave[y + 1][x + 1] == '.':
                    y += 1
                    x += 1  # Move down-right
                    moved = True

                if not moved:
                    # Sand comes to rest when all three options are blocked
                    cave[y][x] = 'o'
                    sand_count += 1
                    break  # Start simulating the next unit of sand


def simulate_sand_in_cave_part1(cave, min_x, min_y):
    """
    Simulates the sand falling process for Part One and returns the count of sand units at rest.
    """
    # Assuming the sand source is at (500, 0)
    source_x = 500
    source_y = 0

    # Simulate sand falling and return the number of units that come to rest
    return simulate_sand_falling_part1(cave, source_x, source_y, min_x, min_y)


def simulate_sand_in_cave_part2(cave, min_x, min_y, floor_y):
    """
    Simulates the sand falling process for Part Two and returns the count of sand units at rest.
    """
    # Assuming the sand source is at (500, 0)
    source_x = 500
    source_y = 0

    # Simulate sand falling with floor and return the number of units that come to rest
    return simulate_sand_falling_part2(cave, source_x, source_y, min_x, min_y, floor_y)


def main():
    file_path = 'input.txt'  # Path to the input file
    paths = parse_input(file_path)

    # ================================
    # Part One Simulation
    # ================================

    # Step 1: Determine grid size based on paths and source (Part One)
    min_x1, max_x1, min_y1, max_y1 = determine_grid_size(paths, add_floor=False)

    # Step 2: Initialize an empty grid for Part One
    grid_part1 = initialize_grid(min_x1, max_x1, min_y1, max_y1)

    # Step 3: Place the sand source at (500, 0) adjusted for the grid (Part One)
    place_source(grid_part1, 500, 0, min_x1, min_y1)

    # Step 4: Draw rocks based on the paths (Part One)
    draw_rocks(grid_part1, paths, min_x1, min_y1)

    # Step 5: Simulate sand falling for Part One and count how many units come to rest
    sand_units_part1 = simulate_sand_in_cave_part1(grid_part1, min_x1, min_y1)
    print(f"Part One - Number of units of sand that come to rest: {sand_units_part1}")

    # Optional: Uncomment to visualize Part One grid
    # print("\nPart One Grid:")
    # print_grid(grid_part1)

    # ================================
    # Part Two Simulation
    # ================================

    # Step 1: Determine grid size based on paths and source (Part Two)
    min_x2, max_x2, min_y2, max_y2 = determine_grid_size(paths, add_floor=True)
    floor_y = max_y2  # Correct calculation: floor_y is already set to max_y + 2 in determine_grid_size

    # Step 2: Initialize an empty grid for Part Two
    grid_part2 = initialize_grid(min_x2, max_x2, min_y2, max_y2)

    # Step 3: Place the sand source at (500, 0) adjusted for the grid (Part Two)
    place_source(grid_part2, 500, 0, min_x2, min_y2)

    # Step 4: Draw rocks based on the paths (Part Two)
    draw_rocks(grid_part2, paths, min_x2, min_y2)

    # Step 5: Draw the floor on the grid (Part Two)
    try:
        draw_floor(grid_part2, min_x2, min_y2, floor_y)
    except IndexError as e:
        print(f"Error drawing floor: {e}")
        return

    # Step 6: Simulate sand falling for Part Two and count how many units come to rest
    sand_units_part2 = simulate_sand_in_cave_part2(grid_part2, min_x2, min_y2, floor_y)
    print(f"Part Two - Number of units of sand that come to rest: {sand_units_part2}")

    # Optional: Uncomment to visualize Part Two grid
    # print("\nPart Two Grid:")
    # print_grid(grid_part2)


if __name__ == "__main__":
    main()
