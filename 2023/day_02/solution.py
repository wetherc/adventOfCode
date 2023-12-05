import re
import os
from typing import List


def load_input():
    input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + 'input.txt',
        'r'
    ) as f:
        for line in f:
            _parts = re.split(': |; ', line.strip())
            _item = {
                'game': _parts[0].split()[-1],
                'rounds': [
                    dict(reversed(elem.split()) for elem in part.split(', '))
                    for part in _parts[1:]
                ]
            }
            input.append(_item)

    return input


def cube_totals(game, max_red: int, max_green:int , max_blue: int) -> bool:
    if (max([int(_round.get('red', 0)) for _round in game]) > max_red):
        return False
    if (max([int(_round.get('green', 0)) for _round in game]) > max_green):
        return False
    if (max([int(_round.get('blue', 0)) for _round in game]) > max_blue):
        return False
    
    return True


def fewest_dice(game) -> int:
    _max_red = 0
    _max_green = 0
    _max_blue = 0

    for _round in game['rounds']:
        _max_red = max(
            _max_red,
            int(_round.get('red', 0)))
        _max_green = max(
            _max_green,
            int(_round.get('green', 0)))
        _max_blue = max(
            _max_blue,
            int(_round.get('blue', 0)))
    
    return _max_red * _max_green * _max_blue


if __name__ == '__main__':
    parsed_rounds = load_input()

    valid_games = [
        int(game['game']) for game in parsed_rounds
        if cube_totals(
            game['rounds'],
            12,
            13,
            14)
    ]

    print(sum(valid_games))
    print(sum([fewest_dice(game) for game in parsed_rounds]))
