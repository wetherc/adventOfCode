import argparse
from re import sub

parser = argparse.ArgumentParser(description='Register instructions')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_garbage(input):
    with open(input) as garbage:
        return garbage.readline()

if __name__ == '__main__':
    garbage = read_garbage(args.input)
    garbage = sub(r'![\S]', r'', garbage)
    garbage = sub(r'<([^>]*)>', r'', garbage)
    garbage = sub(r'},}', r'}}', garbage)
    garbage = sub(r'}{', r'},{', garbage)
    garbage = sub(r'{,', r'{', garbage)

    garbage = sub(r',', '', garbage)

    prev = 0
    total = 0
    for elem in garbage:
        if elem == '{':
            prev += 1
            total += prev
        else:
            prev -= 1

    print(total)
