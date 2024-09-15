
def read_input(file_path: str) -> list:
    with open(file_path, "r") as file:
        return [int(line) for line in file.read().splitlines()]


def mix(data: list) -> list:
    length = len(data)

    # Create a list of tuples (original index, value) to track positions
    indexed_data = list(enumerate(data))

    for i in range(length):
        # Find the current index of the element with the original index `i`
        current_index = next(j for j, (idx, _) in enumerate(indexed_data) if idx == i)

        # Pop the element (remove it from the current position)
        element = indexed_data.pop(current_index)

        # Calculate the new index, handling both positive and negative values
        new_index = (current_index + element[1]) % (length - 1)

        # Insert the element at the new index
        indexed_data.insert(new_index, element)

        # Extract the values from the indexed_data - original return value
        hacked_list = [val for _, val in indexed_data]

        # Shift the circular list by 1 - hack whilst we work on a better solution
        hacked_list.append(hacked_list.pop(0))

    # Return only the values from the indexed_data
    return hacked_list

    # for
    # [1, 2, -3, 3, -2, 0, 4]
    # should return
    # [1, 2, -3, 4, 0, 3, -2]


def find_items(data: list) -> list:
    """
        Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.
    """
    length = len(data)
    grove_coordinates = []
    index_of_zero = data.index(0)  # Find the index of 0 in the list

    for i in [(index_of_zero + 1000), (index_of_zero + 2000), (index_of_zero + 3000)]:  # Find the 1000th, 2000th, and 3000th numbers after the value 0
        index = i % length  # Wrap around the list as necessary by using modulo
        grove_coordinates.append(data[index])
    return grove_coordinates


def main():
    # print(read_input('test.txt'))
    # print(mix(read_input('test.txt')))
    mixed_items = (find_items(mix(read_input('input.txt'))))
    print("Part 1 solution:",  sum(mixed_items))


if __name__ == "__main__":
    main()
