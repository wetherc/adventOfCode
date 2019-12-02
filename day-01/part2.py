import math


def read_input():
    with open('./input.txt', 'r') as f:
        for line in f:
            yield line.strip()


def calc_fuel(mass):
    fuel = math.floor(int(mass) / 3) - 2
    return fuel


def main():
    lines = read_input()
    mass = 0
    for line in lines:
        if line:
            fuel = calc_fuel(line)
            addtl_fuel = fuel
            while calc_fuel(addtl_fuel) > 0:
                addtl_fuel = calc_fuel(addtl_fuel)
                fuel += addtl_fuel
            mass += fuel
    print(mass)


if __name__ == '__main__':
    main()
