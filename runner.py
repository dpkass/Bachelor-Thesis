from main import logger


def run_single(algo, n, m, a):
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
