import os
from typing import List, Tuple


def load_input(test: bool=False) -> List[int]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = f.read()
        return [int(elem) for elem in list(input)]


def expand_filemap(dense_filemap: List[int]) -> List[int]:
    expanded_filemap = []

    # Even indices are file blocks; odd are free blocks
    for idx, elem in enumerate(dense_filemap):
        if idx % 2 == 0:
            expanded_filemap += [idx // 2] * elem
        else:
            expanded_filemap += [None] * elem
    return expanded_filemap


def defrag_blockwise(expanded_filemap: List[int], debug: bool=False) -> List[int]:
    defragged = [elem for elem in expanded_filemap]

    if debug:
        print(defragged)
    for idx, elem in enumerate(defragged[::-1]):
        _idx = len(defragged) - (1 + idx)
        if not elem:
            continue
        _next_free_block = defragged.index(None)
        if _next_free_block < _idx:
            defragged[_idx] = None
            defragged[_next_free_block] = elem
        
        if debug:
            print(defragged)
    return defragged


def defrag_filewise(expanded_filemap: List[int], debug: bool=False) -> List[int]:
    defragged = [elem for elem in expanded_filemap]

    if debug:
        print(defragged)
    
    _prior = None
    for idx, elem in enumerate(defragged[::-1]):
        if elem is None:
            continue
        if elem == _prior:
            continue

        end_idx = len(defragged) - idx
        start_idx = len(defragged) - idx

        while defragged[start_idx - 1] == elem:
            start_idx -= 1

        file_len = (end_idx - start_idx)
        empty_start_idx, empty_len = None, 1

        for block in range(0, start_idx):
            if defragged[block] is not None:
                continue
            empty_start_idx = block
            empty_end_idx = block
            while defragged[empty_end_idx] is None and empty_end_idx <= start_idx:
                empty_end_idx += 1

            empty_len = (empty_end_idx - empty_start_idx)
            if empty_len >= file_len:
                defragged[empty_start_idx:(empty_start_idx + file_len)] = defragged[start_idx:end_idx]
                defragged[start_idx:end_idx] = [None] * file_len

                empty_start_idx, empty_len = None, 1

                break
        _prior = elem

        if debug:
            print(defragged, elem, _prior)
    return defragged


def get_checksum(defragged_filemap: List[int]) -> int:
    checksum = 0
    for idx, elem in enumerate(defragged_filemap):
        checksum += idx * elem if elem else 0
    return checksum


if __name__ == '__main__':
    dense_filemap = load_input(test=False)
    expanded_filemap = expand_filemap(dense_filemap)
    defragged = defrag_blockwise(expanded_filemap)
    print(get_checksum(defragged))

    defragged = defrag_filewise(expanded_filemap, debug=False)
    print(get_checksum(defragged))
