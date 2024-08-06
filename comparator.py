import time

from tabulate import tabulate

from algorithms import DP_DICT
from generator import generate
from main import logger
from runner import run_single


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

    a_res = run_single(algo_a, n, m, a)
    b_res = run_single(algo_b, n, m, a)

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
    :param A: List of lists of weights of a specific generator
    :return: Average "Quality" of algo for specific generator
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


def average_quality_per_no_machines(algo, n, ms, A, desc):
    """
    Calculate the Average Quality for each m, i.e. Number of Machines

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param ms: Options for number of machines
    :param A: List of lists of weights of a specific generator
    :return: Average "Quality" of algo for specific generator
    """
    logger.info(f"======================== {desc}  ========================")
    return [average_quality(algo, n, m, A) for m in ms]


def average_quality_per_generator(algo, n, M):
    """
    Calculate the Average Quality for each generator type and m, and print as a table

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param M: Options for number of machines
    """
    all_A = generate()
    results = [(desc, *average_quality_per_no_machines(algo, n, M, A, desc))
               for (A, desc) in all_A]
    print(tabulate(results, ["Description of a", *M]))
