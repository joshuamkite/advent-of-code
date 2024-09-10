
"""
Opponent:

A=rock
B=paper
C=scissors

So break input into blocks of three rows and
for each block calculate each row according to

You:

X=rock, 1
Y=paper, 2
Z=scissors, 3

plus

Win = 6
Draw = 3
Lose = 0

so

A X = Draw, 3+1=4
A Y = Win, 6+2=8
A Z = Lose, 0+3=3
B X = Lose, 0+1=1
B Y = Draw, 3+2=5
B Z = Win, 6+3=9
C X = Win, 6+1=
C Y = Lose, 0+2=2
C Z = Draw, 3+3=6



 """


def chunk_score(l):
    score = 0
    for entry in l:
        match entry:
            case "A X":
                score += 4
            case "A Y":
                score += 8
            case "A Z":
                score += 3
            case "B X":
                score += 1
            case "B Y":
                score += 5
            case "B Z":
                score += 9
            case "C X":
                score += 7
            case "C Y":
                score += 2
            case "C Z":
                score += 6
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
print(chunks)

# score chunks
scores = [chunk_score(i)for i in chunks]
print(scores)

# total score
print(sum(scores))
