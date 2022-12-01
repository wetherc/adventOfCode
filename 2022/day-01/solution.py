import os


def parse_input() -> list[list[int]]:
    parsed_input: list[list[int]] = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        _tmp: list[int] = []
        for line in f:
            _line = line.strip()
            if _line:
                _tmp.append(int(_line))
            else:
                parsed_input.append(_tmp)
                _tmp = []
    return parsed_input


def collect_calories(elves: list[list[int]]) -> list[int]:
    elf_calories: list[int] = []
    for elf in elves:
        elf_calories.append(sum(elf))
    return elf_calories


def main():
    elf_loads = parse_input()
    elf_calories = sorted(collect_calories(elf_loads), reverse=True)

    print(f'The elf carrying the most has {elf_calories[0]} calories')
    print(f'The top 3 elves together are carrying {sum(elf_calories[0:3])}')
    

if __name__ == '__main__':
    main()