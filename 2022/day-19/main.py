from collections import namedtuple
from functools import lru_cache
import re


def parse_input(file_path):
    """
    Parses the input file and returns a dictionary of blueprints.

    Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    """

    blueprints = {}
    # Regular expression pattern to match each line of the input file.
    pattern = re.compile(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
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
                    blueprint_num, ore_cost, clay_cost, obsidian_cost, obsidian_clay_cost, geode_cost, geode_obsidian_cost = match.groups()
                    # Add the blueprint to the blueprints dictionary with its details.
                    blueprints[int(blueprint_num)] = {
                        'ore_cost': int(ore_cost),
                        'clay_cost': int(clay_cost),
                        'obsidian_cost': int(obsidian_cost),
                        'obsidian_clay_cost': int(obsidian_clay_cost),
                        'geode_cost': int(geode_cost),
                        'geode_obsidian_cost': int(geode_obsidian_cost)
                    }
                else:
                    # If a line doesn't match the expected pattern, print a warning.
                    print(f"Line {line_num} didn't match pattern and was skipped: {line}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return blueprints


# Define the state
State = namedtuple('State', [
    'ore', 'clay', 'obsidian', 'geodes',
    'ore_robots', 'clay_robots', 'obsidian_robots', 'geode_robots',
    'minutes_left'
])


def maximize_geodes(blueprint, time_limit=24):
    max_geodes = 0

    @lru_cache(maxsize=None)
    def dfs(state):
        nonlocal max_geodes
        if state.minutes_left == 0:
            if state.geodes > max_geodes:
                max_geodes = state.geodes
            return state.geodes

        # Upper bound calculation
        potential_geodes = state.geodes + state.geode_robots * state.minutes_left + (state.minutes_left * (state.minutes_left - 1)) // 2
        if potential_geodes <= max_geodes:
            return 0  # Prune this branch

        # Decide what to build
        build_options = []

        # Option to build geode robot
        if state.ore >= blueprint['geode_cost'] and state.obsidian >= blueprint['geode_obsidian_cost']:
            build_options.append('geode')

        # Option to build obsidian robot
        if state.ore >= blueprint['obsidian_cost'] and state.clay >= blueprint['obsidian_clay_cost']:
            build_options.append('obsidian')

        # Option to build clay robot
        if state.ore >= blueprint['clay_cost']:
            build_options.append('clay')

        # Option to build ore robot
        if state.ore >= blueprint['ore_cost']:
            build_options.append('ore')

        # Option to build nothing
        build_options.append(None)

        max_geodes_current = state.geodes

        for option in build_options:
            new_state = list(state)
            # Collect resources
            new_state[0] += state.ore_robots
            new_state[1] += state.clay_robots
            new_state[2] += state.obsidian_robots
            new_state[3] += state.geode_robots

            # Build the robot if any
            if option == 'geode':
                new_state[0] -= blueprint['geode_cost']
                new_state[2] -= blueprint['geode_obsidian_cost']
                new_state[7] += 1  # geode_robots
            elif option == 'obsidian':
                new_state[0] -= blueprint['obsidian_cost']
                new_state[1] -= blueprint['obsidian_clay_cost']
                new_state[6] += 1  # obsidian_robots
            elif option == 'clay':
                new_state[0] -= blueprint['clay_cost']
                new_state[5] += 1  # clay_robots
            elif option == 'ore':
                new_state[0] -= blueprint['ore_cost']
                new_state[4] += 1  # ore_robots

            # Decrement time
            new_state[8] -= 1

            # Create new state
            new_state_tuple = State(*new_state)

            # Recurse
            geodes = dfs(new_state_tuple)
            if geodes > max_geodes_current:
                max_geodes_current = geodes

        return max_geodes_current

    # Initial state
    initial_state = State(
        ore=0,
        clay=0,
        obsidian=0,
        geodes=0,
        ore_robots=1,
        clay_robots=0,
        obsidian_robots=0,
        geode_robots=0,
        minutes_left=time_limit
    )

    max_geodes = dfs(initial_state)
    return max_geodes


def main():
    blueprints = parse_input("input.txt")
    total_quality = 0
    for bp_id, blueprint in blueprints.items():
        geodes = maximize_geodes(blueprint, time_limit=24)
        quality_level = bp_id * geodes
        print(f"Blueprint {bp_id}: Geodes = {geodes}, Quality Level = {quality_level}")
        total_quality += quality_level
    print(f"Total Quality Level: {total_quality}")


if __name__ == "__main__":
    main()
