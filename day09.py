from collections import defaultdict
from functools import cache
from typing import Dict, List, Set, Tuple
from alive_progress import alive_bar


def parse_input(task_input: str) -> List[Tuple[int, int]]:
    return [tuple(map(int, row.split(','))) for row in task_input.split('\n')]


def part1(task_input: str):
    corners = parse_input(task_input)
    max_area = 0
    for c1 in corners:
        for c2 in corners:
            if c1 < c2:
                max_area = max(max_area,
                               (abs(c1[0] - c2[0]) + 1) * (abs(c1[1] - c2[1]) + 1))
    return max_area


# Maps y coordinates to sets of (x-coordinate, symbol) tuples for all corners.
def compute_corner_symbols(corners: List[Tuple[int, int]]) -> Dict[int, Set[Tuple[int, str]]]:
    corner_symbols = defaultdict(set)
    for i, c in enumerate(corners):
        c_next = corners[(i+1) % len(corners)]
        c_prev = corners[(i-1) % len(corners)]
        if c[0] == c_next[0]:
            if c[1] > c_next[1]:
                if c[0] > c_prev[0]:
                    corner_symbols[c[1]].add((c[0], 'J'))  # bottom right corner
                else:
                    corner_symbols[c[1]].add((c[0], 'L'))  # bottom left corner
            else:
                if c[0] > c_prev[0]:
                    corner_symbols[c[1]].add((c[0], '7'))  # top right corner
                else:
                    corner_symbols[c[1]].add((c[0], 'F'))  # top left corner
        else:
            if c[0] > c_next[0]:
                if c[1] > c_prev[1]:
                    corner_symbols[c[1]].add((c[0], 'J'))  # bottom right corner
                else:
                    corner_symbols[c[1]].add((c[0], '7'))  # top right corner
            else:
                if c[1] > c_prev[1]:
                    corner_symbols[c[1]].add((c[0], 'L'))  # bottom left corner
                else:
                    corner_symbols[c[1]].add((c[0], 'F'))  # top left corner
    return corner_symbols


# Maps y coordinates to sets of (x-coordinate, '|') tuples for all vertical edges.
def compute_edge_symbols(corners: List[Tuple[int, int]]) -> Dict[int, Set[Tuple[int, str]]]:
    edge_symbols = defaultdict(set)
    for i, c in enumerate(corners):
        c_next = corners[(i+1) % len(corners)]
        if c[0] == c_next[0]:
            if c[1] < c_next[1]:
                for between in range(c[1]+1, c_next[1]):
                    edge_symbols[between].add((c[0], '|'))
            else:
                for between in range(c_next[1]+1, c[1]):
                    edge_symbols[between].add((c[0], '|'))

        # Otherwise the edge is horizontal and not interesting for our approach.
    return edge_symbols


def is_red_or_green(x: int, y: int, y_symbols: Dict[int, List[Tuple[int, str]]]) -> bool:

    @cache  # Putting @cache on an inner function so the y_symbols aren't cached (they do not change anyway.)
    def inner(x, y):
        if y not in y_symbols:  # (x, y) is above or below the entire loop
            return False

        symbols = y_symbols[y]
        inside = False
        i = 0
        while i < len(symbols):
            cx, sym = symbols[i]
            if cx > x:
                return inside
            match sym:
                case '|':
                    inside = not inside
                case 'F':
                    i += 1
                    next_cx, next_sym = symbols[i]
                    if next_cx >= x:  # (x, y) is on the edge between the current 'F' and the next symbol
                        return True
                    if next_sym == 'J':
                        inside = not inside
                case 'L':
                    i += 1
                    next_cx, next_sym = symbols[i]
                    if next_cx >= x:  # (x, y) is on the edge between the current 'L' and the next symbol
                        return True
                    if next_sym == '7':
                        inside = not inside
            i += 1

        return False  # (x, y) is to the right of the entire loop

    return inner(x, y)


def part2(task_input: str):
    print("Takes about 20 minutes... Here's a nice progress bar for you!")
    corners = parse_input(task_input)
    corner_symbols = compute_corner_symbols(corners)
    edge_symbols = compute_edge_symbols(corners)

    # Merge corner and edge symbols, turn sets of (x-coordinate, symbol) tuples into sorted lists (ascending by x)
    y_symbols = {y: sorted((corner_symbols.get(y) or set()) | (edge_symbols.get(y) or set()))
                 for y in set(corner_symbols.keys()) | set(edge_symbols.keys())}

    max_area = 0
    with alive_bar(len(corners) * len(corners)) as bar:
        for c1 in corners:
            for c2 in corners:
                bar()

                if c1 < c2:
                    area = (abs(c1[0] - c2[0]) + 1) * (abs(c1[1] - c2[1]) + 1)
                    if area <= max_area:
                        continue

                    allowed = True
                    smaller_y = min(c1[1], c2[1])
                    larger_y = max(c1[1], c2[1])
                    smaller_x = min(c1[0], c2[0])
                    larger_x = max(c1[0], c2[0])

                    for y in range(smaller_y, larger_y+1):
                        if (not is_red_or_green(smaller_x, y, y_symbols)) or (not is_red_or_green(larger_x, y, y_symbols)):
                            allowed = False
                            break
                    if not allowed:
                        continue

                    for x in range(smaller_x, larger_x+1):
                        if (not is_red_or_green(x, smaller_y, y_symbols)) or (not is_red_or_green(x, larger_y, y_symbols)):
                            allowed = False
                            break
                    if not allowed:
                        continue

                    max_area = area

    return max_area
