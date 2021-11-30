import numpy as np
import imageio as io
import os
import sys
import math

pi = math.pi
cos = math.cos

file = sys.argv[len(sys.argv)-1]
cwd = os.getcwd()
arr = io.imread(cwd + "\\" + file)
dim1 = len(arr)
dim2 = len(arr[0])
fourier = []
for i in range(8):
    for j in range(8):
        fourier.append(cos((2*i+1)*j*pi/16))

print(dim2)

def extractor(dim1, dim2, array, vecnum):
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(dim2):
        for j in range(dim1):
            result[j][i] = array[j][i][vecnum]

    return result

red = extractor(dim1, dim2, arr, 0)
green = extractor(dim1, dim2, arr, 1)
blue = extractor(dim1, dim2, arr, 2)

print(red), print(green), print(blue), print(arr[dim1-2][dim2-2])
