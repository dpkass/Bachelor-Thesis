"""
statistical_processor.py

Module to compute various statistical metrics for algorithm performance data using xarray.

Functions:
- relative_performance_ratio(solutions, optimal): Compute the Relative Performance Ratio.
- log_scaled_performance(solutions, optimal): Compute the Log-Scaled Performance.
- consistency_metrics(solutions): Compute Consistency Metrics (Standard Deviation, Variance).
- percentage_optimal_solutions(solutions, optimal): Compute Percentage of Optimal Solutions Achieved.
- scalability_metrics(solutions): Compute Scalability Metrics (Slope of Mean Solution vs. Number of Machines).
- cumulative_improvement(solutions): Compute Cumulative Improvement.
- compute_all_metrics(solutions_per_algorithm, optimal): Compute all metrics and aggregate them into a single Dataset.
"""
import xarray as xr
import numpy as np


def relative_performance_ratio(solutions: xr.DataArray, optimal):
    """
    Compute the Relative Performance Ratio for each algorithm.

    **Relative Performance Ratio** is the ratio of an algorithm's solution to the optimal solution.
    A ratio of 1 indicates optimal performance, and ratios greater than 1 show deviations from optimality.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with any dimensions.
    - optimal (xr.DataArray): Optimal solution data with the same dimensions.

    Notes:
    - If 'Algorithm' is a dimension in `solutions`, it may be absent from the `optimal` data array.

    Returns:
    - xr.DataArray: Relative Performance Ratio with the same dimensions as solutions.
    """
    relative_perf_ratio = solutions / optimal
    return relative_perf_ratio.rename('Relative_Performance_Ratio')


def log_scaled_performance(solutions, optimal):
    """
    Compute the Log-Scaled Performance for each algorithm.

    **Log-Scaled Performance** applies a logarithmic transformation to the Relative Performance Ratio.
    This highlights large differences between solutions and the optimal.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with any dimensions.
    - optimal (xr.DataArray): Optimal solution data with the same dimensions.

    Notes:
    - If 'Algorithm' is a dimension in `solutions`, it may be absent from the `optimal` data array.

    Returns:
    - xr.DataArray: Log-Scaled Performance with the same dimensions as solutions.
    """
    relative_perf_ratio = relative_performance_ratio(solutions, optimal)
    log_scaled_perf = xr.where(relative_perf_ratio > 0, np.log(relative_perf_ratio), np.nan)
    return log_scaled_perf.rename('Log_Scaled_Performance')


def consistency_metrics(solutions):
    """
    Compute Consistency Metrics (Standard Deviation and Variance) for each algorithm.

    **Consistency Metrics** indicate the variability in an algorithm's performance across different seeds.
    Lower standard deviation and variance suggest more consistent performance.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with at least dimension 'Seed'.

    Returns:
    - xr.Dataset: Dataset containing 'Std_Solution' and 'Var_Solution' each the same dimensions as solutions.
    """
    std_solution = solutions.std(dim='Seed').rename('Std_Solution')
    var_solution = solutions.var(dim='Seed').rename('Var_Solution')
    coefficient_of_variation = std_solution / solutions.mean(dim='Seed')
    coefficient_of_variation = coefficient_of_variation.rename('Coefficient_of_Variation')

    return xr.Dataset({'Std_Solution': std_solution, 'Var_Solution': var_solution,
                       'Coefficient_of_Variation': coefficient_of_variation})


def percentage_optimal(solutions, optimal):
    """
    Compute the Percentage of Optimal Solutions Achieved for each algorithm.

    **Percentage of Optimal Solutions** reflects how often an algorithm achieves the optimal solution across different runs.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with at least dimensions ['Seed'].
    - optimal (xr.DataArray): Optimal solution data with the same dimensions.

    Notes:
    - If 'Algorithm' is a dimension in `solutions`, it may be absent from the `optimal` data array.

    Returns:
    - xr.DataArray: Percentage of Optimal Solutions with the same dimensions as solutions.
    """
    is_optimal = solutions == optimal
    po = is_optimal.mean(dim='Seed') * 100
    return po.rename('Percentage_Optimal_Solutions')


def scalability_metrics(solutions):
    """
    Compute Scalability Metrics (Slope of Mean Solution vs. Number of Machines) for each algorithm and generator.

    **Scalability Metrics** assess how an algorithm's solution quality changes as the number of machines (`m`) increases.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with at least dimensions ['m', 'Seed'].

    Returns:
    - xr.DataArray: Scalability Slope with the same dimensions as solutions except 'm'.
    """
    mean_sol = solutions.mean(dim='Seed')

    def compute_slope(m, sol):
        if len(m) < 2:
            return np.nan
        else:
            slope, _ = np.polyfit(m, sol, 1)
            return slope

    scalability_slope = xr.apply_ufunc(
        compute_slope,
        mean_sol['m'],
        mean_sol,
        input_core_dims=[['m'], ['m']],
        vectorize=True
    )

    return scalability_slope.rename('Scalability_Slope')


def cumulative_improvement(solutions):
    """
    Compute Cumulative Improvement for each algorithm and generator.

    **Cumulative Improvement** measures how much an algorithm's solution improves as the number of machines (`m`) increases.

    Parameters:
    - solutions (xr.DataArray): Solutions dataset with dimensions ['m', 'Seed'].

    Returns:
    - xr.DataArray: Cumulative Improvement with the same dimensions as solutions except 'Seed'.
    """
    mean_sol = solutions.mean(dim='Seed').sortby('m')

    cumulative_improvement = xr.apply_ufunc(
        lambda x: np.pad(np.diff(x), (1, 0)),
        mean_sol,
        input_core_dims=[['m']],
        output_core_dims=[['m']],
        vectorize=True
    )

    return cumulative_improvement.rename('Cumulative_Improvement')


def compute_all_metrics(solutions, optimal):
    """
    Compute all statistical metrics and aggregate them into a single Dataset.

    This function computes multiple performance metrics for each algorithm by comparing its solutions
    against the optimal solutions, and then aggregates the results into a comprehensive Dataset.

    Metrics Computed:

    1. **Relative Performance Ratio**:
       The ratio between the algorithm's solution and the optimal solution. A value of 1 indicates
       perfect performance, while higher values indicate deviation from the optimal solution.
    2. **Log-Scaled Performance**:
       A logarithmic transformation of the relative performance ratio. It highlights larger differences
       between the algorithm's solution and the optimal.
    3. **Percentage of Optimal Solutions Achieved**:
       The percentage of times the algorithm achieves the optimal solution across different seeds,
       indicating how often the algorithm performs optimally.
    4. **Scalability Slope**:
       The slope of the solution quality as the number of machines (`m`) increases. A negative slope
       suggests performance improvement with more machines, while a positive slope indicates
       performance deterioration.
    5. **Cumulative Improvement**:
       The incremental improvement in the solution quality as the number of machines increases,
       showing the gain in performance by increasing resources.
    6. **Consistency Metrics**:
       These include the standard deviation and variance of the algorithm's performance across seeds.
       Lower values indicate more stable performance across different runs.

    Parameters:
    - solutions (xr.DataArray): Dataset containing solutions at least with dimensions ['m', 'Seed'].
    - optimal (xr.DataArray): Optimal solution dataset with dimensions ['m', 'Seed'].

    Notes:
    - `solutions` usually has dimensions ['Algorithm', 'Generator', 'm', 'Seed'].
    - If 'Algorithm' is a dimension in `solutions`, it may be absent from the `optimal` data array.

    Returns:
    - xr.Dataset: A dataset containing all computed metrics. The dimensions will match those of the
                  `solutions` dataset, but the 'Seed' dimension will be aggregated (removed) since the
                  metrics represent summary statistics across seeds.

                  Metrics in the returned Dataset:
                  - 'Relative_Performance_Ratio'
                  - 'Log_Scaled_Performance'
                  - 'Percentage_Optimal_Solutions'
                  - 'Scalability_Slope'
                  - 'Cumulative_Improvement'
                  - 'Std_Solution' (from Consistency Metrics)
                  - 'Var_Solution' (from Consistency Metrics)
                  - 'Coefficient_of_Variation' (from Consistency Metrics)
    """
    relative_perf_ratio = relative_performance_ratio(solutions, optimal)
    log_scaled_perf = log_scaled_performance(solutions, optimal)
    consistency = consistency_metrics(solutions)
    percentage_opt = percentage_optimal(solutions, optimal)
    scalability_slope = scalability_metrics(solutions)
    cumulative_imp = cumulative_improvement(solutions)

    metrics_ds = xr.Dataset({
        'Relative_Performance_Ratio': relative_perf_ratio.mean(dim='Seed'),
        'Log_Scaled_Performance': log_scaled_perf.mean(dim='Seed'),
        'Percentage_Optimal_Solutions': percentage_opt,
        'Scalability_Slope': scalability_slope,
        'Cumulative_Improvement': cumulative_imp
    }).merge(consistency)

    return metrics_ds
