import sys

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

def eval_instruction(prog_data, prog_idx):
    opcode, inp, outp, num_inp, num_outp = get_opcode_and_parameters(prog_data, prog_idx)
    new_prog_idx = -1
    if opcode == 1:
        assert(num_inp == 2)
        assert(num_outp == 1)
        prog_data[outp[0]] = inp[0] + inp[1]
    elif opcode == 2:
        assert(num_inp == 2)
        assert(num_outp == 1)
        prog_data[outp[0]] = inp[0] * inp[1]
    elif opcode == 3:
        print("INPUT: ", end="")
        v = int(input())
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
        print(f"OUTPUT {inp[0]}")
    elif opcode == 99:
        assert(num_inp == 0)
        assert(num_outp == 0)
        return len(prog_data)
    return (prog_idx + 1 + num_inp + num_outp) if new_prog_idx == -1 else new_prog_idx

def eval_program(prog_data):
    prog_idx = 0
    while prog_idx < len(prog_data):
        prog_idx = eval_instruction(prog_data, prog_idx)

def str_to_program(s):
    return [int(x) for x in s.split(',')]

if __name__ == "__main__":
    for line in open(sys.argv[1]).readlines():
        eval_program(str_to_program(line))
