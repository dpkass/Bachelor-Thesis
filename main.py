from tabulate import tabulate

from algrotihms import *

from comparator import average_quality_per_generator
from computer import compute_averaged as ca, compute_solutions as cs

import log


def _test_algorithm(algorithm, quality=True, compute_averaged=False, compute_solutions=False):
    algorithm_name = algorithm.__class__.name

    if quality:
        avg_q = average_quality_per_generator(algorithm, n, ms)
        print_as_table(avg_q, algorithm_name)

    if compute_averaged:
        cmp_avg = ca(algorithm, n, ms)
        print_as_table(cmp_avg, algorithm_name)

    if compute_solutions:
        sol = cs(algorithm, n, ms)
        print_as_table(sol, algorithm_name)


def print_as_table(data, name):
    print(tabulate(data, [name, *[f"m = {m}" for m in ms]], tablefmt="pipe"), end="\n\n")


if __name__ == "__main__":
    log.configure()

    n = 150
    ms = [2, 3, 4]

    # _test_algorithm(Greedy())
    # _test_algorithm(Lookahead(5))
    # _test_algorithm(Lookahead(15))
    # _test_algorithm(Lookahead(30))
    # _test_algorithm(HeavyFirst())
    # _test_algorithm(SimpleSortAndSplit())
    _test_algorithm(BalancedSequentialInsert())
