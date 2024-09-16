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


def resolve_monkey(monkey, monkeys):
    # Base case: if the monkey already has a number, return it
    if 'number' in monkeys[monkey]:
        return monkeys[monkey]['number']

    # Otherwise, resolve the two neighbours recursively
    neighbour1 = resolve_monkey(monkeys[monkey]['neighbours'][0], monkeys)
    neighbour2 = resolve_monkey(monkeys[monkey]['neighbours'][1], monkeys)
    operator = monkeys[monkey]['operator']

    # Perform the appropriate operation
    if operator == '+':
        monkeys[monkey]['number'] = neighbour1 + neighbour2
    elif operator == '-':
        monkeys[monkey]['number'] = neighbour1 - neighbour2
    elif operator == '*':
        monkeys[monkey]['number'] = neighbour1 * neighbour2
    elif operator == '/':
        monkeys[monkey]['number'] = neighbour1 // neighbour2  # Integer division

    return monkeys[monkey]['number']


def run_monkey_jobs(monkeys: dict):
    """Runs the monkey jobs and returns the final number for 'root' monkey."""
    return resolve_monkey('root', monkeys)


def main():
    monkeys = parse_input('input.txt')
    print("Resolved monkey jobs:", run_monkey_jobs(monkeys))


if __name__ == "__main__":
    main()
