from functools import reduce


def compute_grand_total(problems):
    result = 0
    for numbers, operation in problems:
        if operation == '+':
            result += reduce(lambda x, y: x+y, numbers, 0)
        elif operation == '*':
            result += reduce(lambda x, y: x*y, numbers, 1)
    return result


def part1(task_input: str):
    problem_rows = task_input.split('\n')
    numbers = []

    for row in problem_rows[:-1]:
        fields = [x.strip() for x in row.split(' ') if x.strip()]
        if numbers == []:
            numbers = [[] for _ in range(len(fields))]
        for i, entry in enumerate(fields):
            numbers[i].append(int(entry))

    final_row = problem_rows[-1]
    operations = [x.strip() for x in final_row.split(' ') if x.strip()]
    problems = list(zip(numbers, operations))

    return compute_grand_total(problems)


def part2(task_input: str):
    problem_chars = [list(row) for row in task_input.split('\n')]
    problems = []

    problem = []
    operator = ''

    for x in range(len(problem_chars[0])-1, -1, -1):
        num = 0
        for y in range(len(problem_chars)):
            c = problem_chars[y][x]
            if c == ' ':
                continue
            elif c in ('+', '*'):
                operator = c
            else:
                num *= 10
                num += int(c)

        if num != 0:
            problem.append(num)

        if operator != '':  # we found the left-aligned + or *, so this problem is parsed completely
            problems.append((problem, operator))
            problem = []
            operator = ''

    return compute_grand_total(problems)
