# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math
import os
from utils import flatten, transpose

usage = False

def apply_structure(pixels, structure, result):
    global usage
    usage = False

    def choose(old, new):
        global usage
        if new == result:
            usage = True
            return 0.0
        return old

    utils.apply_kernel_with_f(pixels, structure, choose)

    return usage

def apply_all_structures(pixels, structures):
    usage = False
    for structure in structures:
        usage |= apply_structure(pixels, structure, utils.flatten(structure).count(1))

    return usage

def make_thin(im):
    loaded = utils.load_image(im)
    utils.apply_to_each_pixel(loaded, lambda x: 0.0 if x > 10 else 1.0)
    print "loading phase done"

    t1 = [[1, 1, 1], [0, 1, 0], [0.1, 0.1, 0.1]]
    t2 = utils.transpose(t1)
    t3 = reverse(t1)
    t4 = utils.transpose(t3)
    t5 = [[0, 1, 0], [0.1, 1, 1], [0.1, 0.1, 0]]
    t7 = utils.transpose(t5)
    t6 = reverse(t7)
    t8 = reverse(t5)

    thinners = [t1, t2, t3, t4, t5, t6, t7]

    usage = True
    while(usage):
        usage = apply_all_structures(loaded, thinners)
        print "single thining phase done"

    print "thining done"

    utils.apply_to_each_pixel(loaded, lambda x: 255.0 * (1 - x))
    utils.load_pixels(im, loaded)
    im.show()

def reverse(ls):
    cpy = ls[:]
    cpy.reverse()
    return cpy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image thining")
    parser.add_argument("image", nargs=1, help = "Path to image")
    parser.add_argument("--save", action='store_true', help = "Save result image as src_image_thinned.gif")
    args = parser.parse_args()

    im = Image.open(args.image[0])
    im = im.convert("L")  # covert to grayscale
    im.show()

    make_thin(im)

    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(base_image_name + "_thinned.gif", "GIF")
