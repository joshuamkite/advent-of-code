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
    # checks if range x is a subset of range y, and (y[0] >= x[0] and y[1] <= x[1]) checks if range y is a subset of range x. If either condition is true, return True; otherwise, return False.
    return (x[0] >= y[0] and x[1] <= y[1]) or (y[0] >= x[0] and y[1] <= x[1])


with open('input') as file:
    doubled_up = 0
    for line in file:
        if (row(line)) == True:
            doubled_up += 1
    print(doubled_up)
