from functools import cache


def parse_input(task_input: str):
    return {x.split(': ')[0]: x.split(': ')[1].split(' ') for x in task_input.split('\n')}


def dfs_part1(conns, start):
    if start == 'out':
        return 1

    ways = 0
    for c in conns[start]:
        ways += dfs_part1(conns, c)
    return ways


def part1(task_input: str):
    return
    conns = parse_input(task_input)
    return dfs_part1(conns, 'you')


def dfs_part2(conns, start, has_dac, has_fft):
    @cache
    def inner(start, has_dac, has_fft):
        if start == 'out':
            if has_dac and has_fft:
                return 1
            else:
                return 0

        ways = 0
        if start == 'dac':
            has_dac = True
        if start == 'fft':
            has_fft = True

        for c in conns[start]:
            ways += inner(c, has_dac, has_fft)
        return ways

    return inner(start, has_dac, has_fft)


def part2(task_input: str):
    conns = parse_input(task_input)
    return dfs_part2(conns, 'svr', False, False)
