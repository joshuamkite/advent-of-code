
"""
Opponent:

A=rock
B=paper
C=scissors

You:

rock, 1
paper, 2
scissors, 3

plus
pt 2

X=lose, 0
Y=draw, 3
Z=win, 6

 """


def chunk_score(l):
    score = 0
    for entry in l:
        match entry:
            case "A X":  # rock, lose, scissors
                score += 3  # 0+3
            case "A Y":  # rock,draw, rock
                score += 4  # 3+1
            case "A Z":  # rock, win, paper
                score += 8  # 6+2
            case "B X":  # paper, lose, rock
                score += 1  # 0+1
            case "B Y":  # paper, draw, paper
                score += 5  # 3+2
            case "B Z":  # paper,win, scissors
                score += 9  # 6+3
            case "C X":  # scissors, lose, paper
                score += 2  # 0+2
            case "C Y":  # scissors, draw, scissors
                score += 6  # 3+3
            case "C Z":  # scissors, win, rock
                score += 7  # 6+1
            case _:
                score += 0
    return score


""" This function takes two arguments, l and n. l is a list of elements, and n is the number of elements you want in each chunk.

Now let's break down the list comprehension in the return statement:

[l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n)] - This is a list comprehension, which is essentially a compact way to write a for loop in Python. It's creating a new list.

l[i * n:(i + 1) * n] - This is a slice of the input list l. If l is [1,2,3,4,5,6,7,8,9] and n is 3, the slices will be [1,2,3], [4,5,6], and [7,8,9].

for i in range((len(l) + n - 1) // n) - This is the looping construct for the list comprehension. It's determining how many chunks the list should be divided into. It calculates the number of chunks by taking the ceiling of the length of the list divided by the chunk size.

We have added another list comprehension within the original one: [item.strip() for item in l[i * n:(i + 1) * n]]. This new list comprehension operates on each chunk (i.e., each sublist) and calls strip() on each item in the chunk. The strip() function removes leading and trailing whitespace, including newline characters, from a string. Therefore, if your list elements are strings with newline characters at the end, this will remove those.
 """


def divide_chunks(l, n):
    return [[item.strip() for item in l[i * n:(i + 1) * n]] for i in range((len(l) + n - 1) // n)]


# open local input file 'with' autoclose and read lines
with open('input') as f:
    contents = f.readlines()

# divide list
chunks = list(divide_chunks(contents, 3))
# print(chunks)

# score chunks
scores = [chunk_score(i)for i in chunks]
# print(scores)

# total score
print(sum(scores))
