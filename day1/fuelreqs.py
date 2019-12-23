import sys

def fuel(mass):
    f = int(mass / 3) - 2
    if f > 0:
        return f + fuel(f)
    else:
        return 0 

if __name__ == "__main__":
    s = 0
    for line in open(sys.argv[1]).readlines():
        s += fuel(int(line))
    print(f"Sum: {s}")
