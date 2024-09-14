import re
from collections import deque
import sys


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
            for line in file:
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
                    print(f"Line didn't match pattern and was skipped: {line}")
    except FileNotFoundError:
        # Handle the case where the input file does not exist.
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except Exception as e:
        # Handle any other exceptions that may occur during file reading/parsing.
        print(f"An error occurred while reading the file: {e}")
        exit(1)
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


def maximize_pressure(current_valve, time_elapsed, opened, memo, useful_valves, shortest_paths, time_limit):
    """
    Recursively explores all possible sequences of valve openings to maximize pressure release.

    Utilizes memoization to cache and reuse results of previously computed states, enhancing efficiency.

    Parameters:
    - current_valve (str): The valve where the user is currently located.
    - time_elapsed (int): Total time elapsed so far.
    - opened (set): Set of valves that have been opened.
    - memo (dict): Dictionary used for memoization to cache results of subproblems.
    - useful_valves (dict): Dictionary of valves with positive flow rates.
    - shortest_paths (dict): Precomputed shortest paths between valves.
    - time_limit (int): Total time available (e.g., 30 minutes).

    Returns:
    - int: Maximum pressure that can be released from the current state onward.
    """
    # Create a unique key for the current state to use in memoization.
    # The key consists of the current valve, time elapsed, and a sorted tuple of opened valves.
    key = (current_valve, time_elapsed, tuple(sorted(opened)))
    if key in memo:
        # If the current state has already been computed, return the cached result.
        return memo[key]

    max_pressure = 0  # Initialize the maximum pressure for this state.

    # Iterate through all useful valves to consider opening them next.
    for valve, details in useful_valves.items():
        if valve not in opened:
            # Calculate the time required to move to this valve and open it.
            time_to_valve = shortest_paths[current_valve].get(valve, float('inf'))
            time_needed = time_to_valve + 1  # +1 minute to open the valve.
            new_time = time_elapsed + time_needed  # Update the elapsed time.

            if new_time < time_limit:
                # If there's still time left after opening the valve, calculate the pressure it will release.
                remaining_time = time_limit - new_time
                pressure = details['flow_rate'] * remaining_time

                # Recursively explore the next steps from the new state.
                total_pressure = pressure + maximize_pressure(
                    valve,
                    new_time,
                    opened | {valve},  # Add the current valve to the set of opened valves.
                    memo,
                    useful_valves,
                    shortest_paths,
                    time_limit
                )

                # Update the maximum pressure if the current path yields a higher value.
                if total_pressure > max_pressure:
                    max_pressure = total_pressure

    # Cache the result for the current state to avoid redundant computations.
    memo[key] = max_pressure
    return max_pressure


def main():
    """
    The main function orchestrates the reading of input, processing of data, and computation of the maximum pressure release.

    Steps:
    1. Parse the input file to extract valve information.
    2. Identify useful valves (those with a positive flow rate).
    3. Precompute shortest paths between all relevant valves using BFS.
    4. Handle unreachable useful valves by excluding them from consideration.
    5. Use DFS with memoization to find the optimal sequence of valve openings.
    6. Output the maximum total pressure that can be released.
    """

    input_file = 'input.txt'

    # Step 1: Parse the input file to obtain the valves dictionary.
    valves = parse_input(input_file)

    # Step 2: Identify useful valves (valves with a flow rate greater than 0).
    useful_valves = {valve: details for valve, details in valves.items() if details['flow_rate'] > 0}
    if not useful_valves:
        # If no useful valves are found, there's nothing to do.
        print("No useful valves found (all have flow rate=0). Nothing to do.")
        return

    # Step 3: Precompute shortest paths between all relevant valves.
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

    # Step 4: Verify that all useful valves are reachable from 'AA'.
    # Remove any useful valves that cannot be reached from 'AA'.
    unreachable_valves = [valve for valve in useful_valves if valve not in shortest_paths.get('AA', {})]
    if unreachable_valves:
        print(f"Warning: The following useful valves are not reachable from 'AA' and will be ignored: {unreachable_valves}")
        for valve in unreachable_valves:
            del useful_valves[valve]

    # Step 5: Optimize the valve opening sequence using DFS with memoization.
    memo = {}  # Initialize the memoization dictionary.
    time_limit = 30  # Total time available in minutes.
    max_total_pressure = maximize_pressure(
        current_valve='AA',     # Starting at valve 'AA'.
        time_elapsed=0,         # No time has elapsed at the start.
        opened=set(),           # No valves have been opened yet.
        memo=memo,
        useful_valves=useful_valves,
        shortest_paths=shortest_paths,
        time_limit=time_limit
    )

    # Step 6: Output the result.
    print(f"Maximum Total Pressure Released: {max_total_pressure}")


# Entry point of the script.
if __name__ == "__main__":
    main()
