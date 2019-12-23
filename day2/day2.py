import copy
def eval_program(prog_data):
    for i in range(0, len(prog_data), 4):
        if prog_data[i] == 99:
            break
        else:
            pos1 = prog_data[i+1]
            pos2 = prog_data[i+2]
            pos3 = prog_data[i+3]
            if prog_data[i] == 1:
                prog_data[pos3] = prog_data[pos1] + prog_data[pos2]
            elif prog_data[i] == 2:
                prog_data[pos3] = prog_data[pos1] * prog_data[pos2]
    return prog_data[0]

def process_program(s):
    prog_data = [int(x) for x in s.split(',')]

    found = False

    for j in range(len(prog_data)):
        for k in range(len(prog_data)):
            if j != k:
                p_copy = copy.deepcopy(prog_data)
                p_copy[1] = j
                p_copy[2] = k
                if eval_program(p_copy) == 19690720:
                    print(f"j {j} k {k}")
                    found = True
    if not found:
        print("Failed to find solution")


if __name__ == "__main__":
    s = input()
    process_program(s)
