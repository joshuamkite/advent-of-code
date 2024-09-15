# Boiling Boulders Simulation

## Note on use of ChatGPT

Initially I was looking at architecting the code, focussing first on parsing the input to a suitable data structure. Here I ran afoul of ChatGPT racing ahead, including in this case the solution to part 2 before I had presented it. Obviously it had seen this problem before...

## Overview

This project simulates the surface area calculation of a 3D lava droplet composed of multiple 1x1x1 cubes. It addresses two main challenges:

1. **Part 1:** Calculate the total surface area by counting all exposed sides of each cube.
2. **Part 2:** Calculate the external surface area by excluding sides adjacent to internal cavities within the droplet.

## Design Choices

- **Data Structures:**
  - **Set for Cube Positions:** Utilizes a Python `set` to store cube coordinates for efficient O(1) lookup during neighbor checks.
  
- **Modular Functions:**
  - **`read_input`:** Parses the input file and stores cube positions.
  - **`calculate_total_surface_area`:** Computes the total surface area by checking all six neighbors of each cube.
  - **`calculate_external_surface_area`:** Uses a flood-fill (BFS) algorithm to identify external air pockets and exclude internal cavities from the surface area calculation.

- **Efficiency:**
  - Designed to handle inputs with up to **3,000 cubes** efficiently, ensuring swift execution on modern hardware.
