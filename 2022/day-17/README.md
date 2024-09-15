# Rock Tower Simulation

## Overview

This project simulates rocks falling into a chamber influenced by a sequence of jet pushes. The simulation is divided into two parts:

1. **Part 1:** Simulates the falling of 2,022 rocks to determine the tower's height after all rocks have settled.
2. **Part 2:** Extends the simulation to handle 1,000,000,000,000 (10¹²) rocks efficiently by implementing optimization techniques.

## Design Choices for Part 1

### Object-Oriented Approach

- **Classes:**
  - **`Rock`:** Represents a rock with a specific shape and position. Handles movement and visualization of its shape.
  - **`Chamber`:** Represents the chamber where rocks fall. Manages the state of the chamber, including occupied positions, jet sequences, and the highest point of the tower.

### Simulation Mechanics

- **Rock Shapes:** Defined as lists of `(x, y)` tuples representing their structure. Five distinct shapes (`horizontal_line`, `plus_sign`, `reverse_l`, `vertical_line`, `square`) are used in a repeating sequence. Chosen as most straightforward to work with.
- **Jet Sequence:** Reads a sequence of `<` and `>` characters from an input file (`input.txt`) to determine the direction of jet pushes (`left` or `right`) applied to each falling rock.
- **Movement Logic:** Each rock is pushed by the jet sequence and then attempts to fall down one unit. Collision detection ensures rocks do not overlap, go beyond chamber boundaries, or fall below the floor.
- **Visualization:** Optional visualization prints the chamber's state, showing the positions of settled rocks (`#`) and the currently falling rock (`@`).

## Modifications for Part 2

Simulating 1,000,000,000,000 rocks directly is computationally intensive. To address this, the following optimizations were implemented:

### Cycle Detection

- **Purpose:** Identify repeating patterns in the simulation to predict the tower's height without simulating every single rock.
- **Implementation:**
  - **State Tracking:** After each rock settles, capture a unique state signature consisting of:
    - Current rock shape index.
    - Current jet sequence index.
    - A profile of the chamber's top (relative heights of each column).
  - **Cycle Identification:** Store each unique state in a dictionary. When a state repeats, a cycle is detected.
  - **Height Calculation:** Calculate the number of rocks and height gained per cycle. Use this information to compute the total height for the remaining rocks efficiently.

### Chamber Profile

- **Function:** Captures the top `N` rows of the chamber to create a profile that aids in accurately detecting cycles.
- **Customization:** The depth of the profile can be adjusted to balance between accuracy and memory usage.

### Optimized Simulation Loop

- **Process:**
  - Simulate rocks until a cycle is detected.
  - Calculate how many complete cycles fit into the remaining number of rocks.
  - Increment the tower height based on the number of cycles and the height gained per cycle.
  - Simulate any remaining rocks individually after accounting for complete cycles.
