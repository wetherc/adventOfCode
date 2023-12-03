import re


def load_input():
    with open('input.txt', 'r') as f:
        input = f.read().splitlines()

    return input


def get_symbol_positions(line):
    _matches = re.finditer(r'[^a-zA-Z0-9\.]', line)
    positions = [match.start() for match in _matches]

    return positions


def get_number_positions(line, row):
    _matches = re.finditer(r'[0-9]+', line)
    positions = [
        (match.start(), match.end(), match.group(0), row)
        for match in _matches]

    return positions


def check_adjacency(coord, numbers):
    matches = []
    for row in numbers:
        _matches = [
            num for num in row if
            num[0] <= coord <= num[1] or
            num[0] - coord == 1 or
            num[1] - coord == 0
        ]
        matches += _matches

    return matches


if __name__ == '__main__':
    input = load_input()
    
    symbol_positions = [get_symbol_positions(line) for line in input]
    number_positions = [get_number_positions(line, row) for row, line in enumerate(input)]

    (_height, _width) = (len(input), len(input[0]))

    matches = []
    for row in range(len(input)):
        for symbol in symbol_positions[row]:
            matches += check_adjacency(
                symbol,
                number_positions[
                    max(0, row - 1):
                    min(_height, row + 2)  ## slices use exclusive upper bounds
                ]
            )
            
    # matched = set([int(m[2]) for m in matches])
    matched = [int(m[2]) for m in list(set(matches))]
    print(
        f'matched {len(matched)} out of a possible',
        sum([len(row) for row in number_positions]),
        f'engine part numbers')
    print()
    print(sum(matched))