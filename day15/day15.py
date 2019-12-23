from intcode import Program
from utils import str_to_program
import sys
import random
from collections import deque

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
DIRECTIONS = [NORTH,SOUTH,WEST,EAST]
DEFAULT_CHOICE = [1,1,1,1]

MOVEMENT = {NORTH:(1,0), SOUTH:(-1,0), WEST:(0,-1), EAST:(0,1)}

MAX_DEPTH = 2
DEPTH_FACTOR = {0:100,1:10, 2:1}

def next_pos(dir, pos):
    return (pos[0] + MOVEMENT[dir][0], pos[1] + MOVEMENT[dir][1])

class Map:
    def __init__(self):
        self.map = {}
        self.xmin = -1
        self.xmax = 1
        self.ymin = -1
        self.ymax = 1
        self.source = (0,0)
        self.target = None

    def size(self):
        return len(self.map.keys())

    def update(self, m):
        self.map.update(m.map)
        if m.target != None:
            self.target = m.target

    def setWall(self, pos):
        self.map[pos] = '#'

    def isWall(self, pos):
        return pos in self.map and self.map[pos] == '#'

    def setEmpty(self, pos):
        self.map[pos] = '.'

    def isEmpty(self, pos):
        return pos in self.map and self.map[pos] == '.'

    def isUnexplored(self, pos):
        return pos not in self.map

    def setTarget(self, pos):
        self.map[pos] = 'O'
        self.target = pos

    def isTarget(self, pos):
        return pos in self.map and self.map[pos] == 'O'

    def isWallOrBorder(self, pos, debug):

        x = pos[1]
        y = pos[0]

        if debug:
            print(f"Checking isWallOrBorder for {pos} and xmin/xmax {self.xmin}/{self.xmax} and ymin/ymax {(self.ymin,self.ymax)}")
        # out of bounds means this is a border
        if x < self.xmin or y < self.ymin or x > self.xmax or y > self.ymax:
            if debug:
                print(f"Returning true - out of bounds")
            return True
        return self.isWall((y,x))

    def surroundedByWalls(self, pos, debug):
        xpos = pos[1]
        ypos = pos[0]

        if debug:
            print(f"Checking if {pos} is completely surrounded")

        return self.isWallOrBorder((ypos+1,xpos), debug) and self.isWallOrBorder((ypos-1,xpos), debug) and \
                self.isWallOrBorder((ypos, xpos+1),debug) and self.isWallOrBorder((ypos, xpos-1), debug)

    def autofill(self):
        keys = self.map.keys()
        ykeys = sorted([x[0] for x in keys])
        xkeys = sorted([x[1] for x in keys])
        print("========================================")
        print(set(xkeys))
        print("========================================")
        print(set(ykeys))
        print("========================================")
        self.ymax = max([y for y in ykeys])
        self.ymin = min([y for y in ykeys])
        self.xmax = max([x for x in xkeys])
        self.xmin = min([x for x in xkeys])

        debug = False
        if self.size() >= 1658:
            debug = True

        if debug:
            print(f"Range {(self.ymin,self.xmin)} to {(self.ymax,self.xmax)}")
        for y in range(self.ymin, self.ymax + 1, 1):
            for x in range(self.xmin,self.xmax+1, 1):
                if x == self.xmax:
                    print(f"Mystery point: {(y,x)}")
                if (y,x) not in self.map:
                    if debug:
                        print(f"Blank spot {(y,x)}")
                    if self.surroundedByWalls((y,x), debug):
                        print(f"{(y,x)} is completely surrounded")
                        # declare it as a wall cuz it might as well be
                        self.setWall((y,x))

    def isComplete(self):
        return len(self.map.keys()) == 1681
    def display(self):
        for y in range(self.ymin, self.ymax, 1):
            for x in range(self.xmin,self.xmax, 1):
                if (y,x) in self.map:
                    if (y,x) == self.source:
                        print("D", end="")
                    else:
                        print(self.map[(y,x)], end="")
                else:
                    print(' ', end="")
            print()


class Explore:
    def __init__(self):
        self.map = Map()
        self.dir = NORTH
        self.pos = (0,0)
        self.map.setEmpty(self.pos)
        self.lastStatus = 1
        self.target = None


    def next_pos(self, dir = None, pos = None):
        if dir == None:
            dir = self.dir
        if pos == None:
            pos = self.pos
        assert(dir >= NORTH and dir <= EAST)
        return next_pos(dir, pos)

    def count_unexplored(self, pos, depth):
        if self.map.isWall(pos):
            return 0
        if depth > MAX_DEPTH:
            return 0

        rv = 0

        if self.map.isUnexplored(pos):
            rv = DEPTH_FACTOR[depth]
        for dir in DIRECTIONS:
            npos = self.next_pos(dir, pos)
            v = self.count_unexplored(npos, depth + 1)
            rv += v

        return rv

    def count_nonwalls(self, pos, depth):
        if depth == MAX_DEPTH:
            return 0

        if self.map.isWall(pos):
            return 0

        rv = DEPTH_FACTOR[depth]
        for dir in DIRECTIONS:
            npos = self.next_pos(dir, pos)
            rv += self.count_nonwalls(npos, depth+1)
        return rv

    def status(self, statusCode):
        statusCode = statusCode[0]
        if statusCode == 0:
            self.map.setWall(self.next_pos())
        elif statusCode == 1:
            self.map.setEmpty(self.next_pos())
            self.pos = self.next_pos()
        elif statusCode == 2:
            self.map.setTarget(self.next_pos())
            self.pos = self.next_pos()
            self.target = self.next_pos()
        else:
            assert(False)
    def explorationSpace(self):
        return len(self.map.map.keys())

    def nextCommand(self):
        territory = [self.count_unexplored(self.next_pos(choice,self.pos), 0) for choice in DIRECTIONS] 
        #print(f"territory: {territory}")
        if all([x == 0 for x in territory]):
            # if everything is explored, look for the fewest walls
            #print("Trying for non-walls")
            territory = [self.count_nonwalls(self.next_pos(choice,self.pos), 0) for choice in DIRECTIONS] 
            assert(not all([x==0 for x in territory]))
        self.dir = random.choices(DIRECTIONS, territory)[0]
        #print(f"pos: {self.pos} dir: {self.dir}")
        return self.dir


def astar_search(m, source, target):
    open_list = [(source[0], source[1], 0, 0)]
    closed_list = []

    while len(open_list) > 0:
        open_list = sorted(open_list, key = lambda x: x[2] + x[3])
        q = open_list[0]
        open_list = open_list[1:]
        for dir in DIRECTIONS:
            npos = next_pos(dir, (q[0],q[1]))
            if m.isTarget(npos):
                return q[3] + 1
            elif m.isEmpty(npos):
                assert(npos != None)
                assert(target != None)
                assert(q != None)
                next_f = abs(target[0] - npos[0]) + abs(target[1] - npos[1]) + q[3] + 1
                dups = [item for item in open_list if item[0] == npos[0] and item[1] == npos[1]]
                if len(dups) > 0:
                    bestcopy = dups[0]
                    fbest = bestcopy[3] + bestcopy[4]
                    if next_f > fbest:
                        continue
                closed_items = [item for item in closed_list if item[0] == npos[0] and item[1] == npos[1]]
                if len(closed_items) > 0:
                    best_copy = closed_items[0]
                    if best_copy[2] + best_copy[3] < next_f:
                        continue
                open_list.append((npos[0],npos[1],abs(target[0]-npos[0]) + abs(target[1] - npos[1]), q[3]+1))
        closed_list.append(q)
    print(f"Exiting astar_search with {open_list} {closed_list} target {target}")
    return -1

def fill_space(m, source):
    minutes = 0
    q = [(source[0], source[1], 0)]
    explored = []
    max_minutes = 0
    while len(q) > 0:
        print(f"len(q): {len(q)}")
        p = q[0]
        q = q[1:]
        print(f"appending {(p[0],p[1])}")
        explored.append((p[0],p[1]))
        max_minutes = max(max_minutes,p[2])
        for dir in DIRECTIONS:
            npos = next_pos(dir, (p[0],p[1]))
            if m.isWall(npos):
                continue
            if (npos[0],npos[1]) in explored:
                continue
            q.append((npos[0],npos[1],p[2]+1))
    return max_minutes

def main():

    globalMap = Map()
    data = str_to_program(open(sys.argv[1]).read().rstrip('\n'))

    explorationNum = 1

    while not globalMap.isComplete():
        print(f"Beginning exploration {explorationNum} with {globalMap.size()}")

        p = Program(data)
        e = Explore()
        found = False
        i = 0
        lastExplored = 0
        while not p.isHalted() and e.explorationSpace() < 1600:
            p.pushInput(e.nextCommand())
            output = p.eval()
            e.status(output)
            found = output[0] == 2
            if i % 10000 == 0:
                print(f"Exploration {explorationNum} Iteration {i} has explored {e.explorationSpace()}")
                if e.explorationSpace() == lastExplored:
                    print(f"Restarting map exploration")
                    break
                lastExplored = e.explorationSpace()
            i += 1
        explorationNum += 1
        globalMap.update(e.map)
        print(f"Executing autofill")
        globalMap.autofill()
        globalMap.display()

    #print(f"yrange: {miny,maxy} and {minx,maxx}")
    moves = astar_search(globalMap,(0,0), globalMap.target)
    print(f"Moves to target from origin: {moves}")

    #e.display()

    print(f"{fill_space(globalMap, globalMap.target)} is the answer")


if __name__ == "__main__":
    main()
