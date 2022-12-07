import os


def parse_input() -> str:
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        parsed_input = f.readlines()
    return parsed_input


def hydrate_directories(bash_history):
    directory_sizes = {}

    pwd = []
    for line in bash_history:
        if '$' in line:
            cmd = line.split()
            if cmd[1] == 'cd':
                if cmd[2] == '..':
                    pwd.pop(-1)
                else:
                    pwd.append(cmd[2])
            elif cmd[1] == 'ls':
                pass
            else:
                print('You Died')
                break
        else:
            output = line.split()
            if output[0].isdigit():
                for idx, _ in enumerate(pwd):
                    _dirname = '/'.join(pwd[:(idx + 1)])
                    directory_sizes[_dirname] = (
                        directory_sizes.get(_dirname, 0) +
                        int(output[0])
                    )
    return directory_sizes


def main():
    parsed_input = parse_input()
    dir_sizes = hydrate_directories(parsed_input)
    small_dir_sums = sum([
        val for val in dir_sizes.values()
        if val <= 100000])
    print(f'The sum of all small directories is {small_dir_sums}')

    _used_space = dir_sizes['/']
    _total_space = 70000000
    _min_free_space = 30000000
    _smallest_dir = min([
        val for val in dir_sizes.values()
        if _total_space - _used_space + val >= _min_free_space
    ])
    print(
        'The size of the smallest directory we can delete '
        f'is {_smallest_dir}')



if __name__ == '__main__':
    main()
    