import time

from algorithms import DP_DICT, DP_MDIM, Greedy
from generator import generate

import logging

from tabulate import tabulate


def run(algo, n, m, a):
    """
    Do a single solve.

    :param algo: Algorithm to run
    :param n: Number of Jobs
    :param m: Number of Machines
    :param a: List of Weights
    :return: γ(algo, m, a)
    """
    algo_name = algo.__class__.__name__
    logger.debug(f"Run Algorithm {algo_name}")

    res = algo.fit_transform(n, m, a)
    logger.debug(f"γ({algo_name}, m:{m}, a) = {res}")

    return res


def compare(algo_a, algo_b, n, m, a):
    """
    Compare two algorithms' performance on specified weights.

    :param algo_a: First algorithm (typically the worse)
    :param algo_b: Second algorithm (typically the better)
    :param n: Number of jobs
    :param m: Number of machines
    :param a: List of weights
    :return: γ(algo_a, m, a) divided by γ(algo_b, m, a)
    """
    logger.log(1, f"a = {a}")

    a_res = run(algo_a, n, m, a)
    b_res = run(algo_b, n, m, a)

    logger.debug(f"diff = {a_res - b_res}, quot = {a_res / b_res}")

    return a_res / b_res


def quality(algo, n, m, a):
    """
    Compare an algorithms' performance to the optimal solution.

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param m: Number of machines
    :param a: List of weights
    :return: "Quality" of algo for specified weights
    """
    return compare(algo, DP_DICT(), n, m, a)


def average_quality(algo, n, m, A):
    """
    Average quality of an algorithm over given weights.

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param m: Number of machines
    :param A: List of lists of weights
    :return: Average "Quality" of algo for specified weights
    """
    logger.info(f"Calculate average quality for m = {m}")
    start = time.perf_counter()

    res = 0
    for i, a in enumerate(A, start=1):
        logger.debug(f"Run {i}/{len(A)}")
        res += quality(algo, n, m, a)

    end = time.perf_counter()
    res /= len(A)
    logger.info(f"Quality = {res}, Took = {round(end - start, 3)} s")
    return res


def average_quality_per_machine(algo, n, ms, A, desc):
    logger.info(f"======================== {desc}  ========================")
    return [average_quality(algo, n, m, A) for m in ms]


def average_quality_per_generator(algo, n, M):
    all_A = generate()
    results = [(desc, *average_quality_per_machine(algo, n, M, A, desc))
               for (A, desc) in all_A]
    print(tabulate(results, ["Description of a", *M]))


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s  %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("Comparator")

    n = 150
    M = [1, 2, 3, 4]
    algorithm = Greedy()

    average_quality_per_generator(algorithm, n, M)
