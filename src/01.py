import argparse

parser = argparse.ArgumentParser(description='Solve a Captcha')
parser.add_argument('--input')
parser.add_argument('--type')
args = parser.parse_args()


def solve_captcha(input, type):
    input = list(str(input))

    if type == 'halfway':
        output = sum(int(val) for idx, val in enumerate(input)
                     if input[idx] == input[int(idx + (len(input) / 2)) % len(input)])
    else:
        output = sum(int(val) for idx, val in enumerate(input)
                     if input[idx] == input[(idx + 1) % len(input)])
    return output

if __name__ == '__main__':
    print(solve_captcha(input=args.input, type=args.type))
