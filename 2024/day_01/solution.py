import os
from collections import Counter
from typing import List, Tuple


def load_input(test: bool=False) -> List[str]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = f.read().splitlines()
    return input


def split_lists(input: List[str]) -> List[List[int]]:
    out = [[],[]]
    for elem in input:
        _x, _y = map(int, elem.split())
        out[0].append(_x)
        out[1].append(_y)
    return out


def find_similarities(input: List[List[int]]) -> List[int]:
    lhs = set(input[0])
    rhs = Counter(input[1])

    return sum([idx * rhs.get(idx, 0) for idx in lhs])


if __name__ == '__main__':
    input = load_input(test=False)
    location_lists = split_lists(input)

    location_lists[0].sort()
    location_lists[1].sort()

    deltas = [
        abs(location_lists[0][idx] - location_lists[1][idx])
        for idx in range(0, len(location_lists[0]))
    ]

    print(sum(deltas))
    print(find_similarities(location_lists))
