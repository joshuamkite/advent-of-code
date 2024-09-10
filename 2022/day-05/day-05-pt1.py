

with open('input.txt', 'r') as f:
    lines = f.readlines()
    lines = [entry for entry in lines]
# lines

number_of_crates = len(lines[0])//4

crate_lines = lines[:lines.index('\n')-1]
moving_lines = lines[lines.index('\n')+1:]

items = list(lines)[1:-1:4]


amount, source, target = [
    int(entry) for entry in moving_lines.strip().split(' ') if entry.isdigit()]


print(amount, source, target)
