import math


def read_input():
    with open('./input.txt', 'r') as f:
        for line in f:
            yield line.strip()


def main():
    lines = read_input()
    mass = 0
    for line in lines:
        if line:
            mass += math.floor(int(line) / 3) - 2
    print(mass)


if __name__ == '__main__':
    main()
