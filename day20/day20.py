import argparse
import heapq
import string
import random

UP=1
DOWN=2
LEFT=3
RIGHT=4

def translate(pos, d, val):
    return (pos[0] + val*(1 if d == UP or d == DOWN else 0) * (-1 if d == UP else 1),
            pos[1] + val*(1 if d == RIGHT or d == LEFT else 0) * (-1 if d == LEFT else 1))

class Node:
    def __init__(self, label, pos):
        self.label = label 
        self.edges = []
        self.pos = pos
    def addEdge(self, node, weight):
        for n,w in self.edges:
            if node.label == n.label:
                return
        self.edges.append((node, weight))
    def __eq__(self, other):
        return self.label == other.label

    def __repr__(self):
        return f"Node({self.label},{self.pos}) - {[(n.label,w) for n,w in self.edges]}"

def install_portals(maze, portals):
    for p in portals:
        pos = translate(p.pos, p.dir, 2)

def add_node(nodeList, nodePositions, label2nodes, pos, label):
    found = False
    for n in nodeList:
        if n.label == label and n.pos != pos:
            n.label = n.label + '-A'
            newNode = Node(label + '-B', pos)
            nodeList.append(newNode)
            n.addEdge(newNode, 1)
            newNode.addEdge(n, 1)
            nodePositions[pos] = newNode
            label2nodes[label] = newNode
            found = True
    if not found:
        n = Node(label, pos)
        nodeList.append(n)
        nodePositions[pos] = n
        label2nodes[label] = n

def getmoves(pos):
    return [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]

def connect_maze(maze, label2nodes, nodePositions):
    for nodePos,n in nodePositions.items():
        q = [(0,nodePos[0], nodePos[1])]
        visited = [(nodePos[0],nodePos[1])]
        labelsVisited = [n.label]
        while len(q) > 0:
            moves,py,px = q[0]
            p = (py,px)
            q = q[1:]
            if p in nodePositions:
                if nodePositions[p] != n:
                    nodePositions[p].addEdge(n, moves)
                    n.addEdge(nodePositions[p], moves)

            for move in getmoves(p):
                #print(f"testing new pos{move} {move in maze} {maze[move]} {move in visited}")
                if move in maze and maze[move] != '#' and move not in visited:
                    q.append((moves+1, move[0], move[1]))
                    visited.append(move)

def best_route(label2nodes):
    q = []
    startNode = label2nodes['AA']
    heapq.heappush(q, (0, 0, startNode))

    visited = [(0,'AA')]

    while len(q) > 0:
        moveCount, _, node = heapq.heappop(q)

        if node.label == 'ZZ':
            return moveCount

        for dest,weight in node.edges:
            shouldAdd = True
            for m,l in visited:
                if l == dest.label and m < moveCount+weight:
                    shouldAdd = False
            if shouldAdd:
                print(f"heappush {moveCount + weight} {dest}")
                heapq.heappush(q, (moveCount + weight, random.randint(0,100), dest))
                visited.append((moveCount+weight,dest.label))


    assert(False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input maze file")

    args = parser.parse_args()

    mazelines = open(args.infile).readlines()

    maze = {}
    nodePositions = {}
    label2nodes = {}
    ypos = 0
    nodeList = []
    xlen = len(mazelines[0])
    for xpos,c in enumerate(mazelines[0].rstrip('\n')):
        if c != ' ' and c != '\n':
            portalPos = (2,xpos)
            label = ''.join([c]+[mazelines[1][xpos]])
            add_node(nodeList, nodePositions, label2nodes, portalPos, label)
    #print(f"line {mazelines[len(mazelines)-1]}")
    for xpos,c in enumerate(mazelines[len(mazelines)-1].rstrip('\n')):
        if c != ' ' and c != '\n':
            lastLine = mazelines[len(mazelines)-1]
            secondLine = mazelines[len(mazelines)-2]
            portalPos = (len(mazelines)-3,xpos)
            label = ''.join([secondLine[xpos]] + [c])
            #print(f"Found label at {len(mazelines)-1,xpos} {label}")
            add_node(nodeList, nodePositions, label2nodes, portalPos, label)
    for ypos,line in enumerate(mazelines):
        line = line.rstrip('\n')
        xlen = len(line)
        if line[0] != ' ':
            assert(line[1] != ' ')
            portalPos = (ypos,2)
            label = ''.join([line[0]]+[line[1]])
            #print(f"Found label at {ypos,2} {label}")
            add_node(nodeList, nodePositions, label2nodes, portalPos, label)
        if line[xlen-1] != ' ':
            assert(line[xlen-2] != ' ')
            portalPos = (ypos,xlen-3)
            label = ''.join([line[xlen-2]]+[line[xlen-1]])
            add_node(nodeList, nodePositions, label2nodes, portalPos, label)

    for rawypos,line in enumerate(mazelines[2:len(mazelines)-2]):
        line = line.rstrip('\n')
        for rawxpos,c in enumerate(line[2:len(line)-2]):
            ypos = rawypos+2
            xpos = rawxpos+2
            shouldAdd = False
            if c != ' ':
                if c in string.ascii_uppercase and line[xpos+1] in string.ascii_uppercase:
                    if line[xpos+2] == ' ':
                        portalPos = (ypos,xpos-1)
                    elif line[xpos-1] == ' ':
                        portalPos = (ypos,xpos+2)
                    else:
                        assert(False)
                    shouldAdd = True
                    label = ''.join([line[xpos]]+[line[xpos+1]])
                    add_node(nodeList, nodePositions, label2nodes, portalPos, label)
                elif mazelines[ypos][xpos] in string.ascii_uppercase and mazelines[ypos+1][xpos] in string.ascii_uppercase:
                    if mazelines[ypos-1][xpos] == ' ':
                        portalPos = (ypos+2,xpos)
                    elif mazelines[ypos+2][xpos] == ' ':
                        portalPos = (ypos-1,xpos)
                    else:
                        assert(False)
                    shouldAdd = True
                    label = ''.join([mazelines[ypos][xpos]]+[mazelines[ypos+1][xpos]])
                    add_node(nodeList, nodePositions, label2nodes, portalPos, label)
                else:
                    maze[(ypos,xpos)] = c
    connect_maze(maze, label2nodes, nodePositions)

    rlen = best_route(label2nodes)

    print(f"Best route from AA to ZZ uses {rlen} moves")

if __name__ == "__main__":
    main()


