from tabulate import tabulate

from algorithms import *

from comparator import average_quality_per_generator
from computer import compute_averaged, compute_solutions

import logging

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s  %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    n = 150
    ms = [1, 2, 3, 4, 5]
    algorithm = Greedy()

    headers = ["Description of a", *ms]

    print(tabulate(average_quality_per_generator(algorithm, n, ms), headers))
    print()
    print(tabulate(compute_averaged(algorithm, n, ms), headers))
    print()
    print(tabulate(compute_solutions(algorithm, n, ms), headers))
