import os


def parse_input() -> list[list[str]]:
    parsed_input: list[list[str]] = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            _chars = line.split()
            _chars[1] = chr(ord(_chars[1]) - 23)
            parsed_input.append(_chars)
    return parsed_input


def calculate_score(rounds: list[list[str]]) -> list[list[int]]:
    _shape_points: dict[str: int] = {
        'A': 1,
        'B': 2,
        'C': 3
    }
    _wins: list[list[str]] = [
        ['A', 'B'],
        ['B', 'C'],
        ['C', 'A']
    ]
    tally: list[(int, int)] = []

    for _round in rounds:
        if _round[0] == _round[1]:
            points = 3
        elif _round in _wins:
            points = 6
        else:
            points = 0
        tally.append([
            _shape_points[_round[1]],
            points
        ])
    return tally


def fix_match(rounds) -> list[list[str]]:
    _win_dict: dict[str: str] = {
        'A': 'B',
        'B': 'C',
        'C': 'A'
    }
    _loss_dict: dict[str: str] = {
        'A': 'C',
        'B': 'A',
        'C': 'B'
    }

    fixed_matches: list[list[str]] = []
    for _round in rounds:
        if _round[1] == 'A':
            play = _loss_dict[_round[0]]
        elif _round[1] == 'B':
            play = _round[0]
        else:
            play = _win_dict[_round[0]]
        
        fixed_matches.append([_round[0], play])
    
    return fixed_matches



def main():
    rounds = parse_input()
    round_points = calculate_score(rounds)
    total = sum([sum(elem) for elem in zip(*round_points)])

    print(f'The final score is {total}')

    fixed_matches = fix_match(rounds)
    fixed_match_points = calculate_score(fixed_matches)
    fixed_total = sum([sum(elem) for elem in zip(*fixed_match_points)])

    print(f'The final fixed score is {fixed_total}')
    

if __name__ == '__main__':
    main()