from algrotihms import DP_DICT

import xarray as xr
from computer import _compute_solutions

import logging

logger = logging.getLogger(__name__)

MSG1 = ''' Compute the Average Quality per Generator Type and Number of Machines '''


def average_quality_per_generator(algo, n, ms, use_precomputed=True):
    """
    Compute the Average Quality per Generator Type and Number of Machines

    :param algo: The algorithm to compare
    :param n: Number of jobs
    :param ms: Options for Number of Machines
    :param use_precomputed: Whether to use precomputed solutions
    :return: Average quality per Number of Machines per generator type
    """
    logger.info(f"{'':=^150}")
    logger.info(f"{MSG1:=^150}")
    logger.info(f"{'':=^150}")

    if use_precomputed:
        optimal = xr.open_dataarray("precomputed/dictionary-dp.nc")
        assert n in optimal.coords['n'] and all(m in optimal.coords['m'] for m in ms), \
            "Precomputed Solutions do not cover selected Parameters n and m"
        optimal = optimal.loc[n]
    else:
        optimal = _compute_solutions(DP_DICT(), n, ms)
    result = _compute_solutions(algo, n, ms)

    quality_per_instance = result / optimal
    return quality_per_instance.mean(axis=2).squeeze()
