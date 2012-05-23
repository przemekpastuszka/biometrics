# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math
import frequency
import os

def gabor_kernel(W, angle, freq):
    cos = math.cos(angle)
    sin = math.sin(angle)

    yangle = lambda x, y: x * cos + y * sin
    xangle = lambda x, y: -x * sin + y * cos

    xsigma = ysigma = 4

    return utils.kernel_from_function(W, lambda x, y:
        math.exp(-(
            (xangle(x, y) ** 2) / (xsigma ** 2) +
            (yangle(x, y) ** 2) / (ysigma ** 2)) / 2) *
        math.cos(2 * math.pi * freq * xangle(x, y)))

def gabor(im, W, angles):
    (x, y) = im.size
    im_load = im.load()

    freqs = frequency.freq(im, W, angles)
    print "computing local ridge frequency done"

    gauss = utils.gauss_kernel(3)
    utils.apply_kernel(freqs, gauss)

    for i in range(1, x / W - 1):
        for j in range(1, y / W - 1):
            kernel = gabor_kernel(W, angles[i][j], freqs[i][j])
            for k in range(0, W):
                for l in range(0, W):
                    im_load[i * W + k, j * W + l] = utils.apply_kernel_at(
                        lambda x, y: im_load[x, y],
                        kernel,
                        i * W + k,
                        j * W + l)

    return im

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gabor filter applied")
    parser.add_argument("image", nargs=1, help = "Path to image")
    parser.add_argument("block_size", nargs=1, help = "Block size")
    parser.add_argument("--save", action='store_true', help = "Save result image as src_image_enhanced.gif")
    args = parser.parse_args()

    im = Image.open(args.image[0])
    im = im.convert("L")  # covert to grayscale
    im.show()

    W = int(args.block_size[0])

    f = lambda x, y: 2 * x * y
    g = lambda x, y: x ** 2 - y ** 2

    angles = utils.calculate_angles(im, W, f, g)
    print "calculating orientation done"

    angles = utils.smooth_angles(angles)
    print "smoothing angles done"

    result = gabor(im, W, angles)
    result.show()

    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(base_image_name + "_enhanced.gif", "GIF")
