# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math


def points_on_line(line, W):
    im = Image.new("L", (W, 3 * W), 100)
    draw = ImageDraw.Draw(im)
    draw.line([(0, line(0) + W), (W, line(W) + W)], fill=10)
    im_load = im.load()

    points = []
    for x in range(0, W):
        for y in range(0, 3 * W):
            if im_load[x, y] == 10:
               points.append((x, y - W))

    del draw
    del im

    dist = lambda (x, y): (x - W / 2) ** 2 + (y - W / 2) ** 2

    return sorted(points, cmp = lambda x, y: dist(x) < dist(y))[:W]

def vec_and_step(tang, W):
    (begin, end) = utils.get_line_ends(0, 0, W, tang)
    (x_vec, y_vec) = (end[0] - begin[0], end[1] - begin[1])
    length = math.hypot(x_vec, y_vec)
    (x_norm, y_norm) = (x_vec / length, y_vec / length)
    step = length / W

    return (x_norm, y_norm, step)

def block_frequency(i, j, W, angle, im_load):
    tang = math.tan(angle)
    ortho_tang = -1 / tang

    (x_norm, y_norm, step) = vec_and_step(tang, W)
    (x_corner, y_corner) = (0 if x_norm >= 0 else W, 0 if y_norm >= 0 else W)

    grey_levels = []

    for k in range(0, W):
        line = lambda x: (x - x_norm * k * step - x_corner) * ortho_tang + y_norm * k * step + y_corner
        points = points_on_line(line, W)
        level = 0
        for point in points:
            level += im_load[point[0] + i * W, point[1] + j * W]
        grey_levels.append(level)

    treshold = 100
    upward = False
    last_level = 0
    last_bottom = 0
    count = 0.0
    spaces = len(grey_levels)
    for level in grey_levels:
        if level < last_bottom:
            last_bottom = level
        if upward and level < last_level:
            upward = False
            if last_bottom + treshold < last_level:
                count += 1
                last_bottom = last_level
        if level > last_level:
            upward = True
        last_level = level

    return count / spaces if spaces > 0 else 0

def freq(im, W, angles):
    (x, y) = im.size
    im_load = im.load()
    freqs = [[0] for i in range(0, x / W)]

    for i in range(1, x / W - 1):
        for j in range(1, y / W - 1):
            freq = block_frequency(i, j, W, angles[i][j], im_load)
            freqs[i].append(freq)
        freqs[i].append(0)

    freqs[0] = freqs[-1] = [0 for i in range(0, y / W)]

    return freqs

def freq_img(im, W, angles):
    (x, y) = im.size
    freqs = freq(im, W, angles)
    freq_img = im.copy()

    for i in range(1, x / W - 1):
        for j in range(1, y / W - 1):
            box = (i * W, j * W, min(i * W + W, x), min(j * W + W, y))
            freq_img.paste(freqs[i][j] * 255.0 * 1.2, box)

    return freq_img

if __name__ == "__main__":
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

    freq_img = freq_img(im, W, angles)
    freq_img.show()
