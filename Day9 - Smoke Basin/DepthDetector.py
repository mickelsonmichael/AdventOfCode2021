
class Point:
    def __init__(self, row, col, depth):
        self.id = str(row) + "," + str(col)
        self.row = row
        self.col = col
        self.depth = depth

    def __repr__(self):
        return "{ row: " + str(self.row) + ", col: " + str(self.col) + ", depth: " + str(self.depth) + " }"

    def hasLeft(self):
        return self.col > 0

    def left(self, grid):
        r = self.row
        c = self.col-1
        return Point(r, c, grid[r][c])
    
    def hasRight(self, grid):
        return self.col < len(grid[self.row]) - 1

    def right(self, grid):
        r = self.row
        c = self.col+1
        return Point(r, c, grid[r][c])

    def hasAbove(self):
        return self.row > 0

    def above(self, grid):
        r = self.row-1
        c = self.col
        return Point(r, c, grid[r][c])

    def hasBelow(self, grid):
        return self.row < len(grid) - 1

    def below(self, grid):
        r = self.row+1
        c = self.col
        return Point(r, c, grid[r][c])


class DepthDetector:
    def __init__(self, filename: str):
        self.grid = list[list[int]]()
        self.columnSize = 0

        with open(filename) as file:
            for line in file:
                stripped = line.strip()
                if stripped == "":
                    continue

                row = [int(c) for c in stripped]

                self.grid.append(row)

    def getRiskLevel(self):
        lowPoints = self.getLowPoints()

        riskLevel = sum([p.depth + 1 for p in lowPoints])

        print("Risk level:", riskLevel)

    def getBasinProduct(self):
        lowPoints = self.getLowPoints()
        basins = []

        for lowPoint in lowPoints:
            basins.append(self.getBasinSize(lowPoint))

        basins.sort(reverse=True) # sort descending

        result = basins[0] * basins[1] * basins[2]

        print("Basin product:", result)

        return result

    def getBasinSize(self, lowPoint: Point):
        searched = []
        toSearch = [lowPoint]

        while any(toSearch):
            point = toSearch.pop()

            if point.id in searched:
                continue

            searched.append(point.id)

            if point.hasLeft() and self.leftIsBasin(point) and point.left(self.grid).id not in searched:
                toSearch.append(point.left(self.grid))

            if point.hasRight(self.grid) and self.rightIsBasin(point) and point.right(self.grid).id not in searched:
                toSearch.append(point.right(self.grid))

            if point.hasAbove() and self.aboveIsBasin(point) and point.above(self.grid).id not in searched:
                toSearch.append(point.above(self.grid))

            if point.hasBelow(self.grid) and self.belowIsBasin(point) and point.below(self.grid).id not in searched:
                toSearch.append(point.below(self.grid))

        return len(searched)

    def getLowPoints(self) -> list[Point]:
        lowPoints = list()

        for rowNum in range(0, len(self.grid)):
            row = self.grid[rowNum]
            for colNum in range(0, len(row)):
                val = row[colNum]
                p = Point(row=rowNum, col=colNum, depth=row[colNum])

                if self.leftIsLower(p):
                    continue
                if self.rightIsLower(p):
                    continue
                if self.aboveIsLower(p):
                    continue
                # below
                if self.belowIsLower(p):
                    continue

                # made it through, it's pretty low
                lowPoints.append(p)

        return lowPoints

    def leftIsLower(self, point: Point):
        return point.col > 0 and self.grid[point.row][point.col - 1] <= point.depth

    def leftIsBasin(self, point: Point):
        return point.col > 0 and point.depth < self.grid[point.row][point.col - 1] and self.grid[point.row][point.col - 1] < 9
    
    def rightIsLower(self, point: Point):
        return point.col < len(self.grid[point.row])-1 and self.grid[point.row][point.col + 1] <= point.depth

    def rightIsBasin(self, point: Point):
        return point.col < len(self.grid[point.row])-1 and point.depth < self.grid[point.row][point.col + 1] and self.grid[point.row][point.col + 1] < 9

    def aboveIsLower(self, point: Point):
        return point.row > 0 and self.grid[point.row-1][point.col] <= point.depth

    def aboveIsBasin(self, point: Point):
        return point.row > 0 and point.depth < self.grid[point.row-1][point.col] and self.grid[point.row-1][point.col] < 9

    def belowIsLower(self, point: Point):
        return point.row < len(self.grid)-1 and self.grid[point.row+1][point.col] <= point.depth

    def belowIsBasin(self, point: Point):
        return point.row < len(self.grid)-1 and point.depth < self.grid[point.row+1][point.col] and self.grid[point.row+1][point.col] < 9
