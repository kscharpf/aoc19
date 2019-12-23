import sys

inp = "238345-746315"
#inp = "100000-240000"

def hasDouble(s):
    pureDouble = False

    i = 0
    charToMatch = 'x' # impossible to match
    consecMatches = 0
    while i < len(s):
        if s[i] == charToMatch:
            consecMatches += 1
        elif consecMatches == 2:
            pureDouble = True
            break
        else:
            charToMatch = s[i]
            consecMatches = 1
        i += 1
    if consecMatches == 2:
        pureDouble = True
    return pureDouble

def isNonDecreasing(s):
    for i in range(1, len(s)):
        if s[i] < s[i-1]:
            return False
    return True

def isInRange(x, v1, v2):
    return x>=v1 and x<=v2

def main():

    v1 = 248345
    v2 = 746315
    mySet = set()
    print(f"hasDouble(112233) {hasDouble('112233')}")
    print(f"hasDouble(123444) {hasDouble('123444')}")
    print(f"hasDouble(111122) {hasDouble('111122')}")
    #print(f"hasAdjacent: {hasAdjacent('122345')}")
    #print(f"nonDecreasing: {isNonDecreasing('111123')}")
    #print(f"nonDecreasing: {isNonDecreasing('135679')}")
    #print(f"{hasAdjacent('111111')}: {isNonDecreasing('111111')}")
    #print(f"{hasAdjacent('223450')}: {isNonDecreasing('223450')}")
    #print(f"{hasAdjacent('123789')}: {isNonDecreasing('123789')}")
    #splits = inp.split("-")
    #v1 = int(splits[0])
    #v2 = int(splits[1])

    print(f"Range {v1} {v2}")

    count = 0
    for testVal in range(v1, v2+1):
        s = str(testVal)
        assert(len(s) == 6)
        assert(isInRange(testVal, v1, v2))
        if hasDouble(s) and isNonDecreasing(s):
            count += 1
            mySet.add(testVal)
    print(f"Count: {count} {len(mySet)}")


if __name__ == "__main__":
    main()
