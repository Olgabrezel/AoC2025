def part1(task_input: str):
    grid = [list(row) for row in task_input.split('\n')]
    result = 0

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '@':
                adjacent_occupied = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if ((dx != 0) or (dy != 0)) and (0 <= y+dy < len(grid)) and (0 <= x+dx < len(row)):
                            if grid[y+dy][x+dx] == '@':
                                adjacent_occupied += 1
                if adjacent_occupied < 4:
                    result += 1
    return result


def part2(task_input: str):
    grid = [list(row) for row in task_input.split('\n')]
    result = 0
    newly_removed = 1

    while newly_removed > 0:
        newly_removed = 0
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == '@':
                    adjacent_occupied = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if ((dx != 0) or (dy != 0)) and (0 <= y+dy < len(grid)) and (0 <= x+dx < len(row)):
                                if grid[y+dy][x+dx] == '@':
                                    adjacent_occupied += 1
                    if adjacent_occupied < 4:
                        newly_removed += 1
                        grid[y][x] = 'x'
        result += newly_removed
    return result
