def part1(task_input: str):
    lines = task_input.split('\n')
    dial = 50
    result = 0

    for line in lines:
        op = line[0]
        val = int(line[1:])
        if op == 'R':
            dial = (dial + val) % 100
        else:
            dial = (dial - val) % 100

        if dial == 0:
            result += 1

    return result


def part2(task_input: str):
    lines = task_input.split('\n')
    dial = 50
    result = 0

    for line in lines:
        op = line[0]
        val = int(line[1:])
        if op == 'R':
            for i in range(val):
                dial = (dial + 1) % 100
                if dial == 0:
                    result += 1
        else:
            for i in range(val):
                dial = (dial - 1) % 100
                if dial == 0:
                    result += 1

    return result
