import re


def parse_input(schematic):
    # Parse the input into a 2D grid
    return [list(line) for line in schematic.splitlines() if line.strip()]


def is_symbol(cell):
    # Define what constitutes a symbol, exclude numbers and periods
    return cell not in "0123456789."


def get_full_number(grid, r, c):
    # Get the full number starting at position (r, c)
    number = ''
    while c < len(grid[r]) and grid[r][c].isdigit():
        number += grid[r][c]
        c += 1
    return int(number)


def is_adjacent_to_symbol(grid, r, start_c, end_c):
    # Check if the number is adjacent to a symbol
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for c in range(start_c, end_c):
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
                start_c = c
                number = get_full_number(grid, r, c)
                end_c = c + len(str(number))
                if is_adjacent_to_symbol(grid, r, start_c, end_c):
                    total += number
                c = end_c
            else:
                c += 1

    return total


def main():
    with open('input.txt') as f:
        schematic = f.read()

    print(sum_part_numbers(schematic))


if __name__ == "__main__":
    main()
