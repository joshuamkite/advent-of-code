from itertools import islice
import ast

# Create a dictionary to store the packets
packets = {}

# Create a list to store the indices of the correct packets
correct_packets = []

# Open the file and read it line by line
with open('./input.txt', 'r') as file:
    # Initialize the group counter
    group_counter = 1

    # Process file in chunks of three lines
    while True:
        # Use islice to get the next three lines
        lines = list(islice(file, 3))

        if not lines:  # Break if no lines left
            break

        # Store the first line and the second line in a list as the value for the key by group in dict packets
        packets[group_counter] = [ast.literal_eval(lines[0].strip()), ast.literal_eval(lines[1].strip())]

        # Increment the group counter
        group_counter += 1

"""
When comparing two values, the first value is called left and the second value is called right. Then:

- If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
- If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
- If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].

"""


def compare(left, right):
    # Case 1: Both values are integers
    if isinstance(left, int) and isinstance(right, int):
        # print("evaluating case 1")
        if left < right:
            return True  # Left is in the correct order
        elif left > right:
            return False  # Right is smaller, so not in the correct order
        else:
            return None  # Continue comparing other items

    # Case 2: Both values are lists
    elif isinstance(left, list) and isinstance(right, list):
        # print("evaluating case 2")
        for l_item, r_item in zip(left, right):
            result = compare(l_item, r_item)
            if result is not None:  # If a decision is made (either True or False), return it
                return result

        # If we reach here, both lists are equal so far, now check which list runs out first
        if len(left) < len(right):
            return True  # Left list ran out first, so it's in order
        elif len(left) > len(right):
            return False  # Right list ran out first, not in order
        else:
            return None  # Lists are equal, continue comparing further or return True later

    # Case 3: One value is an integer and the other is a list
    elif isinstance(left, int):
        # print("evaluating case 3")
        return compare([left], right)  # Convert left integer to a list and compare
    elif isinstance(right, int):
        return compare(left, [right])  # Convert right integer to a list and compare

    return False  # Fail-safe return


# Process each packet and compare
for packet_num in packets:
    left_packet, right_packet = packets[packet_num]
    result = compare(left_packet, right_packet)
    # print(f"Packet {packet_num}: {'True' if result else 'False'}")
    if result:
        correct_packets.append(packet_num)
print(f"Part 1 solution: {sum(correct_packets)}")
