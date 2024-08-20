from tabulate import tabulate

from algrotihms import *

from comparator import average_quality_per_generator
from computer import compute_averaged, compute_solutions

import logging


def _test_algorithm(algorithm, quality=True, compute_averaged=False, compute_solutions=False):
    algorithm_name = algorithm.__class__.name

    if quality:
        avg_q = average_quality_per_generator(algorithm, n, ms, True)
        print_as_table(avg_q, algorithm_name)

    if compute_averaged:
        cmp_avg = compute_averaged(algorithm, n, ms)
        print_as_table(cmp_avg, algorithm_name)

    if compute_solutions:
        sol = compute_solutions(algorithm, n, ms)
        print_as_table(sol, algorithm_name)


def print_as_table(data, name):
    print(tabulate(data, [name, *[f"m = {m}" for m in ms]], tablefmt="pipe"), end="\n\n")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s  %(threadName)-25s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    n = 150
    ms = [2, 3, 4]

    # _test_algorithm(Greedy())
    # _test_algorithm(Lookahead(5))
    # _test_algorithm(Lookahead(20))
    _test_algorithm(Lookahead(50))
