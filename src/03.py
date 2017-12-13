from math import ceil, sqrt
import argparse

parser = argparse.ArgumentParser(description='Compute a checksum')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def calculate_spiral(n):
    k = ceil((sqrt(n) - 1) / 2)
    t = 2 * k
    m = (t + 1)**2

    if n >= m - t:
        return (k-(m-n), -k)
    else:
        m = m - t
    if n >= m - t:
        return (-k, -k + (m - n))
    else:
        m = m - t
    if n >= m - t:
        return (-k + (m - n), k)
    else:
        return (k, k - (m - n - t))

def get_neighbors(coords):
    x = coords[0]
    y = coords[1]
    neighbors = [
        (x - 1, y - 1),  # lower left
        (x, y -  1),  # lower center
        (x + 1, y - 1),  # lower right
        (x + 1, y),  # center right
        (x + 1, y + 1),  # upper right
        (x, y + 1),  # upper center
        (x - 1, y + 1),  # upper left
        (x - 1, y)  # center left
    ]
    return neighbors


def spiralize(n):
    points = {(0, 0): 1}
    value = points[(0, 0)]
    x = y = dx = 0
    dy = -1
    while value <= n:
        if (x, y) != (0, 0):
            value = sum(
                filter(None,
                       map(lambda x: points.get(x),
                           get_neighbors((x, y)))))
            points[(x, y)] = value
        if (x == y) or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy
    return value


if __name__ == '__main__':
    if args.part == '1':
        coords = calculate_spiral(int(args.input))
        output = abs(coords[0]) + abs(coords[1])
    else:
        output = spiralize(int(args.input))
    print(output)
