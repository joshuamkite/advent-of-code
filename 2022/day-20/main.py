def read_input(file_path: str) -> list:
    """Reads the input file and returns a list of integers."""
    with open(file_path, "r") as file:
        return [int(line) for line in file.read().splitlines()]


def mix(data: list, times: int = 1) -> list:
    """Mixes the list of numbers based on their original order and returns the updated list."""
    length = len(data)
    indexed_data = list(enumerate(data))  # Track (original_index, value)

    for _ in range(times):
        for i in range(length):
            for j, (idx, val) in enumerate(indexed_data):
                if idx == i:
                    indexed_data.pop(j)
                    new_index = (j + val) % (length - 1)
                    indexed_data.insert(new_index, (idx, val))
                    break

    return [val for _, val in indexed_data]


def find_grove_coordinates(data: list) -> list:
    """Finds the grove coordinates (1000th, 2000th, and 3000th numbers after 0)."""
    length = len(data)
    zero_index = data.index(0)
    return [data[(zero_index + i) % length] for i in [1000, 2000, 3000]]


def main():
    # Part 1
    original_data = read_input('input.txt')
    mixed_data = mix(original_data)
    grove_coordinates = find_grove_coordinates(mixed_data)
    print("Part 1 solution:", sum(grove_coordinates))

    # Part 2
    decryption_key = 811589153
    scaled_data = [x * decryption_key for x in original_data]
    mixed_data = mix(scaled_data, times=10)
    grove_coordinates = find_grove_coordinates(mixed_data)
    print("Part 2 solution:", sum(grove_coordinates))


if __name__ == "__main__":
    main()
