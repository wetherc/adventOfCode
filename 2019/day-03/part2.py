import numpy as np


def load_inputs() -> list:
    wires = []
    with open('input.txt', 'r') as f:
        for line in f:
            wires.append(line.strip())
    return wires


def build_points(wire: str) -> list:
    instructions = wire.split(',')
    points = []
    x = 0
    y = 0

    for instruction in instructions:
        _direction = instruction[0]
        _distance = int(instruction[1:])

        _sign = 1
        _pos = False

        if _direction in ['L', 'D']:
            _sign = -1
        if _direction in ['L', 'R']:
            _pos = True

        for _ in range(_distance):
            x += _sign if not _pos else 0
            y += _sign if _pos else 0
            points.append((x, y))

    return points


def get_intersections(wire_1: set, wire_2: set) -> list:
    intersections = wire_1.intersection(wire_2)
    return intersections


def get_steps(wire: list, point: tuple) -> int:
    # step counts aren't 0-indexed
    return 1 + wire.index(point)


def main():
    wires = load_inputs()
    for idx, wire in enumerate(wires):
        wires[idx] = build_points(wire)

    intersections = get_intersections(set(wires[0]), set(wires[1]))
    closest = {'point': (0, 0), 'steps': np.inf}

    for point in intersections:
        _dist = get_steps(wires[0], point) + get_steps(wires[1], point)
        if _dist < closest['steps']:
            closest = {'point': point, 'steps': _dist}

    print(closest)


if __name__ == '__main__':
    main()
