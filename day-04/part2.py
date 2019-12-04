def load_input():
    with open('./input.txt', 'r') as f:
        input = f.read().strip().split('-')

    input = [int(x) for x in input]
    return input


def check_len(guess):
    if len(repr(guess)) == 6:
        return True
    return False


def check_range(guess, input):
    if input[0] <= guess <= input[1]:
        return True
    return False


def check_adjacency(guess):
    digits = [digit for digit in repr(guess)]
    for idx in range(len(digits) - 1):
        if digits[idx] == digits[idx + 1]:
            if idx >= 1:
                if digits[idx] == digits[idx - 1]:
                    continue
            if idx + 2 < len(digits):
                if digits[idx] == digits[idx + 2]:
                    continue
            return True
    return False


def check_monotonicity(guess):
    digits = [int(digit) for digit in repr(guess)]
    sorted = [int(digit) for digit in repr(guess)]
    sorted.sort()
    if digits == sorted:
        return True
    return False


def main():
    input = load_input()
    possible_passwords = []
    for guess in range(input[0], input[1]):
        if (
            check_len(guess) &
            check_range(guess, input) &
            check_adjacency(guess) &
            check_monotonicity(guess)
        ):
            possible_passwords.append(guess)
    print('Possible valid passwords:\t{}'.format(len(possible_passwords)))


if __name__ == '__main__':
    main()
