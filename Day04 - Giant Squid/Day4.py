# https://adventofcode.com/2021/day/4

from Bingo import Bingo

print("=============")
print("   Example   ")
print("=============")

example = Bingo("./Day4-Example1.txt")
example.play()

print("=============")
print("   Part 1    ")
print("=============")

part1 = Bingo("./Day4-input.txt")
part1.play()

print("=============")
print("   Example 2 ")
print("=============")

example2 = Bingo("./Day4-Example1.txt")
example.takeADive()

print("=============")
print("   Part 2    ")
print("=============")

part1.takeADive()
