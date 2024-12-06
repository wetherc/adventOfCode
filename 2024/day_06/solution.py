import os
import time
from copy import deepcopy
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Set


LOOPIES = set()


class Direction(Enum):
    __order__ = 'UP RIGHT DOWN LEFT'
    UP: Tuple[int, int] = (0, -1)
    RIGHT: Tuple[int, int] = (1, 0)
    DOWN: Tuple[int, int] = (0, 1)
    LEFT: Tuple[int, int] = (-1, 0)


@dataclass
class Coordinate:
    x: int
    y: int

    def move(self, direction: Direction, inplace: bool=False):
        x = self.x + direction.value[0]
        y = self.y + direction.value[1]

        if inplace:
            self.x = x
            self.y = y

        return Coordinate(x=x, y=y)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Guard:
    def __init__(self, position: Coordinate, direction: Direction):
        self.position: Coordinate = position
        self.direction: Direction = direction
        self.position_history: List[Tuple[int, int]] = []
        self.direction_history: List[str] = []
    
    def rotate(self) -> None:
        _rotated = {
            'UP': Direction.RIGHT,
            'RIGHT': Direction.DOWN,
            'DOWN': Direction.LEFT,
            'LEFT': Direction.UP
        }
        self.direction = _rotated[self.direction.name]
        return None
    
    def step_forward(self) -> None:
        self.position_history.append(self.position.to_tuple())
        self.direction_history.append(self.direction.name)
        self.position = self.position.move(self.direction)
        return None


class Room:
    def __init__(self, width: int, height: int, obstacles: List[Coordinate]):
        self.width: int = width
        self.height: int = height
        self.obstacles: List[Coordinate] = obstacles
    
    def check_obstacle_collision(self, position: Coordinate, direction: Direction) -> bool:
        _next_position = position.move(direction)
        if _next_position in self.obstacles:
            return True
        return False
    
    def check_in_room(self, position: Coordinate) -> bool:
        if not self.width >= position.x >= 0:
            return False
        if not self.height >= position.y >= 0:
            return False
        return True
    
    def add_obstacle(self, position: Coordinate, direction: Direction) -> None:
        self.obstacles.append(position.move(direction))


def load_input(test: bool=False) -> Tuple[Room, Guard]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = f.read().splitlines()

    # We'll offset the height and width by 1 so that everything
    # is operating off of a 0-index in later comparisons
    _room_metadata = {
        'width': len(input[0]) - 1,
        'height': len(input) - 1,
        'obstacles': []
    }
    _guard_metadata = {
        'position': None,
        'direction': None
    }

    _directions = {
        '^': Direction.UP,
        '>': Direction.RIGHT,
        'v': Direction.DOWN,
        '<': Direction.LEFT
    }
    for y_idx, row in enumerate(input):
        for x_idx, col in enumerate(row):
            if col == '#':
                _room_metadata['obstacles'].append(Coordinate(x=x_idx, y=y_idx))
            elif col in [key for key in _directions.keys()]:
                _guard_metadata['position'] = Coordinate(x=x_idx, y=y_idx)
                _guard_metadata['direction'] = _directions[col]
    
    room = Room(
        width=_room_metadata['width'],
        height=_room_metadata['height'],
        obstacles=_room_metadata['obstacles']
    )
    guard = Guard(
        position=_guard_metadata['position'],
        direction=_guard_metadata['direction']
    )
    return room, guard


def traverse_room(room: Room, guard: Guard, simulate_loops: bool=False,
                  progress=False, debug=False) -> Guard:
    _in_room = True
    _iters = 0
    _start_time = time.time()

    _obstacles = set()

    while _in_room:
        _iters += 1
        if progress:
            _elapsed = round(time.time() - _start_time, 2)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'step {_iters} ({_elapsed} secs): {guard.direction.name}, {guard.position.to_tuple()}')

        if room.check_obstacle_collision(guard.position, guard.direction):
            _obstacle = (
                guard.direction.name,
                guard.position.move(guard.direction).to_tuple()
            )
            if _obstacle in _obstacles:
                global LOOPIES
                LOOPIES.add(_obstacle)
                if debug:
                    print(f"Loop from obstacle at {guard.position.move(guard.direction).to_tuple()}")
                break
            else:
                _obstacles.add(_obstacle)
                guard.rotate()
        else:
            if simulate_loops:
                room2 = deepcopy(room)
                room2.add_obstacle(guard.position, guard.direction)
                guard2 = deepcopy(guard)
                traverse_room(room2, guard2)

            guard.step_forward()
        _in_room = room.check_in_room(guard.position)
    return guard


if __name__ == '__main__':
    _room, _guard = load_input(test=False)

    _guard = traverse_room(_room, _guard, simulate_loops=True, progress=True)
    print(len(set(_guard.position_history)))
    print(len(LOOPIES))
  
