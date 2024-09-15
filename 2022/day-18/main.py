import sys
from collections import deque

# Define the six possible neighbor directions (±x, ±y, ±z)
NEIGHBORS = [(-1, 0, 0), (1, 0, 0),
             (0, -1, 0), (0, 1, 0),
             (0, 0, -1), (0, 0, 1)]


def read_input(file_path):
    """
    Reads the input file and returns a set of cube positions.

    Parameters:
    - file_path (str): Path to the input file.

    Returns:
    - Set of tuples representing the positions of cubes.
    """
    cubes = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace and split by comma
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue  # Skip invalid lines
            x, y, z = map(int, parts)
            cubes.add((x, y, z))
    return cubes


def calculate_total_surface_area(cubes):
    """
    Calculates the total surface area of the lava droplet.

    Parameters:
    - cubes (set): Set of tuples representing the positions of cubes.

    Returns:
    - int: Total surface area.
    """
    surface_area = 0
    for cube in cubes:
        x, y, z = cube
        # Check all six neighbors
        for dx, dy, dz in NEIGHBORS:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in cubes:
                surface_area += 1  # Exposed side
    return surface_area


def calculate_external_surface_area(cubes):
    """
    Calculates the external surface area of the lava droplet, excluding internal cavities.

    Parameters:
    - cubes (set): Set of tuples representing the positions of cubes.

    Returns:
    - int: External surface area.
    """
    # Determine bounding box
    min_x = min(x for x, _, _ in cubes) - 1
    max_x = max(x for x, _, _ in cubes) + 1
    min_y = min(y for _, y, _ in cubes) - 1
    max_y = max(y for _, y, _ in cubes) + 1
    min_z = min(z for _, _, z in cubes) - 1
    max_z = max(z for _, _, z in cubes) + 1

    # Initialize visited set and queue for BFS
    visited = set()
    queue = deque()
    start = (min_x, min_y, min_z)
    queue.append(start)
    visited.add(start)

    while queue:
        x, y, z = queue.popleft()
        for dx, dy, dz in NEIGHBORS:
            nx, ny, nz = x + dx, y + dy, z + dz
            neighbor = (nx, ny, nz)
            # Check if neighbor is within bounds and not a cube and not visited
            if (min_x <= nx <= max_x and
                min_y <= ny <= max_y and
                min_z <= nz <= max_z and
                neighbor not in cubes and
                    neighbor not in visited):
                visited.add(neighbor)
                queue.append(neighbor)

    # Now, calculate surface area by only counting sides adjacent to external air
    external_surface_area = 0
    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in NEIGHBORS:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in cubes and neighbor in visited:
                external_surface_area += 1  # External exposed side
    return external_surface_area


def main():

    input_file = 'input.txt'

    # Read and parse the input
    cubes = read_input(input_file)

    # Part 1: Calculate total surface area
    part1_surface_area = calculate_total_surface_area(cubes)
    print(f"part1: {part1_surface_area}")

    # Part 2: Calculate external surface area (excluding internal cavities)
    part2_surface_area = calculate_external_surface_area(cubes)
    print(f"part2: {part2_surface_area}")


if __name__ == "__main__":
    main()
