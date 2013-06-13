# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math
import os

cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def minutiae_at(pixels, i, j):
    values = [pixels[i + k][j + l] for k, l in cells]

    crossings = 0
    for k in range(0, 8):
        crossings += abs(values[k] - values[k + 1])
    crossings /= 2

    if pixels[i][j] == 1:
        if crossings == 1:
            return "ending"
        if crossings == 3:
            return "bifurcation"
    return "none"

def calculate_minutiaes(im):
    pixels = utils.load_image(im)
    utils.apply_to_each_pixel(pixels, lambda x: 0.0 if x > 10 else 1.0)

    (x, y) = im.size
    result = im.convert("RGB")

    draw = ImageDraw.Draw(result)

    colors = {"ending" : (150, 0, 0), "bifurcation" : (0, 150, 0)}

    ellipse_size = 2
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            minutiae = minutiae_at(pixels, i, j)
            if minutiae != "none":
                draw.ellipse([(i - ellipse_size, j - ellipse_size), (i + ellipse_size, j + ellipse_size)], outline = colors[minutiae])

    del draw

    return result

parser = argparse.ArgumentParser(description="Minutiae detection using crossing number method")
parser.add_argument("image", nargs=1, help = "Skeleton image")
parser.add_argument("--save", action='store_true', help = "Save result image as src_minutiae.gif")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

result = calculate_minutiaes(im)
result.show()

if args.save:
    base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
    result.save(base_image_name + "_minutiae.gif", "GIF")
