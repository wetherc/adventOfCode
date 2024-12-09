from __future__ import annotations

import os
import itertools
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int

    def get_distance(self, point: Coordinate) -> Tuple[int, int]:
        return (point.x - self.x, point.y - self.y)
    
    def get_antinode(self, point: Coordinate) -> Coordinate:
        _distance = self.get_distance(point)
        _x = self.x + (2 * _distance[0])
        _y = self.y + (2 * _distance[1])
        return Coordinate(_x, _y)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


def load_input(test: bool=False) -> List[List[str]]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = f.read().splitlines()
        return [list(line) for line in input]


def render_map(map: List[List[str]]) -> None:
    for line in map:
        print(''.join(line))
    print('\n\n')


def get_antenna_positions(map: List[List[str]]) -> Dict[str, List[Coordinate]]:
    antennas = {}
    for y_idx, row in enumerate(map):
        for x_idx, cell in enumerate(row):
            if cell != '.':
                antennas[cell] = antennas.get(cell, []) + [Coordinate(x_idx, y_idx)]

    return antennas


def map_antinodes_for_frequency(antennas: List[Coordinate]) -> List[Coordinate]:
    antenna_combinations = itertools.permutations(antennas, 2)
    antinode_coordinates = [
        pair[0].get_antinode(pair[1]) for pair in antenna_combinations
    ]

    return antinode_coordinates

def map_antinodes_for_slope(antennas: List[Coordinate], map_size: Tuple[int, int]) -> List[Coordinate]:
    antenna_combinations = itertools.permutations(antennas, 2)
    antinode_coordinates = []
    for pair in antenna_combinations:
        slope = pair[0].get_distance(pair[1])

        _coordinate = pair[0]
        while 0 <= _coordinate.x < map_size[0] and 0 <= _coordinate.y < map_size[1]:
            antinode_coordinates.append(_coordinate)
            _x = _coordinate.x + slope[0]
            _y = _coordinate.y + slope[1]

            _coordinate = Coordinate(_x, _y)
    return antinode_coordinates


if __name__ == '__main__':
    antenna_map = load_input(test=False)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"-"*40}\n- Original Map\n{"-"*40}')
    render_map(antenna_map)

    antenna_positions = get_antenna_positions(antenna_map)
    antinodes = []
    for frequency in antenna_positions.keys():
        antinodes += [
            node for node in map_antinodes_for_frequency(antenna_positions[frequency])
            if 0 <= node.x < len(antenna_map[0]) and 0 <= node.y < len(antenna_map)
        ]

    for antinode in antinodes:
        antenna_map[antinode.y][antinode.x] = (
            '#' if antenna_map[antinode.y][antinode.x] == '.'
            else antenna_map[antinode.y][antinode.x]
        )

    _n_antinodes = len(set([node.to_tuple() for node in antinodes]))
    print(f'{"-"*40}\n- Antinode Map: {_n_antinodes} unique locations\n{"-"*40}')
    render_map(antenna_map)

    antinodes = []
    for frequency in antenna_positions.keys():
        antinodes += [
            node for node in map_antinodes_for_slope(
                antenna_positions[frequency],
                (len(antenna_map[0]), len(antenna_map))
            )
        ]

    for antinode in antinodes:
        antenna_map[antinode.y][antinode.x] = (
            '#' if antenna_map[antinode.y][antinode.x] == '.'
            else antenna_map[antinode.y][antinode.x]
        )

    _n_antinodes = len(set([node.to_tuple() for node in antinodes]))
    print(f'{"-"*40}\n- Antinode Map: {_n_antinodes} unique locations\n{"-"*40}')
    render_map(antenna_map)
