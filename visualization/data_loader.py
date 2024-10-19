"""
data_loader.py

Module to load and combine algorithm performance data from NetCDF files using xarray.

Functions:
- load_algorithm_data(directory): Load all algorithm data except the optimal solution and combine into a single xarray Dataset.
- load_optimal_solution(directory): Load the optimal solution data as a separate xarray DataArray.
"""

import os
import xarray as xr


def load_algorithm_data(directory='./precomputed'):
    """
    Load data from all NetCDF files in a specified directory, excluding the optimal solution.

    Parameters:
    - directory (str): Path to the directory containing NetCDF (.nc) files for each algorithm.

    Returns:
    - xr.Dataset: Combined Dataset with an added 'Algorithm' dimension for all non-optimal algorithms.

    Raises:
    - ValueError: If no algorithm NetCDF files are found in the directory.
    - RuntimeError: If a NetCDF file fails to load.
    """
    datasets = []
    algorithm_names = []

    for filename in os.listdir(directory):
        if filename.endswith('.nc'):
            filepath = os.path.join(directory, filename)
            # Derive algorithm name from filename (e.g., 'balanced-sequential-insert.nc' -> 'Balanced Sequential Insert')
            algo_name = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
            try:
                da = xr.open_dataarray(filepath)
                da = da.expand_dims('Algorithm').assign_coords(Algorithm=[algo_name])
                datasets.append(da)
                algorithm_names.append(algo_name)
                print(f"Loaded data for algorithm: {algo_name}")
            except Exception as e:
                raise RuntimeError(f"Failed to load {filename}: {e}")

    if not datasets:
        raise ValueError(f"No algorithm NetCDF files found in directory: {directory}")

    combined_ds = xr.concat(datasets, dim='Algorithm')
    return combined_ds


def load_optimal_solution(directory='./precomputed', file='dictionary-dp.nc'):
    """
    Load the optimal solution data from a specified NetCDF file.

    Parameters:
    - directory (str): Path to the directory containing the optimal solution NetCDF (.nc) file.

    Returns:
    - xr.DataArray: Optimal solution DataArray with dimensions ['Generator', 'm', 'Seed'].

    Raises:
    - FileNotFoundError: If the optimal solution file is not found.
    - RuntimeError: If the optimal solution file fails to load.
    """
    filepath = os.path.join(directory, file)

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Optimal solution file '{filepath}' not found")

    try:
        da_optimal = xr.open_dataarray(filepath)
        print(f"Loaded optimal solution from {filepath}")
    except Exception as e:
        raise RuntimeError(f"Failed to load optimal solution from {filepath}: {e}")

    return da_optimal
