import argparse
import csv
import copy

parser = argparse.ArgumentParser(description='Find cyclic singly-linked lists')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()

def read_tsv(input):
    with open(input) as tsv:
        for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONNUMERIC):
            yield line


def rotate(input):
    start = input.index(max(input))
    val = max(input)
    input[start] = 0
    while val > 0:
        input[(start + 1) % len(input)] += 1
        start += 1
        val -= 1
    return input


def find_loop(input, part):
    # Brute forcing it... :-(
    rotations = []
    step = 0

    while input not in rotations:
        old_input = copy.deepcopy(input)
        rotate(input)
        rotations.append(old_input)
        step += 1
    rotations.append(input)

    if(part == '2'):
        output = [idx for idx, val in enumerate(rotations)
                  if val == rotations[-1]]
        output = output[1] - output[0]
    else:
        output = step
    return output

if __name__ == '__main__':
    instructions = read_tsv(args.input)
    output = find_loop(next(instructions), args.part)
    print(output)
