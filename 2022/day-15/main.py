file_path = 'real_input.txt'

sensor_positions = []
beacon_positions = []
row_to_check = 2000000  # Row where we want to count unavailable beacon positions

# Function to calculate Manhattan distance between two points


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def main():
    # Read the input data and parse sensor and beacon positions
    with open(file_path, 'r') as file:
        for line in file:
            # Extract sensor position from the line
            sensor_position = line.split(":")[0].split("at")[1].strip()
            sensor_position = sensor_position.split("=")
            sensor_position = [(sensor_position[1].split(","))[0]] + (sensor_position[2].split(","))
            sensor_position = list(map(int, sensor_position))  # Convert to integers
            sensor_positions.append(sensor_position)

            # Extract beacon position from the line
            beacon_position = line.split("is at")[1].strip()
            beacon_position = beacon_position.split("=")
            beacon_position = [(beacon_position[1].split(","))[0]] + (beacon_position[2].split(","))
            beacon_position = list(map(int, beacon_position))  # Convert to integers
            beacon_positions.append(beacon_position)

    # Set to track all x-positions that are covered by a sensor on row_to_check
    covered_positions = set()

    # Loop through each sensor and its corresponding closest beacon
    for sensor_position, beacon_position in zip(sensor_positions, beacon_positions):
        # Calculate the Manhattan distance between the sensor and its closest beacon
        distance = manhattan_distance(sensor_position, beacon_position)
        sensor_x, sensor_y = sensor_position

        # Check if the sensor's coverage reaches row_to_check
        if abs(sensor_y - row_to_check) <= distance:
            # Calculate how far the sensor's coverage extends horizontally on row_to_check
            x_range = distance - abs(sensor_y - row_to_check)

            # Add all the x-coordinates covered by the sensor on row_to_check to the set
            for x in range(sensor_x - x_range, sensor_x + x_range + 1):
                covered_positions.add(x)

    # Loop through each beacon and remove positions where a beacon is known to exist on row_to_check
    for beacon_position in beacon_positions:
        beacon_x, beacon_y = beacon_position
        if beacon_y == row_to_check and beacon_x in covered_positions:
            covered_positions.remove(beacon_x)

    # The number of positions in row_to_check where no beacon can exist
    print(f"Number of positions where a beacon cannot exist on row {row_to_check}: {len(covered_positions)}")


if __name__ == "__main__":
    main()
