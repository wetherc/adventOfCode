import re
import os
from typing import List, Tuple


def load_input() -> List[str]:
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r'
    ) as f:
        input = f.read().splitlines()

    return input


def get_positions(row: int, line: Tuple[str]):
    _symbol_matches = re.finditer(r'[^a-zA-Z0-9\.]', line)
    symbol_positions = [
        (match.start(), match.group(0))
        for match in _symbol_matches]
    
    _number_matches = re.finditer(r'[0-9]+', line)
    number_positions = [
        (match.start(), match.end(), match.group(0), row)
        for match in _number_matches]
    
    return symbol_positions, number_positions


def check_adjacancies(coord, numbers, is_asterisk: bool=False):
    number_matches = []
    gear_matches = []
    for row in numbers:
        _matches = [
            num for num in row if
            num[0] <= coord <= num[1] or
            num[0] - coord == 1 or
            num[1] - coord == 0
        ]
        number_matches += _matches
        if is_asterisk:
            gear_matches += [int(_match[2]) for _match in _matches]
    if len(gear_matches) != 2:
        gear_matches = (0, 0)
    
    return number_matches, gear_matches


if __name__ == '__main__':
    input = load_input()
    
    symbol_positions = []
    number_positions = []
    for row, line in enumerate(input):
        _sym, _num = get_positions(row, line)
        symbol_positions.append(_sym)
        number_positions.append(_num)

    (_height, _width) = (len(input), len(input[0]))

    matches = []
    gear_ratios = []
    for row in range(len(input)):
        for symbol in symbol_positions[row]:
            _num_matches, _gear_matches = check_adjacancies(
                symbol[0],
                number_positions[
                    max(0, row - 1):
                    min(_height, row + 2)  # slices use exclusive upper bounds
                ],
                symbol[1] == '*'
            )
            matches += _num_matches
            gear_ratios.append(_gear_matches)
                        
    matched = [int(m[2]) for m in list(set(matches))]
    print(
        f'matched {len(matched)} out of a possible',
        sum([len(row) for row in number_positions]),
        f'engine part numbers')
    print()
    print(sum(matched))

    print()
    print(f'found {len(gear_ratios)} gears')
    print(sum([x[0]*x[1] for x in gear_ratios]))