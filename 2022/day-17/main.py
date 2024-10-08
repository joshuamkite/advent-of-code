class Rock:
    def __init__(self, shape, initial_position):
        """
        Initializes a new rock.

        Parameters:
        - shape: List of (x, y) tuples representing the rock's shape.
        - initial_position: (x, y) tuple representing the rock's initial position in the chamber.
        """
        self.shape = shape
        self.position = initial_position  # (x, y)

    def get_absolute_positions(self):
        """
        Calculates the absolute positions of the rock's blocks based on its current position.

        Returns:
        - Set of (x, y) tuples representing the absolute positions.
        """
        x_offset, y_offset = self.position
        return {(x + x_offset, y + y_offset) for (x, y) in self.shape}

    def move(self, direction):
        """
        Moves the rock in the specified direction.

        Parameters:
        - direction: 'left', 'right', or 'down'.

        Returns:
        - New position as a (x, y) tuple after movement.
        """
        x, y = self.position
        if direction == 'left':
            return (x - 1, y)
        elif direction == 'right':
            return (x + 1, y)
        elif direction == 'down':
            return (x, y - 1)
        else:
            raise ValueError("Invalid direction. Use 'left', 'right', or 'down'.")

    def visualize_shape(self):
        """
        Visualizes the rock's shape.

        Returns:
        - None. Prints the shape to the console.
        """
        shape = self.shape

        if not shape:
            print("Empty shape.")
            return

        # Determine the bounds of the shape
        min_x = min(x for x, y in shape)
        max_x = max(x for x, y in shape)
        min_y = min(y for x, y in shape)
        max_y = max(y for x, y in shape)

        # Calculate width and height
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Initialize the grid with empty spaces
        grid = [['.' for _ in range(width)] for _ in range(height)]

        # Mark the rock blocks with '#'
        for x, y in shape:
            grid[max_y - y][x - min_x] = '#'  # Invert y for top-down printing

        # Print the grid
        for row in grid:
            print(''.join(row))
        print()  # Add an empty line for better readability


class Chamber:
    def __init__(self, jet_sequence):
        """
        Initializes the chamber.

        Parameters:
        - jet_sequence: List of jet directions ('<' or '>').
        """
        self.width = 7
        self.occupied = set()  # Set of (x, y) tuples
        self.jet_sequence = jet_sequence
        self.jet_index = 0
        self.highest_y = -1  # Start from floor at y = -1

    def get_next_jet(self):
        """
        Retrieves the next jet direction and updates the jet index.

        Returns:
        - 'left' or 'right'
        """
        jet = self.jet_sequence[self.jet_index % len(self.jet_sequence)]
        self.jet_index += 1
        return 'left' if jet == '<' else 'right'

    def spawn_rock(self, shape):
        """
        Spawns a new rock with the given shape.

        Parameters:
        - shape: List of (x, y) tuples representing the rock's shape.

        Returns:
        - Instance of Rock placed at the initial position.
        """
        initial_x = 2  # Two units away from the left wall
        initial_y = self.highest_y + 4  # Three units above the highest rock
        rock = Rock(shape, (initial_x, initial_y))
        return rock

    def check_collision(self, rock):
        """
        Checks if the rock collides with walls, floor, or other rocks.

        Parameters:
        - rock: Instance of Rock.

        Returns:
        - True if collision occurs, False otherwise.
        """
        for (x, y) in rock.get_absolute_positions():
            # Check walls
            if x < 0 or x >= self.width:
                return True
            # Check floor
            if y < 0:
                return True
            # Check occupied positions
            if (x, y) in self.occupied:
                return True
        return False

    def update_occupied(self, rock):
        """
        Updates the occupied positions with the rock's final position.

        Parameters:
        - rock: Instance of Rock.
        """
        for pos in rock.get_absolute_positions():
            self.occupied.add(pos)
            if pos[1] > self.highest_y:
                self.highest_y = pos[1]

    def move_rock(self, rock, direction):
        """
        Attempts to move the rock in the specified direction.

        Parameters:
        - rock: Instance of Rock.
        - direction: 'left', 'right', or 'down'.

        Returns:
        - True if movement was successful, False otherwise.
        """
        # Get the new position based on the direction
        new_position = rock.move(direction)

        # Temporarily update the rock's position
        original_position = rock.position
        rock.position = new_position

        # Check for collision
        if self.check_collision(rock):
            # Collision detected; revert to original position
            rock.position = original_position
            return False
        return True

    def get_chamber_profile(self, depth=30):
        """
        Captures the top 'depth' rows of the chamber to create a profile.

        Parameters:
        - depth: Number of top rows to include in the profile.

        Returns:
        - Tuple representing the relative heights of each column.
        """
        profile = []
        for x in range(self.width):
            # Find the highest rock in this column
            column_heights = [y for (col_x, y) in self.occupied if col_x == x]
            if column_heights:
                max_y = max(column_heights)
            else:
                max_y = -1  # No rocks in this column
            # Calculate the relative height from the top
            relative_height = self.highest_y - max_y
            profile.append(relative_height)
        return tuple(profile)

    def simulate_fall(self, rock_shapes, total_rocks):
        """
        Simulates the falling of rocks in the chamber.

        Parameters:
        - rock_shapes: List of rock shapes (list of (x, y) tuples).
        - total_rocks: Number of rocks to simulate.

        Returns:
        - Final tower height after simulation.
        """
        rock_count = 0
        shape_index = 0

        # Dictionary to store seen states
        # Key: (shape_index % len(rock_shapes), jet_index % len(jet_sequence), chamber_profile)
        # Value: (rock_count, highest_y)
        seen_states = {}
        additional_height = 0  # Height gained from cycles

        while rock_count < total_rocks:
            # Spawn a new rock based on the current shape in sequence
            shape = rock_shapes[shape_index % len(rock_shapes)]
            rock = self.spawn_rock(shape)
            shape_index += 1

            # Continue moving the rock until it comes to rest
            while True:
                # Apply jet push
                jet_direction = self.get_next_jet()
                self.move_rock(rock, jet_direction)

                # Attempt to move down (gravity)
                moved_down = self.move_rock(rock, 'down')

                if not moved_down:
                    # Rock comes to rest; update occupied positions
                    self.update_occupied(rock)
                    rock_count += 1
                    break

            # After the rock has settled, capture the current state
            state_key = (
                shape_index % len(rock_shapes),
                self.jet_index % len(self.jet_sequence),
                self.get_chamber_profile()
            )

            if state_key in seen_states and rock_count < total_rocks:
                # Cycle detected
                previous_rock_count, previous_height = seen_states[state_key]
                cycle_length = rock_count - previous_rock_count
                cycle_height = self.highest_y - previous_height

                # Calculate how many cycles can fit into the remaining rocks
                remaining_rocks = total_rocks - rock_count
                cycles = remaining_rocks // cycle_length

                if cycles > 0:
                    # Apply the cycle height and increment the rock count accordingly
                    additional_height += cycles * cycle_height
                    rock_count += cycles * cycle_length
            else:
                # Store the state
                seen_states[state_key] = (rock_count, self.highest_y)

        # Total height is the current highest_y plus any additional height from cycles
        total_height = self.highest_y + 1 + additional_height  # +1 to account for zero indexing
        return total_height  # Return the final tower height

    def visualize(self, current_rock=None):
        """
        Visualizes the current state of the chamber.

        Parameters:
        - current_rock: Instance of Rock (optional).

        Returns:
        - None. Prints the chamber to the console.
        """
        # Determine the visualization range
        if current_rock:
            current_rock_max_y = max(y for _, y in current_rock.get_absolute_positions())
            max_y = max(self.highest_y, current_rock_max_y) + 5  # Add extra space for better visibility
        else:
            max_y = self.highest_y + 5  # Add extra space for better visibility
        min_y = 0

        for y in range(max_y, min_y - 1, -1):
            row = '|'
            for x in range(self.width):
                if current_rock and (x, y) in current_rock.get_absolute_positions():
                    row += '@'
                elif (x, y) in self.occupied:
                    row += '#'
                else:
                    row += '.'
            row += '|'
            print(row)
        print('+' + '-' * self.width + '+')


def main():
    # Open the input file once
    with open('input.txt', 'r') as file:
        jet_sequence = list(file.read().strip())

    # Print the jet sequence (Optional: Comment out if not needed)
    # print("Jet Sequence:", ''.join(jet_sequence))

    # Coordinate tuples for falling rock shapes
    horizontal_line = [(0, 0), (1, 0), (2, 0), (3, 0)]
    plus_sign = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    reverse_l = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    vertical_line = [(0, 0), (0, 1), (0, 2), (0, 3)]
    square = [(0, 0), (1, 0), (0, 1), (1, 1)]

    rock_shapes = [horizontal_line, plus_sign, reverse_l, vertical_line, square]

    # Optional: Visualize each rock shape individually for debugging (Comment out if not needed)
    # print("\nIndividual Rock Shapes:")
    # for idx, shape in enumerate(rock_shapes, start=1):
    #     print(f"\nRock {idx}:")
    #     rock = Rock(shape, (0, 0))
    #     rock.visualize_shape()

    # Initialize the chamber
    chamber = Chamber(jet_sequence)

    # -----------------------------
    # Part 1: Simulate 2022 Rocks
    # -----------------------------
    total_rocks_to_simulate_part1 = 2022
    part1_height = chamber.simulate_fall(rock_shapes, total_rocks_to_simulate_part1)

    # Print final tower height for Part 1
    print(f"part1: {part1_height}")

    # -----------------------------
    # Part 2: Simulate 1000000000000 Rocks
    # -----------------------------
    total_rocks_to_simulate_part2 = 1000000000000

    # Reset chamber for Part 2
    chamber = Chamber(jet_sequence)

    part2_height = chamber.simulate_fall(rock_shapes, total_rocks_to_simulate_part2)

    # Print final tower height for Part 2
    print(f"part2: {part2_height}")


if __name__ == "__main__":
    main()
