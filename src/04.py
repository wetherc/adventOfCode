import argparse

parser = argparse.ArgumentParser(description='Compute a checksum')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_input(input):
    with open(input, 'r') as passphrases:
        for passphrase in passphrases:
            yield str.split(passphrase)


def words_are_unique(passphrase):
    if len(passphrase) == len(set(passphrase)):
        return True
    else:
        return False


def anagrams_are_unique(passphrase):
    passphrase = [''.join(sorted(word)) for word in passphrase]
    if len(passphrase) == len(set(passphrase)):
        return True
    else:
        return False


if __name__ == '__main__':
    if args.part == '1':
        output = sum(map(words_are_unique, read_input(args.input)))
    else:
        output = sum(map(anagrams_are_unique, read_input(args.input)))
    print(output)
