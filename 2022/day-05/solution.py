import os
import copy


def parse_input():
    parsed_input = {
        'stacks': [],
        'instructions': []
    }
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            if ord(line[0]) <= 90:
                parsed_input['stacks'].append(
                    line.strip().split()
                )
            else:
                parsed_input['instructions'].append(
                    list(
                        int(line.strip().split()[index])
                        for index in [1, 3, 5]
                    )
                )
    return parsed_input


def rearrange_crates(crates: list[list[str]], num: int, from_pos: int,
                     to_pos: int, preserve_order=False):
    _crates = crates[from_pos - 1][(-1 * num):]
    del crates[from_pos - 1][(-1 * num):]
    
    if preserve_order:
        for crate in _crates:
            crates[to_pos - 1].append(crate)
    else:
        for crate in _crates[::-1]:
            crates[to_pos - 1].append(crate)
    return crates


def main():
    parsed_input = parse_input()
    rearranged_crates = copy.deepcopy(parsed_input['stacks'])
    for instruction in parsed_input['instructions']:
        rearranged_crates = rearrange_crates(
            rearranged_crates,
            instruction[0],
            instruction[1],
            instruction[2]
        )
    
    print(''.join([crate[len(crate) - 1] for crate in rearranged_crates]))

    rearranged_crates_ordered = copy.deepcopy(parsed_input['stacks'])
    for instruction in parsed_input['instructions']:
        rearranged_crates_ordered = rearrange_crates(
            rearranged_crates_ordered,
            instruction[0],
            instruction[1],
            instruction[2],
            True
        )
    print(''.join([crate[len(crate) - 1] for crate in rearranged_crates_ordered]))


if __name__ == '__main__':
    main()