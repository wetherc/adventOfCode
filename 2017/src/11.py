import argparse
from re import sub

parser = argparse.ArgumentParser(description='Register instructions')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_file(input):
    with open(input) as file:
        return file.readline().rstrip()

def sum_steps(path, direction):
    steps = sum(1 for elem in path if elem == direction)
    return steps

def cancel_steps(dir1, dir2):
    canceled = min(steps[dir1], steps[dir2])
    steps[dir1] -= canceled
    steps[dir2] -= canceled

    return canceled

if __name__ == '__main__':
    path = read_file(args.input)
    path = path.split(',')

    #steps = {
    #    'n': sum_steps(path, 'n'),
    #    'ne': sum_steps(path, 'ne'),
    #    'se': sum_steps(path, 'se'),
    #    's': sum_steps(path, 's'),
    #    'sw': sum_steps(path, 'sw'),
    #    'nw': sum_steps(path, 'nw')
    #}

    steps = {
        'n': 0,
        'ne': 0,
        'se': 0,
        's': 0,
        'sw': 0,
        'nw': 0
    }

    #done = False
    max_steps = 0
    final_steps = 0
    #while not done:
    for elem in path:
        length = sum(steps.values())

        steps[elem] += 1
        cancel_steps('n', 's')
        cancel_steps('sw', 'ne')
        cancel_steps('se', 'nw')

        steps['n'] += cancel_steps('ne', 'nw')
        steps['ne'] += cancel_steps('se', 'n')
        steps['se'] += cancel_steps('ne', 's')
        steps['s'] += cancel_steps('se', 'sw')
        steps['sw'] += cancel_steps('s', 'nw')
        steps['nw'] += cancel_steps('n', 'sw')

        max_steps = max(max_steps, sum(steps.values()))
        if length == sum(steps.values()):
            final_steps = length
            #done = True

    # Should be 1560 & 773
    print('Max distance: {}; Final distance: {}'.format(
        max_steps, final_steps))
