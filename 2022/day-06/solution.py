import os


def parse_input():
    parsed_input = {
        'stacks': [],
        'instructions': []
    }
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        parsed_input = f.readline().strip()
    return parsed_input


def find_start_marker(signal, buff_size=4):
    for idx, _ in enumerate(signal):
        buffer = signal[idx:(idx + buff_size)]
        
        if len(buffer) == len(set(buffer)):
            return (idx, buffer)
    return None



def main():
    parsed_input = parse_input()
    start_index, _ = find_start_marker(parsed_input)
    print(f'Start marker was detected after {start_index + 4}')

    message_start_index, _ = find_start_marker(parsed_input, 14)
    print(f'Start marker was detected after {message_start_index + 14}')


if __name__ == '__main__':
    main()