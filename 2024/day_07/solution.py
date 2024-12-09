import os
import operator
from typing import List, Dict, Tuple


def load_input(test: bool=False) -> Tuple[List[int], List[int]]:
    filename = 'input' if not test else 'sample'
    with open(
        os.path.dirname(os.path.abspath(__file__)) + f'/{filename}.txt',
        'r'
    ) as f:
        input = f.read().splitlines()

        solutions = []
        operands = []
        for line in input:
            lhs, rhs = line.split(': ')
            operands.append([elem for elem in map(int, rhs.split(' '))])
            solutions.append(int(lhs))
        return solutions, operands


def solve_equation(_equation: List[int], concat: bool=False) -> List[int]:
    _solutions = []

    _operand = _equation.pop()
    if len(_equation) == 0:
        return [_operand]
    
    _solutions += [
        operator.mul(
            _operand,
            elem
        ) for elem in solve_equation([elem for elem in _equation], concat=concat)
    ]
    _solutions += [
        operator.add(
            _operand,
            elem
        ) for elem in solve_equation([elem for elem in _equation], concat=concat)
    ]
    if concat:
        _solutions += [
            int(
                operator.concat(
                    str(elem),
                    str(_operand)
                )
            ) for elem in solve_equation([elem for elem in _equation], concat=concat)
        ]
    
    return _solutions


if __name__ == '__main__':
    solutions, operands = load_input(test=False)
    possible_solutions = [solve_equation(equation) for equation in operands]
    valid_solutions = [
        idx for idx, solution in zip(solutions, possible_solutions)
        if idx in solution
    ]

    print(sum(valid_solutions))

    solutions, operands = load_input(test=False)
    possible_solutions = [solve_equation(equation, concat=True) for equation in operands]
    valid_solutions = [
        idx for idx, solution in zip(solutions, possible_solutions)
        if idx in solution
    ]
    print(sum(valid_solutions))
