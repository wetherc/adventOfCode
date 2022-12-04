import os


def parse_input() -> list[list[str]]:
    parsed_input: list[list[str]] = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append([
                [
                    section for section in range(
                        int(assignment.split('-')[0]),
                        int(assignment.split('-')[1]) + 1)
                ] for assignment in line.strip().split(',')
            ])
    return parsed_input


def main():
    assignments = parse_input()
    subsets = []
    overlaps = []
    for assignment in assignments:
        asgn_1 = set(assignment[0])
        asgn_2 = set(assignment[1])
        subsets.append(
            max(
                asgn_1.issuperset(asgn_2),
                asgn_1.issubset(asgn_2)
            )
        )

        overlaps.append(len(asgn_1.intersection(asgn_2)) > 0)


    print(f'There are {sum(subsets)} elves with redundant assignments')
    print(f'There are {sum(overlaps)} elves with partially-redundant assignments')

    


if __name__ == '__main__':
    main()