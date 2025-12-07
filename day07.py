from collections import defaultdict


def part1(task_input: str):
    grid = [list(row) for row in task_input.split('\n')]
    beams = {grid[0].index('S')}
    splits = 0

    for y in range(1, len(grid)):
        new_beams = set()
        for b in beams:
            if grid[y][b] == '.':
                new_beams.add(b)
            elif grid[y][b] == '^':
                new_beams.add(b-1)
                new_beams.add(b+1)
                splits += 1
        beams = new_beams
    return splits


def part2(task_input: str):
    grid = [list(row) for row in task_input.split('\n')]
    beams = {grid[0].index('S'): 1}

    for y in range(1, len(grid)):
        new_beams = defaultdict(lambda: 0)
        for b in beams:
            if grid[y][b] == '.':
                new_beams[b] += beams[b]
            elif grid[y][b] == '^':
                new_beams[b-1] += beams[b]
                new_beams[b+1] += beams[b]
        beams = new_beams

    return sum(beams.values())
