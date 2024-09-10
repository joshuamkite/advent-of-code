def get_priority(ch):
    if 'a' <= ch <= 'z':  # if the character is a lowercase letter
        # return its position in the sequence of lowercase letters, plus an offset of 1
        return ord(ch) - ord('a') + 1
    else:  # the character is an uppercase letter
        # return its position in the sequence of uppercase letters, plus an offset of 27
        return ord(ch) - ord('A') + 27


def solve(rucksacks):
    total_priority = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        first_half = set(rucksack[:half])
        second_half = set(rucksack[half:])
        common_item = first_half & second_half
        if common_item:  # there should be exactly one common item
            total_priority += get_priority(list(common_item)[0])
    return total_priority


def main():
    with open('input', 'r') as file:
        rucksacks = file.read().splitlines()
    print(solve(rucksacks))


if __name__ == "__main__":
    main()
