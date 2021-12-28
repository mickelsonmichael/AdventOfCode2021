# https://adventofcode.com/2021/day/7

from numpy import median, mean, floor

class Crabs:
    def solve(self):
        fuelUsed = 0

        for i in range(0, len(self.crabs)):
            while self.crabs[i] != self.median:
                fuelUsed += 1
                self.crabs[i] = self.crabs[i] + (1 if self.crabs[i] < self.median else -1)

        print("Fuel used:", fuelUsed)

    def solve2(self):
        fuelUsed = 0

        for i in range(0, len(self.crabs)):
            consumption = 1
            while self.crabs[i] != self.mean:
                fuelUsed += consumption
                consumption += 1
                self.crabs[i] = self.crabs[i] + (1 if self.crabs[i] < self.mean else -1)

        print("Fuel used:", fuelUsed)

    def __init__(self, filename: str):
        with open(filename) as file:
            line = file.readline()
            self.crabs = list(map(lambda x : int(x), line.split(",")))

            self.median = median(self.crabs)
            self.mean = floor(mean(self.crabs))

# print("=============")
# print("   Example   ")
# print("=============")

# example1 = Crabs("./Day7.Example.txt")
# example1.solve()

# print("=============")
# print("   Part 1    ")
# print("=============")

# part1 = Crabs("./Day7.Input.txt")
# part1.solve()

# print("=============")
# print("  Example 2  ")
# print("=============")

# example2 = Crabs("./Day7.Example.txt")
# example2.solve2()

print("=============")
print("   Part 2    ")
print("=============")

part2 = Crabs("./Day7.Input.txt")
part2.solve2()
