import argparse

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


if __name__ == '__main__':
    instructions = read_input(args.input)
    output = escape_list(instructions, args.part)
    print(output)
