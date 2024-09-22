input_file = open('input.txt', "r")
input_file = input_file.read().splitlines()


# Function to convert a SNAFU string to its decimal value
def snafu_to_decimal(snafu_str):
    # Create a dictionary to map SNAFU digits to their integer values
    snafu_digit_map = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }

    decimal_value = 0
    power_of_five = 1  # This will represent powers of 5 (5^0, 5^1, 5^2, etc.)

    # Iterate over the SNAFU number from right to left
    for digit in reversed(snafu_str):
        decimal_value += snafu_digit_map[digit] * power_of_five
        power_of_five *= 5

    return decimal_value

# Function to convert a decimal number back to its SNAFU representation


def decimal_to_snafu(decimal):
    # This will store the resulting SNAFU number
    snafu_digits = []

    while decimal != 0:
        remainder = decimal % 5
        decimal //= 5

        if remainder <= 2:
            snafu_digits.append(str(remainder))
        else:
            # We need to adjust for the SNAFU negative digits (i.e., -1 or -2)
            if remainder == 3:
                snafu_digits.append('=')
                decimal += 1
            elif remainder == 4:
                snafu_digits.append('-')
                decimal += 1

    # Since we built the number from the least significant to the most significant place, reverse the result
    return ''.join(reversed(snafu_digits))


# Convert all SNAFU numbers to decimal and sum them
total_decimal = sum(snafu_to_decimal(snafu) for snafu in input_file)

# Convert the sum back to SNAFU
result_snafu = decimal_to_snafu(total_decimal)

# Output the results
print(f"The sum of SNAFU numbers in decimal is: {total_decimal}")
print(f"The sum of SNAFU numbers in SNAFU format is: {result_snafu}")
