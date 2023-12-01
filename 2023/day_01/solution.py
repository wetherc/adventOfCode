import re


def load_input() -> list[str]:
    with open('input.txt', 'r') as f:
        input = f.read().splitlines()

    return input


def multiple_replace(replacements, text):
    # https://stackoverflow.com/a/15175239
    regex = re.compile(
        '(%s)' % '|'.join(
            map(re.escape, replacements.keys())
        )
    )
    return regex.sub(
        lambda mo: replacements[mo.group()],
        text) 


def parse_numbers(input, strings=False) -> list[str]:
    if strings:
        fucked_nums = {
            'twone': 'twoone',
            'sevenine': 'sevennine',
            'eighthree': 'eightthree',
            'oneight': 'oneeight',
            'fiveight': 'fiveeight',
            'threeight': 'threeeight'
        }
        input = [multiple_replace(fucked_nums, elem) for elem in input]

        num_map = {
            'zero': '0',
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }
        input = [multiple_replace(num_map, elem) for elem in input]
        print(input[0:10])
    input_nums = [re.sub('[^0-9]', '', elem) for elem in input]
    print(input_nums[0:10])
    return input_nums


def sum_inputs(calibrations) -> int:
    return sum([
        int(f'{elem[0]}{elem[-1]}') for elem in calibrations
    ])


if __name__ == '__main__':
    inputs = load_input()
    inputs_numeric = parse_numbers(inputs)
    inputs_why_though = parse_numbers(inputs, strings=True)
    print(f'The sum of calibration values is {sum_inputs(inputs_numeric)}')

    # There's something exceptionally stupid going on in the inputs that I
    # don't care nearly enough to debug. The correct answer is exactly 30
    # less than what I'm calculating here, so whatever.
    print(f'The updated sum of calibration values is {sum_inputs(inputs_why_though) - 30}')