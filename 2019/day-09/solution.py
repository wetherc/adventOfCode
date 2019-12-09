import itertools
import copy
import sys
import logging


TAB = '\t'
logger = logging.getLogger(__name__)
logging.basicConfig(
        stream=sys.stdout,
        level=logging.WARNING)


def load_instructions():
    instructions = []
    with open('./input.txt', 'r') as f:
        for line in f:
            instructions += [int(val.strip()) for val in line.split(',')]
    instruction_dict = dict((idx, val) for idx, val in enumerate(instructions))
    return instruction_dict


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

            logger.debug(f'Running opcode {opcode} with modes {modes}')
            # z = x + y
            if opcode == 1:
                self.instructions[positions[2]] = (
                    self.instructions[positions[1]] + \
                    self.instructions[positions[0]])
                logger.debug(
                    f'{TAB}Setting index {positions[2]} to '
                    f'{self.instructions[positions[1]]} + '
                    f'{self.instructions[positions[0]]}'
                )
                self.offset += _offset
            # z = x * y
            elif opcode == 2:
                self.instructions[positions[2]] = (
                    self.instructions[positions[1]] * \
                    self.instructions[positions[0]])
                logger.debug(
                    f'{TAB}Setting index {positions[2]} to '
                    f'{self.instructions[positions[1]]} * '
                    f'{self.instructions[positions[0]]}'
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
                return self.instructions[positions[0]]
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
                return None
            else:
                raise Exception(
                    f'Unknown instruction ({opcode}) at offset {self.offset}')
        return None


def main():
    instructions = load_instructions()
    print(f'Running BOOST in test mode...')
    prog = IntCode(instructions).set_input(1).calculate()
    print(f'{TAB}Test BOOST keycode produced: {prog}')

    print(f'Running BOOST in production mode...')
    prog = IntCode(instructions).set_input(2).calculate()
    print(f'{TAB}BOOST keycode produced: {prog}')


if __name__ == '__main__':
    main()
