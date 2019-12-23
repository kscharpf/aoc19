from utils import str_to_program
from intcode import Program
import sys
from collections import deque
from collections import defaultdict
from utils import str_to_program
from PIL import Image
import copy
import numpy as np


UP=0
RIGHT=1
DOWN=2
LEFT=3

BLACK=0
WHITE=1

POS_DELTA = {UP:(1,0), RIGHT:(0,1), DOWN:(-1,0), LEFT:(0,-1)}

if __name__ == "__main__":
    pdata = []
    for line in open(sys.argv[1]).readlines():
        pdata.extend(str_to_program(line))

    p = Program(pdata)
    pos = (0,0)
    positions = [pos]
    position_color_map = defaultdict(int)
    position_color_map[pos] = WHITE
    p.pushInput(position_color_map[pos])
    dir = UP
    while not p.isHalted():
        if p.waitingForInput():
            #print(f"INPUT: {position_color_map[pos]}")
            # v = input()
            p.pushInput(position_color_map[pos])
        color, turn = p.eval()
        dir = (dir + 4 + (1 if turn == 1 else -1)) % 4
        #print(f"Turn {turn}")
        #print(f"New Direction {dir}")
        position_color_map[pos] = color
        new_pos = (pos[0] + POS_DELTA[dir][0], pos[1] + POS_DELTA[dir][1])
        pos = new_pos
        #print(f"New Position {pos}")

        if pos not in positions:
            positions.append(pos)
        #print(f"Num Positions {len(positions)}")
    positions = position_color_map.keys()

    ymin = min([x[0] for x in positions])
    ymax = max([x[0] for x in positions])
    yrange = ymax - ymin + 1
    yoffset = -ymin

    xmin = min([x[1] for x in positions])
    xmax = max([x[1] for x in positions])
    xdrange = xmax - xmin + 1
    xoffset = -xmin

    text_view = np.zeros((xdrange, yrange))
    for i in range(xdrange):
        for j in range(yrange):
            col = position_color_map[(j-yoffset, i-xoffset)] 
            assert(col == 1 or col == 0)
            if col == 0:
                print(".", end="")
            else:
                print("#", end="")
        print()

    exit(1)
    #translated_position_color_map = np.zeros((yrange, xdrange, 3), 'uint8')

    #for

    translated_position_color_map = np.zeros((yrange, xdrange, 3), 'uint8')
    for i in range(yrange):
        for j in range(xdrange):
            col = position_color_map[(i-yoffset,j-xoffset)]
            if col == 1:
                print(f"found white at {i - xoffset}, {j - yoffset}")
                translated_position_color_map[i,j,0] = 0xff
                translated_position_color_map[i,j,1] = 0xff
                translated_position_color_map[i,j,2] = 0xff
    img = Image.fromarray(translated_position_color_map)
    img.save('myimg.jpeg')
