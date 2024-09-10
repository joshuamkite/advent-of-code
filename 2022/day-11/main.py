import operator
import math

monkeys = []
worry_levels = {}
# Dictionary to store monkey instances by their IDs for easy access
inspections = {}  # Dictionary to track the number of inspections per round
monkey_dict = {}
challenge_part = 2  # 1 or 2 - depending on which part of the challenge we are tackling

if challenge_part == 1:
    rounds = 20
elif challenge_part == 2:
    rounds = 10000


# need to calculate the Lowest Common Multiple of all the monkeys' inspect_test values to limit the growth of worry levels bringing the system to a halt
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def calculate_lcm_of_monkeys(monkeys):
    lcm_value = monkeys[0].inspect_test
    for monkey in monkeys[1:]:
        lcm_value = lcm(lcm_value, monkey.inspect_test)
    return lcm_value


class Monkey:
    def __init__(self, name, starting_items, new_op, inspect_test, is_true, is_false, challenge_part, lcm_value):
        self.name = name
        self.items = starting_items  # List of starting worry levels
        self.new_op = new_op         # A function to calculate new worry level
        self.inspect_test = inspect_test  # The test for where to throw the item
        self.is_true = is_true       # Monkey to throw to if test is true
        self.is_false = is_false     # Monkey to throw to if test is false
        self.challenge_part = challenge_part  # Store challenge part as instance variable
        self.lcm_value = lcm_value   # LCM value to reduce worry level growth

    def inspect_item(self, old_worry_level):
        # Calculate new worry level using the operation
        new_worry_level = self.new_op(old_worry_level)

        if self.challenge_part == 1:
            # Apply the worry relief (dividing by 3 and rounding down)
            new_worry_level = new_worry_level // 3
        elif self.challenge_part == 2:
            # Don't change the worry level, but apply modulus to limit its growth
            new_worry_level = new_worry_level % self.lcm_value

        return new_worry_level

    def test(self, new_worry_level):
        if new_worry_level % self.inspect_test == 0:
            return self.is_true
        else:
            return self.is_false


def create_monkey_instance(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 7):
        name = int(lines[i].split()[1][:-1])
        starting_items = [int(item.strip()) for item in lines[i + 1].split(':')[1].split(',')]

        operator_mapping = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }

        operation_precursor = lines[i + 2].split('=', 1)
        operation = operation_precursor[1].split()
        operation_operator = operation[1]
        operation_value = (operation[2])

        if operation_value == 'old':
            new_op = lambda x, op=operator_mapping[operation_operator]: op(x, x)
        else:
            new_op = lambda x, op=operator_mapping[operation_operator], val=int(operation_value): op(x, val)

        inspect_precursor = lines[i + 3].split(':')
        inspect_precursor_two = inspect_precursor[1].split()
        inspect_test = int(inspect_precursor_two[2])

        is_true = int(lines[i + 4].split()[5])
        is_false = int(lines[i + 5].split()[5])

        monkey = Monkey(name, starting_items, new_op, inspect_test, is_true, is_false, challenge_part, 0)  # Temp 0 for now
        monkeys.append(monkey)
        monkey_dict[name] = monkey


def play_round(round_num):
    inspections[round_num] = {monkey.name: 0 for monkey in monkeys}

    for monkey in monkeys:
        new_items = []
        for item in monkey.items:
            new_worry_level = monkey.inspect_item(item)
            next_monkey_id = monkey.test(new_worry_level)

            monkey_dict[next_monkey_id].items.append(new_worry_level)
            worry_levels.setdefault(monkey.name, {}).setdefault(next_monkey_id, []).append(new_worry_level)

            inspections[round_num][monkey.name] += 1
            inspections_total[monkey.name] += 1

        monkey.items = new_items  # Clear monkey's items after processing


def main():
    create_monkey_instance('input.txt')

    lcm_value = calculate_lcm_of_monkeys(monkeys)
    for monkey in monkeys:
        monkey.lcm_value = lcm_value  # Set the LCM for each monkey

    global inspections_total
    inspections_total = {monkey.name: 0 for monkey in monkeys}

    for i in range(rounds):
        play_round(i + 1)
        print(f"Round {i + 1} completed")

    inspection_totals = [total for total in inspections_total.values()]
    score = sorted(inspection_totals, reverse=True)
    product_score = score[0] * score[1]
    print(product_score)


if __name__ == "__main__":
    main()
