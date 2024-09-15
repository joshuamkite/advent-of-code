Here I adapted the input passing from an earlier solution in this series to use `re` and populate a dictionary. After this I had to hand over!

## Overview

This Python solution simulates the process of building resource-collecting robots based on blueprints and maximizing the number of geodes that can be cracked within a 24-minute time limit. The objective is to determine the quality level of each blueprint by multiplying the blueprint's ID with the largest number of geodes cracked using that blueprint.

The solution involves parsing the input, representing the state of resources and robots at each minute, and using a depth-first search (DFS) with memoization and pruning to explore possible robot-building sequences and maximize geode cracking.

## Solution Workflow

1. **Input Parsing:** 
   The program reads the input file containing blueprints and extracts the robot costs for ore, clay, obsidian, and geode-cracking robots.

2. **State Representation:**
   The state at any minute includes:
   - Resources (ore, clay, obsidian, geodes)
   - Robots (ore-collecting, clay-collecting, obsidian-collecting, geode-cracking)
   - Minutes remaining

3. **Depth-First Search (DFS):**
   A DFS algorithm explores possible sequences of robot builds over the 24-minute time limit, with memoization to cache states and pruning to eliminate branches that cannot surpass the current best solution.

4. **Maximization of Geodes:**
   The goal is to maximize the number of geodes cracked. At each minute, the algorithm considers whether to build a robot (if resources allow) or do nothing, updating the state accordingly.

5. **Output:**
   The program outputs the quality level for each blueprint by multiplying the blueprint's ID by the number of geodes cracked. It also provides the total quality level sum across all blueprints.

## Optimization

The program uses memoization and pruning techniques to minimize the computational cost of exploring possible robot build sequences, making it efficient even with multiple blueprints.