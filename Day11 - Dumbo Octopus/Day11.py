# https://adventofcode.com/2021/day/11

filename = "./Input.txt"
octopi = []

with open(filename) as file:
    for line in file:
        octopi.append(list(map(lambda x: int(x), list(line.strip()))))

def dump(octopi):
    for line in octopi:
        print("".join(map(lambda o: str(o), line)))

# print("========== Before the flash")
# dump(octopi)

flashes = 0
def flash(rowNum, colNum):
    global flashes
    global octopi

    assert(9 < octopi[rowNum][colNum] < 12) # either 10 or 11

    if octopi[rowNum][colNum] == 11:
        return # can't flash twice
    
    flashes += 1
    octopi[rowNum][colNum] += 1

    neighbors = [
        (rowNum, colNum-1), # left
        (rowNum, colNum+1), # right
        (rowNum-1, colNum), # above
        (rowNum+1, colNum), # below
        (rowNum-1, colNum-1), # top-left
        (rowNum-1, colNum+1), # top-right
        (rowNum+1, colNum-1), # bottom-left
        (rowNum+1, colNum+1), # bottom-right
    ]

    for row, col in neighbors:
        if row < 0 or row > len(octopi)-1: # either up or down is invalid
            continue
        if col < 0 or col > len(octopi[row])-1: # either left or right is invalid
            continue
        
        if octopi[row][col] < 10:
            octopi[row][col] += 1

        if octopi[row][col] == 10:
            flash(row, col) # the neighbor is now flashing!

# perform x of these steps
step = 0
while True:
    step+=1 

    # step 1, increase energy levels
    for row in range(0, len(octopi)):
        for col in range(0, len(octopi[row])):
            if octopi[row][col] < 10:
                octopi[row][col] += 1

    # step 2, flash
    for rowNum in range(0, len(octopi)):
        for colNum in range(0, len(octopi[rowNum])):
            if octopi[rowNum][colNum] == 10:
                flash(rowNum, colNum)



    # any that have flashed should be reset to 0
    for row in range(0, len(octopi)):
        for col in range(0, len(octopi[row])):

            assert(octopi[row][col] != 10)
            
            if octopi[row][col] > 10:
                octopi[row][col] = 0

    # are we synced up?
    if not any([octopi[row][col] != 0 for col in range(0, len(octopi[row])) for row in range(0, len(octopi))]):
        print("Synced up at", step)
        break

    # print("========== After step", step, ":")
    # dump(octopi)

print("Flashes:", flashes)