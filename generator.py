import numpy as np

from generators import generators as gs

import xarray as xr

from algrotihms.base import dtype


def generate(n=150, seeds=range(10)):
    """
    Generate Lists of Weights for all generators and given seeds.

    :param n: Length of a's. Defaults to 150.
    :param seeds: Reproducibility Seeds. Defaults to [0, ..., 9]
    :return: DataArray with generated instances
    """
    generator_names = [g.name for g in gs]

    data = np.array([[g(n, seed) for seed in seeds] for g in gs], dtype=object)
    return xr.DataArray(data,
                        coords={'generator': generator_names, 'seed': seeds},
                        dims=['generator', 'seed', 'a']).astype(dtype)
