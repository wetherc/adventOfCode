import copy


def load_input():
    input = []
    with open('./input.txt', 'r') as f:
        for line in f:
            input += [int(val.strip()) for val in line.split(',')]
    return input


def calculate(_input, _noun, _verb):
    _input[1] = _noun
    _input[2] = _verb
    offset = 0

    while True:
        if _input[offset] == 1:
            _input[_input[offset + 3]] = (
                _input[_input[offset + 1]] +
                _input[_input[offset + 2]]
            )
            offset += 4
        elif _input[offset] == 2:
            _input[_input[offset + 3]] = (
                _input[_input[offset + 1]] *
                _input[_input[offset + 2]]
            )
            offset += 4
        elif _input[offset] == 99:
            print('Encountered EOF. Terminating cleanly')
            break
        else:
            print(f'Bad inputs: noun {_noun} and verb {_verb}')
            print(f'Unknown instruction ({_input[offset]}) at offset {offset}')
            break
    return _input[0]


def main():
    input = load_input()

    for noun in range(0, 100):
        for verb in range(0, 100):
            output = calculate(copy.deepcopy(input), noun, verb)
            if output == 19690720:
                print(f'Value remaining at offset 0: {output}')
                print(f'Given by noun {noun} and verb {verb}')


if __name__ == '__main__':
    main()
