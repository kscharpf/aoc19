import sys
from collections import deque
from utils import str_to_program
from intcode import Program
if __name__ == "__main__":
    inputQ = deque()

    for line in open(sys.argv[1]).readlines():
        p = Program(str_to_program(line))
        out = p.eval()
        print(f"out: {out}")
        #v = eval_program(str_to_program(line), 0, inputQ, 0)
