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

    return set(points)


def get_intersections(wire_1: set, wire_2: set) -> list:
    intersections = wire_1.intersection(wire_2)
    return intersections


def get_manhattan_distance(point: tuple) -> int:
    return abs(0 - point[0]) + abs(0 - point[1])


def main():
    wires = load_inputs()
    for idx, wire in enumerate(wires):
        wires[idx] = build_points(wire)

    intersections = get_intersections(wires[0], wires[1])
    closest = {'point': (0, 0), 'distance': np.inf}

    for point in intersections:
        _dist = get_manhattan_distance(point)
        if _dist < closest['distance']:
            closest = {'point': point, 'distance': _dist}

    print(closest)


if __name__ == '__main__':
    main()
