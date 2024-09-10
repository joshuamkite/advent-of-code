def get_priority(ch):
    if 'a' <= ch <= 'z':
        return ord(ch) - ord('a') + 1
    else:
        return ord(ch) - ord('A') + 27


def solve(rucksacks):
    total_priority = 0
    for i in range(0, len(rucksacks), 3):  # group the rucksacks in threes
        common_items = set(rucksacks[i])
        for j in range(1, 3):
            common_items &= set(rucksacks[i+j])
        if common_items:  # there should be exactly one common item
            total_priority += get_priority(list(common_items)[0])
    return total_priority


def main():
    with open('input', 'r') as file:
        rucksacks = file.read().splitlines()
    print(solve(rucksacks))


if __name__ == "__main__":
    main()
