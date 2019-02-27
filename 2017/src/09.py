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
    
    remaining_char_count = len(garbage)
    removed_char_count = 0

    garbage = sub(r'<([^>]*)>', r'<>', garbage)
    removed_char_count += remaining_char_count - len(garbage)
    remaining_char_count = len(garbage)

    #garbage = sub(r'},}', r'}}', garbage)
    #garbage = sub(r'}{', r'},{', garbage)
    #garbage = sub(r'{,', r'{', garbage)

    garbage = sub(r',', '', garbage)

    prev = 0
    total = 0
    for elem in garbage:
        if elem == '{':
            prev += 1
            total += prev
        elif elem == '}':
            prev -= 1
        else:
            pass

    print("Score: {}; Removed: {}".format(total, removed_char_count))
