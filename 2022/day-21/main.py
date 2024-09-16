import copy


def parse_input(file_path: str):
    """
    Parses the input file and returns a dictionary of monkey jobs.
    """
    monkeys = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            monkey, jobs = line.split(":")
            jobs = jobs.split(" ")
            jobs = [job for job in jobs if job != '']  # Remove empty strings
            if len(jobs) == 1:
                monkeys[monkey] = {'number': int(jobs[0])}
            else:
                monkeys[monkey] = {'neighbours': [jobs[0], jobs[2]], 'operator': jobs[1]}
    return monkeys


def resolve_monkey(monkey, monkeys_local):
    """Resolve the value of a monkey recursively."""
    # Base case: if the monkey already has a number, return it
    if 'number' in monkeys_local[monkey]:
        return monkeys_local[monkey]['number']

    # Otherwise, resolve the two neighbours recursively
    neighbour1 = resolve_monkey(monkeys_local[monkey]['neighbours'][0], monkeys_local)
    neighbour2 = resolve_monkey(monkeys_local[monkey]['neighbours'][1], monkeys_local)
    operator = monkeys_local[monkey]['operator']

    # Perform the appropriate operation
    if operator == '+':
        monkeys_local[monkey]['number'] = neighbour1 + neighbour2
    elif operator == '-':
        monkeys_local[monkey]['number'] = neighbour1 - neighbour2
    elif operator == '*':
        monkeys_local[monkey]['number'] = neighbour1 * neighbour2
    elif operator == '/':
        monkeys_local[monkey]['number'] = neighbour1 // neighbour2  # Integer division

    return monkeys_local[monkey]['number']


def depends_on_humn(monkey, monkeys_local):
    """Recursively check if a monkey depends on 'humn'."""
    if monkey == 'humn':
        return True
    if 'neighbours' not in monkeys_local[monkey]:
        return False
    # Recursively check both neighbours
    return (depends_on_humn(monkeys_local[monkey]['neighbours'][0], monkeys_local) or
            depends_on_humn(monkeys_local[monkey]['neighbours'][1], monkeys_local))


def reverse_operations(monkey, target_value, monkeys_local):
    """Backtrack through the operations to solve for 'humn'."""
    if monkey == 'humn':
        return target_value

    # Check if the monkey has neighbours (if not, it’s a number-yelling monkey and we can stop)
    if 'neighbours' not in monkeys_local[monkey]:
        raise ValueError(f"Monkey {monkey} has no neighbours but still being backtracked.")

    # Get the two neighbours
    neighbour1_name = monkeys_local[monkey]['neighbours'][0]
    neighbour2_name = monkeys_local[monkey]['neighbours'][1]
    operator = monkeys_local[monkey]['operator']

    # Determine which neighbour depends on humn
    if depends_on_humn(neighbour1_name, monkeys_local):
        neighbour_to_solve = neighbour1_name
        other_value = resolve_monkey(neighbour2_name, monkeys_local)
    else:
        neighbour_to_solve = neighbour2_name
        other_value = resolve_monkey(neighbour1_name, monkeys_local)

    # Reverse the operations based on the operator
    if operator == '+':
        return reverse_operations(neighbour_to_solve, target_value - other_value, monkeys_local)
    elif operator == '-':
        if neighbour_to_solve == neighbour1_name:
            return reverse_operations(neighbour_to_solve, target_value + other_value, monkeys_local)
        else:
            return reverse_operations(neighbour_to_solve, other_value - target_value, monkeys_local)
    elif operator == '*':
        return reverse_operations(neighbour_to_solve, target_value // other_value, monkeys_local)
    elif operator == '/':
        if neighbour_to_solve == neighbour1_name:
            return reverse_operations(neighbour_to_solve, target_value * other_value, monkeys_local)
        else:
            return reverse_operations(neighbour_to_solve, other_value // target_value, monkeys_local)


def run_monkey_jobs(monkeys: dict, part_two=False):
    """Runs the monkey jobs and returns the final number for 'root' monkey.
       If part_two is True, it solves for 'humn' by backtracking."""

    if part_two:
        # For part two, root's operation is equality, so we want to find what value makes both sides equal.
        root_deps = monkeys['root']['neighbours']
        left_value = resolve_monkey(root_deps[0], monkeys)
        right_value = resolve_monkey(root_deps[1], monkeys)

        # Determine which side depends on 'humn'
        if depends_on_humn(root_deps[0], monkeys):
            # Backtrack on the left side
            return reverse_operations(root_deps[0], right_value, monkeys)
        else:
            # Backtrack on the right side
            return reverse_operations(root_deps[1], left_value, monkeys)

    # Otherwise, resolve from the root as in part 1
    return resolve_monkey('root', monkeys)


def main():
    # Load the input data once
    monkeys = parse_input('input.txt')

    # Create a deep copy for each part
    monkeys_part1 = copy.deepcopy(monkeys)
    monkeys_part2 = copy.deepcopy(monkeys)

    # Solve Part 1
    part1_result = run_monkey_jobs(monkeys_part1)
    print("Part 1 - Resolved monkey jobs:", part1_result)

    # Solve Part 2
    part2_result = run_monkey_jobs(monkeys_part2, part_two=True)
    print("Part 2 - Value for 'humn' that satisfies root's equality:", part2_result)


# Run the main function to get results for both parts
main()
