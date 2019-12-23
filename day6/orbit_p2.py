import sys
from collections import deque
from collections import defaultdict

class Tree:
    def __init__(self):
        self.leaves = []
        

def bfs(nodes, source, target):
    q = deque()
    q.append((source, 0))
    visited = defaultdict(bool)
    visited[source] = True

    while len(q) > 0:
        node_name, depth = q.popleft()
        print(f"Visiting {node_name} with {depth} transfers")

        if node_name == target:
            return depth

        for leaf in nodes[node_name].leaves:
            if not visited[leaf]:
                visited[leaf] = True
                q.append((leaf, depth + 1))
    print(f"bfs() failed to find path between {source} and {target}")
    return -1

def process_map(lines):
    relations = [line.rstrip('\n').split(')') for line in lines]
    orbit_roots = {}
    for r in relations:
        if r[1] not in orbit_roots:
            orbit_roots[r[1]] = Tree()
        if r[0] not in orbit_roots:
            orbit_roots[r[0]] = Tree()
        orbit_roots[r[0]].leaves.append(r[1])
        orbit_roots[r[1]].leaves.append(r[0])
    return orbit_roots

def main():
    nodes = process_map(open(sys.argv[1]).readlines())
    print(f"OUTPUT: {bfs(nodes, 'YOU', 'SAN') - 2} transfers to get to Santa")

if __name__ == "__main__":
    main()



