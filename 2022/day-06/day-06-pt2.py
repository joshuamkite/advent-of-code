""" find 4 characters that are all different

identify the first position where the four most recently received characters were all different. Specifically, it needs to report the number of characters from the beginning of the buffer to the end of the first such four-character marker.

1234567890
mjqjpqmgbljsphdztnvjfqwrcgsmlb = 7

bvwbjplbgvbhsrlpgdmjqwftvncz: character 5
nppdvjthqldpwncqszvftbrmjlhg: character 6 - seems to be an error
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: character 11




# read input and find first position of first character that isn a sequence of 4 unique characters

# based on https://galaxyinferno.com/how-to-solve-advent-of-code-2022-day-6-with-python/

 """

with open('input.txt', 'r') as f:
    signal = f.readline().strip()

for i in range(len(signal)):
    if len(set(signal[i:i+14])) == 14:
        print(i+14)
        break
