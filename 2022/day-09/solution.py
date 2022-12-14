import os
from operator import add, sub


def parse_input() -> list[list[str]]:
    parsed_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append(line.strip().split())
    return parsed_input


def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b) 
    

def move_rope(rope: list[list[int]], direction: str, magnitude: int):
    _directions = {
        'U': [0, 1],
        'R': [1, 0],
        'D': [0, -1],
        'L': [-1, 0]
    }

    tail_positions = []
    for _ in range(magnitude):
        rope[0] = list(map(add, rope[0], _directions[direction]))
        
        for knot in range(1, len(rope)):
            rope[knot] = follow_leader(rope[knot], rope[knot - 1])
        tail_positions.append(tuple(rope[-1]))
    return rope, tail_positions


def follow_leader(follower: list[int],
                  leader: list[int]) -> list[int]:
    _distance = list(map(sub, leader, follower))

    if any(abs(elem) > 1 for elem in _distance):
        _idx = _distance.index(max(_distance, key=abs))
        _sign = cmp(_distance[_idx], 0)

        _distance[_idx] =  _distance[_idx] + (_sign * -1)
        follower = list(map(add, follower, _distance))
    return follower


def simulate(num_knots, parsed_input):
    # Simulation with a single tail knot
    tail_history = [(0, 0)]
    # Elem 0 is the head, elem 1 is the first knot, and so on
    knot_positions = [[0, 0]] * (1 + num_knots)

    for instruction in parsed_input:
        knot_positions, _tail_movement = move_rope(
            knot_positions,
            instruction[0],
            int(instruction[1])
        )
        tail_history = tail_history + _tail_movement
    return tail_history


def main():
    parsed_input = parse_input()

    tail_history = simulate(1, parsed_input)
    print(len(set(tail_history)))

    tail_history = simulate(9, parsed_input)
    print(len(set(tail_history)))


if __name__ == '__main__':
    main()
    