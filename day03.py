def get_banks(task_input: str):
    banks = task_input.split('\n')
    return [[int(x) for x in bank] for bank in banks]


def part1(task_input: str):
    banks = get_banks(task_input)
    result = 0

    for bank in banks:
        first_digit = max(bank[:-1])
        second_digit = max(bank[bank.index(first_digit)+1:])
        joltage = 10 * first_digit + second_digit
        result += joltage
    return result


def part2(task_input: str):
    banks = get_banks(task_input)
    result = 0

    for bank in banks:
        joltage = 0
        index = 0
        for k in range(11, -1, -1):
            if k > 0:
                battery = max(bank[index:-k])
            else:
                battery = max(bank[index:])
            joltage *= 10
            joltage += battery
            index = bank.index(battery, index) + 1
        result += joltage
    return result
