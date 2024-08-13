from algrotihms import DP_DICT
from generator import generate

from computer import compute_single

import time
import logging

logger = logging.getLogger(__name__)

MSG1 = ' Compute the Average Quality per Generator Type and Number of Machines '
MSG2 = 'Compute the Average Quality per Number of Machines for Generator Type:'


def compare(algo_a, algo_b, m, a):
    """
    Compare two algorithms' performance on specified Weights.

    :param algo_a: First algorithm (typically the worse)
    :param algo_b: Second algorithm (typically the better)
    :param m: Number of Machines
    :param a: List of Weights
    :return: γ(algo_a, m, a) divided by γ(algo_b, m, a)
    """
    a_res = compute_single(algo_a, m, a)
    b_res = compute_single(algo_b, m, a)

    logger.debug(f"diff = {a_res - b_res}, quot = {a_res / b_res}")

    return a_res / b_res


def quality(algo, m, a):
    """
    Compute the Quality of an Algorithm for Weight List.

    :param algo: The algorithm to compare
    :param m: Number of Machines
    :param a: List of Weights
    :return: "Quality" of algo for specified Weights
    """
    return compare(algo, DP_DICT(), m, a)


def average_quality(algo, m, A):
    """
    Compute the Average Quality of an Algorithm for Weight Lists.

    :param algo: The algorithm to compare
    :param m: Number of Machines
    :param A: List of Lists of Weights of a specific generator
    :return: Average "Quality" of algo for specific generator
    """
    logger.info(f"Compute the Average Quality for {m} Machines")
    start = time.perf_counter()

    res = 0
    for i, a in enumerate(A, start=1):
        logger.debug(f"Compute {i}/{len(A)}")
        logger.log(1, f"a = {a}")
        res += quality(algo, m, a)

    end = time.perf_counter()
    res /= len(A)
    logger.info(f"Quality = {res}, Took = {round(end - start, 3)} s")
    return res


def average_quality_per_no_machines(algo, ms, A, desc):
    """
    Compute the Average Quality per Number of Machines

    :param algo: The algorithm to compare
    :param ms: Options for Number of Machines
    :param A: List of Lists of Weights of a specific generator
    :return: Average "Quality" of algo for specific generator
    """
    logger.info(f"{f' {MSG2} {desc} ':-^150}")

    return [average_quality(algo, m, A) for m in ms]


def average_quality_per_generator(algo, n, ms):
    """
    Compute the Average Quality per Generator Type and Number of Machines

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param ms: Options for Number of Machines
    :return: Average quality per Number of Machines per generator type
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG1:=^150}")
    logger.info(f"{'':=^150}")

    results = [(desc, *average_quality_per_no_machines(algo, ms, A, desc))
               for (A, desc) in generate(n)]
    return results
