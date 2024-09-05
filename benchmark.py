from algrotihms import DP_DICT

from computer import _compute_solutions

import logging

logger = logging.getLogger(__name__)

MSG1 = ''' Compute the Average Quality per Generator Type and Number of Machines '''


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

    optimal = _compute_solutions(DP_DICT(), n=150, ms=[2, 3, 4])
    result = _compute_solutions(algo, n, ms)

    quality_per_instance = result / optimal
    return quality_per_instance.mean(axis=2)
