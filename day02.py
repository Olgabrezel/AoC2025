def get_ranges(task_input: str):
    ranges = task_input.split(',')
    return [(int(x.split('-')[0]), int(x.split('-')[1])) for x in ranges]


def part1(task_input: str):
    result = 0
    ranges = get_ranges(task_input)
    for (start, stop) in ranges:
        for j in range(start, stop+1):
            strj = str(j)
            if len(strj) % 2 == 0 and strj[len(strj)//2:] == strj[:len(strj)//2]:
                result += j
    return result


def part2(task_input: str):
    invalids = set()
    ranges = get_ranges(task_input)
    for (start, stop) in ranges:
        for j in range(start, stop+1):
            strj = str(j)
            for k in range(1, len(strj)//2 + 1):
                if len(strj) % k == 0:
                    for part in range(len(strj) // k - 1):
                        if strj[part*k:(part+1)*k] != strj[(part+1)*k:(part+2)*k]:
                            break
                    else:
                        invalids.add(j)
    return sum(invalids)
