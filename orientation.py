# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse

parser = argparse.ArgumentParser(description="Rao's and Chinese algorithms")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument("block_size", nargs=1, help = "Block size")
parser.add_argument('--smooth', "-s", action='store_true', help = "Use Gauss for smoothing")
parser.add_argument('--chinese', "-c", action='store_true', help = "Use Chinese alg. instead of Rao's")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

W = int(args.block_size[0])

f = lambda x, y: 2 * x * y
g = lambda x, y: x ** 2 - y ** 2

if args.chinese:
    normalizator = 255.0
    f = lambda x, y: 2 * x * y / (normalizator ** 2)
    g = lambda x, y: ((x ** 2) * (y ** 2)) / (normalizator ** 4)

angles = utils.calculate_angles(im, W, f, g)
utils.draw_lines(im, angles, W).show()

if args.smooth:
    smoothed_angles = utils.smooth_angles(angles)
    utils.draw_lines(im, smoothed_angles, W).show()
