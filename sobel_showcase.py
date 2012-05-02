# Metody biometryczne
# Przemyslaw Pastuszka

import sobel
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="Sobel filter")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument('--showX', "-x", action='store_true', help = "Show Sobel filter for X coordinate")
parser.add_argument('--showY', "-y", action='store_true', help = "Show Sobel filter for Y coordinate")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

(xSobel, ySobel, fullSobel) = sobel.full_sobels(im)

if args.showX:
    xSobel.show()
if args.showY:
    ySobel.show()
fullSobel.show()
