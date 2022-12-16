import os
from ast import literal_eval
from itertools import zip_longest


def parse_input():
    literal_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/sample.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            if line.strip():
                literal_input.append(line.strip())
    
    parsed_input = []
    for idx in range(0, len(literal_input), 2):
        parsed_input.append([
            literal_eval(literal_input[idx]),
            literal_eval(literal_input[idx + 1])
        ])
    
    return parsed_input


def evaluate_packets(left, right):
    print(left, right)

    if isinstance(left, int) ^ isinstance(right, int):
        left, right = (
            [elem] if not isinstance(elem, list)
            else elem
            for elem in (left, right)
        )
        evaluate_packets(left, right)
    if isinstance(left, list) and isinstance(right, list):
        # if len(left) > len(right):
        #     return False
        # for (x, y) in zip_longest(left, right, fillvalue=99999):
        for (x, y) in zip(left, right):
            if not evaluate_packets(x, y):
                return False
    if isinstance(left, int) and isinstance(right, int):
        return left <= right

    # if left is None:
    #     return True
    # if right is None:
    #     return False

    return True
    

def main():
    parsed_input = parse_input()
    tally = []
    for elem in parsed_input:
        print(elem)
        if len(elem[0]) > len(elem[1]):
            print(False)
            tally.append(False)
            continue
        _res = evaluate_packets(elem[0], elem[1])
        tally.append(_res)
        print(_res)
    print(sum([
        idx + 1 if val is True else 0
        for idx, val in enumerate(tally)
    ]))

if __name__ == '__main__':
    main()
    