from utils import str_to_program
from intcode import Program
import sys
import argparse
import copy

def check_in_beam(pdata, xpos, ypos):

    p = Program(copy.copy(pdata))
    p.eval()

    assert(p.waitingForInput())
    p.pushInput(xpos)
    p.pushInput(ypos)
    output = p.eval()
    assert(len(output)==1)
    return output[0] == 1

def find_beam_edgex(pdata, ypos, lastxstart, lastdx):
    xpos = lastxstart

    maxx = lastxstart + (lastdx+1)*2
    while not check_in_beam(pdata, xpos, ypos) and xpos < maxx:
        xpos += 1 
    if xpos >= maxx:
        print(f"Unable to find left edge of beam for y={ypos}")
        return -1,-1,-1

    lastdx = xpos - lastxstart
    xstart = xpos

    while check_in_beam(pdata, xpos, ypos):
        xpos += 1

    return xstart, lastdx, xpos

def check_square(pdata, xpos, ypos):
    return check_in_beam(pdata, xpos, ypos) and \
            check_in_beam(pdata, xpos+99, ypos) and \
            check_in_beam(pdata, xpos, ypos+99) and \
            check_in_beam(pdata, xpos + 99, ypos+99)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="program source")
    args = parser.parse_args()

    pdata = str_to_program(open(sys.argv[1]).read().rstrip('\n'))
    count = 0

    consecY = [0]*500

    sleigh_size = 1

    debug = False
    ypos = 30
    xleft = 0
    lastdx = 100
    done = False
    while not done:
        xleft, lastdx, xright = find_beam_edgex(pdata, ypos, xleft, lastdx)
        if xleft == -1:
            print(f"Unable to find beam for ypos {ypos}")
            exit(-1)
        print(f"Beam for y {ypos} from {xleft} to {xright}")
        ypos += 1
        if xright - xleft >= 99:
            xpos = xleft
            while (xpos+99) <= xright:
                if check_square(pdata, xpos, ypos):
                    print(f"Found beam with square 100 at {xpos, ypos}")
                    done = True
                xpos += 1

if __name__ == "__main__":
    main()
