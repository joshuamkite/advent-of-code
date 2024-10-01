with open('input.txt', "r") as input_file:
    file_total = 0
    for line in input_file:
        digits = ''.join(filter(str.isdigit, line))
        line_digits = int(digits[0] + digits[-1])
        file_total += line_digits
print("part 1 solution: ", file_total)


number_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def process_line(line, number_map):
    line_numbers = []
    i = 0  # Start from the first character
    while i < len(line):
        if line[i].isdigit():
            # If the current character is a digit, append the digit and move to the next character
            line_numbers.append(int(line[i]))
            i += 1
        else:
            match = None
            for word in number_map:
                if line.startswith(word, i):  # Check if the string starts with the word at position i
                    match = word
                    break
            if match:
                # If a match is found, append the corresponding number and move the index
                line_numbers.append(number_map[match])
                i += len(match)  # Skip past the matched substring
            else:
                # If no match, move to the next character
                i += 1
    return line_numbers


with open('input.txt', "r") as input_file:
    file_numbers = []
    first_last = 0
    for line in input_file:
        line = line.strip()  # Remove leading/trailing whitespace
        line_numbers = process_line(line, number_map)
        file_numbers.append(line_numbers)
        first_last += int(str(line_numbers[0]) + str(line_numbers[-1]))  # Concatenate the first and last elements of the list as strings and convert to int for addition
        print("line_numbers: ", line_numbers)  # debug
        print(int(str(line_numbers[0]) + str(line_numbers[-1])))  # debug
    # print(file_numbers)  # debug

    print("part 2 solution: ", first_last)

    # 54412 is too low for part 2
