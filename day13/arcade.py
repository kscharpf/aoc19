import sys
from intcode import Program
from utils import str_to_program

def main():
    inp = str_to_program(open(sys.argv[1]).read().rstrip('\n'))
    inp[0] = 2
    p = Program(inp)
    output = []
    joystick_input = None 
    score = 0
    tiles = {}
    while not p.isHalted():
        print("==================================================================================")
        if joystick_input != None:
            p.pushInput(joystick_input)
        output = p.eval()
        blockTileCount = 0
        for i in range(0,len(output),3):
            if output[i] == -1 and output[i+1] == 0:
                score = output[i+2]
            else:
                x,y = output[i],output[i+1]

                if output[i+2] == 2:
                    blockTileCount += 1

                tiles[(x,y)] = output[i+2]
        keys = tiles.keys()
        keys = sorted(keys)
        minX = min([x[0] for x in keys])
        maxX = max([x[0] for x in keys])
        minY = min([x[1] for x in keys])
        maxY = max([x[1] for x in keys])

        paddle_x = -1
        ball_x = -1
        for j in range(minY, maxY, 1):
            for i in range(minX, maxX, 1):
                #print(f"Reading tile {(i,j)}")
                t = tiles[(i,j)]
                if t == 0:
                    print(".",end="")
                elif t == 1:
                    print("|",end="")
                elif t == 2:
                    print("#", end="")
                elif t == 3:
                    print("_", end="")
                    paddle_x = i
                elif t == 4:
                    print("o", end="")
                    ball_x = i
                else:
                    assert(False)
            print()
        assert(paddle_x >= 0)
        assert(ball_x >= 0)
        if paddle_x < ball_x:
            joystick_input = 1
        elif paddle_x > ball_x:
            joystick_input = -1
        else:
            joystick_input = 0
        print(f"Ball at {ball_x} and paddle at {paddle_x} joystick {joystick_input}")
    print(f"Game ended with score {score}")



        #print(f"{blockTileCount} block tiles")






if __name__ == "__main__":
    main()
