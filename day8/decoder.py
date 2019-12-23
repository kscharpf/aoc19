import sys
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
import numpy as np

def count(layer, num):
    c = Counter(layer)
    return c[num]
    

def main():
    lines = open(sys.argv[1]).readlines()
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    layers = []
    line = lines[0].rstrip('\n')
    offset = 0
    while offset < len(line):
        layerPixels = line[offset:offset+6*25]
        layers.append(layerPixels)
        offset += (height*width)

    decodedImg = ""
    for idx in range(height * width):
        i = 0
        while layers[i][idx] == '2':
            i += 1
        decodedImg += layers[i][idx]
    rgbArray = np.zeros((6,25,3), 'uint8')

    for i in range(height):
        for j in range(width):
            if decodedImg[i*width + j] == '1':
                rgbArray[i,j,0] = 0xff
                rgbArray[i,j,1] = 0xff
                rgbArray[i,j,2] = 0xff
    img = Image.fromarray(rgbArray)
    img.save('myimg.jpeg')


if __name__ == "__main__":
    main()
