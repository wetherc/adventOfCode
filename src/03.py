from math import ceil, sqrt
import argparse

parser = argparse.ArgumentParser(description='Compute a checksum')
parser.add_argument('--input')
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
        (x, y + 1),  # lower right
        (x + 1, y),  # center right
        (x + 1, y + 1),  # upper right
        (x, y + 1),  # upper center
        (x - 1, y + 1),  # upper left
        (x, y - 1)  # center left
    ]
    return neighbors


def spiralize(n):
    points, value = [[1]], 1
    coords = (0, 0)

    while value < n:
        value = sum(map(lambda x: points[x[0]][x[1]], get_neighbors(coords)))
        points[coords[0]][coords[1]].append(value)
    return value


if __name__ == '__main__':
    coords = calculate_spiral(int(args.input))
    distance = abs(coords[0]) + abs(coords[1])
    print(distance)
