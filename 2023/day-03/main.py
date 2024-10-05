import re


def parse_input(schematic):
    return [list(line) for line in schematic.splitlines() if line.strip()]


def is_symbol(cell):
    return cell not in "0123456789."


def is_star(cell):
    return cell == "*"


def get_full_number(grid, r, c):
    # Get the full number, moving left first, then right
    number = ''
    left = c
    while left >= 0 and grid[r][left].isdigit():
        left -= 1
    left += 1  # Move back to the first digit
    while left < len(grid[r]) and grid[r][left].isdigit():
        number += grid[r][left]
        left += 1
    return int(number), left - 1  # Return the number and the last digit position


def is_adjacent_to_symbol(grid, r, start_c, end_c):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for c in range(start_c, end_c + 1):
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
                if is_symbol(grid[nr][nc]):
                    return True
    return False


def sum_part_numbers(schematic):
    grid = parse_input(schematic)
    total = 0

    for r in range(len(grid)):
        c = 0
        while c < len(grid[r]):
            if grid[r][c].isdigit():
                number, end_c = get_full_number(grid, r, c)
                if is_adjacent_to_symbol(grid, r, c, end_c):
                    total += number
                c = end_c + 1
            else:
                c += 1

    return total


def get_adjacent_numbers_to_star(grid, star_r, star_c):
    adjacent_numbers = set()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        nr, nc = star_r + dr, star_c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc].isdigit():
            number, _ = get_full_number(grid, nr, nc)
            adjacent_numbers.add(number)
    return list(adjacent_numbers)


def sum_gear_ratios(schematic):
    grid = parse_input(schematic)
    total = 0

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if is_star(grid[r][c]):
                adjacent_numbers = get_adjacent_numbers_to_star(grid, r, c)
                if len(adjacent_numbers) == 2:
                    total += adjacent_numbers[0] * adjacent_numbers[1]

    return total


def main():
    with open('input.txt') as f:
        schematic = f.read()

    print("Part 1 solution:", sum_part_numbers(schematic))
    print("Part 2 solution:", sum_gear_ratios(schematic))


if __name__ == "__main__":
    main()
