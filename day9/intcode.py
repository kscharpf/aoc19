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
    elif op == 9:
        return 1,0
    elif op == 99:
        return 0,0
    else:
        assert(False)

def extend_prog_data(prog_data, idx):
    if idx >= len(prog_data):
        delta = idx - len(prog_data) + 1
        prog_data.extend([0]*delta)

def get_parameter_values(in_parameters, parameter_modes, prog_data, relative_base):
    vals = []
    for i in range(len(in_parameters)):
        if parameter_modes[i] == 0:
            vals.append(prog_data[in_parameters[i]])
        elif parameter_modes[i] == 1:
            vals.append(in_parameters[i])
        elif parameter_modes[i] == 2:
            idx = relative_base + in_parameters[i]
            #print(f"Mode 2 relative base {relative_base} inp {in_parameters[i]} idx {idx} {prog_data[idx]}")
            vals.append(prog_data[idx])
        else:
            assert(False)
    return vals

def get_opcode_and_modes(v):
    return v % 100, [(v // 100)%10, (v // 1000) % 10, (v // 10000) % 10]

def get_opcode_and_parameters(prog_data, prog_idx, relative_base):
    opcode, modes = get_opcode_and_modes(prog_data[prog_idx])
    num_in_params, num_out_params = get_num_params(opcode)
    in_parameters = []
    out_parameters = []
    if num_in_params > 0:
        in_parameters = get_parameter_values(
                prog_data[prog_idx+1:prog_idx+1+num_in_params], 
                modes,
                prog_data,
                relative_base)
    outrelbase = 0
    if num_out_params > 0:
        if modes[num_in_params] == 2:
            outrelbase = relative_base
        #for i in range(num_out_params):
            #relbase = relative_base if modes[i] == 2 else 0
            #out_parameters.append(prog_data[relbase + prog_idx + num_in_params + 1])
        out_parameters.append(prog_data[prog_idx + num_in_params + 1])
    print(f"Idx {prog_idx} opcode {opcode} modes {modes} inp {in_parameters} outp {out_parameters} {prog_data[prog_idx+1:prog_idx+1+num_in_params]}")
    return opcode, in_parameters, out_parameters, num_in_params, num_out_params, outrelbase

def eval_instruction(prog_data, prog_idx, inputQ, outputQ, relative_base):
    opcode, inp, outp, num_inp, num_outp, outp_relbase = get_opcode_and_parameters(prog_data, prog_idx, relative_base)
    new_prog_idx = -1
    if opcode == 1:
        assert(num_inp == 2)
        assert(num_outp == 1)
        prog_data[outp_relbase + outp[0]] = inp[0] + inp[1]
    elif opcode == 2:
        assert(num_inp == 2)
        assert(num_outp == 1)
        prog_data[outp_relbase + outp[0]] = inp[0] * inp[1]
    elif opcode == 3:
        if len(inputQ) == 0:
            # ask the user
            print("INPUT: ", end="")
            v = int(input())
        else:
            print("Reading from inputQ")
            v = inputQ.popleft()
        prog_data[outp_relbase + outp[0]] = v
    elif opcode == 5:
        if inp[0] != 0:
            new_prog_idx = inp[1]
    elif opcode == 6:
        if inp[0] == 0:
            new_prog_idx = inp[1]
    elif opcode == 7:
        prog_data[outp_relbase + outp[0]] = 1 if inp[0] < inp[1] else 0
    elif opcode == 8:
        prog_data[outp_relbase + outp[0]] = 1 if inp[0] == inp[1] else 0
    elif opcode == 9:
        relative_base += inp[0]
        extend_prog_data(prog_data, len(prog_data) + relative_base*2)
        print(f"New relative base {relative_base}")
    elif opcode == 4:
        print(f"Appending to outputQ {prog_idx}")
        outputQ.append(inp[0])
    elif opcode == 99:
        assert(num_inp == 0)
        assert(num_outp == 0)
        print("HALT")
        return len(prog_data),-1
    return ((prog_idx + 1 + num_inp + num_outp), relative_base) if new_prog_idx == -1 else (new_prog_idx, relative_base)

def eval_program(prog_data, prog_idx, inputQ, relative_base):
    outputQ = deque()
    extend_prog_data(prog_data, len(prog_data)*5)
    while prog_idx < len(prog_data):
        prog_idx, relative_base = eval_instruction(prog_data, prog_idx, inputQ, outputQ, relative_base)
        #print(f"{prog_idx} / {len(outputQ)}")
        assert(prog_idx >= 0)
    print(",".join([f"{x}" for x in outputQ]))
    return prog_idx, outputQ.popleft() if len(outputQ) > 0 else -1

if __name__ == "__main__":
    inputQ = deque()

    for line in open(sys.argv[1]).readlines():
        v = eval_program(str_to_program(line), 0, inputQ, 0)
        #print(f"OUTPUT {v}")
