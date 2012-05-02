# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse

parser = argparse.ArgumentParser(description="Singularities with Poincare index")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument("block_size", nargs=1, help = "Block size")
parser.add_argument("tolerance", nargs=1, help = "Tolerance for Poincare index")
parser.add_argument('--smooth', "-s", action='store_true', help = "Use Gauss for smoothing")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

W = int(args.block_size[0])

f = lambda x, y: 2 * x * y
g = lambda x, y: x ** 2 - y ** 2

angles = utils.calculate_angles(im, W, f, g)
if args.smooth:
    angles = utils.smooth_angles(angles)

utils.calculate_singularities(angles, int(args.tolerance[0]))
