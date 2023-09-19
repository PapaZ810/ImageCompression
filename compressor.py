import threading

from PIL import Image
<<<<<<< Updated upstream
import threading
=======
import math
import sys
>>>>>>> Stashed changes
import timeit
import numpy as np

start = timeit.default_timer()
PI = math.pi
COS = math.cos
np.set_printoptions(threshold=sys.maxsize, linewidth=1000)

file = sys.argv[-1].strip()
image = Image.open("" + file).convert("YCbCr")
arr = np.array(image)
x = len(arr)
y = len(arr[0])

<<<<<<< Updated upstream
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
=======
global topLeft
global topRight
global bottomLeft
global bottomRight

fourier = np.empty(64).reshape(8, 8)
for i in range(8):
    for j in range(8):
        fourier[i][j] = (COS((2*i+1)*j*PI/16))

fourierInv = np.linalg.inv(fourier)


def fourierConversion(finv, array):
>>>>>>> Stashed changes
    dim1, dim2 = len(array), len(array[0])
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(int(len(array) / 8)):
        for j in range(int(len(array[i]) / 8)):
            result[i:i+8, j:j+8] = (finv * array[i:i+8, j:j+8])
    return array


def clearBadValues(array, quality):
    dim1, dim2 = len(array), len(array[0])
    for i in range(dim1):
        for j in range(dim2):
            if array[i][j] < quality:
                array[i][j] = 0
    return array

<<<<<<< Updated upstream
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
=======

topLeft = arr[:int(x/2), :int(y/2)]
topRight = arr[int(x/2):x, :int(y/2)]
bottomLeft = arr[:int(x/2), int(y/2):]
bottomRight = arr[int(x/2):, int(y/2):]


def compression(array: np.array):
    luminance = array[0:-1, 0:-1, 0]
    Cb = array[0:-1, 0:-1, 1]
    Cr = array[0:-1, 0:-1, 2]

    luminance = fourierConversion(fourier, clearBadValues(fourierConversion(fourierInv, luminance), 2))
    Cb = fourierConversion(fourier, clearBadValues(fourierConversion(fourierInv, Cb), 2))
    Cr = fourierConversion(fourier, clearBadValues(fourierConversion(fourierInv, Cr), 2))

    global topLeft
    global topRight
    global bottomLeft
    global bottomRight

    if threading.current_thread().name == "tl":
        topLeft = np.dstack((luminance, Cb, Cr))
    elif threading.current_thread().name == "tr":
        topRight = np.dstack((luminance, Cb, Cr))
    elif threading.current_thread().name == "bl":
        bottomLeft = np.dstack((luminance, Cb, Cr))
    else:
        bottomRight = np.dstack((luminance, Cb, Cr))


t1 = threading.Thread(target=compression, args=(topLeft,), name="tl")
t2 = threading.Thread(target=compression, args=(topRight,), name="tr")
t3 = threading.Thread(target=compression, args=(bottomLeft,), name="bl")
t4 = threading.Thread(target=compression, args=(bottomRight,), name="br")

t1.start(), t2.start(), t3.start(), t4.start()

t1.join(), t2.join(), t3.join(), t4.join()


top = np.concatenate((topLeft, bottomLeft), axis=1)
bottom = np.concatenate((topRight, bottomRight), axis=1)
resultArr = np.concatenate((top, bottom), axis=0)


Image.fromarray(resultArr, "YCbCr").save("compressed_" + file)

stop = timeit.default_timer()
print("Time: ", stop - start)
>>>>>>> Stashed changes
