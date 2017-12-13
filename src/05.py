import argparse

parser = argparse.ArgumentParser(description='Escape a linked list')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_input(input):
    l = []
    with open(input, 'r') as instructions:
        for instruction in instructions:
            l.append(int(instruction))
    return l


def escape_list(instructions, part):
    step = position = prior = 0
    while position <= len(instructions):
        try:
            prior, position = position, position + instructions[position]
            if instructions[prior] >= 3 and part == '2':
                instructions[prior] -= 1
            else:
                instructions[prior] += 1
            # print('step {}: {}/{}'.format(step, position, len(instructions)))
            step += 1
        except:
            return step
    return step


if __name__ == '__main__':
    instructions = read_input(args.input)
    output = escape_list(instructions, args.part)
    print(output)
