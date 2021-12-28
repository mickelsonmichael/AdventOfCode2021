# https://adventofcode.com/2021/day/6

from Lanternfish import SchoolOfLanternfish, EfficientSchoolOfLanternfish

# print("=============")
# print("   Example   ")
# print("=============")

# example1 = SchoolOfLanternfish("./Day6.Example.txt")
# example1.solve()

# print("=============")
# print("   Part 1    ")
# print("=============")

# part1 = SchoolOfLanternfish("./Day6.Input.txt")
# part1.solve()

# print("=============")
# print("  Example 2  ")
# print("=============")

# example2 = EfficientSchoolOfLanternfish("./Day6.Example.txt")
# example2.solve(numDays=256)

print("=============")
print("    Part 2   ")
print("=============")

part2 = EfficientSchoolOfLanternfish("./Day6.Input.txt")
part2.solve(numDays=256)
