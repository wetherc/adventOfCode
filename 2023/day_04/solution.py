import re
import os


def load_input():
    input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r'
    ) as f:
        for line in f:
            _parts = re.split(': |\| ', line.strip())
            _item = {
                'card': int(_parts[0].split()[-1]),
                'winning': [
                    int(elem)
                    for elem in re.split(' +', _parts[1])
                    if elem],
                'picks': [
                    int(elem)
                    for elem in re.split(' +', _parts[2])
                    if elem],
                'card_count': 1
            }
            input.append(_item)

    return input


def calculate_points(card):
    doubling_len = len(set(card['winning']).intersection(set(card['picks'])))
    if doubling_len == 0:
        return 0, 0
    
    points = 1
    for _ in range(1, doubling_len):
        points *= 2
    
    return points, doubling_len


if __name__ == '__main__':
    input = load_input()
    for card in input:
        # Card numbers are 1-indexed so for list indices we need to decrement
        input[card['card'] - 1]['points'], _extras = calculate_points(card)
        for extra_card in range(card['card'], card['card'] + _extras):
            # for each winning number match, we add a new copy of a
            # scratchoff ticket from n + 1 through n + (1 * num_matches)
            input[extra_card]['card_count'] += 1 * card['card_count']
    
    print(f'Your original scratchcard count was {len(input)}')
    print(
        'Your scratchcards totalled',
        f'{sum([card["points"] for card in input])} points')
    print(
        'Your scratchcard count totalled',
        f'{sum([card["card_count"] for card in input])} cards')

