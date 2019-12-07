def load_input():
    input = []
    with open('./input.txt', 'r') as f:
        for line in f:
            input += [int(val.strip()) for val in line.split(',')]
    return input


def main():
    input = load_input()

    # Need some manual tweaks to restore the program to the state
    # it had just before it crashed
    input[1] = 12
    input[2] = 2
    offset = 0

    while True:
        if input[offset] == 1:
            input[input[offset + 3]] = (
                input[input[offset + 1]] +
                input[input[offset + 2]]
            )
            offset += 4
        elif input[offset] == 2:
            input[input[offset + 3]] = (
                input[input[offset + 1]] *
                input[input[offset + 2]]
            )
            offset += 4
        elif input[offset] == 99:
            print('Encountered EOF. Terminating cleanly')
            break
        else:
            print(f'Encountered an unknown opcode ({input[offset]})')
            break

    print(f'Value remaining at offset 0: {input[0]}')


if __name__ == '__main__':
    main()
