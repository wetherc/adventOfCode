import os
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Coordinate:
    """Class for keeping track of word search coordinates."""
    x: int
    y: int


def load_input(test: bool=False) -> List[List[str]]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = [list(line) for line in f.read().splitlines()]

    return input


def get_horizontal(
        line: List[str], x_coord: int,
        invert: bool=False) -> bool:
    _invert = -1 if invert else 1
    if not 0 <= x_coord + (3 * _invert) < len(line):
        return False
    
    if ''.join([
        line[idx]
        for idx in range(x_coord, (x_coord + (4 * _invert)), _invert)
     ]) == 'XMAS':
        return True    
    return False


def get_vertical(
        input: List[List[str]], coord: Coordinate,
        invert: bool=False) -> bool:
    _invert = -1 if invert else 1
    if not 0 <= coord.y + (3 * _invert) < len(input):
        return False
    
    if ''.join([
        input[y_idx][coord.x]
        for y_idx in range(coord.y, (coord.y + (4 * _invert)), _invert)
    ]) == 'XMAS':
        return True
    return False


def get_diag(
        input: List[List[str]], coord: Coordinate,
        invert_x: bool=False, invert_y: bool=False) -> bool:
    _invert_x = -1 if invert_x else 1
    _invert_y = -1 if invert_y else 1

    if not 0 <= coord.y + (3 * _invert_y) < len(input):
        return False
    if not 0 <= coord.x + (3 * _invert_x) < len(line):
        return False
    
    x_seq = [x for x in range(coord.x, coord.x + (4 * _invert_x), _invert_x)]
    y_seq = [y for y in range(coord.y, coord.y + (4 * _invert_y), _invert_y)]
    if ''.join([
        input[y_seq[idx]][x_seq[idx]] for idx in range(4)
    ]) == 'XMAS':
        return True

    return False


def get_x_mas(
        input: List[List[str]], coord: Coordinate) -> bool:

    if not 0 <= coord.y + 1 < len(input):
        return False
    if not 0 <= coord.y - 1 < len(input):
        return False
    if not 0 <= coord.x + 1 < len(line):
        return False
    if not 0 <= coord.x - 1 < len(line):
        return False
    
    if all([
        ''.join([input[coord.y + idx][coord.x + idx] for idx in range(-1, 2, 1)]) in ['MAS', 'SAM'],
        ''.join([input[coord.y + (-1 * idx)][coord.x + idx] for idx in range(-1, 2, 1)]) in ['MAS', 'SAM'],
    ]):
        return True

    return False


if __name__ == '__main__':
    input = load_input(test=False)
    matches = 0
    for y_idx, line in enumerate(input):
        for x_idx, elem in enumerate(line):
            if elem == 'X':
                    coord = Coordinate(x=x_idx, y=y_idx)
                    matches += sum([
                        get_horizontal(line, x_idx),  # LTR
                        get_horizontal(line, x_idx, invert=True),  # RTL
                        get_vertical(input, coord),  # top-to-bottom
                        get_vertical(input, coord, invert=True),  # bottom-to-top
                        get_diag(input, coord),  # southeast
                        get_diag(input, coord, invert_y=True),  # northeast
                        get_diag(input, coord, invert_x=True),  # southwest
                        get_diag(input, coord, invert_x=True, invert_y=True),  # northwest
                    ])
    print(matches)

    matches = 0
    for y_idx, line in enumerate(input):
        for x_idx, elem in enumerate(line):
            if elem == 'A':
                coord = Coordinate(x=x_idx, y=y_idx)
                matches += get_x_mas(input, coord)
    print(matches)
