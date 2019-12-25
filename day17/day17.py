from utils import str_to_program
from intcode import Program
import sys
import argparse

def isWall(m, coords):
    x,y = coords
    if (x,y) in m:
        if m[x,y] == 35:
            return True
    return False

def next(coords, xdir, ydir):
    return (coords[0] + xdir, coords[1] + ydir)

def nexty(coords):
    return next(coords, 0, 1)
def prevy(coords):
    return next(coords, 0, -1)
def nextx(coords):
    return next(coords, 1, 0)
def prevx(coords):
    return next(coords, -1, 0)

def wallBothDirectionsY(m, coords):
    if isWall(m, nexty(coords)) and isWall(m, prevy(coords)):
        return True
    if isWall(m, nexty(coords)) and prevy(coords) not in m:
        return True
    if isWall(m, prevy(coords)) and nexty(coords) not in m:
        return True
    return False

def wallBothDirectionsX(m, coords):
    if isWall(m, nextx(coords)) and isWall(m, prevx(coords)):
        return True
    if isWall(m, nextx(coords)) and prevx(coords) not in m:
        return True
    if isWall(m, prevx(coords)) and nextx(coords) not in m:
        return True
    return False



def isIntersection(m, coords):
    return isWall(m, coords) and wallBothDirectionsY(m, coords) and wallBothDirectionsX(m, coords)

robot_main = "A,B,A,A,B,C,B,C,C,B\n"
robot_func_a = "L,12,R,8,L,6,R,8,L,6\n"
robot_func_b = "R,8,L,12,L,12,R,8\n"
robot_func_c = "L,6,R,6,L,12\n"

def driverobot(p):
    for c in robot_main:
        print(f"pushing {ord(c)}")
        p.pushInput(ord(c))
    for c in robot_func_a:
        print(f"pushing {ord(c)}")
        p.pushInput(ord(c))
    for c in robot_func_b:
        print(f"pushing {ord(c)}")
        p.pushInput(ord(c))
    for c in robot_func_c:
        print(f"pushing {ord(c)}")
        p.pushInput(ord(c))
    p.pushInput(ord('n'))
    p.pushInput(ord('\n'))

    output = []
    while not p.isHalted():
        output = p.eval()
    if len(output) > 0:
        print(f"Dust collected: {output}")
    else:
        print(f"No output from program collected")

def buildmap(p):
    m = {}
    ypos = 0
    xpos = 0
    while not p.isHalted():
        output = p.eval()
        for c in output:
            if c == 10:
                xpos = 0
                ypos += 1
            else:
                m[(xpos,ypos)] = c
                xpos += 1

            print(chr(c), end="")

    keys = m.keys()
    xmax = max([x for x,y in keys])
    ymax = max([y for x,y in keys])

    total = 0
    for x in range(0,xmax+1):
        for y in range(0,ymax+1):
            if isIntersection(m, (x,y)):
                print(f"Intersection found at {(x,y)}")
                m[(x,y)] = 79
                total += x*y

    print(f"Total {total}")
    for y in range(0,ymax+1):
        for x in range(0,xmax+1):
            print(chr(m[(x,y)]), end="")
        print()

# L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,12,R,8,L,6,R,8,L,6,L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,6,R,6,L,12,R,8,L,12,L,12,R,8,L,6,R,6,L,12,L,6,R,6,L,12,R,8,L,12,L,12,R,8


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="program source")
    parser.add_argument("--buildmap", 
            help="build out the map",
            action="store_true",
            default=False)
    parser.add_argument
    args = parser.parse_args()

    p = Program(str_to_program(open(sys.argv[1]).read().rstrip('\n')))

    if args.buildmap:
        buildmap(p)
    else:
        driverobot(p)



if __name__ == "__main__":
    main()
