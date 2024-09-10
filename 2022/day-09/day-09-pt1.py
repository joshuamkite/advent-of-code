""" 
need to read into numpy array and encode rules

 """

#  based on https://galaxyinferno.com/how-to-solve-advent-of-code-2022-day-9-with-python/

import numpy as np

with open('input.txt', 'r') as f:
    # read input by line and generate list of tuples for letter and number following it)
    lines = f.readlines()
    movements = [(entry.strip().split(' ')[0],
                  int(entry.strip().split(' ')[1])
                  )
                 for entry in lines]


print(movements)


# create empty arrays for head and tail

head = np.array([0, 0])
tail = np.array([0, 0])

# encode movement rules


def update_tail(head, tail):
    difference = head - tail
    change_for_tail = {
        # head is 2 up 1 right from tail then tail follows up and right once
        (2, 1): (1, 1),
        # 1 up, 2 right
        (1, 2): (1, 1),
        # 2 up
        (2, 0): (1, 0),
        # 2 up, 1 left
        (2, -1): (1, -1),
        # 1 up, 2 left
        (1, -2): (1, -1),
        # 2 left
        (0, -2): (0, -1),
        # jk additional comments from here
        # 1 down, 2 left
        (-1, -2): (-1, -1),
        # 2 down, 1 left
        (-2, -1): (-1, -1),
        # 2 down
        (-2, 0): (-1, 0),
        # 2 down, 1 right
        (-2, 1): (-1, 1),
        # 1 down, 2 right
        (-1, 2): (-1, 1),
        # 2 right
        (0, 2): (0, 1),
    }
    new_tail_pos = tail + \
        np.array(change_for_tail.get(tuple(difference), (0, 0)))
    return new_tail_pos


def update_head(head, direction):
    if direction == 'R':
        head[1] += 1
    elif direction == 'L':
        head[1] -= 1
    elif direction == 'U':
        head[0] += 1
    elif direction == 'D':
        head[0] -= 1
    return head


tail_positions = set([tuple(tail)])
for direction, distance in movements:
    while distance > 0:
        head = update_head(head, direction)
        distance -= 1
        tail = update_tail(head, tail)
        tail_positions.add(tuple(tail))
        print(f"movements and consequences: {head=}, {tail=}")
print(f"set of tail positions is {tail_positions}")
print(f"number of positing visited by tail is {len(tail_positions)}")
