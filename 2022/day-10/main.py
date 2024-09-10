""" Start by figuring out the signal being sent by the CPU. The CPU has a single register, X, which starts with the value 1. It supports only two instructions:

addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
noop takes one cycle to complete. It has no other effect.
  if noop

else addx
"""

"""Part 2

1. **2D Array (Screen)**: You're constructing a 2D grid where each row represents a line of pixels (40 pixels wide).
   
2. **Mapping Columns to Clock Cycles**: Each column in a row corresponds to a clock cycle, so as you iterate through cycles, you're filling in the pixels row by row.

3. **Sprite Position (Controlled by X)**: The sprite's position is determined by the value of `X` at each cycle. This value describes the center of the sprite, and the sprite spans `X-1`, `X`, and `X+1`.

4. **Sprite Visibility Check**: For each cycle, you need to check if the current pixel (i.e., column) being drawn falls within the sprite's range `[X-1, X, X+1]`.

5. **Rendering the Pixel**: If the sprite is within the range of the current pixel, render a `#`. If it isn't, render a `.`.

This system ensures that each clock cycle evaluates the sprite's visibility for that specific pixel, building the display row by row. 

"""


# define iterator (ordered dict)
cycles = {}
cycle_counter = 0
x = 1  # Register X starts at 1


with open('input.txt', 'r') as file:

    for line in file:

        line = line.strip()

        if line == 'noop':
            # noop takes 1 cycle, X doesn't change
            cycle_counter += 1
            cycles[cycle_counter] = x  # Record X value for this cycle

        elif line.startswith('addx'):
            # addx takes 2 cycles to complete
            cycle_counter += 1
            cycles[cycle_counter] = x  # Record X before the change (1st cycle)

            cycle_counter += 1
            cycles[cycle_counter] = x  # Record X again (2nd cycle)

            # Update X after 2 cycles
            _, value = line.split()
            x += int(value)

# Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?

cycles_of_interest = [20, 60, 100, 140, 180, 220]

sum_of_signal_strengths = 0

# Get the signal strength for each cycle of interest and sum them
for cycle in cycles_of_interest:
    sum_of_signal_strengths += cycles[cycle]*cycle

print("part 1 answer:", sum_of_signal_strengths)


# 2D Array (Screen) - 40 pixels wide
screen = [[' ' for _ in range(40)] for _ in range(6)]

# Mapping Columns to Clock Cycles
for cycle in cycles:
    # Sprite Position (Controlled by X)
    x = cycles[cycle]

    # Sprite Visibility Check
for cycle, x in cycles.items():
    # Calculate row and column for the current cycle
    row = (cycle - 1) // 40  # Which row the cycle falls into
    col = (cycle - 1) % 40   # Which column the cycle falls into

    # Make sure we're within screen bounds
    if row < 6:
        # Check if the current column is within the sprite's range (X-1, X, X+1)
        if col in [x-1, x, x+1]:
            screen[row][col] = '#'  # Render a lit pixel

# Print the screen
for row in screen:
    print(''.join(row))  # Print each row as a string
