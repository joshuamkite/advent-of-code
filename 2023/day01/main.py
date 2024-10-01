with open('input.txt', "r") as input_file:
    file_total = 0
    for line in input_file:
        digits = ''.join(filter(str.isdigit, line))
        line_digits = int(digits[0] + digits[-1])
        file_total += line_digits
        # print(line_digits)
print(file_total)
