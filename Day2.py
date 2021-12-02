# https://adventofcode.com/2021/day/2

##########################
#        Part 1          #
##########################

position=0
depth=0

with open("./Day2Input.txt") as directions:
    for direction in directions:
        commands = direction.split(" ")

        dir = commands[0]
        x = int(commands[1])

        if dir == "forward":
            position += x
        elif dir == "up":
            depth -= x
        elif dir == "down":
            depth += x

print("depth: ", str(depth))
print("position: ", str(position))
print("answer: ", str(depth * position))

##########################
#        Part 2          #
##########################

print("==============")

aim = 0
depth = 0
position = 0

with open("./Day2Input.txt") as directions:
    for direction in directions:
        commands = direction.split(" ")

        dir = commands[0]
        x = int(commands[1])

        if dir == "forward":
            position += x
            depth += aim * x
        elif dir == "up":
            aim -= x
        elif dir == "down":
            aim += x

print("depth: ", str(depth))
print("position: ", str(position))
print("aim: ", str(aim))
print("answer: ", str(depth * position))
