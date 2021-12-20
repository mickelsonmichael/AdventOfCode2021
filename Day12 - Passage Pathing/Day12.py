# https://adventofcode.com/2021/day/12

from typing import DefaultDict


connections = DefaultDict(set) # dictionary containing the nodes and their connected nodes, with an empty list as the default value

with open("./SmallExample.txt") as file:
    for line in file:
        fr, to = line.strip().split("-")

        connections[fr].add(to) # add the connection
        connections[to].add(fr) # connections go both ways

def visit(node, visited):
    global connections
    global pathsToEnd

    # print(node, list(filter(lambda n : n == "end" or n.isupper() or (n.islower() and n not in visited), connections[node])))
    for n in filter(lambda n : n == "end" or n.isupper() or (n.islower() and n not in visited), connections[node]):
        if n == "end":
            pathsToEnd.append(visited + [n]) # this is a full path
        else:
            visit(n, visited=visited+[n]) # there may be more to visit

node = "start" # start at the root node
pathsToEnd = []

visit(node, [node])

print(len(pathsToEnd), "paths")
