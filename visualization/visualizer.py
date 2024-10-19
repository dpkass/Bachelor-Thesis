"""
visualizer.py

Module containing higher-level helper functions for plotting specific statistical metrics using the plotter.

Functions:
- plot_relative_performance_ratio: Plot Relative Performance Ratio with multiple plot types.
- plot_log_scaled_performance: Plot Log-Scaled Performance with multiple plot types.
- plot_percentage_optimal_solutions: Plot Percentage of Optimal Solutions Achieved with multiple plot types.
- plot_scalability_slope: Plot Scalability Slope with multiple plot types.
- plot_cumulative_improvement: Plot Cumulative Improvement with multiple plot types.
- plot_consistency_metrics: Plot Consistency Metrics (Std_Solution and Var_Solution) with multiple plot types.
"""

import xarray as xr
from plotter import plot_line, plot_heatmap, plot_bar, plot_box, plot_scatter


def plot_relative_performance_ratio(
    metrics_ds: xr.Dataset,
    plot_type: str = "heatmap",
    **kwargs
):
    """
    Plot the Relative Performance Ratio using a specified plot type.

    **Relative Performance Ratio** indicates how an algorithm's solution compares to the optimal solution.
    A ratio of 1 signifies optimal performance, while values greater than 1 show deviations.

    Supported Plot Types:
    - "heatmap": Visualizes the ratio across Generators and Algorithms, faceted by number of machines (`m`).
    - "line": Shows the trend of the ratio with respect to the number of machines for each algorithm.
    - "bar": Compares the average ratio across Generators or Algorithms.
    - "box": Displays the distribution of ratios across different Algorithms.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Relative_Performance_Ratio'.
    - plot_type (str): Type of plot to generate ('heatmap', 'line', 'bar', 'box').
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plot using the chosen plot type.
    """
    if plot_type == "heatmap":
        plot_heatmap(
            data=metrics_ds,
            metric="Relative_Performance_Ratio",
            x="Generator",
            y="Algorithm",
            facet="m",
            title="Relative Performance Ratio Heatmap",
            xlabel="Generator",
            ylabel="Algorithm",
            **kwargs
        )
    elif plot_type == "line":
        plot_line(
            data=metrics_ds,
            metric="Relative_Performance_Ratio",
            x="m",
            hue="Algorithm",
            title="Relative Performance Ratio vs Number of Machines",
            xlabel="Number of Machines (m)",
            ylabel="Relative Performance Ratio",
            **kwargs
        )
    elif plot_type == "bar":
        plot_bar(
            data=metrics_ds,
            metric="Relative_Performance_Ratio",
            x="Algorithm",
            hue="Generator",
            title="Average Relative Performance Ratio by Algorithm and Generator",
            xlabel="Algorithm",
            ylabel="Average Relative Performance Ratio",
            **kwargs
        )
    elif plot_type == "box":
        plot_box(
            data=metrics_ds,
            metric="Relative_Performance_Ratio",
            x="Algorithm",
            title="Distribution of Relative Performance Ratio by Algorithm",
            xlabel="Algorithm",
            ylabel="Relative Performance Ratio",
            **kwargs
        )
    else:
        raise ValueError(f"Unsupported plot type '{plot_type}' for Relative Performance Ratio.")


def plot_log_scaled_performance(
    metrics_ds: xr.Dataset,
    plot_type: str = "heatmap",
    **kwargs
):
    """
    Plot the Log-Scaled Performance using a specified plot type.

    **Log-Scaled Performance** applies a logarithmic transformation to the Relative Performance Ratio,
    enhancing the visibility of large deviations from optimal performance.

    Supported Plot Types:
    - "heatmap": Visualizes log-scaled performance across Generators and Algorithms, faceted by number of machines (`m`).
    - "line": Shows the trend of log-scaled performance with respect to the number of machines for each algorithm.
    - "scatter": Examines the relationship between log-scaled performance and another metric.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Log_Scaled_Performance'.
    - plot_type (str): Type of plot to generate ('heatmap', 'line', 'scatter').
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plot using the chosen plot type.
    """
    if plot_type == "heatmap":
        plot_heatmap(
            data=metrics_ds,
            metric="Log_Scaled_Performance",
            x="Generator",
            y="Algorithm",
            facet="m",
            title="Log-Scaled Performance Heatmap",
            xlabel="Generator",
            ylabel="Algorithm",
            **kwargs
        )
    elif plot_type == "line":
        plot_line(
            data=metrics_ds,
            metric="Log_Scaled_Performance",
            x="m",
            hue="Algorithm",
            title="Log-Scaled Performance vs Number of Machines",
            xlabel="Number of Machines (m)",
            ylabel="Log-Scaled Performance",
            **kwargs
        )
    elif plot_type == "scatter":
        plot_scatter(
            data=metrics_ds,
            x_metric="Scalability_Slope",
            y_metric="Log_Scaled_Performance",
            hue="Algorithm",
            title="Log-Scaled Performance vs Scalability Slope",
            xlabel="Scalability Slope",
            ylabel="Log-Scaled Performance",
            **kwargs
        )
    else:
        raise ValueError(f"Unsupported plot type '{plot_type}' for Log-Scaled Performance.")


def plot_percentage_optimal_solutions(
    metrics_ds: xr.Dataset,
    plot_type: str = "bar",
    **kwargs
):
    """
    Plot the Percentage of Optimal Solutions Achieved using a specified plot type.

    **Percentage of Optimal Solutions Achieved** indicates the proportion of runs where an algorithm attained the optimal solution,
    reflecting its consistency and reliability.

    Supported Plot Types:
    - "bar": Compares the percentage across Algorithms and Generators.
    - "box": Displays the distribution of percentages across different Algorithms.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Percentage_Optimal_Solutions'.
    - plot_type (str): Type of plot to generate ('bar', 'box').
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plot using the chosen plot type.
    """
    if plot_type == "bar":
        plot_bar(
            data=metrics_ds,
            metric="Percentage_Optimal_Solutions",
            x="Generator",
            hue="Algorithm",
            title="Percentage of Optimal Solutions Achieved by Algorithm and Generator",
            xlabel="Algorithm",
            ylabel="Percentage of Optimal Solutions (%)",
            **kwargs
        )
    elif plot_type == "box":
        plot_box(
            data=metrics_ds,
            metric="Percentage_Optimal_Solutions",
            x="Algorithm",
            title="Distribution of Percentage of Optimal Solutions Achieved by Algorithm",
            xlabel="Algorithm",
            ylabel="Percentage of Optimal Solutions (%)",
            **kwargs
        )
    else:
        raise ValueError(
            f"Unsupported plot type '{plot_type}' for Percentage of Optimal Solutions Achieved.")


def plot_scalability_slope(
    metrics_ds: xr.Dataset,
    plot_type: str = "bar",
    **kwargs
):
    """
    Plot the Scalability Slope using a specified plot type.

    **Scalability Slope** measures how an algorithm's solution quality changes with the number of machines (`m`).
    A positive slope indicates improvement, while a negative slope signifies deterioration as `m` increases.

    Supported Plot Types:
    - "bar": Compares the scalability slope across Algorithms and Generators.
    - "scatter": Examines the relationship between scalability slope and another metric.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Scalability_Slope'.
    - plot_type (str): Type of plot to generate ('bar', 'scatter').
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plot using the chosen plot type.
    """
    if plot_type == "bar":
        plot_bar(
            data=metrics_ds,
            metric="Scalability_Slope",
            x="Algorithm",
            hue="Generator",
            title="Scalability Slope by Algorithm and Generator",
            xlabel="Algorithm",
            ylabel="Scalability Slope",
            **kwargs
        )
    elif plot_type == "scatter":
        plot_scatter(
            data=metrics_ds,
            x_metric="Scalability_Slope",
            y_metric="Relative_Performance_Ratio",
            hue="Algorithm",
            title="Scalability Slope vs Relative Performance Ratio",
            xlabel="Scalability Slope",
            ylabel="Relative Performance Ratio",
            **kwargs
        )
    else:
        raise ValueError(f"Unsupported plot type '{plot_type}' for Scalability Slope.")


def plot_cumulative_improvement(
    metrics_ds: xr.Dataset,
    plot_type: str = "line",
    **kwargs
):
    """
    Plot the Cumulative Improvement using a specified plot type.

    **Cumulative Improvement** shows the incremental improvement in solution quality as the number of machines (`m`) increases,
    highlighting the benefits of scaling resources.

    Supported Plot Types:
    - "line": Tracks the cumulative improvement across the number of machines for each algorithm.
    - "scatter": Visualizes individual improvement points.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Cumulative_Improvement'.
    - plot_type (str): Type of plot to generate ('line', 'scatter').
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plot using the chosen plot type.
    """
    if plot_type == "line":
        plot_line(
            data=metrics_ds,
            metric="Cumulative_Improvement",
            x="m",
            hue="Algorithm",
            title="Cumulative Improvement vs Number of Machines",
            xlabel="Number of Machines (m)",
            ylabel="Cumulative Improvement",
            **kwargs
        )
    elif plot_type == "scatter":
        plot_scatter(
            data=metrics_ds,
            x_metric="m",
            y_metric="Cumulative_Improvement",
            hue="Algorithm",
            title="Cumulative Improvement vs Number of Machines",
            xlabel="Number of Machines (m)",
            ylabel="Cumulative Improvement",
            **kwargs
        )
    else:
        raise ValueError(f"Unsupported plot type '{plot_type}' for Cumulative Improvement.")


def plot_consistency_metrics(
    metrics_ds: xr.Dataset,
    plot_type: str = "heatmap",
    plot_var: bool = False,
    **kwargs
):
    """
    Plot the Consistency Metrics (Std_Solution and Var_Solution) using specified plot types.

    **Consistency Metrics** (Standard Deviation and Variance) assess the variability and reliability of an algorithm's performance
    across different runs (seeds). Lower values indicate more consistent and reliable performance.

    Supported Plot Types:
    - "bar": Compares the standard deviation and variance across Algorithms and Generators.
    - "box": Displays the distribution of standard deviation and variance across Algorithms.

    Parameters:
    - metrics_ds (xr.Dataset): Aggregated Dataset containing 'Std_Solution' and 'Var_Solution'.
    - plot_type (str): Type of plot to generate ('heatmap', 'box').
    - plot_type (bool): Whether to create a plot for Variance.
    - **kwargs: Additional keyword arguments for the specific plot function.

    Returns:
    - None: Saves the plots using the chosen plot types.
    """
    if plot_type == "heatmap":
        plot_heatmap(
            data=metrics_ds,
            metric="Std_Solution",
            x="m",
            y="Algorithm",
            facet="Generator",
            title="Standard Deviation of Solutions by Algorithm and Generator",
            xlabel="Number of Machines (m)",
            ylabel="Algorithm",
            **kwargs
        )
        if plot_var:
            plot_heatmap(
                data=metrics_ds,
                metric="Var_Solution",
                x="m",
                y="",
                facet="Generator",
                title="Variance of Solutions by Algorithm and Generator",
                xlabel="Number of Machines (m)",
                ylabel="Algorithm",
                **kwargs
            )
    elif plot_type == "box":
        plot_box(
            data=metrics_ds,
            metric="Std_Solution",
            x="Algorithm",
            title="Distribution of Standard Deviation by Algorithm",
            xlabel="Algorithm",
            ylabel="Standard Deviation",
            **kwargs
        )
        if plot_var:
            plot_box(
                data=metrics_ds,
                metric="Var_Solution",
                x="Algorithm",
                title="Distribution of Variance by Algorithm",
                xlabel="Algorithm",
                ylabel="Variance",
                **kwargs
            )
    else:
        raise ValueError(f"Unsupported plot type '{plot_type}' for Consistency Metrics.")


if __name__ == "__main__":
    from data_loader import load_algorithm_data, load_optimal_solution
    from statistical_processor import compute_all_metrics

    algorithms_ds = load_algorithm_data()
    optimal_da = load_optimal_solution()

    metrics_ds = compute_all_metrics(algorithms_ds, optimal_da)

    plot_relative_performance_ratio(metrics_ds, plot_type="heatmap")
    # plot_log_scaled_performance(metrics_ds, plot_type="heatmap")
    # plot_percentage_optimal_solutions(metrics_ds, plot_type="bar")
    # plot_scalability_slope(metrics_ds, plot_type="scatter")
    # plot_cumulative_improvement(metrics_ds, plot_type="scatter")
    # plot_consistency_metrics(metrics_ds)
