# https://adventofcode.com/2021/day/3

##########################
#        Part 1          #
##########################

def getCounts(lines):
  lineCount = 0
  counts = []

  for line in lines:
      # initialize counts to size of bin str
      if counts == []:
        counts = [0] * (len(line)) #-1

      lineCount = lineCount + 1

      n = int(line, 2)
      i = len(line) - 1

      while n > 0:
        
        # check if the first bit is 1 or 0
        if n & 1 == 1:
          counts[i] = counts[i] + 1

        # shift down to remove the first bit
        n = n >> 1
        i = i - 1
  return (counts, lineCount)

def getFileCounts(filename):
  with open(filename) as file:
    return getCounts(file)

def getGammaAndEpsilon(counts, lines):
  gamma = []
  epsilon = []
  half = lines // 2

  for i in range(0, len(counts)):

      if counts[i] > half:
          gamma.append("1")
          epsilon.append("0")
      else:
          gamma.append("0")
          epsilon.append("1")

  gamma.reverse()
  epsilon.reverse()

  return (gamma, epsilon)

def printAnswer(gamma, epsilon):

  g = "".join(gamma)
  e = "".join(epsilon)

  print("        ", "bin".ljust(len(g), " "), "  ", "int")
  print("gamma   ", g, "  ", str(int(g, 2)))
  print("epsilon ", e, "  ", str(int(e, 2)))
  print("answer  ", "".ljust(len(g), " "), "  ", str(int(g, 2) * int(e, 2)))

exCounts, exLines = getFileCounts("./Day3_Example.txt")
exGamma, exEpsilon = getGammaAndEpsilon(exCounts, exLines)

print("=============")
print("   Example   ")
print("=============")

printAnswer(exGamma, exEpsilon)

counts, lines = getFileCounts("./Day3_Input.txt")
gamma, epsilon = getGammaAndEpsilon(counts, lines)

print("=============")
print("   Part 1    ")
print("=============")

printAnswer(gamma, epsilon)

##########################
#        Part 2          #
##########################

class RatingsParser:
  def __init__(self, filename):
    self.lines = open(filename).readlines()

    for i in range(0, len(self.lines)):
      self.lines[i] = self.lines[i].rstrip("\n")

    self.bitLen = len(self.lines[0])
    self.o2 = ""
    self.co2 = ""

  def getO2(self):
    if self.o2 != "":
      return self.o2

    o2candidates = self.lines.copy()
    for pos in range(0, self.bitLen):
      counts, lines = getCounts(o2candidates)
      check = "1" if lines - counts[pos] <= counts[pos] else "0"
      temp = []

      for candidate in o2candidates:
        if check == candidate[pos]:
          temp.append(candidate)

      if len(temp) == 1:
        self.o2 = temp[0]
        break

      o2candidates = temp

    return self.o2

  def getCO2(self):
    if self.co2 != "":
      return self.co2

    co2candidates = self.lines.copy()
    for pos in range(0, self.bitLen):
      counts, lines = getCounts(co2candidates)
      check = "0" if lines - counts[pos] <= counts[pos] else "1"
      temp = []

      for candidate in co2candidates:
        if check == candidate[pos]:
          temp.append(candidate)

      if len(temp) == 1:
        self.co2 = temp[0]
        break

      co2candidates = temp

    return self.co2
    
  def getLifeSupportRating(self):
    return int(self.getCO2(), 2) * int(self.getO2(), 2)

  def print(self):
    o2 = self.getO2()
    co2 = self.getCO2()
    lifeSupportRating = self.getLifeSupportRating()

    print("     ", "bin".ljust(len(o2), " "), "  ", "int")
    print("O2   ", o2, "  ", str(int(o2, 2)))
    print("CO2  ", co2, "  ", str(int(co2, 2)))
    print("LSR  ", "".ljust(len(o2), " "), " ", lifeSupportRating)


print("=============")
print("  Example 2  ")
print("=============")

example2 = RatingsParser("./Day3_Example.txt")
example2.print()

print("=============")
print("   Part 2    ")
print("=============")

part2 = RatingsParser("./Day3_Input.txt")
part2.print()
