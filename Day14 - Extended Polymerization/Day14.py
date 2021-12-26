# https://adventofcode.com/2021/day/14

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

steps = 40

for step in range(1, steps+1):
    result = ""

    for i,c in enumerate(template):
        result += c

        if i >= len(template) - 1:
            continue

        n = template[i+1] # next char

        rule = rules[c + n] # get matching rule

        if rule is not None:
            result += rule

    template = result
    # print("template after step", step, "is", template)

counts: dict[str, int] = {}
for c in template:
    counts[c] = counts.setdefault(c, 0) + 1

print("len(", len(template), ")")
print(counts)

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

print("min", min, "max", max)

print("part 1 solution", (counts[max] - counts[min]))