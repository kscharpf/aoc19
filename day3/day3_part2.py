import numpy as np
import sys
def get_pos_delta(move):
    x_delta = 0
    y_delta = 0
    dir = 1
    if move[0] == 'R':
        x_delta = int(move[1:])
    elif move[0] == 'L':
        x_delta = -int(move[1:])
        dir = -1
    elif move[0] == 'U':
        y_delta = int(move[1:])
    else:
        y_delta = -int(move[1:])
        dir = -1
    return x_delta, y_delta, dir

def populate_grid(g, p, orig, idx, other):
    last_pos_x = orig[0] 
    last_pos_y = orig[1] 

    intersections = []

    steps = 0
    for pos in p:
        x_delta, y_delta, dir = get_pos_delta(pos)
        new_pos_x = last_pos_x + x_delta
        new_pos_y = last_pos_y + y_delta

        for i in range(last_pos_x + dir, new_pos_x + dir, dir):
            steps += 1
            if g[last_pos_y, i, idx] == 0 and (last_pos_y != orig[1] or i != orig[0]):
                g[last_pos_y, i, idx] = steps
                if g[last_pos_y, i, other] != 0:
                    intersections.append((last_pos_y, i, steps, g[last_pos_y, i, other]))
        for i in range(last_pos_y + dir, new_pos_y + dir, dir):
            steps += 1
            if g[i, last_pos_x, idx] == 0 and (last_pos_x != orig[0] or i != orig[1]):
                g[i, last_pos_x, idx] = steps
                if g[i, last_pos_x, other] != 0:
                    intersections.append((i, last_pos_x, steps, g[i,last_pos_x, other]))

        last_pos_x = new_pos_x
        last_pos_y = new_pos_y
    return intersections

def get_extrema(p):
    x_pos = 0
    y_pos = 0
    min_x = 0
    min_y = 0
    
    max_x = 0
    max_y = 0
    for pos in p:
        x_delta, y_delta, dir = get_pos_delta(pos)
        print(f"xd/yd {x_delta},{y_delta}")
        x_pos += x_delta
        y_pos += y_delta
        min_x = min(x_pos, min_x)
        max_x = max(x_pos, max_x)
        min_y = min(y_pos, min_y)
        max_y = max(y_pos, max_y)
    print(f"Extrema {min_x},{max_x},{min_y},{max_y}")
    return (min_x, max_x, min_y, max_y)

def create_grid(p1, p2):
    min_x, max_x, min_y, max_y = get_extrema(p1)
    min_x2, max_x2, min_y2, max_y2 = get_extrema(p2)

    min_x = min(min_x, min_x2)
    max_x = max(max_x, max_x2)
    min_y = min(min_y, min_y2)
    max_y = max(max_y, max_y2)

    return np.zeros((max_y - min_y + 1, max_x - min_x + 1, 2), np.int32), -min_x, -min_y


def find_intersection(p1,p2):
    print("Making grid")
    grid, orig_x, orig_y = create_grid(p1, p2)
    print(f"grid shape: {grid.shape}")
    print("Populating grid - wire 1")
    populate_grid(grid, p1, (orig_x,orig_y), 0, 1)
    print("Populating grid - wire 2")
    intersections = populate_grid(grid, p2, (orig_x,orig_y), 1, 0)

    min_steps = None
    best_x = -1 
    best_y = -1
    for pos_y, pos_x, steps1, steps2 in intersections:
        if min_steps is None or (steps1 + steps2) < min_steps:
            min_steps = steps1 + steps2
            best_x = pos_x
            best_y = pos_y
    print(f"{best_y},{best_x},{min_steps}")

if __name__ == "__main__":
    wires = []
    for line in sys.stdin:
        wires.append(line.split(','))
    find_intersection(wires[0], wires[1])
