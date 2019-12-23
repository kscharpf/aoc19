import sys
import math
import copy
from collections import deque

def sign(x):
    return 1 if x>0 else -1 

def doesNotInterfere(interferer, target):
    debug = False
    #if target[0] == 1 and target[1] == 3:
        #debug = True
    rv = True
    cond = -1
    if interferer[2] == 0 and target[2] == 0 and sign(target[3]) == sign(interferer[3]):
        cond = 1
        rv = False
    elif interferer[3] == 0 and target[3] == 0 and sign(target[2]) == sign(interferer[2]):
        cond = 2
        rv = False
    elif interferer[2] == 0 or target[2] == 0 or interferer[3] == 0 or target[3] == 0:
        rv = True
    elif target[2]/interferer[2] == target[3]/interferer[3] and sign(target[2]) == sign(interferer[2]) and sign(target[3]) == sign(interferer[3]):
        cond = 3
        rv = False

    #if debug:
        #print(f"{interferer} and {target} returning {rv} {cond}")

    return rv

def exploreTargets(sourcePosition, allAsteroids):
    filtered_asteroids = [x for x in allAsteroids if x != sourcePosition]
    asteroid_queue = [(x[0],x[1],x[0] - sourcePosition[0],x[1] - sourcePosition[1]) for x in filtered_asteroids]
    asteroid_queue = sorted(asteroid_queue, key = lambda x: (abs(x[2]),abs(x[3])))

    #print(f"{asteroid_queue}")

    visible_asteroids = []

    while len(asteroid_queue) > 0:
        next_target = asteroid_queue[0]
        visible_asteroids.append((next_target[0],next_target[1]))
        asteroid_queue = [x for x in asteroid_queue[1:] if doesNotInterfere(next_target, x)]
        #print(f"{asteroid_queue}")

    visible_asteroids = sorted(visible_asteroids)

    #print(f"Found {len(visible_asteroids)} {visible_asteroids}")

    return visible_asteroids

def bestStation(asteroidMap):
    bestLocation = None
    targetsAtBestLocation = -1
    bestTargetList = []
    for a in asteroidMap:
        allTargets = exploreTargets(a, copy.deepcopy(asteroidMap))
        if len(allTargets) > targetsAtBestLocation:
            bestLocation = a
            targetsAtBestLocation = len(allTargets)
            bestTargetList = copy.deepcopy(allTargets)
    return bestLocation, targetsAtBestLocation,bestTargetList

# goal is to calculate the minimum angle delta between view lines based upon the grid
# then we can iterate through all possible view lines and pull out the first identified
# asteroid from each location

def mapToAsteroidPositions(inMap):
    positions = []
    for y in range(len(inMap)):
        for x in range(len(inMap[0])):
            if inMap[y][x] == '#':
                positions.append((x,y))

    return positions

def main():
    lines = []
    for line in open(sys.argv[1]).readlines():
        lines.append(line)
    bestLocation, numTargets, bestTargetList = bestStation(mapToAsteroidPositions(lines))
    #exploreTargets((1,2), mapToAsteroidPositions(lines))
    #exploreTargets((1,2),[(1,2),(0,3)])

    print("bestLocation is " + str(bestLocation) + " with " + str(numTargets))
    #print(f"bestLocation {bestLocation} numTargets {numTargets} {bestTargetList}")

if __name__ == "__main__":
    main()
