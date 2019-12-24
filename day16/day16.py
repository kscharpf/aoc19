import copy
import sys
BASE_PATTERN = [0,1,0,-1]

def get_expanded_pattern(sigidx, siglen):
    out = []
    pattern_pos = 0
    while len(out) < (siglen+1):
        i = 0
        while i < (sigidx+1) and len(out) < (siglen+1):
            out.append(BASE_PATTERN[pattern_pos])
            i += 1
        pattern_pos += 1
        pattern_pos %= len(BASE_PATTERN)

    return out[1:]

def sig2list(s):
    return [int(x) for x in str(s)]

def eval_no_mod(signal, idx):
    pattern = get_expanded_pattern(idx, len(signal))
    s = sum([a*b for a,b in zip(signal, pattern)])
    return s

def eval(signal, idx):
    return abs(eval_no_mod(signal, idx)) % 10

def evalsig(signal):
    return [eval(signal, idx) for idx in range(len(signal))]

def evalphases_new(signal, num, offset):
    outsig = copy.copy(signal)

    for iter in range(num):
        for i in range(len(signal)-2,offset-1,-1):
            outsig[i] = (outsig[i+1] + outsig[i])%10

    print(f"evalphases_new returning {outsig[offset:offset+8]}")
    return outsig[offset:offset+8]

def evalphases(signal, num):

    print(f"=====================================")
    print(signal)
    outsig = copy.copy(signal)
    for i in range(num):
        outsig = evalsig(outsig)
        print(outsig)

    print(f"=====================================")
    return outsig

def repeatsig(sig,num):
    out = []
    for i in range(num):
        out.extend(sig)
    return out

def main():
    #assert(get_expanded_pattern(0, 10) == [1,0,-1,0,1,0,-1,0,1,0])
    #rv = get_expanded_pattern(1, 10)
    #assert(rv == [0,1,1,0,0,-1,-1,0,0,1])
    #rv = get_expanded_pattern(2, 10)
    #assert(rv == [0,0,1,1,1,0,0,0,-1,-1])
    #assert(sig2list("12345678") == [1,2,3,4,5,6,7,8])
    #assert(eval([1,2,3,4,5,6,7,8], 0) == 4)
    #assert(eval([1,2,3,4,5,6,7,8], 1) == 8)
    #assert(eval([1,2,3,4,5,6,7,8], 2) == 2)
    #assert(evalsig([1,2,3,4,5,6,7,8]) == [4,8,2,2,6,1,5,8])
    #assert(evalphases(sig2list("69317163492948606335995924319873"), 100) == [5,2,4,3,2,1,3,3])
    #assert(evalphases(sig2list("19617804207202209144916044189917"), 100) == [7,3,7,4,5,4,1,8])
    #assert(evalphases(sig2list("80871224585914546619083218645595"), 100) == [2,4,1,7,6,1,7,6])
    #print(f"{eval([1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8], 0)}")
    #print(f"{eval([1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8],1)}")
    #print(f"{eval([1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8],2)}")
#
    #assert(repeatsig([1,2,3,4],3) == [1,2,3,4,1,2,3,4,1,2,3,4])
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],3),0)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],3),1)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],1),2)}")
    ###print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],2),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],3),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],4),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],5),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],6),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],7),2)}")
    #print(f"{eval(repeatsig([1,2,3,4,5,6,7,8],8),2)}")

    
    #print(evalphases(sig2list("111122225440"), 100))
    #print(evalphases(sig2list("111122225441"), 100))
    #print(evalphases(sig2list("111122225442"), 100))
    #print(evalphases(sig2list("111122224443"), 100))
    #print(evalphases(sig2list("111122225444"), 100))
    #print(evalphases(sig2list("111122223333"), 100))
    #print(evalphases(sig2list("222233334444"), 100))
    #print(evalphases(sig2list("222233330000"), 100))
    #print(evalphases(sig2list("000055559999"), 100))
    #print(evalphases(sig2list("0000555599990"), 100))
    #print(evalphases(sig2list("00005558999950"), 100))
    #print(evalphases(sig2list("11111111111111"), 10))
    #print(evalphases(sig2list("00000001111111"), 10))
    #print(evalphases(sig2list("00000001111122"), 10))

    #print("================== BEGIN TEST =========================")
    #sig = sig2list("0000001111122")
    #assert(evalphases(sig, 20) == evalphases_new(sig, 20))
    #print(evalphases(sig2list("00000001111122"), 10))
    #for i in range(30):
        #sig = [1,2,3,4,5,6,7,8]
        #print(f"i: {i} {eval_no_mod(repeatsig(sig,i+1),4)} {eval(repeatsig(sig,i+1),4)}")


    d = open(sys.argv[1]).read().rstrip('\n')
    offset = int(d[0:7])
    print(f"{evalphases_new(repeatsig(sig2list(d), 10000), 100, offset)}")


if __name__ == "__main__":
    main()

