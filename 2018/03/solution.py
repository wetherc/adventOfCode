#!/usr/bin/env python3

import re
import itertools


def read_input():
    with open('./input.txt', 'r') as input:
        for line in input:
            yield line


def parse_input(input):
    claim_regex = r'^#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)$'

    # [claim_no, x_0, y_0, x, y]
    claim_parts = re.search(claim_regex, input).groups()
    claim_parts = [int(part) for part in claim_parts]

    # range of points in range(x), range(y)
    claim_parts.append(range(claim_parts[1], claim_parts[1] + claim_parts[3]))
    claim_parts.append(range(claim_parts[2], claim_parts[2] + claim_parts[4]))

    return claim_parts


def get_overlap(rect_1, rect_2):
    dx, dy = [], []

    for x in rect_2[5]:
      if x in rect_1[5]:
        dx.append(x)

    for y in rect_2[6]:
      if y in rect_1[6]:
        dy.append(y)

    if (len(dx) > 0) and (len(dy) > 0):
        return [rect_1[0], rect_2[0], list(itertools.product(dx, dy))]
    else:
        return None


def main():
    claims = []
    overlaps = set()
    overlapping_claims = set()

    for claim in read_input():
        claims.append(parse_input(claim))

    for claim_0 in claims:
        for claim_1 in claims:
            if claim_0 == claim_1:
                continue
            else:
                overlap = get_overlap(claim_0, claim_1)
                if overlap is not None:
                    for point in overlap[2]:
                        overlaps.add(point)
                    overlapping_claims.add(overlap[0])
                    overlapping_claims.add(overlap[1])

    print('Overlapping square inches:\t{}'.format(len(overlaps)))
    print('Non-overlapping claim ID:\t{}'.format(
        [elem[0] for elem in claims if elem[0] not in overlapping_claims]
    ))


if __name__ == '__main__':
    main()
