import numpy as np
import os, sys, math
from PIL import Image
import threading
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

resultList = [np.unsignedinteger] * 3

def extractor(array, vecnum, list):
    dim1, dim2 = len(array), len(array[0])
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(dim1):
        for j in range(dim2):
            result[i][j] = array[i][j][vecnum]
    list[vecnum] = result

t1 = threading.Thread(target = extractor, args=(arr, 0, resultList))
t2 = threading.Thread(target = extractor, args=(arr, 1, resultList))
t3 = threading.Thread(target = extractor, args=(arr, 2, resultList))

t1.start(), t2.start(), t3.start()
t1.join(), t2.join(), t3.join()

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

fourLum = fourierconversion(fourierinv, resultList[0])
clearedLum = clearBadValues(fourLum, quality)
resultLum = fourierconversion(fourier, clearedLum)

fourCb = fourierconversion(fourierinv, resultList[1])
clearedCb = clearBadValues(fourCb, quality)
resultCb = fourierconversion(fourier, clearedCb)

fourCr = fourierconversion(fourierinv, resultList[2])
clearedCr = clearBadValues(fourCr, quality)
resultCr = fourierconversion(fourier, clearedCr)

def integrator(vec1, vec2, vec3):
    dim1, dim2 = len(vec1), len(vec1[0])
    result = np.empty(dim1*dim2*3, dtype=np.uint8).reshape(dim1, dim2, 3)
    for i in range(dim1):
        for j in range(dim2):
            result[i][j][0], result[i][j][1], result[i][j][2] = vec1[i][j], vec2[i][j], vec3[i][j]
    return result

stop = timeit.default_timer()
print('Time: ', stop - start)