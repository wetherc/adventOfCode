import argparse
from re import search

parser = argparse.ArgumentParser(description='Find cyclic singly-linked lists')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()

def read_programs(input):
    with open(input) as programs:
        for program in programs:
            yield program

def parse_programs(input):
    
    return program

    
if __name__ == '__main__':
    programs = read_programs(args.input)
    programs = parse_program(programs)
    output = find_loop(next(instructions), args.part)
    print(output)
