import numpy as np

from algrotihms import DP_DICT

from computer import _compute_solutions

import logging

logger = logging.getLogger(__name__)

MSG1 = ''' Compute the Average Quality per Generator Type and Number of Machines '''


def detach_descriptions(arr):
    arr = np.array(arr, object)
    return arr[:, 0], np.array(arr[:, 1:].tolist())


def attach_descriptions(arr, descriptions):
    return [(desc, *a) for desc, a in zip(descriptions, arr)]


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

    descriptions, optimal = detach_descriptions(_compute_solutions(DP_DICT(), n, ms))
    _, result = detach_descriptions(_compute_solutions(algo, n, ms))

    quality_per_instance = result / optimal
    average_quality_per_generator = quality_per_instance.mean(axis=2).tolist()
    return attach_descriptions(average_quality_per_generator, descriptions)
