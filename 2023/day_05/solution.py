import os
from functools import reduce


def load_input():
    input_map = []
    seeds = []

    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r'
    ) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if 'seeds' in line:
                seeds = [
                    int(val)
                    for val in line.split()
                    if val != 'seeds:'
                ]

            elif ':' in line:
                input_map.append([])
            else:
                _map_vals = [int(val) for val in line.split()]
                input_map[-1].append({
                    'dst': _map_vals[0],
                    'src': _map_vals[1],
                    'range': _map_vals[2]
                })

    return seeds, input_map


def calculate_locations(seed, input_map):
    val = seed
    for _step in range(len(input_map)):
        try:
            val = [
                next_val['dst'] + (val - next_val['src'])
                for next_val in input_map[_step]
                if next_val['src'] <= val < next_val['src'] + next_val['range']
            ][0]
        except IndexError:
            pass
    return val


def kill_my_cpu(seed_range):
    _locations = []
    print(
            f'Chugging through {seed_range[1] - seed_range[0]} seeds'
        )
    for seed in range(seed_range[0], seed_range[1]):
        _locations.append(calculate_locations(seed, input_map))
    return _locations


def calculate_locations_big_brain(seeds, input_map):
    for start, seed_range in seeds:
        while seed_range > 0:
            for _step in input_map:
                _len = _step['range']
                _delta = start - _step['src']
                if _delta in range(_len):
                    _len = min(
                        _len - _delta,
                        seed_range
                    )
                    yield (_step['dst'] + _delta, _len)
                    start += _len
                    seed_range -= _len
                    break
            else:
                yield (start, seed_range)
                break


if __name__ == '__main__':
    seeds, input_map = load_input()

    locations = []
    for seed in seeds:
        locations.append(calculate_locations(seed, input_map))
    print(min(locations))

    # lol what even is computational complexity
    # 
    # seriously tho, don't ever be as stupid as me
    # this ain't going to finish running before the heat
    # death of the universe. Let's try something less
    # silly instead...
    # 
    # _seed_pairs = len(seeds) // 2
    # seed_ranges = []
    # for pair in range(_seed_pairs):
    #     seed_ranges.append(
    #         (seeds[pair * 2], seeds[pair * 2] + seeds[pair * 2 + 1])
    #     )
    # 
    # from multiprocessing import Pool
    # with Pool(12) as p:
    #     locations = p.map(
    #         kill_my_cpu,
    #         seed_ranges
    #     )
    
    # this is still wrong, but now my brain is also broken so I'm
    # just going to leave this alone and go cry in a corner
    print(
        min(
            reduce(
                calculate_locations_big_brain,
                input_map,
                zip(seeds[0::2], seeds[1::2])
            )
        )[0]
    )