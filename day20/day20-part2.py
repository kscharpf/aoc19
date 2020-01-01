import argparse
import heapq
import string
import random
from collections import namedtuple

UP=1
DOWN=2
LEFT=3
RIGHT=4

def translate(pos, d, val):
    return (pos[0] + val*(1 if d == UP or d == DOWN else 0) * (-1 if d == UP else 1),
            pos[1] + val*(1 if d == RIGHT or d == LEFT else 0) * (-1 if d == LEFT else 1))

Edge = namedtuple('Edge',['dest','weight','depthChange'])
GraphPoint = namedtuple('GraphPoint',['minDist','moves','estRemaining','depth','node', 'path'])

class Node:
    def __init__(self, label, pos, isInsideNode = False):
        self.label = label 
        self.edges = []
        self.pos = pos
        self.isInsideNode = isInsideNode
    def addEdge(self, node, weight, depthChange):
        for e in self.edges:
            if e.dest.label == node.label:
                return
        self.edges.append(Edge(node,weight,depthChange))
    def __eq__(self, other):
        return self.label == other.label

    def __repr__(self):
        #return f"Node({self.label},{self.pos}) - {[(e.dest.label, e.weight, e.depthChange) for e in self.edges]}"
        return "Node({},{} - {}".format(self.label,self.pos,[(e.dest.label, e.weight, e.depthChange) for e in self.edges])

def install_portals(maze, portals):
    for p in portals:
        pos = translate(p.pos, p.dir, 2)

def add_node(nodeList, nodePositions, label2nodes, pos, label, isInsideNode = False):
    if label != 'AA' and label != 'ZZ':
        if isInsideNode:
            label = label + '-A'
        else:
            label = label + '-B'
    newNode = Node(label, pos, isInsideNode)
    nodeList.append(newNode)
    nodePositions[pos] = newNode
    label2nodes[label] = newNode
    for n in nodeList:
        if n.label[:2] == label[:2] and n.pos != pos:
            if n.isInsideNode:
                n.addEdge(newNode, 1, 1)
                newNode.addEdge(n, 1, -1)
            else:
                n.addEdge(newNode, 1, -1)
                newNode.addEdge(n, 1, 1)

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
                    nodePositions[p].addEdge(n, moves, 0)
                    n.addEdge(nodePositions[p], moves, 0)

            for move in getmoves(p):
                #print(f"testing new pos{move} {move in maze} {maze[move]} {move in visited}")
                if move in maze and maze[move] != '#' and move not in visited:
                    q.append((moves+1, move[0], move[1]))
                    visited.append(move)

# A* search
def best_route(label2nodes):
    startNode = label2nodes['AA']
    openList = [GraphPoint(1,0,1,0,startNode, ['AA:0'])]
    closedList = []

    while len(openList) > 0:
        openList = sorted(openList, key=lambda x: x[0])
        n  = openList[0]
        openList = openList[1:]

        #print(f"Visiting {n.node.label} @depth {n.depth} - path {n.path} - moves {n.moves}")
        #print(f"Visiting {n.node.label} @depth {n.depth}")

        for e in n.node.edges:
            #print(f"Checking edge from {n.node.label} to {e.dest.label} - moves this edge {e.weight} and total {n.moves}")
            if e.dest.label == 'ZZ' and (n.depth + e.depthChange) == 0:
                print("Solved in {} with path {} -> ZZ".format(n.moves + e.weight, n.path))
                return n.moves + e.weight

            if (e.dest.label == 'ZZ' or e.dest.label == 'AA') and n.depth != 0:
                continue

            if n.depth == 0 and e.depthChange < 0:
                continue

            #if n.depth > 50:
                #continue

            g = n.moves + e.weight
            estRemaining = 2 + abs(n.depth)
            minDist = g + estRemaining
            skip = False
            debug = False
            for node in openList:
                if node.node.label == e.dest.label and node.depth == (n.depth + e.depthChange) and node.minDist < minDist:
                    #print(f"Skipping item on open list")
                    skip = True
            if not skip:
                for node in closedList:
                    if node[0] == e.dest.label and node[1] == (n.depth + e.depthChange) and node[2] < minDist:
                        skip = True
            #if skip:
                #print(f"Skipping transition from {n.node.label} to {e.dest.label}")
            if not skip:
                openList.append(GraphPoint(minDist,g,estRemaining,n.depth + e.depthChange, e.dest, n.path + [e.dest.label + ':' + str(n.depth + e.depthChange) + '(' + str(n.moves + e.weight) + ')']))
                #if e.depthChange != 0:
                    #print(f"Changing depth in visit to {e.dest.label} from {n.node.label} current depth {n.depth} new depth {n.depth + e.depthChange}")
        #print(f"Closing node {n.node.label} at depth {n.depth} and minDist {n.minDist}")
        #print(f"Closing path to {n.node.label} at depth {n.depth} with cost {n.minDist} {n.moves} - {len(closedList)}")
        closedList.append((n.node.label, n.depth, n.minDist))



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
            add_node(nodeList, nodePositions, label2nodes, portalPos, label, False)
    #print(f"line {mazelines[len(mazelines)-1]}")
    for xpos,c in enumerate(mazelines[len(mazelines)-1].rstrip('\n')):
        if c != ' ' and c != '\n':
            lastLine = mazelines[len(mazelines)-1]
            secondLine = mazelines[len(mazelines)-2]
            portalPos = (len(mazelines)-3,xpos)
            label = ''.join([secondLine[xpos]] + [c])
            #print(f"Found label at {len(mazelines)-1,xpos} {label}")
            add_node(nodeList, nodePositions, label2nodes, portalPos, label, False)
    for ypos,line in enumerate(mazelines):
        line = line.rstrip('\n')
        xlen = len(line)
        if line[0] != ' ':
            assert(line[1] != ' ')
            portalPos = (ypos,2)
            label = ''.join([line[0]]+[line[1]])
            #print(f"Found label at {ypos,2} {label}")
            add_node(nodeList, nodePositions, label2nodes, portalPos, label, False)
        if line[xlen-1] != ' ':
            assert(line[xlen-2] != ' ')
            portalPos = (ypos,xlen-3)
            label = ''.join([line[xlen-2]]+[line[xlen-1]])
            add_node(nodeList, nodePositions, label2nodes, portalPos, label, False)

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
                    add_node(nodeList, nodePositions, label2nodes, portalPos, label, True)
                elif mazelines[ypos][xpos] in string.ascii_uppercase and mazelines[ypos+1][xpos] in string.ascii_uppercase:
                    if mazelines[ypos-1][xpos] == ' ':
                        portalPos = (ypos+2,xpos)
                    elif mazelines[ypos+2][xpos] == ' ':
                        portalPos = (ypos-1,xpos)
                    else:
                        assert(False)
                    shouldAdd = True
                    label = ''.join([mazelines[ypos][xpos]]+[mazelines[ypos+1][xpos]])
                    add_node(nodeList, nodePositions, label2nodes, portalPos, label, True)
                else:
                    maze[(ypos,xpos)] = c
    connect_maze(maze, label2nodes, nodePositions)
    print("label2nodes {}".format(label2nodes))

    rlen = best_route(label2nodes)

    print("Best route from AA to ZZ uses {} moves".format(rlen))

if __name__ == "__main__":
    main()


