from generator import generate

import numpy as np

import time
import logging

logger = logging.getLogger("Runner")

MSG1 = 'Compute the Solutions per Number of Machines for Generator Type:'
MSG2 = 'Compute the Solution Average per Number of Machines for Generator Type:'
MSG3 = ' Compute the Solutions per Number of Machines for multiple Weight Lists of a Generator Type '
MSG4 = ' Compute the Average Value per Number of Machines per Generator Type '


def compute_single(algo, m, a):
    """
    Compute a single solution of an algorithm for set n, m, and Weight List a

    :param algo: Algorithm to run
    :param m: Number of Machines
    :param a: List of Weights
    :return: γ(algo, m, a)
    """
    res = algo.fit_transform(m, a)

    algo_name = algo.__class__.__name__
    logger.debug(f"γ({algo_name}, m:{m}, a) = {res}")

    return res


def compute_each(algo, m, A):
    """
    Compute the solutions for each Weight List in A.

    :returns: A List of Solutions for each given a in A
    """
    logger.info(f"Compute the Solutions for {m} Machines")
    start = time.perf_counter()

    res = []
    for i, a in enumerate(A, start=1):
        logger.debug(f"Compute {i}/{len(A)}")
        logger.log(1, f"a = {a}")
        sol = compute_single(algo, m, a)
        res.append(sol)

    end = time.perf_counter()
    logger.info(f"Took = {round(end - start, 3)} s")
    return res


def compute_per_number_of_machines(algo, ms, A, desc, fill):
    """
    Compute the Solutions per Number of Machines for each Weight List in A.

    :returns: A List of Solutions for each given Number of Machines m in ms
    """
    logger.info(f"{f' {MSG1} {desc} ':-^150}")

    return [compute_each(algo, m, A) * fill for m in ms]


def _compute_solutions(algo, n, ms):
    seeds = range(10)
    return [(desc, *compute_per_number_of_machines(algo, ms, A, desc, 1 if rnd else len(seeds)))
            for (A, desc, rnd) in generate(n, seeds)]


def compute_solutions(algo, n, ms):
    """
    Compute a 3D-Array with the following axes:
    1. Generator Type
    2. Number of Machines
    3. Seed (if random)

    :param algo: Algorithm to calculate the values for
    :param n: Number of Jobs
    :param ms: Options for Numbers of Machines
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG3:=^150}")
    logger.info(f"{'':=^150}")

    return _compute_solutions(algo, n, ms)


def compute_averaged(algo, n, ms):
    """
    Compute a 2D-Array with the following axes:
    1. Generator Type
    2. Number of Machines

    :param algo: Algorithm to calculate the values for
    :param n: Number of Jobs
    :param ms: Options for Numbers of Machines
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG4:=^150}")
    logger.info(f"{'':=^150}")

    vals = _compute_solutions(algo, n, ms)

    return [[desc, *(np.mean(row) for row in rows)] for [desc, *rows] in vals]
