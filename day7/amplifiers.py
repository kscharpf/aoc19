import sys
from intcode import eval_program
from utils import str_to_program
from collections import deque
from itertools import permutations
import copy

def run_amplifiers(phaseSettingList, program):

    print(f"Running amps with phases {phaseSettingList}")
    amp_input = 0
    amp_output = 0
    programs = [copy.deepcopy(program) for amp in range(5)]
    program_indices = [0 for amp in range(5)]
    ampQueues = [deque() for amp in range(5)]
    [ampQueues[amp].append(phaseSettingList[amp]) for amp in range(5)]
    halted = False
    while not halted:
        for amp in range(5):
            print(f"Processing amp {amp} with input {amp_output}")
            ampQueues[amp].append(amp_output)
            program_indices[amp], tmp_amp_output = eval_program(programs[amp], program_indices[amp], ampQueues[amp])
            if program_indices[amp] >= len(program):
                halted = True
                print(f"amp {amp} has halted")
            else:
                amp_output = tmp_amp_output
            #print(f"phase setting {phaseSettingList} produced output {amp_output}")
            print(f"Exiting with amp_output: {amp_output}")
    return amp_output


def optimize_program(program):
    best_amp_output = None
    best_phase_setting = []

    for phaseSettingList in permutations([5,6,7,8,9]):
        amp_output = run_amplifiers(phaseSettingList, program)

        if best_amp_output is None or amp_output > best_amp_output:
            best_amp_output = amp_output
            best_phase_setting = phaseSettingList
    print(f"Amplifier optimization complet with output {best_amp_output} and phase settings {best_phase_setting}")

def main():
    for line in open(sys.argv[1]).readlines():
        program = str_to_program(line)
        optimize_program(program)
        #run_amplifiers([9,8,7,6,5],program)

if __name__ == "__main__":
    main()
