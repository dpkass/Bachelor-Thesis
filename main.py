from algorithms import Greedy
from comparator import average_quality_per_generator

import logging

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s  %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("Comparator")

    n = 100
    M = [1, 2, 3]
    algorithm = Greedy()

    average_quality_per_generator(algorithm, n, M)
