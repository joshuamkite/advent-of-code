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


def find_first_and_last_digit(line, number_map):
    # Find the first valid digit from the left
    first_digit = None
    last_digit = None

    # Scan from the left for the first digit
    i = 0
    while i < len(line):
        if line[i].isdigit():
            first_digit = int(line[i])
            break
        for word in number_map:
            if line.startswith(word, i):
                first_digit = number_map[word]
                i += len(word) - 1  # Move the index past the matched word
                break
        if first_digit is not None:
            break
        i += 1

    # Scan from the right for the last digit
    i = len(line) - 1
    while i >= 0:
        if line[i].isdigit():
            last_digit = int(line[i])
            break
        for word in number_map:
            if line.startswith(word, i - len(word) + 1):
                last_digit = number_map[word]
                i -= len(word) - 1  # Move the index past the matched word
                break
        if last_digit is not None:
            break
        i -= 1

    return first_digit, last_digit


with open('input.txt', "r") as input_file:
    total_sum = 0
    for line in input_file:
        line = line.strip()  # Remove leading/trailing whitespace
        first_digit, last_digit = find_first_and_last_digit(line, number_map)

        if first_digit is not None and last_digit is not None:
            calibration_value = int(f"{first_digit}{last_digit}")
            total_sum += calibration_value

            # Debug output
            # print(f"line: {line}, first_digit: {first_digit}, last_digit: {last_digit}, calibration_value: {calibration_value}")

    # Final total for part 2 solution
    print("part 2 solution: ", total_sum)
