import sys
from intcode import Program
from utils import str_to_program
from collections import deque
from itertools import permutations
import copy

def run_amplifiers(phaseSettingList, program):
    programs = [Program(copy.deepcopy(program)) for amp in range(5)]
    print(f"type(phaseSettingList[amp]): {type(phaseSettingList[0])} settings {phaseSettingList}")
    [programs[amp].pushInput(phaseSettingList[amp]) for amp in range(5)]
    halted = False
    amp_output = [0]

    while not halted:
        for amp in range(5):
            print(f"Processing amp {amp} with input {amp_output[0]}")
            p = programs[amp]
            if not p.isHalted():
                p.pushInput(amp_output[0])
                amp_output = p.eval()
                if p.isHalted():
                    print(f"Program {amp} halted out {amp_output}")
                    halted = True
            else:
                print(f"Program {amp} halted")
            print(f"Exiting with amp_output {amp_output}")

    return amp_output[0]


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
