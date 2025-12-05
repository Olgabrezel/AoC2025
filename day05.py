def parse_input(task_input: str):
    ranges, ingredients = task_input.split('\n\n')
    ranges = [(int(r.split('-')[0]), int(r.split('-')[1])) for r in ranges.split('\n')]
    ingredients = [int(x) for x in ingredients.split('\n')]
    return ranges, ingredients


def part1(task_input: str):
    ranges, ingredients = parse_input(task_input)
    return len({ing
                for ing in ingredients
                for r_min, r_max in ranges
                if r_min <= ing <= r_max})


def part2(task_input: str):
    ranges, _ = parse_input(task_input)

    # Merge ranges until there are no more overlaps
    changed = True
    while changed:
        changed = False
        merged = []
        for r_min, r_max in ranges:
            for i in range(len(merged)):
                m_min, m_max = merged[i]
                if (r_min < m_min) and (r_max >= m_min):    # Overlap on the left of m
                    merged[i] = (r_min, max(r_max, m_max))  # m now covers both ranges
                    changed = True
                    break
                elif (r_max > m_max) and (r_min <= m_max):  # Overlap on the right of m
                    merged[i] = (min(r_min, m_min), r_max)  # m now covers both ranges
                    changed = True
                    break
                elif (r_min >= m_min) and (r_max <= m_max):  # r is completely contained in m
                    changed = True                           # m already covered both ranges
                    break
            else:
                merged.append((r_min, r_max))
        ranges = merged

    return sum(r_max - r_min + 1
               for r_min, r_max in ranges)
