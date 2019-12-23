import sys

class Tree:
    def __init__(self, name):
        self.name = name
        self.leaves = []

def walk_orbit(tree):
    if len(tree.leaves) == 0:
        print(f"{tree.name} has nothing orbiting it - returning 0 ")
    print(f"{tree.name} has orbiters")
    return len(tree.leaves) + sum([walk_orbit(tree.leaves[i]) for i in range(len(tree.leaves))])

def process_map(lines):
    relations = [line.rstrip('\n').split(')') for line in lines]
    orbit_roots = {}
    for r in relations:
        if r[1] not in orbit_roots:
            orbit_roots[r[1]] = Tree(r[1])
        if r[0] in orbit_roots:
            orbit_roots[r[0]].leaves.append(orbit_roots[r[1]])
        else:
            orbit_roots[r[0]] = Tree(r[0])
            orbit_roots[r[0]].leaves.append(orbit_roots[r[1]])
    return sum([walk_orbit(t) for t in orbit_roots.values()])

def main():
    print(f"OUTPUT: {process_map(open(sys.argv[1]).readlines())}")

if __name__ == "__main__":
    main()



