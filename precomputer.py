from algrotihms import *

from computer import compute_solutions

import xarray as xr
import numpy as np

import log
import logging

log.configure()

kebab = lambda s: s.replace(' ', '-').lower()


def precompute(algorithm, n=150, ms=range(2, 5), seeds=range(10)):
    file_name = f"precomputed/{kebab(algorithm.name)}"
    nc_file = file_name + ".nc"
    csv_file = file_name + ".csv"

    res = np.array(compute_solutions(algorithm, n, ms, seeds), object)
    generator_names = res[:, 0].astype(str)

    data = np.array(res[:, 1:].tolist())  # axes: gen, m, seed
    data = data.transpose(1, 0, 2)  # axes: m, gen, seed
    data = np.expand_dims(data, axis=0)  # axes: n, m, gen, seed

    new_da = xr.DataArray(data,
                          coords=[[n], ms, generator_names, seeds],
                          dims=['n', 'm', 'Generator', 'Seed'])

    try:
        with xr.open_dataarray(nc_file) as curr_da:
            da = xr.combine_by_coords([curr_da, new_da])
            logging.info("Found previous data and merged")
    except FileNotFoundError:
        da = new_da
    except Exception as e:
        da = new_da
        nc_file = nc_file.replace(".nc", "-unmerged.nc")

        logging.warning(e)
        logging.info("Could not merge")
        logging.warning(f"Will write to file {nc_file}, in order avoid overwriting previous data")

    logging.info("Writing NetCDF")
    da.to_netcdf(nc_file)

    logging.info("Writing CSV")
    df = da.stack(combined=da.dims).to_pandas()
    df.to_csv(csv_file)


if __name__ == "__main__": precompute(BalancedSequentialInsert())
