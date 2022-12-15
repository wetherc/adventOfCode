import os
import re


class Monkey(object):
    def __init__(self, raw_input: list[list[str]]):
        self.id = int(re.findall(r'\d+', raw_input[0][0])[0])
        self.items = self.parse_item_list(raw_input[1])
        self.operation = self.parse_operation(raw_input[2])
        self.test = self.parse_test(raw_input[3:])
        self.items_inspected = 0
    
    def parse_item_list(self, raw_items: list[str]) -> list[int]:
        items = [
            int(item) for item in raw_items[1].split(', ')
        ]
        return items
    
    def parse_operation(self, raw_operation: list[str]) -> tuple[str, str]:
        operation = re.findall(r'[\+\-\*/]', raw_operation[1])[0]
        try:
            operand = re.findall(r'\d+', raw_operation[1])[0]
        except IndexError:
            operand = re.findall(r'old', raw_operation[1])[1]
        return (operation, operand)

    def parse_test(self, raw_test: list[list[str]]):
        test = {
            'Test': int(re.findall(r'\d+', raw_test[0][1])[0]),
            'True': int(re.findall(r'\d+', raw_test[1][1])[0]),
            'False': int(re.findall(r'\d+', raw_test[2][1])[0])
        }
        return test


def parse_input() -> list[list[str]]:
    parsed_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parsed_input.append(line.strip().split(':'))
    return parsed_input


def eval_operation(item: int, operation: tuple[str, str]):
    # I'm in danger :-)
    _expr = f'{item} {operation[0]} {operation[1] if operation[1].isdigit() else item}'
    return eval(_expr)


def update_item_worry_levels(monkey: Monkey, floor_div: bool = True) -> Monkey:
    for idx, item in enumerate(monkey.items):
        _item = eval_operation(item, monkey.operation)
        if floor_div:
            _item = _item // 3
        monkey.items[idx] = _item
    monkey.items_inspected += len(monkey.items)
    return monkey


def yeet_shit(monkey: Monkey) -> list[int]:
    item_destinations = [
        monkey.test[repr(item % monkey.test['Test'] == 0)]
        for item in monkey.items
    ]
    return item_destinations


def simulate(parsed_input, n_rounds: int = 20, floor_div: bool = True) -> None :
    monkeys = [
        Monkey(parsed_input[idx:(idx + 6)])
        for idx in range(0, len(parsed_input), 6)
    ]
    
    for _ in range(n_rounds):
        for monkey in monkeys:
            monkey = update_item_worry_levels(monkey, floor_div)
            item_destinations = yeet_shit(monkey)
            for destination in item_destinations:
                _item = monkey.items.pop(0)
                monkeys[destination].items.append(_item)
    
    for monkey in monkeys:
        print(f'Monkey {monkey.id} inspected items {monkey.items_inspected} times')
    
    monkey_business = [monkey.items_inspected for monkey in monkeys]
    monkey_business.sort(reverse=True)
    print(f'The level of monkey business is {monkey_business[0] * monkey_business[1]}')
    return None


def main():
    parsed_input = parse_input()
    simulate(parsed_input)

    # who needs efficiency when you have brute force?
    # simulate(parsed_input, 10000, False)
    

if __name__ == '__main__':
    main()
    