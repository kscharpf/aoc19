import sys

inp = "238345-746315"
#inp = "100000-240000"

def hasAdjacent(s):
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            return True
    return False

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
    #print(f"hasAdjacent: {hasAdjacent('122345')}")
    #print(f"nonDecreasing: {isNonDecreasing('111123')}")
    print(f"nonDecreasing: {isNonDecreasing('135679')}")
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
        if hasAdjacent(s) and isNonDecreasing(s):
            count += 1
            mySet.add(testVal)
            print(f"{testVal}")
    print(f"Count: {count} {len(mySet)}")


if __name__ == "__main__":
    main()
