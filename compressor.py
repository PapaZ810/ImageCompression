import numpy as np
import os, sys, math
from PIL import Image

pi = math.pi
cos = math.cos
np.set_printoptions(threshold = sys.maxsize, linewidth = 750)

file = sys.argv[len(sys.argv)-1]
quality = sys.argv[len(sys.argv)-2]
cwd = os.getcwd()
arr = Image.open(cwd + "\\" + file).convert('YCbCr')
arr = np.array(arr)
dim1 = len(arr)
dim2 = len(arr[0])

fourier = np.empty(64).reshape(8, 8)
for i in range(8):
    for j in range(8):
        fourier[j][i] = (cos((2*i+1)*j*pi/16))

def extractor(dim1, dim2, array, vecnum):
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(dim2):
        for j in range(dim1):
            result[j][i] = array[j][i][vecnum]

    return result

luminance = extractor(dim1, dim2, arr, 0)
Cr = extractor(dim1, dim2, arr, 1)
Cb = extractor(dim1, dim2, arr, 2)

#print(luminance), print(Cr), print(Cb)

fourierinv = np.linalg.inv(fourier.T)

def fourierconversion(finv, array):
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(int(len(array) / 8)):
        for j in range(int(len(array[0]) / 8)):
            result[j:j+8, i:i+8] = ( finv * array[j:j+8, i:i+8])
    return result

print(fourierconversion(fourierinv, luminance))