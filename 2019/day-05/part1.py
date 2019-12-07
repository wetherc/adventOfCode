def load_input():
    input = []
    with open('./input.txt', 'r') as f:
        for line in f:
            input += [int(val.strip()) for val in line.split(',')]
    return input


def calculate(input, _noun):
    offset = 0

    while True:
        opcode = int(repr(input[offset])[-2:])
        modes = [int(x) for x in repr(input[offset])[-3::-1]]

        if opcode in [1, 2]:
            _offset = 4
        elif opcode in [3, 4]:
            _offset = 2
        elif opcode == 99:  # 99, terminate program
            print('Encountered EOF. Terminating cleanly')
            break
        else:
            print(f'Unknown instruction ({opcode}) at offset {offset}')
            break

        # leading zeroes are omitted as positional markers
        if len(modes) < (_offset - 1):
            modes = modes + [0] * ((_offset - 1) - len(modes))

        positions = []
        for _idx, mode in enumerate(modes):
            if mode == 0:
                positions.append(input[offset + _idx + 1])
            else:
                positions.append(offset + _idx + 1)

        if opcode == 1:
            input[positions[2]] = input[positions[1]] + input[positions[0]]
        elif opcode == 2:
            input[positions[2]] = input[positions[1]] * input[positions[0]]
        elif opcode == 3:
            input[positions[0]] = _noun
        elif opcode == 4:
            print(input[positions[0]])
        else:
            print(f'Bad inputs: noun {_noun} and verb {_verb}')
            print(f'Unknown instruction ({_input[offset]}) at offset {offset}')
            break
        offset += _offset
    return True


def main():
    input = load_input()
    calculate(input, 1)


if __name__ == '__main__':
    main()
