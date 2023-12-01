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


def parse_numbers(input, strings=False) -> list[list[str]]:
    r = '1|2|3|4|5|6|7|8|9'
    if strings:
        r += '|one|two|three|four|five|six|seven|eight|nine'

    numeric_input = []
    for line in input:
        numeric_input.append([
            *map({n: str(i%9+1) for i, n in enumerate(r.split('|'))}.get,
            re.findall(rf'(?=({r}))', line))
        ])

    return numeric_input


def sum_inputs(calibrations) -> int:
    return sum([
        int(f'{elem[0]}{elem[-1]}') for elem in calibrations
    ])


if __name__ == '__main__':
    inputs = load_input()
    inputs_numeric = parse_numbers(inputs)
    inputs_why_though = parse_numbers(inputs, strings=True)
    print(f'The sum of calibration values is {sum_inputs(inputs_numeric)}')
    print(f'The updated sum of calibration values is {sum_inputs(inputs_why_though)}')
