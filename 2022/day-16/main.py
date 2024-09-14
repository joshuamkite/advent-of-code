import re
from collections import deque
import sys
from functools import lru_cache


def parse_input(file_path):
    """
    Parses the input file and returns a dictionary of valves.

    Each valve is represented as a key with a dictionary value containing:
    - 'flow_rate': Integer flow rate of the valve.
    - 'tunnels': List of connected valves.

    Parameters:
    - file_path (str): The path to the input file.

    Returns:
    - dict: A dictionary representing all valves with their flow rates and connected tunnels.
    """
    valves = {}
    # Regular expression pattern to match each line of the input file.
    # It captures the valve name, flow rate, and the list of connected tunnels.
    pattern = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )
    try:
        # Open and read the input file line by line.
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()  # Remove leading/trailing whitespace.
                if not line:
                    continue  # Skip empty lines.
                match = pattern.match(line)
                if match:
                    valve, flow_rate, tunnels = match.groups()
                    # Split the tunnels by comma and remove any extra whitespace.
                    tunnels = [tunnel.strip() for tunnel in tunnels.split(",")]
                    # Add the valve to the valves dictionary with its details.
                    valves[valve] = {
                        'flow_rate': int(flow_rate),
                        'tunnels': tunnels
                    }
                else:
                    # If a line doesn't match the expected pattern, print a warning.
                    print(f"Line {line_num} didn't match pattern and was skipped: {line}")
    except FileNotFoundError:
        # Handle the case where the input file does not exist.
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        # Handle any other exceptions that may occur during file reading/parsing.
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    return valves


def bfs(start, graph):
    """
    Performs Breadth-First Search (BFS) to find the shortest paths from the start valve to all other valves.

    Since each tunnel traversal takes 1 minute, BFS efficiently finds the minimum time required to reach each valve.

    Parameters:
    - start (str): The starting valve.
    - graph (dict): The graph representing valves and their connected tunnels.

    Returns:
    - dict: A dictionary mapping each reachable valve to its distance (in minutes) from the start valve.
    """
    queue = deque([(start, 0)])  # Initialize the queue with the start valve and distance 0.
    visited = {start: 0}          # Dictionary to keep track of visited valves and their distances.
    while queue:
        current, distance = queue.popleft()  # Dequeue the next valve and its distance.
        for neighbor in graph[current]['tunnels']:
            if neighbor not in visited:
                visited[neighbor] = distance + 1  # Update distance for the neighbor.
                queue.append((neighbor, distance + 1))  # Enqueue the neighbor for further exploration.
    return visited


def main():
    """
    The main function orchestrates the reading of input, processing of data, and computation of the maximum pressure release.
    It handles both Part One and Part Two of the challenge.

    Steps:
    1. Parse the input file to extract valve information.
    2. Identify useful valves (those with a positive flow rate).
    3. Assign each useful valve a unique bit position.
    4. Precompute shortest paths between all relevant valves using BFS.
    5. Use DFS with memoization to find the optimal sequence of valve openings for Part One.
    6. Collect maximum pressures for all subsets of valves for Part Two.
    7. Combine the results of two actors (you and the elephant) to find the maximum total pressure for Part Two.
    8. Output the results for both parts.
    """

    input_file = 'input.txt'  # Specify the input file path.

    # Step 1: Parse the input file to obtain the valves dictionary.
    valves = parse_input(input_file)

    # Step 2: Identify useful valves (valves with a flow rate greater than 0).
    useful_valves = {valve: details for valve, details in valves.items() if details['flow_rate'] > 0}
    if not useful_valves:
        # If no useful valves are found, there's nothing to do.
        print("No useful valves found (all have flow rate=0). Nothing to do.")
        return

    # Step 3: Assign each useful valve a unique bit position.
    valve_indices = {valve: idx for idx, valve in enumerate(useful_valves)}
    # For debugging purposes, you can print the valve indices.
    # print("Valve Indices:", valve_indices)

    # Step 4: Precompute shortest paths between all relevant valves.
    # Relevant valves include all useful valves plus the starting valve 'AA'.
    all_relevant = list(useful_valves.keys()) + ['AA']
    shortest_paths = {}
    for valve in all_relevant:
        if valve in valves:
            # Compute the shortest paths from the current valve to all other valves.
            shortest_paths[valve] = bfs(valve, valves)
        else:
            # Warn if a relevant valve is not found in the valves dictionary.
            print(f"Warning: Valve '{valve}' not found in the valves dictionary.")

    # Ensure that 'AA' is present in the shortest paths.
    if 'AA' not in shortest_paths:
        print("Error: Starting valve 'AA' not found in the shortest paths.")
        sys.exit(1)

    # Step 5: Use DFS with memoization to find the optimal sequence of valve openings for Part One.
    # We'll use bitmasking to represent opened valves.

    @lru_cache(maxsize=None)
    def dfs(current_valve, time_elapsed, opened_bitmask):
        """
        Recursively explores all possible sequences of valve openings to maximize pressure release.

        Utilizes memoization to cache and reuse results of previously computed states, enhancing efficiency.

        Parameters:
        - current_valve (str): The valve where the user is currently located.
        - time_elapsed (int): Total time elapsed so far.
        - opened_bitmask (int): Bitmask representing the set of opened valves.

        Returns:
        - int: Maximum pressure that can be released from the current state onward.
        """
        max_pressure = 0

        for valve, details in useful_valves.items():
            bit = 1 << valve_indices[valve]
            if not (opened_bitmask & bit):
                # Calculate the time required to move to this valve and open it.
                time_to_valve = shortest_paths[current_valve].get(valve, float('inf'))
                time_needed = time_to_valve + 1  # +1 minute to open the valve.
                new_time = time_elapsed + time_needed

                if new_time < 30:
                    # Calculate the pressure released by opening this valve.
                    remaining_time = 30 - new_time
                    pressure = details['flow_rate'] * remaining_time

                    # Recursively explore further openings.
                    total_pressure = pressure + dfs(valve, new_time, opened_bitmask | bit)

                    if total_pressure > max_pressure:
                        max_pressure = total_pressure

        return max_pressure

    # Calculate Part One
    part_one_result = dfs('AA', 0, 0)
    print(f"Part One: {part_one_result}")

    # Step 6: For Part Two, compute the maximum pressure achievable by two actors without overlapping valves.
    # We'll iterate through all possible subsets, calculate their pressures, and find the best pair of disjoint subsets.

    # Initialize a dictionary to store maximum pressure for each subset.
    max_pressures = {}

    def dfs_part2(current_valve, time_elapsed, opened_bitmask, pressure):
        """
        DFS function for Part Two that records maximum pressure for each subset of opened valves.

        Parameters:
        - current_valve (str): Current valve position.
        - time_elapsed (int): Time elapsed so far.
        - opened_bitmask (int): Bitmask of opened valves.
        - pressure (int): Current accumulated pressure.

        Updates:
        - max_pressures (dict): Updates the maximum pressure for the current subset.
        """
        # If the current subset has a higher pressure, update it.
        if opened_bitmask not in max_pressures or pressure > max_pressures[opened_bitmask]:
            max_pressures[opened_bitmask] = pressure

        for valve, details in useful_valves.items():
            bit = 1 << valve_indices[valve]
            if not (opened_bitmask & bit):
                # Calculate the time required to move to this valve and open it.
                time_to_valve = shortest_paths[current_valve].get(valve, float('inf'))
                time_needed = time_to_valve + 1  # +1 minute to open the valve.
                new_time = time_elapsed + time_needed

                if new_time < 26:
                    # Calculate the pressure released by opening this valve.
                    remaining_time = 26 - new_time
                    new_pressure = details['flow_rate'] * remaining_time

                    # Recursively explore further openings.
                    dfs_part2(valve, new_time, opened_bitmask | bit, pressure + new_pressure)

    # Start DFS for Part Two.
    dfs_part2('AA', 0, 0, 0)

    # Step 7: Combine the results of two actors to find the maximum total pressure.
    max_total_pressure_part2 = 0
    all_bitmasks = list(max_pressures.keys())

    for i, bitmask1 in enumerate(all_bitmasks):
        pressure1 = max_pressures[bitmask1]
        for bitmask2 in all_bitmasks[i:]:  # Start from i to avoid duplicate pairs.
            if bitmask1 & bitmask2 == 0:
                pressure2 = max_pressures[bitmask2]
                total_pressure = pressure1 + pressure2
                if total_pressure > max_total_pressure_part2:
                    max_total_pressure_part2 = total_pressure

    # Output the result for Part Two.
    print(f"Part Two: {max_total_pressure_part2}")


# Entry point of the script.
if __name__ == "__main__":
    main()
