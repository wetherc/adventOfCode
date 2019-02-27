#!/usr/bin/env python3

import itertools
import editdistance


def read_input():
    with open('./input.txt', 'r') as input:
        for line in input:
            yield line


def get_unique_occurrences(input):
    occurrences = [
        (g[0], len(list(g[1])))
        for g in itertools.groupby(sorted(input))
    ]

    twos = [twos for twos in occurrences if twos[1] == 2]
    threes = [threes for threes in occurrences if threes[1] == 3]

    return (
        True if len(twos) > 0 else False,
        True if len(threes) > 0 else False
    )


def get_edit_distance(left, right):
    return editdistance.eval(left, right)

    
def main():
    twos, threes = 0, 0
    common_ids = None
    lines = []

    for line in read_input():
        _two, _three = get_unique_occurrences(line)

        twos += _two
        threes += _three

        lines.append(line)

    for line in lines:
        for match in lines:
            if line == match:
                continue
            else:
                distance = get_edit_distance(line, match)

            if distance == 1:
                common_ids = [line, match]
                break

    checksum = twos * threes
    print(
        'Checksum: {} * {} = {}'.format(
            twos, threes, checksum
        )
    )

    print('Lev=1:\n\t{}\n\t{}'.format(common_ids[0], common_ids[1]))
    print(
        'Common elements:\t{}'.format(
            ''.join([
                elem for idx, elem in enumerate(common_ids[0]) if elem == common_ids[1][idx]
            ])
        )
    )


if __name__ == '__main__':
    main()
