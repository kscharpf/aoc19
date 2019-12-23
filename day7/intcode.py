import sys
from collections import deque
from utils import str_to_program

def get_opcode(v):
    return v % 100

def get_num_params(operator):
    op = get_opcode(operator)
    if op == 1 or op == 2:
        return 2,1
    elif op == 3:
        return 0,1
    elif op == 4:
        return 1,0
    elif op == 5:
        return 2,0
    elif op == 6:
        return 2,0
    elif op == 7:
        return 2,1
    elif op == 8:
        return 2,1
    elif op == 99:
        return 0,0
    else:
        assert(False)

def get_parameter_values(in_parameters, parameter_modes, prog_data):
    vals = []
    for i in range(len(in_parameters)):
        if parameter_modes[i] == 0:
            vals.append(prog_data[in_parameters[i]])
        elif parameter_modes[i] == 1:
            vals.append(in_parameters[i])
    return vals

def get_opcode_and_modes(v):
    return v % 100, [(v // 100)%10, (v // 1000) % 10, (v // 10000) % 10]

def get_opcode_and_parameters(prog_data, prog_idx):
    opcode, modes = get_opcode_and_modes(prog_data[prog_idx])
    num_in_params, num_out_params = get_num_params(opcode)
    in_parameters = []
    out_parameters = []
    if num_in_params > 0:
        in_parameters = get_parameter_values(
                prog_data[prog_idx+1:prog_idx+1+num_in_params], 
                modes,
                prog_data)
    if num_out_params > 0:
        out_parameters.append(prog_data[prog_idx + num_in_params + 1])
    return opcode, in_parameters, out_parameters, num_in_params, num_out_params

def eval_instruction(prog_data, prog_idx, inputQ, outputQ):
    print(f"Idx: {prog_idx} op {prog_data[prog_idx:prog_idx+4]}")
    opcode, inp, outp, num_inp, num_outp = get_opcode_and_parameters(prog_data, prog_idx)
    new_prog_idx = -1
    if opcode == 1:
        assert(num_inp == 2)
        assert(num_outp == 1)
        print(f"ADD: {outp[0]} set to {inp[0]} + {inp[1]} = {inp[0]+inp[1]}")
        prog_data[outp[0]] = inp[0] + inp[1]
    elif opcode == 2:
        assert(num_inp == 2)
        assert(num_outp == 1)
        print(f"MUL: {outp[0]} set to {inp[0]} * {inp[1]} = {inp[0]*inp[1]}")
        prog_data[outp[0]] = inp[0] * inp[1]
    elif opcode == 3:
        if len(inputQ) == 0:
            # ask the user
            print("INPUT: ", end="")
            v = int(input())
        else:
            #print("Reading from inputQ")
            v = inputQ.popleft()
        prog_data[outp[0]] = v
    elif opcode == 5:
        if inp[0] != 0:
            new_prog_idx = inp[1]
    elif opcode == 6:
        if inp[0] == 0:
            new_prog_idx = inp[1]
    elif opcode == 7:
        prog_data[outp[0]] = 1 if inp[0] < inp[1] else 0
    elif opcode == 8:
        prog_data[outp[0]] = 1 if inp[0] == inp[1] else 0
    elif opcode == 4:
        print(f"Writing {inp[0]} to output")
        #print("Appending to outputQ")
        outputQ.append(inp[0])
    elif opcode == 99:
        assert(num_inp == 0)
        assert(num_outp == 0)
        return len(prog_data)
    return (prog_idx + 1 + num_inp + num_outp) if new_prog_idx == -1 else new_prog_idx

def eval_program(prog_data, prog_idx, inputQ):
    outputQ = deque()
    while prog_idx < len(prog_data) and len(outputQ) == 0:
        #print(f"Evaluating {prog_idx} {prog_data[prog_idx:prog_idx+4]}")
        prog_idx = eval_instruction(prog_data, prog_idx, inputQ, outputQ)
    #print(f"eval_program() returning")
    return prog_idx, outputQ.popleft() if len(outputQ) > 0 else -1

if __name__ == "__main__":
    inputQ = deque()

    for line in open(sys.argv[1]).readlines():
        v = eval_program(str_to_program(line), 0, inputQ)
        #print(f"OUTPUT {v}")
