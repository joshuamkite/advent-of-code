class ElfSimulation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.elf_coordinates = self.parse_input(file_path)
        self.directions = ['N', 'S', 'W', 'E']

    def reset(self):
        self.elf_coordinates = self.parse_input(self.file_path)
        self.directions = ['N', 'S', 'W', 'E']

    def parse_input(self, file_path):
        """ Parse input file and return a set of coordinates of the elves.
        """
        elf_coordinates = set()  # Initialize as a set
        with open(file_path, "r") as file:
            for i, line in enumerate(file):
                for j, char in enumerate(line.strip()):
                    if char == '#':
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
        """
        For a given elf, check the surrounding neighbors and propose a valid move
        based on the direction priority.
        """
        x, y = elf
        neighbors = self.get_neighbors(x, y)
        # Only consider moving if there are other elves in neighboring cells
        if not any(neighbor in self.elf_coordinates for neighbor in neighbors):
            return elf  # No need to move if no neighbors

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
        any_moves = False  # Flag to track if any moves are proposed

        # First half: propose moves
        for elf in self.elf_coordinates:
            proposed_move = self.propose_move(elf)
            if proposed_move != elf:  # If there's a proposed move
                any_moves = True  # At least one move was proposed
                # print(f"Elf at {elf} proposes move to {proposed_move}")  # Debug print

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
                # print(f"Conflict for move to {move} by elves {elves}")  # Debug print
                new_elf_coordinates.update(elves)

        # Rotate directions for the next round
        self.directions = self.directions[1:] + self.directions[:1]

        self.elf_coordinates = new_elf_coordinates

        # Log the result of the round to confirm if moves were made
        # print(f"Round result: any_moves = {any_moves}")

        # Return True if any moves were made, otherwise False
        return any_moves

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

    def run_simulation(self, max_rounds=1000, print_map=False):
        for i in range(max_rounds):
            if print_map:
                print(f"== Round {i + 1} ==")
                self.print_map()

            any_moves = self.simulate_round()

            if not any_moves:
                # print(f"No moves occurred in round {i + 1}. Simulation stopped.")
                return i + 1  # Return the number of rounds completed

        empty_tiles = self.calculate_empty_tiles()
        # print(f"Empty ground tiles after {max_rounds} rounds: {empty_tiles}")
        return max_rounds  # Return max_rounds if we didn't stop early


if __name__ == "__main__":
    file_path = 'input.txt'
    simulation = ElfSimulation(file_path)

    # Part 1: Run 10 rounds and print the map
    part1_rounds = simulation.run_simulation(max_rounds=10, print_map=False)
    empty_tiles = simulation.calculate_empty_tiles()
    print(f"Part 1: Empty ground tiles after {part1_rounds} rounds: {empty_tiles}")

    # Reset the simulation for Part 2
    simulation.reset()

    # Part 2: Run up to 10000 rounds or until no moves occur, no map printing
    part2_rounds = simulation.run_simulation(max_rounds=10000, print_map=False)
    print(f"Part 2: First round with no moves: {part2_rounds}")

    # Debug: Print final state
    # print("Final state:")
    # simulation.print_map()
