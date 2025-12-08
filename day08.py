from typing import List, Tuple
from math import sqrt


def parse_input(task_input: str) -> List[Tuple[int, int, int]]:
    return [tuple(map(int, row.split(','))) for row in task_input.split('\n')]


def compute_distances(boxes: List[Tuple[int, int, int]]) -> List[Tuple[float, Tuple[int, int, int], Tuple[int, int, int]]]:
    return sorted([(sqrt((x1-x2)**2 + (y1-y2)**2 + (z1 - z2)**2), (x1, y1, z1), (x2, y2, z2))
                  for (x1, y1, z1) in boxes
                  for (x2, y2, z2) in boxes
                  if (x1, y1, z1) < (x2, y2, z2)])  # pairwise distances, not with same box, each unordered pair just once


def part1(task_input: str):
    boxes = parse_input(task_input)
    distances = compute_distances(boxes)

    circuits = {box: i for i, box in enumerate(boxes)}  # give each cirtuit an identifier

    for _, box1, box2 in distances[:1000]:
        if circuits[box1] != circuits[box2]:  # these are in different circuits, merge them!
            merge_from = circuits[box1]
            merge_to = circuits[box2]
            for otherbox in circuits:
                if circuits[otherbox] == merge_from:
                    circuits[otherbox] = merge_to

    circuit_lists = [(v, [x for x in circuits if circuits[x] == v]) for v in set(circuits.values())]
    circuit_lists.sort(key=lambda tpl: len(tpl[1]), reverse=True)

    return len(circuit_lists[0][1]) * len(circuit_lists[1][1]) * len(circuit_lists[2][1])


def part2(task_input: str):
    boxes = parse_input(task_input)
    distances = compute_distances(boxes)

    circuits = {box: i for i, box in enumerate(boxes)}  # give each cirtuit an identifier

    for _, box1, box2 in distances:
        if circuits[box1] != circuits[box2]:   # these are in different circuits, merge them!
            if len(set(circuits.values())) == 2:
                return box1[0] * box2[0]  # this is the final merge!

            merge_from = circuits[box1]
            merge_to = circuits[box2]
            for otherbox in circuits:
                if circuits[otherbox] == merge_from:
                    circuits[otherbox] = merge_to
