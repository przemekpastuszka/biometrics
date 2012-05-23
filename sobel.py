# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageFilter
from math import sqrt
import utils

sobelOperator = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

def merge_images(a, b, f):
    result = a.copy()
    result_load = result.load()
    a_load = a.load()
    b_load = b.load()

    (x, y) = a.size
    for i in range(0, x):
        for j in range(0, y):
            result_load[i, j] = f(a_load[i, j], b_load[i, j])

    return result

def partial_sobels(im):
    ySobel = im.filter(ImageFilter.Kernel((3, 3), utils.flatten(sobelOperator), 1))
    xSobel = im.filter(ImageFilter.Kernel((3, 3), utils.flatten(utils.transpose(sobelOperator)), 1))
    return (xSobel, ySobel)

def full_sobels(im):
    (xSobel, ySobel) = partial_sobels(im)
    sobel = merge_images(xSobel, ySobel, lambda x, y: sqrt(x**2 + y**2))
    return (xSobel, ySobel, sobel)
