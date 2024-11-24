from algrotihms import *

from computer import compute_solutions

import xarray as xr

import log
import logging

log.configure()


def precompute(algorithms, n=150, ms=range(1, 7), seeds=range(10)):
    file_name = "precomputed"
    nc_file = file_name + ".nc"
    csv_file = file_name + ".csv"

    res = []

    for algorithm in algorithms:
        logging.info("Compute " + algorithm.name)
        solutions = compute_solutions(algorithm, n, ms, seeds)
        res += [solutions.expand_dims(algorithm=[algorithm.name], axis=0)]

    da = xr.combine_by_coords(res)

    try:
        with xr.open_dataarray(nc_file) as full_data:
            da = xr.concat([full_data, da], dim='algorithm').sortby('algorithm')
            logging.info("Found previous data and merged")
    except FileNotFoundError:
        pass
    except Exception as e:
        nc_file = nc_file.replace(".nc", "-unmerged.nc")

        logging.warning(e)
        logging.info("Could not merge")
        logging.warning(f"Will write to file {nc_file}, in order avoid overwriting previous data")

    logging.info("Writing NetCDF")
    da.to_netcdf(nc_file)

    logging.info("Writing CSV")
    df = da.stack(combined=da.dims).to_pandas()
    df.to_csv(csv_file)


if __name__ == "__main__":
    all = [
        DP_DICT(),
        LeastLoaded(),
        HeavyFirst(),
        Lookahead(5),
        Lookahead(15),
        SimpleSortAndSplit(),
        BalancedSequentialInsert()
    ]

    precompute(all)
