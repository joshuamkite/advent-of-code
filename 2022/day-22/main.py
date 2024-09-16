import re


class CodeMap:
    def parse_input(self, data):
        with open(data) as f:
            data = f.read().split("\n\n")
        board_map = data[0].split("\n")
        path_map = data[1].strip()
        return board_map, path_map

    def split_path_map(self, path_map):
        return re.findall(r'\d+|[RL]', path_map)

    def define_grid(self, board_map):
        height = len(board_map)
        width = max(len(row) for row in board_map)
        grid = [list(row.ljust(width)) for row in board_map]
        return grid, height, width

    def find_start_position(self, grid):
        return 0, next(i for i, tile in enumerate(grid[0]) if tile == '.')

    def move(self, grid, row, col, facing, count):
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        dr, dc = moves[facing]

        for _ in range(count):
            new_row, new_col = row + dr, col + dc

            if not (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0])) or grid[new_row][new_col] == ' ':
                # Wrap around
                wrap_row, wrap_col = row, col
                while 0 <= wrap_row < len(grid) and 0 <= wrap_col < len(grid[0]) and grid[wrap_row][wrap_col] != ' ':
                    wrap_row -= dr
                    wrap_col -= dc
                wrap_row += dr
                wrap_col += dc

                if grid[wrap_row][wrap_col] == '#':
                    break
                row, col = wrap_row, wrap_col
            elif grid[new_row][new_col] == '#':
                break
            else:
                row, col = new_row, new_col

        return row, col

    def read_route(self, path_map, grid):
        steps = self.split_path_map(path_map)
        row, col = self.find_start_position(grid)
        facing = 0  # Start facing right

        for step in steps:
            if step.isdigit():
                row, col = self.move(grid, row, col, facing, int(step))
            elif step == 'R':
                facing = (facing + 1) % 4
            elif step == 'L':
                facing = (facing - 1) % 4

        return row, col, facing

    def calculate_password(self, row, col, facing):
        return 1000 * (row + 1) + 4 * (col + 1) + facing


def main():
    my_obj = CodeMap()
    board_map, path_map = my_obj.parse_input('input.txt')
    grid, height, width = my_obj.define_grid(board_map)

    row, col, facing = my_obj.read_route(path_map, grid)

    password = my_obj.calculate_password(row, col, facing)
    print("Final Password:", password)


if __name__ == "__main__":
    main()
