
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


def main():
    print(mix(read_input('test.txt')))


if __name__ == "__main__":
    main()
