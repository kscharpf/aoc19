import sys
from collections import deque
from utils import str_to_program
from intcode import eval_program
if __name__ == "__main__":
    inputQ = deque()

    for line in open(sys.argv[1]).readlines():
        v = eval_program(str_to_program(line), 0, inputQ, 0)
