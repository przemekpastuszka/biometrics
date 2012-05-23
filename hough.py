# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math


def get_hough_image(im):
    (x, y) = im.size
    x *= 1.0
    y *= 1.0

    im_load = im.load()

    result = Image.new("RGBA", im.size, 0)
    draw = ImageDraw.Draw(result)

    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            if im_load[i, j] > 220:
                line = lambda t: (t, (-(i / x - 0.5) * (t / x) + (j / y - 0.5)) * x)
                draw.line([line(0), line(x)], fill=(50, 0, 0, 10))

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hough transform")
    parser.add_argument("image", nargs=1, help = "Path to image")
    args = parser.parse_args()

    im = Image.open(args.image[0])
    im = im.convert("L")  # covert to grayscale
    im.show()

    hough_img = get_hough_image(im)
    hough_img.show()
