import numpy as np
import math
import sys
import logging
from PIL import Image


TAB = '\t'
logger = logging.getLogger(__name__)
logging.basicConfig(
        stream=sys.stdout,
        level=logging.WARNING)


class IntCode:
    def __init__(self, instructions):
        self.offset = 0
        self.instructions = instructions
        self.inputs = []
        self.relative_base = 0

    def set_input(self, input):
        self.inputs.append(input)
        return self

    def get_offset(self, opcode):
        if opcode in [1, 2, 7, 8]:
            return 4
        elif opcode in [5, 6]:
            return 3
        elif opcode in [3, 4, 9]:
            return 2
        elif opcode == 99:
            return 1
        else:
            raise Exception(
                f'Unknown instruction ({opcode}) at offset {self.offset}')

    def calculate(self):
        while True:
            opcode = int(repr(self.instructions[self.offset])[-2:])
            modes = [
                int(x) for x in repr(self.instructions[self.offset])[-3::-1]]
            _offset = self.get_offset(opcode)

            # leading zeroes are omitted as positional markers
            if len(modes) < (_offset - 1):
                modes = modes + [0] * ((_offset - 1) - len(modes))

            positions = []
            for _idx, mode in enumerate(modes):
                # position mode
                if mode == 0:
                    positions.append(self.instructions[self.offset + _idx + 1])
                # immediate mode
                elif mode == 1:
                    positions.append(self.offset + _idx + 1)
                # relative mode
                elif mode == 2:
                    positions.append(
                        self.instructions[self.offset + _idx + 1] + \
                        self.relative_base)
                else:
                    raise Exception(f'Unknown operating mode, {mode}, found')

            logger.info(
                f'Running opcode {opcode} with modes {modes} '
                f'from offset {self.offset}')
            # z = x + y
            if opcode == 1:
                self.instructions[positions[2]] = (
                    self.instructions.get(positions[1], 0) + \
                    self.instructions.get(positions[0], 0))
                logger.debug(
                    f'{TAB}Setting index {positions[2]} to '
                    f'{self.instructions.get(positions[1], 0)} + '
                    f'{self.instructions.get(positions[0], 0)}'
                )
                self.offset += _offset
            # z = x * y
            elif opcode == 2:
                self.instructions[positions[2]] = (
                    self.instructions.get(positions[1], 0) * \
                    self.instructions.get(positions[0], 0))
                logger.debug(
                    f'{TAB}Setting index {positions[2]} to '
                    f'{self.instructions.get(positions[1], 0)} * '
                    f'{self.instructions.get(positions[0], 0)}'
                )
                self.offset += _offset
            # y = input(x)
            elif opcode == 3:
                logger.debug(
                    f'{TAB}Storing {self.inputs[0]} to index {positions[0]}')
                self.instructions[positions[0]] = self.inputs.pop(0)
                self.offset += _offset
            # logger.debug(x)
            elif opcode == 4:
                self.offset += _offset
                return self.instructions[positions[0]], self
            # jump to y if x != 0
            elif opcode == 5:
                if self.instructions[positions[0]] != 0:
                    self.offset = self.instructions[positions[1]]
                else:
                    self.offset += _offset
                logger.debug(f'{TAB}Jumping to offset {self.offset}')
            # jump to y if x == 0
            elif opcode == 6:
                if self.instructions[positions[0]] == 0:
                    self.offset = self.instructions[positions[1]]
                else:
                    self.offset += _offset
                logger.debug(f'{TAB}Jumping to offset {self.offset}')
            # z = 1 if x < y else 0
            elif opcode == 7:
                if self.instructions[positions[0]] < self.instructions[positions[1]]:
                    self.instructions[positions[2]] = 1
                else:
                    self.instructions[positions[2]] = 0
                self.offset += _offset
            # x = 1 if x == y else o
            elif opcode == 8:
                if self.instructions[positions[0]] == self.instructions[positions[1]]:
                    self.instructions[positions[2]] = 1
                else:
                    self.instructions[positions[2]] = 0
                self.offset += _offset
            # modify relative base
            elif opcode == 9:
                logger.debug(
                    f'{TAB}Adjusting relative base by '
                    f'{self.instructions[positions[0]]}')
                self.relative_base += self.instructions[positions[0]]
                logger.debug(f'{TAB}New relative base is {self.relative_base}')
                self.offset += _offset
            # cleanly terminate program
            elif opcode == 99:
                return None, None
            else:
                raise Exception(
                    f'Unknown instruction ({opcode}) at offset {self.offset}')
        return None


def load_instructions():
    instructions = []
    with open('./input.txt', 'r') as f:
        for line in f:
            instructions += [int(val.strip()) for val in line.split(',')]
    instruction_dict = dict((idx, val) for idx, val in enumerate(instructions))
    return instruction_dict


def turn_and_move(x, y, degree, res):
    if res == 1:
        rotate = 90
    else:
        rotate = -90

    degree = (degree + rotate) % 360
    # I don't feel clever today
    if degree == 0:
        y -= 1
    elif degree == 90:
        x += 1
    elif degree == 180:
        y += 1
    elif degree == 270:
        x -= 1
    else:
        raise Exception(f'Trying to move at {degree} degrees')

    return x, y, degree


def paint(input, instructions, height, width):
    # I'm going to just take a stab and guess that we'll be able
    # to satisfy the problem using a 50x50 grid
    coordinates = np.full((height, width), 0, dtype=np.uint8)
    degree = 0
    x = 5
    y = 5
    should_paint = True
    _history = []

    # Returns 0/1 on instruction 4 or None
    # on program termination
    coordinates[x][y] = input
    res, prog = IntCode(instructions).set_input(coordinates[x][y]).calculate()

    while res is not None:
        if should_paint:
            coordinates[x][y] = res
            res, prog = prog.calculate()
            if res is None:
                break
            _history.append((x, y))
        else:
            x, y, degree = turn_and_move(x, y, degree, res)
            res, prog = (
                prog
                .set_input(coordinates[x][y])
                .calculate())
            if res is None:
                break
        should_paint = not should_paint

    return _history, coordinates


def render_painting(coordinates, width, height):
    out = np.full((height, width, 3), [0, 0, 0], dtype=np.uint8)

    # Layers are rendered with the first in front, last in back
    # so we'll iterate through them back-to-front here
    for col_idx, col in enumerate(coordinates):
        for row_idx, val in enumerate(col):
            if val == 0:
                out[row_idx, col_idx] = [0, 0, 0]
            if val == 1:
                out[row_idx, col_idx] = [255, 255, 255]
    img = Image.fromarray(out, 'RGB')
    img.save('decoded.png')

    return True


def main():
    instructions = load_instructions()
    height = 100
    width = 100
    history, coordinates = paint(0, instructions, height, width)
    print(f'Painted {len(set(history))} tiles n >= 1 times')

    history, coordinates = paint(1, instructions, height, width)
    render_painting(coordinates, height, width)

if __name__ == '__main__':
    main()
