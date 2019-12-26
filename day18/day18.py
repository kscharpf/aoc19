import argparse
import string
import copy
from heapq import heappush, heappop
from collections import namedtuple

Edge = namedtuple('Edge', ['source','dest','weight', 'doorsInPath'])
Node = namedtuple('Node', ['x','y','name'])
Door = namedtuple('Door', ['x','y','name'])

def potential_moves(p):
    return [(p[0]+1,p[1]),(p[0],p[1]+1),(p[0]-1,p[1]),(p[0],p[1]-1)]

def is_wall(m,p):
    return m[p] == '#'

def is_door(m,p,doorList):
    return str.isupper(m[p]) and m[p].lower() in doorList

def maze2graph(nodes, maze):
    shortestPaths = []

    for node in nodes:
        debug = False
        if node.name == 'a':
            debug = True
        visited = []
        print(f"Searching from {node}")
        q = [(0, node.y, node.x, [])]
        while len(q) > 0:
            moveCount, posy, posx, doorsInPath = q[0]
            p = (posy,posx)
            q = q[1:]

            if debug:
                print(f"position {p} maze state {maze[p]} moves {moveCount}")

            if str.isupper(maze[p]):
                doorsInPath = copy.copy(doorsInPath)
                doorsInPath.append(maze[p])

            if node.name != maze[p] and str.islower(maze[p]):
                canAdd = True
                for e in shortestPaths:
                    if e.source == node.name and e.dest == maze[p]:
                        canAdd = False

                if canAdd:
                    shortestPaths.append(Edge(node.name,maze[p],moveCount, doorsInPath))
                    shortestPaths.append(Edge(maze[p],node.name,moveCount, doorsInPath))
            for move in potential_moves(p):
                if move in maze:
                    if not is_wall(maze, move) and move not in visited:
                        q.append((moveCount+1, move[0], move[1], doorsInPath))
                        visited.append(p)
    for e in shortestPaths:
        print(f"{e.source} to {e.dest} in {e.weight} with {e.doorsInPath}")
    return shortestPaths

def edgesFromSource(source, edges, keysCollected):
    out = []
    for e in edges:
        if e.source == source:
            canTraverse = True
            for d in e.doorsInPath:
                if d.lower() not in keysCollected:
                    canTraverse = False
                    break
            if canTraverse:
                out.append(e)
    #print(fredgesFromSource {source} returning: ")
    #for e in out:
        #print(f"{e.source} to {e.dest} in {e.weight}")
    return out


def collectkeys(shortestPaths, start, allKeys):
    q = []
    keysCollected = ['@']
    heappush(q, (0, '@', keysCollected))
    pathsExplored = {('@'):0}

    while len(q) > 0:
        moveCount, pos, keysCollected = heappop(q)

        #print(f"Num keys collected {sorted(keysCollected)} {len(keysCollected)} {sorted(allKeys)} {len(allKeys)}")

        if list(sorted(keysCollected)) == allKeys:
            print(f"Path: {keysCollected}")
            return moveCount
        debug = False
        if len(keysCollected) == 16:
            debug = True

        if debug:
            print(f"Visiting node {pos} {keysCollected}")

        #print(f"Visiting node {pos} in {moveCount} moves collected {sorted(keysCollected)} all {allKeys}")


        edges = edgesFromSource(pos, shortestPaths, keysCollected)
        for e in edges:
            if debug:
                print(f"At {pos} checking edge to {e.dest} with weight {e.weight}")
            if e.dest not in keysCollected:
                # have I seen this path before
                newKeysCollected = tuple(list(keysCollected) + [e.dest])
                #if len(keysCollected) == 17:
                    #print(f"****************** Checking full collection **************************")
                pathToAdd = tuple(sorted(list(keysCollected)) + [e.dest])
                shouldAdd = True
                if pathToAdd in pathsExplored:
                    if pathsExplored[pathToAdd] <= moveCount + e.weight:
                        shouldAdd = False
                if shouldAdd:
                    heappush(q, (moveCount + e.weight, e.dest, newKeysCollected))
                    if debug:
                        print(f"Adding path: {newKeysCollected} with val {e.weight+moveCount}")
                    if len(keysCollected) == 17:
                        print(f"****************** Adding full collection **************************")
                        print(f"move count {moveCount} edge weight {e.weight} from {e.source} to {e.dest}")
                    pathsExplored[pathToAdd] = e.weight + moveCount
                else:
                    pass
                    #if debug:
                        #print(f"Not visiting {e.dest} as {newKeysCollected} has already been explored with weight {pathsExplored[tuple(sorted(newKeysCollected))]} vs {e.weight + moveCount}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input map file name")
    args = parser.parse_args()

    ypos = 0
    m = {}
    keys = []
    doors = []
    nodes = []
    for line in open(args.infile,"r").readlines():
        for xpos,c in enumerate(line):
            if c == '@':
                nodes.append(Node(xpos, ypos, '@'))
                start = (ypos,xpos)
                keys.append('@')
            elif str.islower(c):
                nodes.append(Node(xpos, ypos, c))
                keys.append(c)
            elif str.isupper(c):
                doors.append(Door(xpos, ypos, c.lower()))
            m[(ypos,xpos)] = c
        ypos += 1

    edges = maze2graph(nodes, m)

    print(f"Maze solved")

    #print(f"Maze edges: {edges}")
    for edge in edges:
        print(f"{edge.source} to {edge.dest} with weight {edge.weight} and doors {edge.doorsInPath}")
    keys = sorted(keys)

    movesToSolve = collectkeys(edges, start, keys)
    print(f"Collected all keys in {movesToSolve}")

if __name__ == "__main__":
    main()





