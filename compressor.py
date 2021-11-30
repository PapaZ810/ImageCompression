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
fourier = []
for i in range(8):
    for j in range(8):
        fourier.append(cos((2*i+1)*j*pi/16))
print(arr.size, arr)

