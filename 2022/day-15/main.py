# Define the path to your input file
file_path = 'input.txt'

# Initialize lists to store sensor and beacon positions
sensor_positions = []
beacon_positions = []

# Constants for the specific row to check in Part 1 and the grid limit for Part 2
row_to_check = 2000000  # For Part 1
grid_limit = 4000000     # For Part 2


def manhattan_distance(p1, p2):
    """
    Calculate the Manhattan distance between two points p1 and p2.

    Parameters:
    - p1: Tuple[int, int] representing the (x, y) coordinates of the first point.
    - p2: Tuple[int, int] representing the (x, y) coordinates of the second point.

    Returns:
    - int: The Manhattan distance between p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def parse_input(file_path):
    """
    Parse the input file to extract sensor and beacon positions.

    Each line in the input file is expected to be in the format:
    "Sensor at x=<x1>, y=<y1>: closest beacon is at x=<x2>, y=<y2>"

    Parameters:
    - file_path: str representing the path to the input file.

    Returns:
    - Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        - First list contains sensor positions as (x, y) tuples.
        - Second list contains beacon positions as (x, y) tuples.
    """
    sensors = []
    beacons = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into sensor and beacon parts
            parts = line.strip().split(':')

            # Parse sensor coordinates
            sensor_part = parts[0].split('at')[1].strip()
            # Remove commas and split into x and y
            sensor_coords = sensor_part.replace(',', '').replace('x=', '').replace('y=', '').split()
            sensor_x, sensor_y = map(int, sensor_coords)
            sensors.append((sensor_x, sensor_y))

            # Parse beacon coordinates
            beacon_part = parts[1].split('at')[1].strip()
            # Remove commas and split into x and y
            beacon_coords = beacon_part.replace(',', '').replace('x=', '').replace('y=', '').split()
            beacon_x, beacon_y = map(int, beacon_coords)
            beacons.append((beacon_x, beacon_y))

    return sensors, beacons


def part_1(sensor_positions, beacon_positions):
    """
    Part 1: Count the number of positions in a specific row where a beacon cannot exist.

    This function calculates all x-coordinates in the specified row that are covered
    by at least one sensor's exclusion zone, then subtracts any positions where a beacon
    is already present on that row.

    Parameters:
    - sensor_positions: List of tuples representing sensor positions.
    - beacon_positions: List of tuples representing beacon positions.

    Returns:
    - None: Prints the result directly.
    """
    covered_positions = set()  # To store all x positions that are covered on the row

    # Iterate through each sensor and its closest beacon
    for sensor, beacon in zip(sensor_positions, beacon_positions):
        distance = manhattan_distance(sensor, beacon)  # Sensor's coverage radius
        sensor_x, sensor_y = sensor

        # Determine if the sensor's coverage intersects with the row_to_check
        vertical_distance = abs(sensor_y - row_to_check)
        if vertical_distance > distance:
            # If the sensor's coverage does not reach the row, skip
            continue

        # Calculate the horizontal range covered on the row
        horizontal_range = distance - vertical_distance
        # Add all x positions within this range to the covered_positions set
        for x in range(sensor_x - horizontal_range, sensor_x + horizontal_range + 1):
            covered_positions.add(x)

    # Remove any positions where a beacon is already present on the row
    for beacon in beacon_positions:
        beacon_x, beacon_y = beacon
        if beacon_y == row_to_check and beacon_x in covered_positions:
            covered_positions.remove(beacon_x)

    # The result is the number of positions where a beacon cannot exist
    print(f"Part 1: Number of positions where a beacon cannot exist on row {row_to_check}: {len(covered_positions)}")


def get_perimeter(sensor, distance):
    """
    Generate all points that are exactly one unit outside the sensor's coverage area.

    This function leverages the properties of Manhattan distance to efficiently
    iterate over the perimeter points of the sensor's coverage diamond.

    Parameters:
    - sensor: Tuple[int, int] representing the (x, y) coordinates of the sensor.
    - distance: int representing the sensor's coverage radius.

    Yields:
    - Tuple[int, int]: Coordinates of a perimeter point.
    """
    x, y = sensor
    d = distance + 1  # Perimeter is one unit beyond the coverage

    # Iterate over all possible deltas that sum up to the perimeter distance
    for dx in range(d + 1):
        dy = d - dx
        # Yield all four symmetric points around the sensor
        yield (x + dx, y + dy)
        yield (x + dx, y - dy)
        yield (x - dx, y + dy)
        yield (x - dx, y - dy)


def part_2(sensor_positions, beacon_positions):
    """
    Part 2: Find the position of the distress beacon and calculate its tuning frequency.

    This function efficiently searches for the single position not covered by any sensor
    by examining the perimeters of all sensor coverage areas. Once found, it computes
    the tuning frequency based on the beacon's coordinates.

    Parameters:
    - sensor_positions: List of tuples representing sensor positions.
    - beacon_positions: List of tuples representing beacon positions.

    Returns:
    - None: Prints the result directly.
    """
    # Precompute the coverage distance for each sensor
    sensor_coverage = []
    for sensor, beacon in zip(sensor_positions, beacon_positions):
        distance = manhattan_distance(sensor, beacon)
        sensor_coverage.append((sensor, distance))

    # Iterate through each sensor's perimeter points
    for idx, (sensor, distance) in enumerate(sensor_coverage):
        # Generate all perimeter points for the current sensor
        for point in get_perimeter(sensor, distance):
            x, y = point

            # Check if the point is within the allowed grid bounds
            if not (0 <= x <= grid_limit and 0 <= y <= grid_limit):
                continue  # Skip points outside the grid

            # Assume the point is not covered by any sensor initially
            is_covered = False
            # Check coverage against all sensors
            for other_sensor, other_distance in sensor_coverage:
                # If the point is within any sensor's coverage, mark as covered and break
                if manhattan_distance(other_sensor, point) <= other_distance:
                    is_covered = True
                    break  # No need to check other sensors

            # If the point is not covered by any sensor, it's the distress beacon
            if not is_covered:
                tuning_frequency = x * 4_000_000 + y  # Calculate tuning frequency
                print(f"Part 2: Distress beacon found at x={x}, y={y} with tuning frequency {tuning_frequency}")
                return  # Exit after finding the beacon

    # If no beacon is found within the grid limits
    print("Part 2: Distress beacon not found within the grid limits.")


def main():
    """
    Main function to execute Part 1 and Part 2 of the challenge.

    This function parses the input, runs both parts, and displays the results.

    Returns:
    - None
    """
    # Parse the input file to get sensor and beacon positions
    sensor_positions, beacon_positions = parse_input(file_path)

    # Execute Part 1
    part_1(sensor_positions, beacon_positions)

    # Execute Part 2
    part_2(sensor_positions, beacon_positions)


# Entry point of the script
if __name__ == "__main__":
    main()
