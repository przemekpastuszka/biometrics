# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageStat
import argparse
from math import sqrt

def distance(x, y, W):
    return 1 + sqrt((x - W) ** 2 + (y - W) ** 2)

def create_segmented_and_variance_images(im, W, threshold):
    (x, y) = im.size
    variance_image = im.copy()
    segmented_image = im.copy()
    for i in range(0, x, W):
        for j in range(0, y, W):
            box = (i, j, min(i + W, x), min(j + W, y))
            block_stddev = ImageStat.Stat(im.crop(box)).stddev[0]
            variance_image.paste(block_stddev, box)
            if block_stddev < threshold:
                segmented_image.paste(0, box)  # make block black if rejected
    return (segmented_image, variance_image)

parser = argparse.ArgumentParser(description="Image segmentation")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument("block_size", nargs=1, help = "Block size")
parser.add_argument("threshold", nargs=1, help = "Treshold on stddev for accepting / rejecting blocks")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

im.show()

(segmented, variance) = create_segmented_and_variance_images(im, int(args.block_size[0]), int(args.threshold[0]))
segmented.show()
variance.show()
