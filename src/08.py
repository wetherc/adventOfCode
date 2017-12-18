import argparse
from re import sub

parser = argparse.ArgumentParser(description='Register instructions')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_instructions(input):
    with open(input) as instructions:
        for instruction in instructions:
            yield str.split(instruction)


def evaluate_condition(input, operator, condition):
    if input is None:
        return False

    if operator == '==':
        return input == condition
    elif operator == '!=':
        return input != condition
    elif operator == '<':
        return input < condition
    elif operator == '>':
        return input > condition
    elif operator == '<=':
        return input <= condition
    elif operator == '>=':
        return input >= condition
    else:
        return False


def get_register_operation(register, operation, value):
    if operation == 'dec':
        return register - value
    elif operation == 'inc':
        return register + value
    else:
        pass


if __name__ == '__main__':
    instructions = read_instructions(args.input)

    registers = {}
    for instruction in instructions:
        if registers.get(instruction[4]) is None:
            registers[instruction[4]] = 0
        if registers.get(instruction[0]) is None:
             registers[instruction[0]] = 0

        if evaluate_condition(input=registers.get(instruction[4]),
                              operator=instruction[5],
                              condition=int(instruction[6])) == True:
            registers[instruction[0]] = get_register_operation(
                register=registers.get(instruction[0]),
                operation=instruction[1],
                value=int(instruction[2]))
    output = max(registers, key=registers.get)
    output = (output, registers[output])

    print(output)
