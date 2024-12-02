import os
import copy
from typing import List


def load_input(test: bool=False) -> List[List[int]]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = [list(map(int, line.split())) for line in f.read().splitlines()]
    return input


def _check_asc(report: List[int]) -> List[bool]:
    return [report[i] < report[i + 1] for i in range(len(report) - 1)]


def _check_desc(report: List[int]) -> List[bool]:
    return [report[i] > report[i + 1] for i in range(len(report) - 1)]


def _check_gaps(report: List[int]) -> List[bool]:
    return [0 < abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1)]


def get_report_safety(input: List[List[int]]) -> List[bool]:
    out = []
    for report in input:
        out.append(
            (
                all(_check_asc(report)) or
                all(_check_desc(report))
            ) and (
                all(_check_gaps(report))
            )
        )
    return out


def get_report_dampened_safety(input: List[List[int]]) -> List[bool]:
    out = []
    for report in input:
        valid = False
        for idx in range(len(report)):
            _report = copy.deepcopy(report)
            _report.pop(idx)
            valid = max(
                valid,
                (
                    all(_check_asc(_report)) or
                    all(_check_desc(_report))
                ) and all(_check_gaps(_report))
            )
        out.append(valid)

    return out


if __name__ == '__main__':
    input = load_input(test=False)

    print(sum(get_report_safety(input)))
    print(sum(get_report_dampened_safety(input)))
