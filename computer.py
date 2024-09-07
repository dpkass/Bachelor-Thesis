from generator import generate

import xarray as xr

import time
import logging

logger = logging.getLogger("Runner")

MSG1 = ''' Compute the Solutions per Number of Machines for multiple Weight Lists of a Generator Type '''
MSG2 = ''' Compute the Average Value per Number of Machines per Generator Type '''


def compute_single(instance, m, algo):
    """
    Compute a single solution of an algorithm for set n, m, and Weight List a

    :param algo: Algorithm to run
    :param m: Number of Machines
    :param instance: List of Weights
    :return: γ(algo, m, a)
    """
    algo_name = algo.name
    logger.info(f"Calculate γ({algo_name}, m:{m}, a).")

    start = time.perf_counter()
    res = algo.fit_transform(m, instance)
    end = time.perf_counter()

    logger.info(f"γ({algo_name}, m:{m}, a) = {res}. Took {round(end - start, 3)} s")

    return res


def _compute_solutions(algo, n, ms, seeds=range(10)):
    instances = generate(n, seeds).expand_dims(dim={'m': ms}, axis=1)

    return xr.apply_ufunc(
        compute_single,
        instances,
        instances['m'],
        input_core_dims=[['a'], []],
        vectorize=True,
        kwargs={'algo': algo},
    )


def compute_solutions(algo, n, ms, seeds=range(10)):
    """
    Compute a 3D-Array with the following axes:
    1. Generator Type
    2. Seed
    3. Number of Machines

    Note: in place

    :param algo: Algorithm to calculate the values for
    :param n: Number of Jobs
    :param ms: Options for Numbers of Machines
    :param seeds: Which seeds to use
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG1:=^150}")
    logger.info(f"{'':=^150}")

    return _compute_solutions(algo, n, ms, seeds)


def compute_averaged(algo, n, ms, seeds=range(10)):
    """
    Compute a 2D-Array with the following axes:
    1. Generator Type
    2. Number of Machines

    :param algo: Algorithm to calculate the values for
    :param n: Number of Jobs
    :param ms: Options for Numbers of Machines
    :param seeds: Which seeds to use
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG2:=^150}")
    logger.info(f"{'':=^150}")

    return _compute_solutions(algo, n, ms, seeds).mean(dim='seed')
