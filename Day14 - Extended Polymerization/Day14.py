# https://adventofcode.com/2021/day/14

from threading import Thread
from math import ceil

template = ""
rules = {}

with open("./Input.txt") as file:

    template = file.readline().strip()

    for line in file.readlines():
        if line.strip() == "":
            continue

        matcher, insert = line.strip().split(" -> ")

        rules[matcher] = insert


assert(template != "")
assert(any(rules))
assert(all([len(x) == 2 for x in rules.keys()]))
assert(all([len(x) == 1 for x in rules.values()]))

pairs = {}
for i,c in enumerate(template):
    if i + 1 == len(template):
        continue

    pairs[c + template[i+1]] = pairs.setdefault(c + template[i+1], 0) + 1

last = template[-1]

steps = 40
for step in range(1, steps+1):
    newPairs = {}
    counts = {}

    for key in pairs:
        a,b = key
        ins = rules[key]
        times = pairs[key]

        newPairs[a+ins] = newPairs.setdefault(a+ins, 0) + times
        newPairs[ins+b] = newPairs.setdefault(ins+b, 0) + times

        counts[a] = counts.setdefault(a, 0) + times
        counts[ins] = counts.setdefault(ins, 0) + times

    counts[last] = counts.setdefault(last, 0) + 1

    pairs = newPairs


min = ""
max = ""

for key in counts:
    if min == "":
        min = key
    if max == "":
        max = key

    if counts[key] < counts[min]:
        min = key

    if counts[key] > counts[max]:
        max = key

print("part 2 solution", (counts[max] - counts[min]))
