
import itertools

class Point:
    def __init__(self, coord: str):
        self.x, self.y = map(lambda x : int(x), coord.split(","))

    def toStr(self):
        return str(self.x) + "," + str(self.y)

class Line:
    def __init__(self, line: str):
        self.pointA, self.pointB = map(lambda coord : Point(coord) ,line.split(" -> "))

        iter1, iter2, iter3, iter4 = itertools.tee((self.pointA, self.pointB), 4)
        self.minX = min(iter1, key = lambda pt : pt.x).x
        self.maxX = max(iter2, key = lambda pt : pt.x).x
        self.minY = min(iter3, key = lambda pt : pt.y).y
        self.maxY = max(iter4, key = lambda pt : pt.y).y

    def toStr(self):
        return self.pointA.toStr() + " -> " + self.pointB.toStr()

    def mark(self, grid, skipDiag = bool):
        if skipDiag is True and self.minX != self.maxX and self.minY != self.maxY:
            # skip printing, it's a diagonal
            return grid
        elif self.minX == self.maxX:
            for y in range(self.minY, self.maxY + 1):
                grid[y][self.minX] += 1
        elif self.minY == self.maxY:
            for x in range(self.minX, self.maxX + 1):
                grid[self.minY][x] += 1
        else:
            xInc = self.pointA.x > self.pointB.x
            yInc = self.pointA.y > self.pointB.y

            nextX = (lambda x : x + 1) if xInc else (lambda x : x - 1)
            nextY = (lambda y : y + 1) if yInc else (lambda y : y - 1)

            x = self.minX if xInc else self.maxX
            y = self.minY if yInc else self.maxY

            while self.minX <= x <= self.maxX and self.minY <= y <= self.maxY:
                grid[y][x] += 1

                x = nextX(x)
                y = nextY(y)
        
        return grid

class Map:
    def initGrid(self):
        iter2, iter4 = itertools.tee(self.lines, 2)
        self.minX = 0
        self.maxX = max(iter2, key = lambda line : line.maxX).maxX
        self.minY = 0
        self.maxY = max(iter4, key = lambda line : line.maxY).maxY
        
        # create empty grid
        self.grid = [([0] * (self.maxX - self.minX + 1)) for i in range((self.maxY - self.minY + 1)) ]

    def mark(self, skipDiag = bool):
        for line in self.lines:
            self.grid = line.mark(self.grid, skipDiag=skipDiag)

    def solve(self):
        print("Solution:", str(sum(map(lambda ln : sum(n > 1 for n in ln), self.grid))))

    def __init__(self, filename: str, skipDiag = bool):
        with open(filename) as lines:
            self.lines: list[Line] = list(map(lambda ln : Line(ln), lines))

            self.initGrid()

            self.mark(skipDiag = skipDiag)

    def print(self):
        for x in range(0, len(self.grid)):
            line = ""
            for y in range(0, len(self.grid[x])):
                line += "." if self.grid[x][y] == 0 else str(self.grid[x][y])
            print(line)
        print('')

