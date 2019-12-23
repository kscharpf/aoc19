import sys
from collections import deque
from collections import defaultdict
from utils import str_to_program
import copy
ADD=1
MUL=2
READ=3
WRITE=4
JUMP_NZERO=5
JUMP_EQZERO=6
SET_LT=7
SET_EQ=8
SET_BASE=9
HALT=99

class Program:
    def __init__(self, prog_data):
        self.prog_idx = 0
        self.prog_data = copy.deepcopy(prog_data)
        self.inputQ = deque()
        self.outputQ = deque()
        self.relative_base = 0
        self.op_map = {ADD:self.add, \
                       MUL:self.mul, \
                       READ:self.read,\
                       WRITE:self.write, \
                       JUMP_NZERO:self.jump_nz, \
                       JUMP_EQZERO:self.jump_eq, \
                       SET_LT:self.set_lt, 
                       SET_EQ:self.set_eq, \
                       SET_BASE:self.set_base}

    def get_opcode(self):
        v = self.prog_data[self.prog_idx]
        return v % 100, [(v // 100)%10, (v // 1000) % 10, (v // 10000) % 10]

    def check_idx(self, idx):
        if idx >= len(self.prog_data):
            self.prog_data.extend([0]*(idx*2))

    def get_idx(self, idx):
        self.check_idx(idx)
        return self.prog_data[idx]

    def add(self, modes):
        out_idx = self.prog_data[self.prog_idx + 3] + (self.relative_base if modes[2] == 2 else 0) 
        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]

        relbase = 0 if modes[0] == 0 else self.relative_base
        #print(f"modes {modes} relbase {relbase} relative_base {self.relative_base} inp1 {inp1}")
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        self.check_idx(out_idx)

        self.prog_data[out_idx] = inp1 + inp2
        #print(f"ADD {out_idx} set to {inp1} + {inp2} = {inp1+inp2}")

        self.prog_idx += 4

    def mul(self, modes):
        out_idx = self.prog_data[self.prog_idx + 3] + (self.relative_base if modes[2] == 2 else 0) 
        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]

        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        self.check_idx(out_idx)
        self.prog_data[out_idx] = inp1 * inp2
        #print(f"MUL {out_idx} set to {inp1*inp2}")
        #print(f"MUL {out_idx} set to {inp1} * {inp2} = {inp1*inp2}")

        self.prog_idx += 4

    def read(self, modes):
        out_idx = self.prog_data[self.prog_idx + 1] + (self.relative_base if modes[0] == 2 else 0) 
        self.check_idx(out_idx)
        self.prog_data[out_idx] = self.inputQ.popleft()
        #print(f"READ {out_idx} len {len(self.inputQ)}")

        self.prog_idx += 2

    def write(self, modes):
        inp1 = self.prog_data[self.prog_idx + 1]
        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        self.outputQ.append(inp1)

        self.prog_idx += 2

    def jump_nz(self, modes):
        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]


        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        if inp1 != 0:
            self.prog_idx = inp2
            #print(f"Non-zero jump to {self.prog_idx}")
        else:
            self.prog_idx += 3
            #print(f"Non-zero jump Ingored")

    def jump_eq(self, modes):
        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]

        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        if inp1 == 0:
            self.prog_idx = inp2
            #print(f"Equals zero jump to {self.prog_idx}")
        else:
            #print(f"Equals zero jump Ingored")
            self.prog_idx += 3

    def set_lt(self, modes):
        out_idx = self.prog_data[self.prog_idx + 3] + (self.relative_base if modes[2] == 2 else 0) 

        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]

        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1) 
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        if inp1 < inp2:
            self.prog_data[out_idx] = 1
            #print(f"Prog LT {out_idx} set to 1")
        else:
            self.prog_data[out_idx] = 0
            #print(f"Prog LT ignored")
            pass

        self.prog_idx += 4

    def set_eq(self, modes):
        out_idx = self.prog_data[self.prog_idx + 3] + (self.relative_base if modes[2] == 2 else 0) 

        inp1 = self.prog_data[self.prog_idx + 1]
        inp2 = self.prog_data[self.prog_idx + 2]

        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)
        relbase = 0 if modes[1] == 0 else self.relative_base
        inp2 = inp2 if modes[1] == 1 else self.get_idx(relbase + inp2)

        if inp1 == inp2:
            #print(f"Prog EQ {out_idx} set to 1")
            self.prog_data[out_idx] = 1
        else:
            self.prog_data[out_idx] = 0
            #print(f"Prog EQ ignored")
            pass

        self.prog_idx += 4

    def set_base(self, modes):
        inp1 = self.prog_data[self.prog_idx + 1]
        relbase = 0 if modes[0] == 0 else self.relative_base
        inp1 = inp1 if modes[0] == 1 else self.get_idx(relbase + inp1)

        self.relative_base += inp1
        self.extend_prog_data()

        self.prog_idx += 2

    def waitingForInput(self):
        op, _ = self.get_opcode()
        if op == READ and len(self.inputQ) == 0:
            #print(f"waitingForInput returning True {self.prog_idx}")
            return True
        #print(f"not waitingForInput")
        return False

    def evalInstruction(self):
        op, modes = self.get_opcode()
        self.op_map[op](modes)

    def pushInput(self, inputVal):
        self.inputQ.append(inputVal)

    def isHalted(self):
        op, _ = self.get_opcode()
        return op == HALT

    def eval(self):
        #print(f"len(self.inputQ): {len(self.inputQ)}")
        #print(f"Idx: {self.prog_idx} op {self.prog_data[self.prog_idx:self.prog_idx+4]}")
        while not self.waitingForInput() and not self.isHalted():
            #print(f"Idx: {self.prog_idx} op {self.prog_data[self.prog_idx:self.prog_idx+4]} {type(self.prog_data[0])}")
            self.evalInstruction()
        #print(f"eval() returning {self.prog_idx} op {self.prog_data[self.prog_idx:self.prog_idx+4]} returns {self.outputQ}")
        rv = list(self.outputQ)
        self.outputQ = deque()
        return rv

    def restart(self):
        self.prog_idx = 0

    def extend_prog_data(self):
        if (self.relative_base*2) >= len(self.prog_data):
            self.prog_data.extend([0] * ((self.relative_base * 2) - len(self.prog_data) + 1))

