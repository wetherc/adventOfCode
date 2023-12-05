import re
import os
from typing import List


def load_input() -> List[str]:
    with open(
        os.path.dirname(os.path.abspath(__file__)) + 'input.txt',
        'r'
    ) as f:
        input = f.read().splitlines()

    return input


def parse_numbers(input, strings=False) -> List[List[str]]:
    r = '0|1|2|3|4|5|6|7|8|9'
    if strings:
        r += '|zero|one|two|three|four|five|six|seven|eight|nine'

    numeric_input = []
    for line in input:
        numeric_input.append([
            *map({n: str(i%10) for i, n in enumerate(r.split('|'))}.get,
            re.findall(rf'(?=({r}))', line))
        ])

    return numeric_input


def sum_inputs(calibrations) -> int:
    return sum([
        int(f'{elem[0]}{elem[-1]}') for elem in calibrations
    ])


if __name__ == '__main__':
    inputs = load_input()
    inputs_numeric = parse_numbers(inputs)
    inputs_why_though = parse_numbers(inputs, strings=True)
    print(f'The sum of calibration values is {sum_inputs(inputs_numeric)}')
    print(f'The updated sum of calibration values is {sum_inputs(inputs_why_though)}')
