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


def get_tuple(idx, array, newval):
    return tuple([newval if i == idx else array[i] for i in range(len(array))])

def collectkeys(shortestPaths, start, allKeys):
    q = []
    keysCollected = ['@1','@2','@3','@4']
    heappush(q, (0, ('@1','@2','@3','@4'), keysCollected))
    pathsExplored = {('@1','@2','@3','@4'):0}

    while len(q) > 0:
        moveCount, robots, keysCollected = heappop(q)

        #print(f"Num keys collected {sorted(keysCollected)} {len(keysCollected)} {sorted(allKeys)} {len(allKeys)}")

        if list(sorted(keysCollected)) == allKeys:
            print(f"Path: {keysCollected}")
            return moveCount
        debug = True

        if debug:
            print(f"Visiting node {robots} {keysCollected} {allKeys}")

        #print(f"Visiting node {pos} in {moveCount} moves collected {sorted(keysCollected)} all {allKeys}")

        for robotidx,pos in enumerate(robots):
            edges = edgesFromSource(pos, shortestPaths, keysCollected)
            for e in edges:
                if debug:
                    print(f"At {pos} checking edge to {e.dest} with weight {e.weight}")
                if e.dest not in keysCollected:
                    # have I seen this path before
                    newKeysCollected = tuple(list(keysCollected) + [e.dest])
                    #if len(keysCollected) == 17:
                        #print(f"****************** Checking full collection **************************")
                    pathToAdd = tuple(sorted(list(keysCollected)) + [get_tuple(robotidx, robots, e.dest)])
                    shouldAdd = True
                    if pathToAdd in pathsExplored:
                        if pathsExplored[pathToAdd] <= moveCount + e.weight:
                            shouldAdd = False
                    if shouldAdd:
                        heappush(q, (moveCount + e.weight, get_tuple(robotidx, robots, e.dest), newKeysCollected))
                        if debug:
                            print(f"Adding path: {newKeysCollected} with val {e.weight+moveCount}")
                        if len(keysCollected) == 17:
                            print(f"****************** Adding full collection **************************")
                            print(f"move count {moveCount} edge weight {e.weight} from {e.source} to {e.dest}")
                        pathsExplored[pathToAdd] = e.weight + moveCount
    
def read_map(inf):
    ypos = 0
    m = {}
    keys = []
    doors = []
    nodes = []
    starts = []
    for line in open(inf,"r").readlines():
        if ypos == 1:
            print(f"line: {line}")
        for xpos,c in enumerate(line.rstrip('\n')):
            if c == '@':
                starts.append((ypos,xpos))
                startlabel = '@' + str(len(starts))
                keys.append(startlabel)
                nodes.append(Node(xpos, ypos, startlabel))
            elif str.islower(c):
                nodes.append(Node(xpos, ypos, c))
                keys.append(c)
            elif str.isupper(c):
                doors.append(Door(xpos, ypos, c.lower()))
            m[(ypos,xpos)] = c
        ypos += 1

    edges = maze2graph(nodes, m)

    return [starts], edges, doors, keys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input map file name")
    args = parser.parse_args()

    starts, edges, doors, keys =  read_map(args.infile)
    
    keys = sorted(keys)

    movesToSolve = collectkeys(edges, starts, keys)

    print(f"Solved in {movesToSolve}")

if __name__ == "__main__":
    main()





