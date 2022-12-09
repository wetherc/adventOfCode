import os


def parse_input() -> str:
    parsed_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append(line.strip().split())
    return parsed_input


def move_on_grid(head_pos, tail_pos, instruction):
    tail_movement = []
    _tail_pos = tail_pos
    _head_pos = head_pos
    spaces_to_move = int(instruction[1])

    _is_initial = 0 if head_pos == tail_pos else 1
    _is_lateral = any([
        (head_pos[1] == tail_pos[1] and instruction[0] in ['L', 'R']),
        (head_pos[0] == tail_pos[0] and instruction[0] in ['U', 'D'])
    ])
    _is_diagonal = (head_pos[1] != tail_pos[1] and head_pos[0] != tail_pos[0])

    delta = 0
    if not _is_lateral:
        delta = 1

        if instruction[0] == 'L':
            _head_pos = [_head_pos[0] - (delta + _is_diagonal), _head_pos[1]]
        elif instruction[0] == 'R':
            _head_pos = [_head_pos[0] + (delta + _is_diagonal), _head_pos[1]]
        elif instruction[0] == 'U':
            _head_pos = [_head_pos[0], _head_pos[1] - (delta + _is_diagonal)]
        elif instruction[0] == 'D':
            _head_pos = [_head_pos[0], _head_pos[1] + (delta + _is_diagonal)]

        spaces_to_move -= delta + _is_diagonal + 1
        if spaces_to_move <= 0:
            # print(instruction, _is_lateral, _head_pos, _tail_pos)
            return _head_pos, _tail_pos, tail_movement

        diag = [b - a for a, b in zip(_tail_pos, _head_pos)]
        _tail_pos = [a + b for a, b in zip(_tail_pos, diag)]
        tail_movement.append((_tail_pos[0], _tail_pos[1]))

    if instruction[0] == 'L':
        _head_pos = [_head_pos[0] - (spaces_to_move + delta), _head_pos[1]]
        tail_movement = tail_movement + [
            (_tail_pos[0] - (elem + _is_initial), _tail_pos[1])
            for elem in range(spaces_to_move)
        ]
    elif instruction[0] == 'R':
        _head_pos = [_head_pos[0] + (spaces_to_move + delta), _head_pos[1]]
        tail_movement = tail_movement + [
            (_tail_pos[0] + (elem + _is_initial), _tail_pos[1])
            for elem in range(spaces_to_move)
        ]
    elif instruction[0] == 'U':
        _head_pos = [_head_pos[0], _head_pos[1] - (spaces_to_move + delta)]
        tail_movement = tail_movement + [
            (_tail_pos[0], _tail_pos[1] - (elem + 1))
            for elem in range(spaces_to_move)
        ]
    elif instruction[0] == 'D':
        _head_pos = [_head_pos[0], _head_pos[1] + (spaces_to_move + delta)]
        tail_movement = tail_movement + [
            (_tail_pos[0], _tail_pos[1] + (elem + _is_initial))
            for elem in range(spaces_to_move)
        ]

    # print(instruction, _is_lateral, _head_pos, tail_movement[-1])
    return _head_pos, tail_movement[-1], tail_movement


def main():
    parsed_input = parse_input()
    tail_history = [(0, 0)]
    head_pos = [0, 0]
    tail_pos = [0, 0]
    for instruction in parsed_input:
        head_pos, tail_pos, tail_movement = move_on_grid(
            head_pos,
            tail_pos,
            instruction
        )
        # print(tail_pos, tail_movement)
        tail_history = tail_history + tail_movement
    print(len(set(tail_history)))


if __name__ == '__main__':
    main()
    