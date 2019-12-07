import itertools
import copy


def load_instructions():
    instructions = []
    with open('./input.txt', 'r') as f:
        for line in f:
            instructions += [int(val.strip()) for val in line.split(',')]
    return instructions


class IntCode:
    def __init__(self, instructions):
        self.offset = 0
        self.instructions = [val for val in instructions]
        self.inputs = []

    def set_input(self, input):
        self.inputs.append(input)
        return self

    def get_offset(self, opcode):
        if opcode in [1, 2, 7, 8]:
            return 4
        elif opcode in [5, 6]:
            return 3
        elif opcode in [3, 4]:
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
                if mode == 0:
                    positions.append(self.instructions[self.offset + _idx + 1])
                else:
                    positions.append(self.offset + _idx + 1)

            if opcode == 1:
                self.instructions[positions[2]] = (
                    self.instructions[positions[1]] + \
                    self.instructions[positions[0]])
                self.offset += _offset
            elif opcode == 2:
                self.instructions[positions[2]] = (
                    self.instructions[positions[1]] * \
                    self.instructions[positions[0]])
                self.offset += _offset
            elif opcode == 3:
                self.instructions[positions[0]] = self.inputs.pop(0)
                self.offset += _offset
            elif opcode == 4:
                self.offset += _offset
                return self.instructions[positions[0]]
            elif opcode == 5:
                if self.instructions[positions[0]] != 0:
                    self.offset = self.instructions[positions[1]]
                else:
                    self.offset += _offset
            elif opcode == 6:
                if self.instructions[positions[0]] == 0:
                    self.offset = self.instructions[positions[1]]
                else:
                    self.offset += _offset
            elif opcode == 7:
                if self.instructions[positions[0]] < self.instructions[positions[1]]:
                    self.instructions[positions[2]] = 1
                else:
                    self.instructions[positions[2]] = 0
                self.offset += _offset
            elif opcode == 8:
                if self.instructions[positions[0]] == self.instructions[positions[1]]:
                    self.instructions[positions[2]] = 1
                else:
                    self.instructions[positions[2]] = 0
                self.offset += _offset
            elif opcode == 99:
                return None
            else:
                raise Exception(
                    f'Unknown instruction ({opcode}) at offset {self.offset}')
        return None


def main():
    instructions = load_instructions()
    max_output = 0
    for sequence in itertools.permutations(range(5, 10), 5):
        res = 0
        amp_array = [
            IntCode(instructions).set_input(phase)
            for phase in sequence]
        while res is not None:
            for amplifier in amp_array:
                amp_input = res
                res = amplifier.set_input(amp_input).calculate()
                if not res:
                    break
        max_output = max(max_output, amp_input)
    print(f'Max amplifier signal achieved: {max_output}')


if __name__ == '__main__':
    main()
