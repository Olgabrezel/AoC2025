import itertools
import scipy
import numpy as np


def parse_input(task_input: str):
    parsed = []
    for line in task_input.split('\n'):
        diagram = line.split(' ')[0][1:-1]
        schematics = tuple(tuple(map(int, x[1:-1].split(','))) for x in line.split(' ')[1:-1])
        joltages = tuple(int(x) for x in line.split(' ')[-1][1:-1].split(','))
        parsed.append((diagram, schematics, joltages))
    return parsed


def simulate(machine_len, btn_seq):
    lst = ['.'] * machine_len
    for btn in btn_seq:
        for idx in btn:
            lst[idx] = '#' if lst[idx] == '.' else '.'
    return ''.join(lst)


def part1(task_input: str):
    manual = parse_input(task_input)
    total_presses = 0

    for target, buttons, _ in manual:
        presses = 0
        found = False
        while not found:
            presses += 1
            for seq in itertools.combinations_with_replacement(buttons, presses):
                if simulate(len(target), seq) == target:
                    found = True
                    break
        total_presses += presses

    return total_presses


def get_restrictions(buttons, joltage):
    restrictions = []
    for idx in range(len(joltage)):
        target_val = joltage[idx]
        target_btns = [i for i, btn in enumerate(buttons) if idx in btn]  # buttons that affect the current joltage
        restrictions.append((tuple(target_btns), target_val))  # number of presses for those buttons must match that value
    return restrictions


def part2(task_input: str):
    manual = parse_input(task_input)
    total_presses = 0

    for _, buttons, joltage in manual:
        restrictions = get_restrictions(buttons, joltage)
        # And at this point, it's an ILP (Integer Linear Program). Blergh.

        A = np.array([[(1 if idx in r[0] else 0) for idx in range(len(buttons))] for r in restrictions])
        b = np.array([r[1] for r in restrictions])
        c = np.ones(len(buttons))

        res = scipy.optimize.linprog(c, A_eq=A, b_eq=b, integrality=1).x
        total_presses += int(sum(res))

    return total_presses


# I think it's worth keeping this earlier attempt at part 2:
# EARLY IDEA using sympy for solving the underdetermined system of linear equations that is the ILP:
#
#  # We search for a vector x that solves Ax = b, for the following A and b:
#  A = sympy.Matrix([[(1 if idx in r[0] else 0) for idx in range(len(buttons))] for r in restrictions])
#  b = sympy.Matrix([[r[1]] for r in restrictions])
#
#  symbols = [sympy.symbols(f'x{i}') for i in range(len(buttons))]  # coefficients x0, x1, ... that we solve for
#  solution = sympy.linsolve((A, b), symbols)
#  free_vars = solution.free_symbols
#
#  # Now we need to find an assignment of these free variables that minimizes the sum of the presses
#  # while maintaining the basic ILP restrictions (only positive integers allowed as button press counts)
#  # ... Turns out, finding such an assignment is still hard, and brute-force is still not feasible at this point.
#  #     Will need to properly solve the ILP instead.
