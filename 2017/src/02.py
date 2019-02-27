import argparse
import csv

parser = argparse.ArgumentParser(description='Compute a checksum')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_spreadsheet(input):
    with open(input) as tsv:
        for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONNUMERIC):
            yield line


def calculate_checksum(input):
    output = sum(map(lambda x: int(max(x) - min(x)), read_spreadsheet(input)))
    return output


def get_quotient(input):
    denominators = sorted(input)
    numerators = denominators[::-1]
    
    for numerator in numerators:
        for denominator in denominators:
            if (numerator % denominator == 0) and (numerator != denominator):
                return int(numerator / denominator)


if __name__ == '__main__':
    if args.part == '1':
        print(calculate_checksum(args.input))
    else:
        print(sum(map(get_quotient, read_spreadsheet(args.input))))
