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


if __name__ == '__main__':
    coords = calculate_spiral(int(args.input))
    distance = abs(coords[0]) + abs(coords[1])
    print(distance)
