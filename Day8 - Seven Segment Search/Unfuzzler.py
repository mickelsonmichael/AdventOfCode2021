
class Input:
    def __init__(self, line: str):
        self.segment1, self.segment2 = line.split(" | ")
        self.numbers1 = self.segment1.split(" ")
        self.numbers2 = self.segment2.split(" ")

    def dump(self):
        print(self.numbers1, "|", self.numbers2)

class Panel:
    def dump(self):
        print("", self.segments[0] * 3, "")
        print(self.segments[1], " ", self.segments[2])
        print(self.segments[1], " ", self.segments[2])
        print("", self.segments[3] * 3, "")
        print(self.segments[4], " ", self.segments[5])
        print(self.segments[4], " ", self.segments[5])
        print("", self.segments[6] * 3, "")
    
    def solveTop(self):
        assert(self.numbers[1] != "")
        assert(self.numbers[7] != "")

        for c in self.numbers[7]:
            if c not in self.numbers[1]:
                self.segments[0] = c # this is the top pip

    def getThree(self):
        for two_three_five in self.inputs[5]: # three values that could be 2, 3, or 5
            match = True
            for c in self.numbers[1]:
                if c not in two_three_five:
                    match = False
                    break # go to the next option of 2, 3, or 5

            if match:
                self.numbers[3] = two_three_five
                return

    def solveMiddleAndBottom(self):
        assert(self.numbers[1] != "")
        assert(self.numbers[3] != "")
        assert(self.numbers[4] != "")

        pip_3_or_6 = list(filter(lambda p : p not in self.numbers[1] and p != self.segments[0], self.numbers[3]))

        assert(len(pip_3_or_6) == 2) # there should only be two options

        # whichever one isn't in the four is the bottom pip and the other is the middle pip
        self.segments[6], self.segments[3] = [pip_3_or_6[1], pip_3_or_6[0]] if pip_3_or_6[0] in self.numbers[4] else pip_3_or_6

    def solveTopLeft(self):
        assert(self.numbers[3] != "")
        assert(self.numbers[4] != "")

        # the last pip in the four is the second
        for c in self.numbers[4]:
            if c not in self.numbers[3]:
                self.segments[1] = c
                return

    def getSix(self):
        assert(self.numbers[1] != "")

        for zero_six_or_nine in self.inputs[6]:
            # this line creates an array of boolean values indicating whether or not each character of on is inside
            # if any of the characters are 0 (false), then that is the six
            if 0 in [c in zero_six_or_nine for c in self.numbers[1]]:
                self.numbers[6] = zero_six_or_nine
                break

    def solveRight(self):
        assert(self.numbers[1] != "")
        assert(self.numbers[6] != "")

        self.segments[2], self.segments[5] = self.numbers[1] if self.numbers[1][1] in self.numbers[6] else [self.numbers[1][1], self.numbers[1][0]]

    def solveBottomRight(self):
        # finally, find the last pip in the bottom left
        for c in filter(lambda x : x != "-", self.segments):
            self.lettersRemaining.remove(c)

        assert(len(self.lettersRemaining) == 1)

        self.segments[4] = self.lettersRemaining[0]

    def process(self):
        assert(len(self.inputs[2]) == 1) # there should be only one 1
        assert(len(self.inputs[4]) == 1) # there should be only one 4
        assert(len(self.inputs[3]) == 1) # there should be only one 7

        self.numbers[1] = self.inputs[2][0] # 1
        self.numbers[4] = self.inputs[4][0] # 4
        self.numbers[7] = self.inputs[3][0] # 7

        self.solveTop()
        self.getThree() # 3
        self.solveMiddleAndBottom()
        self.solveTopLeft()
        self.getSix() # 6
        self.solveRight()
        self.solveBottomRight()
        
        self.numbers[8] = "".join(self.segments) # 8
        self.numbers[0] = self.numbers[8].replace(self.segments[3], "") # 0
        self.numbers[2] = self.segments[0] + self.segments[2] + self.segments[3] + self.segments[4] + self.segments[6] # 2
        self.numbers[5] = self.segments[0] + self.segments[1] + self.segments[3] + self.segments[5] + self.segments[6] # 5
        self.numbers[9] = self.numbers[8].replace(self.segments[4], "") # 9

    def solve(self):
        assert(any(filter(lambda n : n == "", self.segments)) == False)

    def getCounts(self):
        d = dict(enumerate(self.numbers))
        d = dict(sorted(d.items(), key=lambda x : len(x[1]), reverse=True))

        counts = [0] * 10
        for unknown in self.scrambled:
            for num, numStr in d.items():
                if 0 not in [c in unknown for c in numStr]:
                    # all matches
                    counts[num] += 1
                    break

        return counts

    def getOutput(self):
        d = dict(enumerate(self.numbers))
        d = dict(sorted(d.items(), key=lambda x : len(x[1]), reverse=True))

        output = ""
        for unknown in self.scrambled:
            for num, numStr in d.items():
                if 0 not in [c in unknown for c in numStr]:
                    # all matches
                    output += str(num)
                    break

        return int(output)

    def __init__(self, line: str):
        self.segments = ["-"] * 7
        self.lettersRemaining = ["a", "b", "c", "d", "e", "f", "g"]
        self.inputs = {
                    2: [], # 1
                    3: [], # 7
                    4: [], # 4
                    5: [], # 2, 3, 5
                    6: [], # 0, 6, 9
                    7: [], # 8
                }
        self.numbers = [""] * 10
        self.scrambled = []

        front, back = line.split(" | ")

        for n in front.split(" "):
            self.inputs[len(n)].append(n)

        for n in back.split(" "):
            self.scrambled.append(n)

        self.process()

class Unfuzzler:
    def __init__(self, filename: str):
        self.readings = list()

        with open(filename) as file:
            for line in file:
                self.readings.append(Panel(line))

    def getCounts(self):
        sum = 0
        totals = { "1": 0, "4": 0, "7": 0, "8": 0 }
        for reading in self.readings:
            _, one, _, _, four, _, _, seven, eight, _ = reading.getCounts()
            sum += one + four + seven + eight
            totals["1"] += one
            totals["4"] += four
            totals["7"] += seven
            totals["8"] += eight

        print(totals)
        print("Sum:", sum)

    def getOutput(self):
        sum = 0

        for reading in self.readings:
            sum += reading.getOutput()

        print("Sum:", sum)
