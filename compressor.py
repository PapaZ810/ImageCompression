import numpy as np
import os, sys, math
from PIL import Image

pi = math.pi
cos = math.cos

file = sys.argv[len(sys.argv)-1]
cwd = os.getcwd()
arr = Image.open(cwd + "\\" + file).convert('YCbCr')
arr = np.array(arr)
dim1 = len(arr)
dim2 = len(arr[0])

fourier = np.empty(64).reshape(8, 8)
for i in range(8):
    for j in range(8):
        fourier[j][i] = (cos((2*i+1)*j*pi/16))

print(dim2)

def extractor(dim1, dim2, array, vecnum):
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(dim2):
        for j in range(dim1):
            result[j][i] = array[j][i][vecnum]

    return result

luminance = extractor(dim1, dim2, arr, 0)
Cr = extractor(dim1, dim2, arr, 1)
Cb = extractor(dim1, dim2, arr, 2)

print(luminance), print(Cr), print(Cb)

fourierinv = np.linalg.inv(fourier)

def fourierconversion(finv, array):
    count = 0
    for i in range(len(array) % 8)
        for j in range(len(array[0] % 8))
            result = finv * array[count:j % 8 * 8][count:i % 8 * 8]
            count++
    return result

