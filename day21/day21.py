from utils import str_to_program
from intcode import Program
import sys
import argparse
import copy
import random

#pos (x2)
#A +
#B +
#C -
#D +
#E -
#F + 
#G -
#H - 
#I - 
AND_C_T = 'AND C T\n'
AND_D_J = 'AND D J\n'
AND_D_T = 'AND D T\n'
AND_E_T = 'AND E T\n'
AND_H_J = 'AND H J\n'
AND_H_T = 'AND H T\n'
AND_I_J = 'AND I J\n'
AND_T_J = 'AND T J\n'
OR_C_J = 'OR C J\n'
OR_D_J = 'OR D J\n'
OR_D_T = 'OR D T\n'
OR_H_J = 'OR H J\n'
OR_H_T = 'OR H T\n'
OR_A_J = 'OR A J\n'
OR_T_J = 'OR T J\n'
NOT_A_J = 'NOT A J\n'
NOT_A_T = 'NOT A T\n'
NOT_B_T = 'NOT B T\n'
NOT_C_T = 'NOT C T\n'
NOT_C_J = 'NOT C J\n'
NOT_D_J = 'NOT D J\n'
NOT_E_J = 'NOT E J\n'
NOT_E_T = 'NOT E T\n'

WALK_PROGRAM = [NOT_A_T,OR_T_J,NOT_C_T,AND_D_T,OR_T_J, 'WALK\n']
#RUN_PROGRAM = [NOT_A_J,AND_D_J, NOT_A_T, AND_H_T, AND_T_J, 'RUN\n']
#RUN_PROGRAM = [NOT_A_J,NOT_E_T,AND_H_T,AND_D_T,OR_T_J,'RUN\n']
RUN_PROGRAM = [NOT_A_J,NOT_C_T,AND_D_T,AND_H_T,OR_T_J,NOT_B_T,AND_D_T,AND_H_T,OR_T_J,'RUN\n']

def main():
    i = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('infile',help='input file',type=str)
    parser.add_argument('--run', help='run instead of walk', action='store_true')
    args = parser.parse_args()

    pdata = str_to_program(open(args.infile).read().rstrip('\n'))
    solved = False
    plen = 1
    while not solved:
        if i % 100 == 0:
            print("Program {}".format(i))
        p = Program(pdata)
        output = p.eval()
        if p.waitingForInput():
            instructions = RUN_PROGRAM if args.run else WALK_PROGRAM
        
            for ins in instructions:
                [p.pushInput(ord(c)) for c in ins]

            output = p.eval()
            if output[-1] > 255:
                print(f"Solved: {int(output[-1])}")
            else:
                for c in output:
                    print(chr(c), end='')
            #solved = output[0] != ord('.') and output[0] != ord('#') and output[0] != ord('@') and output[0] != ord('\n')
            #if solved:
                #print("Program {} solved with {}".format(i, instructions))
                #print(output)
            solved = True
        i += 1

if __name__ == "__main__":
    #s = ['{:2x}'.format(ord(c)) for c in 'NOT A J']
    #print(int(''.join(s), 16))
    #print(s)
    main()
