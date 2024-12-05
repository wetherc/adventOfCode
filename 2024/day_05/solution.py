import os
from typing import List, Tuple


def load_input(test: bool=False) -> List[List[str]]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        ordering, updates = f.read().split('\n\n')

    ordering = [line.split('|') for line in ordering.split('\n')]
    updates = [update.split(',') for update in updates.split('\n')]
    return ordering, updates


def get_page_order_correctness(rules, updates) -> List[bool]:
    correctness_bool = []
    for update in updates:
        correctness_bool.append(
            all([
                set(update[0:idx]).intersection(
                    rules.get(page, set([]))
                ) == set()
                for idx, page in enumerate(update)
            ])
        )
    return correctness_bool


def get_median_val(array: List[str]) -> int:
    median_val = int(array[len(array) // 2])
    return median_val


def reorder_pages(pages, rules) -> List[str]:
    ordered_pages = []
    for page in pages:
        _conflicts = [
            idx for idx, o_page in enumerate(ordered_pages)
            if o_page in rules.get(page, [])
        ]
        if not _conflicts:
            ordered_pages.append(page)
        else:
            ordered_pages.insert(_conflicts[0], page)
    return ordered_pages


if __name__ == '__main__':
    ordering, updates = load_input(test=False)
    ordering_dict = {}

    for elem in ordering:
        ordering_dict[elem[0]] = [elem[1]] + ordering_dict.get(elem[0], [])
        reversed_dict[elem[1]] = [elem[0]] + ordering_dict.get(elem[1], [])
    
    ordering_dict = dict(
        zip(ordering_dict.keys(), map(set, ordering_dict.values()))
    )

    correctness_bools = get_page_order_correctness(ordering_dict, updates)
    median_vals = [
        get_median_val(update)
        for idx, update in zip(correctness_bools, updates) if idx
    ]
    print(sum(median_vals))

    reordered_updates = [
        reorder_pages(update, ordering_dict)
        for idx, update in zip(correctness_bools, updates) if not idx
    ]
    median_vals = [
        get_median_val(update)
        for update in reordered_updates
    ]
    print(sum(median_vals))
