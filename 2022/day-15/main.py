file_path = 'input.txt'

sensor_positions = []
beacon_positions = []
row_to_check = 2000000  # Row where we want to count unavailable beacon positions


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def main():
    with open(file_path, 'r') as file:
        for line in file:
            sensor_position = line.split(":")[0].split("at")[1].strip()
            sensor_position = sensor_position.split("=")
            sensor_position = [(sensor_position[1].split(","))[0]] + (sensor_position[2].split(","))
            sensor_position = list(map(int, sensor_position))
            sensor_positions.append(sensor_position)

            beacon_position = line.split("is at")[1].strip()
            beacon_position = beacon_position.split("=")
            beacon_position = [(beacon_position[1].split(","))[0]] + (beacon_position[2].split(","))
            beacon_position = list(map(int, beacon_position))
            beacon_positions.append(beacon_position)

    covered_positions = set()  # Use a set to track x positions that are covered

    for sensor_position, beacon_position in zip(sensor_positions, beacon_positions):
        distance = manhattan_distance(sensor_position, beacon_position)
        sensor_x, sensor_y = sensor_position

        # If the sensor's coverage reaches row_to_check
        if abs(sensor_y - row_to_check) <= distance:
            # Calculate the range of x values covered by the sensor on this row
            x_range = distance - abs(sensor_y - row_to_check)
            for x in range(sensor_x - x_range, sensor_x + x_range + 1):
                covered_positions.add(x)

    # Remove beacon positions that are on row_to_check (since a beacon can exist there)
    for beacon_position in beacon_positions:
        beacon_x, beacon_y = beacon_position
        if beacon_y == row_to_check and beacon_x in covered_positions:
            covered_positions.remove(beacon_x)

    # The result is the count of positions in row_to_check where no beacon can exist
    print(f"Number of positions where a beacon cannot exist on row {row_to_check}: {len(covered_positions)}")


if __name__ == "__main__":
    main()
