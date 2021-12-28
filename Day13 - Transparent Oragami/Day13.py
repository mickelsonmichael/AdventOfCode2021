# https://adventofcode.com/2021/day/13

marked = "█"
unmakred = " "

dots = []
folds = []

with open("./Input.txt") as file:
    instructions = False

    for line in file:
        if line == "\n":
            instructions = True
            continue

        if instructions: # parse the instructions
            axis, line = line.strip().split(" ")[2].split("=")
            folds.append((axis, int(line)))
        else: # parse the dots
            x, y = line.strip().split(",")
            dots.append((int(x), int(y)))

maxX = max(map(lambda p : p[0], dots))
maxY = max(map(lambda p : p[1], dots))
paper = [[unmakred for x in range(0, maxX+1)] for y in range(0, maxY+1)] # initialize the paper of proper size

# func to print paper
def dump(foldX=None, foldY=None):
    global paper
    global maxX
    print("\n ", "=" * (maxX+1), " ", sep="")
    for y,row in enumerate(paper):
        if foldY == y:
            print("|", "="* (maxX + 1), "|", sep="")
        else:
            print("|", end="")
            for x,v in enumerate(row):
                if foldX == x:
                    print("|", end="")
                else:
                    print(v, end="")
            print("|")

    print(" ", "=" * (maxX+1), " \n", sep="")

# mark the paper
for x,y in dots:
    paper[y][x] = marked

for axis,line in folds:
    if axis == "x":
        # dump(foldX=line)
        maxX = line - 1
        for y,row in enumerate(paper):
            for x in range(line+1, len(row)):
                if paper[y][x] == marked:
                    i = x - (2 * (x - line))
                    paper[y][i] = marked # mark the opposite side

            paper[y] = paper[y][:-line-1]


    if axis == "y":
        # dump(foldY=line)
        maxY = line
        for y in range(line, len(paper)):
            for x,sp in enumerate(paper[y]):
                if sp == marked:
                    i = y - (2 * (y - line))
                    paper[i][x] = marked
        
        paper = paper[:line]

numMarked = 0
for row in paper:
    for v in row:
        numMarked += 1 if v == marked else 0

print("Dots visible:", numMarked)

# dump should output four letters
dump()
