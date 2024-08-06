from algorithms import DP_DICT, Greedy
from generator import generate

import logging

from tabulate import tabulate


def compare(algo_a, algo_b, n, m, a):
    """
    Compare two algorithms' performance on specified weights.

    :param algo_a: First algorithm (typically the worse)
    :param algo_b: Second algorithm (typically the better)
    :param n: Number of jobs
    :param m: Number of machines
    :param a: List of weights
    :return: T(algo_a) divided by T(algo_b)
    """
    return algo_a.fit_transform(n, m, a) / algo_b.fit_transform(n, m, a)


def compare_to_optimal(algo, n, m, a):
    """
    Compare an algorithms' performance to the optimal solution.

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param m: Number of machines
    :param a: List of weights
    :return: "Quality" of algo for specified weights
    """
    return compare(algo, DP_DICT(), n, m, a)


def average_quality(algo, n, m, as_):
    """
    Average quality of an algorithm over given weights.

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param m: Number of machines
    :param as_: List of lists of weights
    :return: Average "Quality" of algo for specified weights
    """
    return sum(compare_to_optimal(algo, n, m, a) for a in as_) / len(as_)


def run(algo, n, ms, as_):
    return [average_quality(algo, n, m, as_) for m in ms]


def run_all(algorithm, n, ms):
    all_as = generate()
    results = [(desc, *run(algorithm, n, ms, as_))
               for (as_, desc) in all_as]
    print(tabulate(results, ["Description of a", *ms]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    n = 150
    ms = [2, 3, 4]
    algorithm = Greedy()

    run_all(algorithm, n, ms)
