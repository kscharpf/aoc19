import numpy as np
import sys

def populate_grid(g, p, val, checkVal):
    orig_x = 0
    orig_y = 0
    last_pos_x = 0
    last_pos_y = 0

    intersections = []
    print(f"orig {orig_x} {orig_y}")
    for pos in p:
        print(f"new move {pos}")
        if pos[0] == 'R':
            new_pos_x = last_pos_x + int(pos[1:])
            print(f"last x {last_pos_x} last y {last_pos_y} new_pos_x {new_pos_x}")
            for i in range(last_pos_x, new_pos_x+1):
                if g[i, last_pos_y] == checkVal and i != orig_x and last_pos_y != orig_y:
                    print(f"1) {i},{last_pos_y}, {orig_x}, {orig_y} {g[i, last_pos_y]}")
                    intersections.append([i, last_pos_y])
                g[i,last_pos_y] = val
            last_pos_x = new_pos_x
        elif pos[0] == 'L':
            new_pos_x = last_pos_x - int(pos[1:])
            for i in range(last_pos_x, new_pos_x-1, -1):
                if g[i, last_pos_y] == checkVal and i != orig_x and last_pos_y != orig_y:
                    print(f"2) {i},{last_pos_y}, {orig_x}, {orig_y} {g[i,last_pos_y]}")
                    intersections.append([i, last_pos_y])
                g[i,last_pos_y] = val
            last_pos_x = new_pos_x
        elif pos[0] == 'U':
            new_pos_y = last_pos_y + int(pos[1:])
            for i in range(last_pos_y, new_pos_y+1, 1):
                if g[last_pos_x, i] == checkVal and i != orig_y and last_pos_x != orig_x:
                    print(f"3) {last_pos_x},{i} {orig_x}, {orig_y}")
                    intersections.append([last_pos_x, i])
                g[last_pos_x,i] = val
            last_pos_y = new_pos_y
        elif pos[0] == 'D':
            new_pos_y = last_pos_y - int(pos[1:])
            for i in range(last_pos_y, new_pos_y-1, -1):
                if g[last_pos_x, i] == checkVal and i != orig_y and last_pos_x != orig_x:
                    print(f"4) {last_pos_x},{i} {orig_x}, {orig_y}")
                    intersections.append([last_pos_x, i])
                g[last_pos_x,i] = val
            last_pos_y = new_pos_y
        else:
            assert(False)
    if len(intersections) == 0: return []

    return min([abs(x[0]) + abs(x[1]) for x in intersections])


def get_extrema(p):
    x_pos = 0
    y_pos = 0
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for pos in p:
        if pos[0] == 'R':
            x_pos += int(pos[1:])
        elif pos[0] == 'L':
            x_pos -= int(pos[1:])
        elif pos[0] == 'U':
            y_pos += int(pos[1:])
        else:
            y_pos -= int(pos[1:])
        min_x = min(x_pos, min_x)
        max_x = max(x_pos, max_x)
        min_y = min(y_pos, min_y)
        max_y = max(y_pos, max_y)
    return (min_x, max_x, min_y, max_y)

def create_grid(p1, p2):
    min_x, max_x, min_y, max_y = get_extrema(p1)
    min_x2, max_x2, min_y2, max_y2 = get_extrema(p2)

    min_x = min(min_x, min_x2)
    max_x = max(max_x, max_x2)
    min_y = min(min_y, min_y2)
    max_y = max(max_y, max_y2)

    return np.zeros((max_x - min_x + 1, max_y - min_y + 1))
        
def find_intersection(p1,p2):
    grid = create_grid(p1, p2)
    print(f"grid.shape: {grid.shape}")
    i1 = populate_grid(grid, p1, 1, -1)
    assert(len(i1) == 0)
    i2 = populate_grid(grid, p2, 2, 1)
    print(f"Intersections: {i2}")

if __name__ == "__main__":
    wires = []
    for line in sys.stdin:
        wires.append(line.split(','))
    find_intersection(wires[0], wires[1])
