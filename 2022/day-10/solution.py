import os


def parse_input() -> list[list[str]]:
    parsed_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append(line.strip().split())
    return parsed_input


def draw_sprite(cycles):
    crt = [
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40
    ]
        
    for idx, register in enumerate(cycles):
        _row = idx // 40
        _x_pos = idx - (40 * _row)
        _sprite = [register - 1, register, register + 1]

        if _x_pos in _sprite:
            crt[_row][_x_pos] = '#'
    for row in crt:
        print(''.join(row))


def main():
    parsed_input = parse_input()
    cycles = [1]

    for line in parsed_input:
        _val = cycles[-1]
        # Always a wasted cycle for both addx and noop
        cycles.append(_val)
        if len(line) == 2:
            cycles.append(_val + int(line[1]))

    signals = [20, 60, 100, 140, 180, 220]

    # We care about what's happening _during_ a cycle, which will always
    # be strictly equal to the output of the prior cycle, which is why
    # I add the -1 to the index here
    print(sum([signal * cycles[signal - 1] for signal in signals]))
    draw_sprite(cycles)


if __name__ == '__main__':
    main()
    