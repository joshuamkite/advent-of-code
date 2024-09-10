""" Initial planning:
chunk list by single row
split chunk on comma
for each split convert notation to range
return count of instances where one range is a subset of the other
"""


def row(l):
    # remove whitespace and split into two strings `n-n`
    couple = [pair.strip() for pair in l.split(',')]
    # replace the `-` in each with a comma
    ranged = [item.replace("-", ",")for item in couple]
    # convert to nested list of int `[[n,n],[n,n]]` using `map()`on each part
    cast = [list(map(int, s.split(',')))for s in ranged]
    # create intermediate variables to avoid crazy syntax
    x, y = cast[0], cast[1]

    # checks whether the start of the intersection range (the maximum of the two starts) is less than or equal to the end of the intersection range (the minimum of the two ends).

    return (max(x[0], y[0]) <= min(x[1], y[1]))


with open('input') as file:
    doubled_up = 0
    for line in file:
        if (row(line)) == True:
            doubled_up += 1
    print(doubled_up)
