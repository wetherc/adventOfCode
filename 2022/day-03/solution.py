import os


def parse_input() -> list[list[str]]:
    parsed_input: list[list[str]] = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append([*line.strip()])
    return parsed_input


def make_compartments(inventory: list[str]) -> list[list[str]]:
    num_items = len(inventory)
    assert num_items % 2 == 0

    compartments = [
        inventory[0:(num_items // 2)],
        inventory[(num_items // 2):]
    ]

    return compartments


def get_item_priority(item: str) -> int:
    ascii_int = ord(item)
    if ascii_int <= 90:
        # A - Z are ASCII ints 65 - 90
        ascii_int = ascii_int - 38
    else:
        # a - z are ASCII ints 97 - 122
        ascii_int = ascii_int - 96
    return ascii_int


def get_group_badges(elves: list[list[str]]) -> list[str]:
    assert len(elves) % 3 == 0

    badges = []
    for group in range(len(elves) // 3):
        _group = [
            set(elves[3 * group]),
            set(elves[(3 * group) + 1]),
            set(elves[(3 * group) + 2])
        ]
        badge = _group[0].intersection(_group[1], _group[2])
        badges.append(list(badge)[0])

    return badges


def main():
    rucksacks = parse_input()
    rucksack_compartments = [
        make_compartments(rucksack)
        for rucksack in rucksacks]
    intersections = [
        set(elem[0]).intersection(set(elem[1]))
        for elem in rucksack_compartments
    ]
    priorities = [
        get_item_priority(list(dupe)[0])
        for dupe in intersections
    ]

    print(f'Duplicated item priorities sum to {sum(priorities)}')

    group_badges = get_group_badges(rucksacks)
    badge_priorities = [
        get_item_priority(badge)
        for badge in group_badges
    ]
    print(f'Group badge priorities sum to {sum(badge_priorities)}') 


if __name__ == '__main__':
    main()