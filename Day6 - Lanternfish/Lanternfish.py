
class Lanternfish:

    def toStr(self):
        return str(self.timeUntilSpawn)

    def age(self):
        newTime = self.timeUntilSpawn - 1

        if newTime < 0:
            self.timeUntilSpawn = 6
            return Lanternfish()
        else:
            self.timeUntilSpawn = newTime

    def __init__(self, timeUntilSpawn: str = "8"):
        self.timeUntilSpawn = int(timeUntilSpawn)

class SchoolOfLanternfish:

    def age(self):
        for i in range(0, len(self.lanternfish)):
            newFish = self.lanternfish[i].age()

            if newFish is not None:
                self.lanternfish.append(newFish)

    def solve(self, numDays: int = 80):
        for i in range(0, numDays):
            print("Day", i)
            self.age()

        print("After " + str(numDays) + " days:", len(self.lanternfish))

    def __init__(self, filename: str):
        with open(filename) as file:
            initialSpawns = file.readline().split(",")

            self.lanternfish = list(map(lambda s : Lanternfish(s), initialSpawns))

class EfficientSchoolOfLanternfish:

    def age(self):
        prev = 0
        for age in range(len(self.ageCounts) - 1, -1, -1):
            temp = self.ageCounts[age]
            
            self.ageCounts[age] = prev

            prev = temp

            if age == 0:
                self.ageCounts[8] += temp
                self.ageCounts[6] += temp

    def solve(self, numDays = int):
        for i in range(0, numDays):
            self.age()

        print("Total lanternfish:", str(sum(self.ageCounts)))

    def __init__(self, filename: str):
        with open(filename) as file:
            line = file.readline()
            ages = list(map(lambda a : int(a), line.split(",")))

            self.n = max(max(ages), 8)
            self.ageCounts = [0] * (self.n + 1)

            for age in ages:
                self.ageCounts[age] += 1
