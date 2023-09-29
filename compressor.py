import numpy as np
import sys
import math
from PIL import Image
import timeit

start = timeit.default_timer()

pi = math.pi
cos = np.cos
file = sys.argv[-1].strip()
quality = 2

image = Image.open(file).convert('YCbCr')
arr = np.array(image)


def compression(arr):
    fourier = np.empty((8, 8))
    for i in range(8):
        for j in range(8):
            fourier[i][j] = (cos(((2*i+1)*j*pi)/16))


    fourierinv = np.linalg.inv(fourier)
    
    luminance = arr[:-1, :-1, 0]
    Cb = arr[:-1, :-1, 1]
    Cr = arr[:-1, :-1, 2]

    luminance = fourierconversion(fourierinv, clearBadValues(fourierconversion(fourier, luminance), quality))
    Cb = fourierconversion(fourierinv, clearBadValues(fourierconversion(fourier, Cb), quality))
    Cr = fourierconversion(fourierinv, clearBadValues(fourierconversion(fourier, Cr), quality))

    resultArr = np.dstack((luminance, Cb, Cr))

    Image.fromarray(resultArr, "YCbCr").save("compressed_" + file)


def fourierconversion(four, array):
    dim1, dim2 = array.shape
    result = np.zeros_like(array)
    for i in range(int(dim1/8)):
        for j in range(int(dim2/8)):
            result[8*i:8*i+8, 8*j:8*j+8] = np.dot(four, array[8*i:8*i+8, 8*j:8*j+8])
    return array


def clearBadValues(array, quality):
    array[array < quality] = 0
    return array


compression(arr)

stop = timeit.default_timer()
print('Time: ', stop-start)
