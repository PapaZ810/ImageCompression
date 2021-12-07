import numpy as np
import os, sys, math
from PIL import Image
import timeit

start = timeit.default_timer()

pi = math.pi
cos = math.cos
np.set_printoptions(threshold = sys.maxsize, linewidth = 1000)

file = sys.argv[len(sys.argv)-1].strip()
if file.__contains__(".\\"):
    file = file.removeprefix(".\\")
if len(sys.argv) < 3:
    quality = 2
else:
    quality = (1-(int(sys.argv[len(sys.argv)-2]) / 10)) * 10

cwd = os.getcwd()
image = Image.open(cwd + "\\" + file).convert('YCbCr')
arr = np.array(image)
dim1 = len(arr)
dim2 = len(arr[0])

fourier = np.empty(64).reshape(8, 8)
for i in range(8):
    for j in range(8):
        fourier[i][j] = (cos((2*i+1)*j*pi/16))

def extractor(array, vecnum):
    dim1, dim2 = len(array), len(array[0])
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(dim1):
        for j in range(dim2):
            result[i][j] = array[i][j][vecnum]

    return result

luminance = extractor(arr, 0)
Cb = extractor(arr, 1)
Cr = extractor(arr, 2)

fourierinv = np.linalg.inv(fourier)

def fourierconversion(finv, array):
    dim1, dim2 = len(array), len(array[0])
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(int(len(array) / 8)):
        for j in range(int(len(array[i]) / 8)):
            result[i:i+8, j:j+8] = ( finv * array[i:i+8, j:j+8])
    return array

def clearBadValues(array, quality):
    dim1, dim2 = len(array), len(array[0])
    for i in range(dim1):
        for j in range(dim2):
            if array[i][j] < quality:
                array[i][j] = 0
    return array

fourLum = fourierconversion(fourierinv, luminance)
clearedLum = clearBadValues(fourLum, quality)
resultLum = fourierconversion(fourier, clearedLum)

fourCb = fourierconversion(fourierinv, Cb)
clearedCb = clearBadValues(fourCb, quality)
resultCb = fourierconversion(fourier, clearedCb)

fourCr = fourierconversion(fourierinv, Cr)
clearedCr = clearBadValues(fourCr, quality)
resultCr = fourierconversion(fourier, clearedCr)

def integrator(vec1, vec2, vec3):
    dim1, dim2 = len(vec1), len(vec1[0])
    result = np.empty(dim1*dim2*3, dtype=np.uint8).reshape(dim1, dim2, 3)
    for i in range(dim1):
        for j in range(dim2):
            result[i][j][0], result[i][j][1], result[i][j][2] = vec1[i][j], vec2[i][j], vec3[i][j]
    return result

resultArr = integrator(resultLum, resultCb, resultCr)

Image.fromarray(resultArr, "YCbCr").save(cwd + "\\compressed_" + file)

stop = timeit.default_timer()
print('Time: ', stop-start)