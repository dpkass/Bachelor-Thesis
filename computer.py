from generator import generate

from statistics import fmean

import time
import logging

logger = logging.getLogger("Runner")

MSG1 = '''Compute the Solutions per Number of Machines for Generator Type:'''
MSG2 = '''Compute the Solution Average per Number of Machines for Generator Type:'''
MSG3 = ''' Compute the Solutions per Number of Machines for multiple Weight Lists of a Generator Type '''
MSG4 = ''' Compute the Average Value per Number of Machines per Generator Type '''


def compute_single(algo, m, instance):
    """
    Compute a single solution of an algorithm for set n, m, and Weight List a

    :param algo: Algorithm to run
    :param m: Number of Machines
    :param a: List of Weights
    :return: γ(algo, m, a)
    """
    start = time.perf_counter()
    res = algo.fit_transform(m, instance.values)
    end = time.perf_counter()

    algo_name = algo.__class__.__name__
    logger.debug(f"    DONE: γ({algo_name}, m:{m}, a) = {res}. "
                 f"Took {round(end - start, 3)} s")

    return res


def compute_each_instance(algo, m, instances):
    """
    Compute the solutions for each Weight List in A.
    Note: in place
    """
    logger.info(f"START: {m} Machines.")
    start = time.perf_counter()

    res = []
    for i, instance in enumerate(instances, start=1):
        logger.debug(f"    START: Compute Instance {i}/{len(instances)}")
        logger.log(1, f"    a = {instance}")
        sol = compute_single(algo, m, instance)
        res.append(sol)

    end = time.perf_counter()
    logger.info(
        f"DONE: {m} Machines. "
        f"Took {round(end - start, 3)} s for {len(res)} Instance{'s' if len(res) > 1 else ''}.")
    return res


def compute_per_number_of_machines(algo, machines):
    """
    Compute the Solutions per Number of Machines for each Weight List in A.
    Note: in place
    """
    for instances in machines:
        m = instances.coords['m'].values.item()
        compute_each_instance(algo, m, instances)


def _compute_solutions(algo, n, ms, seeds=range(10)):
    results = generate(n, seeds).expand_dims(dim={'m': ms}, axis=1)

    for machines in results:
        description = machines.coords['Generator'].values.item()
        logger.info(f"{f' {MSG1} {description} ':-^150}")
        compute_per_number_of_machines(algo, machines)

    return results


def compute_solutions(algo, n, ms, seeds=range(10)):
    """
    Compute a 3D-Array with the following axes:
    1. Generator Type
    2. Number of Machines
    3. Seed (if random)

    Note: in place

    :param algo: Algorithm to calculate the values for
    :param n: Number of Jobs
    :param ms: Options for Numbers of Machines
    :param seeds: Which seeds to use
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG3:=^150}")
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
    logger.info(f"{MSG4:=^150}")
    logger.info(f"{'':=^150}")

    vals = _compute_solutions(algo, n, ms, seeds)

    return [[desc, *(fmean(row) for row in rows)] for [desc, *rows] in vals]
