class ElfSimulation:
    def __init__(self, file_path):
        self.elf_coordinates = self.parse_input(file_path)
        self.directions = ['N', 'S', 'W', 'E']

    def parse_input(self, file_path):
        """ Parse input file and return a set of coordinates of the elves.
        """
        elf_coordinates = set()  # Initialize as a set
        with open(file_path, "r") as file:
            for i, line in enumerate(file):
                for j in range(len(line.strip())):
                    if line[j] == '#':
                        elf_coordinates.add((i, j))
        return elf_coordinates

    def get_neighbors(self, x, y):
        """For each item in the set, check the neighbors."""
        return [
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
        ]

    def propose_move(self, elf):
        """Propose a valid move based on the direction priority."""
        x, y = elf
        for direction in self.directions:
            if direction == 'N':
                if all((x - 1, y + i) not in self.elf_coordinates for i in [-1, 0, 1]):
                    return (x - 1, y)  # Move north
            elif direction == 'S':
                if all((x + 1, y + i) not in self.elf_coordinates for i in [-1, 0, 1]):
                    return (x + 1, y)  # Move south
            elif direction == 'W':
                if all((x + i, y - 1) not in self.elf_coordinates for i in [-1, 0, 1]):
                    return (x, y - 1)  # Move west
            elif direction == 'E':
                if all((x + i, y + 1) not in self.elf_coordinates for i in [-1, 0, 1]):
                    return (x, y + 1)  # Move east
        return elf  # If no valid move, stay in place

    def simulate_round(self):
        """Simulate one round of movement."""
        proposals = {}  # Track proposed moves

        # First half: propose moves
        for elf in self.elf_coordinates:
            proposed_move = self.propose_move(elf)
            if proposed_move not in proposals:
                proposals[proposed_move] = [elf]
            else:
                proposals[proposed_move].append(elf)

        # Second half: execute moves
        new_elf_coordinates = set()
        for move, elves in proposals.items():
            if len(elves) == 1:  # No conflict, move the Elf
                new_elf_coordinates.add(move)
            else:  # Conflict, all Elves stay in place
                new_elf_coordinates.update(elves)

        # Rotate directions for the next round
        self.directions = self.directions[1:] + self.directions[:1]

        self.elf_coordinates = new_elf_coordinates

    def calculate_empty_tiles(self):
        """Calculate the number of empty ground tiles in the bounding rectangle."""
        min_x = min(x for x, y in self.elf_coordinates)
        max_x = max(x for x, y in self.elf_coordinates)
        min_y = min(y for x, y in self.elf_coordinates)
        max_y = max(y for x, y in self.elf_coordinates)

        # Total grid area
        total_tiles = (max_x - min_x + 1) * (max_y - min_y + 1)

        # Empty ground tiles are total minus number of elves
        empty_tiles = total_tiles - len(self.elf_coordinates)

        return empty_tiles

    def print_map(self):
        """Print the current state of the map, showing Elf positions."""
        min_x = min(x for x, y in self.elf_coordinates)
        max_x = max(x for x, y in self.elf_coordinates)
        min_y = min(y for x, y in self.elf_coordinates)
        max_y = max(y for x, y in self.elf_coordinates)

        for x in range(min_x, max_x + 1):
            row = []
            for y in range(min_y, max_y + 1):
                if (x, y) in self.elf_coordinates:
                    row.append('#')  # Elf present
                else:
                    row.append('.')  # Empty ground
            print("".join(row))  # Print the row as a string
        print()  # Add an empty line for spacing between rounds

    def run_simulation(self, rounds):
        for i in range(rounds):
            print(f"== Round {i + 1} ==")
            self.print_map()  # Print the map at the start of each round
            self.simulate_round()

        empty_tiles = self.calculate_empty_tiles()
        print(f"Empty ground tiles after {rounds} rounds: {empty_tiles}")


if __name__ == "__main__":
    simulation = ElfSimulation('test.txt')
    simulation.run_simulation(10)
