#!/usr/bin/eng python3

def read_input():
    with open('./input.txt', 'r') as input:
        for line in input:
            yield line


def update_frequency(frequency, change):
    frequency += change

    return frequency


def main():
    frequency = 0
    input_lines = []
    frequencies = []
    dupe = None

    for line in read_input():
        frequency = update_frequency(frequency, int(line))
        input_lines.append(int(line))
        if frequency in frequencies:
            dupe = frequency
        frequencies.append(frequency)
    print('The final frequency is {}'.format(frequency))

    iterations = 0
    while dupe is None:
        print('iteration {} ({} items)'.format(iterations, len(frequencies)))
        for line in input_lines:
            frequency = update_frequency(frequency, line)
            if frequency in frequencies:
                dupe = frequency
                print(dupe)
                break
            else:
                frequencies.append(frequency)
        iterations += 1

    print('The first duplicated frequency is {}'.format(dupe))


if __name__ == '__main__':
    main()
