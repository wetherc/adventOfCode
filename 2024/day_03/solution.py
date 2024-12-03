import os
import re
from typing import List, Tuple


def load_input(test: bool=False) -> List[List[int]]:
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r'
    ) as f:
        input = f.read()

    return input


def get_statements(input: str, conditionals=False) -> List[Tuple[str, int, int]]:
    _match = r'mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don\'t\(\)'
    matches = re.findall(_match, input)
    out = []

    conditional_map = {
        'do()': True,
        'don\'t()': False
    }
    conditional_process = True

    for match in matches:
        if match in ['do()', 'don\'t()']:
            if not conditionals:
                continue
            conditional_process = conditional_map[match]
            continue

        if conditional_process:
            op, lhs, rhs, _ = re.split(r'[\(\),]', match)
            out.append((op, int(lhs), int(rhs)))

    return out


if __name__ == '__main__':
    input = load_input(test=False)
    matches = get_statements(input)
    
    print(sum([match[1] * match[2] for match in matches]))

    conditional_matches = get_statements(input, conditionals=True)
    print(sum([match[1] * match[2] for match in conditional_matches]))
