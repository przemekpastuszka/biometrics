# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageStat
import argparse
from math import sqrt

# x - pixel value
# v0 - desired variance
# v - actual image variance
# m - actual image mean
# m0 - desired mean
def normalize_pixel(x, v0, v, m, m0):
    dev_coeff = sqrt((v0 * ((x - m)**2)) / v)
    if x > m:
        return m0 + dev_coeff
    return m0 - dev_coeff

def normalize(im, m0, v0):
    stat = ImageStat.Stat(im)
    m = stat.mean[0]
    v = stat.stddev[0] ** 2

    return im.point(lambda x: normalize_pixel(x, v0, v, m, m0))  # normalize each pixel

parser = argparse.ArgumentParser(description="Image normalization")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument("mean", nargs=1, help = "desired mean")
parser.add_argument("variance", nargs=1, help = "desired variance (squared stdev)")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

im.show()

normalizedIm = normalize(im, float(args.mean[0]), float(args.variance[0]))
normalizedIm.show()
