import threading
from PIL import Image
import math
import sys
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

fourier = np.empty(64).reshape(8, 8)
for i in range(8):
    for j in range(8):
        fourier[i][j] = (COS((2*i+1)*j*PI/16))

fourierinv = np.linalg.inv(fourier)

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
    dim1, dim2 = len(array), len(array[0])
    result = np.empty(dim1*dim2).reshape(dim1, dim2)
    for i in range(int(len(array) / 8)):
        for j in range(int(len(array[i]) / 8)):
            result[i:i+8, j:j+8] = (finv * array[i:i+8, j:j+8])
    return result


def clearBadValues(array, quality):
    dim1, dim2 = len(array), len(array[0])
    for i in range(dim1):
        for j in range(dim2):
            if array[i][j] < quality:
                array[i][j] = 0
    return array


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
