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
dim3 = len(arr[0][0])
fourier = []
for i in range(8):
    for j in range(8):
        fourier.append(cos((2*i+1)*j*pi/16))

print(dim2)

luminance = [ [None for y in range(dim2)] for x in range(dim1)]
for i in range(dim2-1):
    for j in range(dim1-1):
            luminance[i][j] = arr[i][j][0]

print(luminance)
