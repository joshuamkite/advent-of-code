

test_game = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


class Game:
    def __init__(self, id, cubes_set):
        self.id = id
        self.red = []
        self.green = []
        self.blue = []
        self.parse_cubes_set(cubes_set)

    def parse_cubes_set(self, cubes_set):
        for entry in cubes_set.strip().split(";"):
            entry = entry.split(",")
            for s in entry:
                s = s.strip().split(" ")
                color = s[1]
                value = int(s[0])
                getattr(self, color).append(value)

    def get_max_values(self):
        max_values = {
            'red': max(self.red) if self.red else None,
            'green': max(self.green) if self.green else None,
            'blue': max(self.blue) if self.blue else None
        }
        return max_values

    def is_possible_against_test_game(self, test_game):
        max_values = self.get_max_values()
        # Check if any value exceeds the test_game's corresponding value
        for color in ['red', 'green', 'blue']:
            if max_values[color] and max_values[color] > test_game[color]:
                return False  # If any value exceeds, the game is invalid
        return True  # Return true if all values are valid


# Parsing the input file and creating Game objects
with open('input.txt', "r") as input_file:
    games_objects = []
    for line in input_file:
        line = line.split(":")
        id = int(''.join(filter(str.isdigit, line[0])))
        cubes_set = line[1].strip()
        game = Game(id, cubes_set)
        games_objects.append(game)

# # Display game information and max values
# for game in games_objects:
#     print("Game ID:", game.id)
#     print("Max Values:", game.get_max_values())
#     print()

# print(test_game)


# Comparing each game with the test_game

id_sum = 0

for game in games_objects:
    is_possible = game.is_possible_against_test_game(test_game)
    # print(f"Game ID: {game.id} is possible: {is_possible}")  # debug
    if is_possible:
        id_sum += game.id


print("Part 1 solution:", id_sum)
