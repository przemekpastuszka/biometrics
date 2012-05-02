# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math

def points_on_line(line, W):
    points = []
    for x in range(0, W):
        y = round(line(x))
        if 0 <= y and y < W:
            points.append((x, y))
    print points
    return points

def ortho_vec_and_step(tang, W):
    ortho_tang = -1.0 / tang
    (ortho_begin, ortho_end) = utils.get_line_ends(0, 0, W, ortho_tang)
    (x_vec, y_vec) = (ortho_end[0] - ortho_begin[0], ortho_end[1] - ortho_begin[1])
    length = math.hypot(x_vec, y_vec)
    (x_norm, y_norm) = (x_vec / length, y_vec / length)
    step = length / W

    print (x_norm, y_norm, step)
    return (x_norm, y_norm, step)

def block_frequency(i, j, W, angle, im_load):
    tang = math.tan(angle)

    (x_norm, y_norm, step) = ortho_vec_and_step(tang, W)
    (x_corner, y_corner) = (0 if x_norm >= 0 else W, 0 if y_norm >= 0 else W)

    treshold = 0

    upward = False
    last_level = 0
    count = 0.0
    spaces = 0.0
    dist = 0
    for i in range(0, W):
        line = lambda x: (x - x_norm * i * step - x_corner) * tang + y_norm * i * step + y_corner
        points = points_on_line(line, W)
        level = 0
        for point in points:
            level += im_load[point[0] + i * W, point[1] + j * W]
        if upward and level + treshold < last_level:
            upward = False
            count += 1
            spaces += dist - 1
            dist = 1
        if level > last_level + treshold:
            upward = True
        last_level = level
        dist += 1

    return count / spaces if spaces > 0 else 0

def freq(im, W, angles):
    (x, y) = im.size
    im_load = im.load()
    freq_img = im.copy()

    for i in range(0, x / W):
        for j in range(0, y / W):
            freq = block_frequency(i, j, W, angles[i][j], im_load)
            box = (i * W, j * W, min(i * W + W, x), min(j * W + W, y))
            freq_img.paste(freq * 255, box)

    return freq_img

parser = argparse.ArgumentParser(description="Image frequency")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument("block_size", nargs=1, help = "Block size")
parser.add_argument('--smooth', "-s", action='store_true', help = "Use Gauss for smoothing")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale
im.show()

W = int(args.block_size[0])

f = lambda x, y: 2 * x * y
g = lambda x, y: x ** 2 - y ** 2

angles = utils.calculate_angles(im, W, f, g)
if args.smooth:
    angles = utils.smooth_angles(angles)

freq_img = freq(im, W, angles)
freq_img.show()
