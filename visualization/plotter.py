"""
plotter.py

Module to generate generalized and configurable plots for different statistical metrics using xarray datasets.

Functions:
- plot_line: Generate line plots.
- plot_heatmap: Generate heatmaps.
- plot_bar: Generate bar charts.
- plot_box: Generate box plots.
- plot_scatter: Generate scatter plots.
- plot_violin: Generate violin plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os
import xarray as xr


def plot_line(
    data: xr.Dataset,
    metric: str,
    x: str,
    hue: str = None,
    style: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    palette: str = "viridis",
    output_dir: str = "plots",
    filename: str = None,
    **kwargs
):
    """
    Generate a line plot for a specified metric.

    **Usage**:
    Ideal for visualizing how a metric changes with a continuous variable (e.g., number of machines `m`).

    Parameters:
    - data (xr.Dataset): Dataset containing the metric to plot.
    - metric (str): The metric variable name in the dataset.
    - x (str): The dimension to plot on the x-axis.
    - hue (str, optional): Dimension for color encoding (e.g., 'Algorithm').
    - style (str, optional): Dimension for line style encoding.
    - title (str, optional): Title of the plot.
    - xlabel (str, optional): Label for the x-axis.
    - ylabel (str, optional): Label for the y-axis.
    - palette (str, optional): Color palette for the plot.
    - output_dir (str, optional): Directory to save the plot.
    - filename (str, optional): Name of the saved plot file. If None, generated from metric and plot type.
    - **kwargs: Additional keyword arguments for Seaborn's lineplot.

    Returns:
    - None: Saves the plot to the specified directory.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=data.to_dataframe().reset_index(),
        x=x,
        y=metric,
        hue=hue,
        style=style,
        palette=palette,
        marker="o",
        **kwargs
    )
    plt.title(title or f"{metric} vs {x}")
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or metric)
    plt.legend(title=hue if hue else "")
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filename = filename or f"{metric}_line_plot.png"

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def plot_heatmap(
    data: xr.Dataset,
    metric: str,
    x: str,
    y: str,
    facet: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    cmap: str = "YlGnBu",
    annot: bool = True,
    fmt: str = ".2f",
    output_dir: str = "plots",
    filename: str = None,
    **kwargs
):
    """
    Generate a heatmap for a specified metric.

    **Usage**:
    Ideal for visualizing the relationship between two categorical variables and the corresponding metric value.

    Parameters:
    - data (xr.Dataset): Dataset containing the metric to plot.
    - metric (str): The metric variable name in the dataset.
    - x (str): The dimension to plot on the x-axis.
    - y (str): The dimension to plot on the y-axis.
    - facet (str, optional): Dimension to create separate heatmaps (e.g., 'Algorithm').
    - title (str, optional): Title of the plot.
    - xlabel (str, optional): Label for the x-axis.
    - ylabel (str, optional): Label for the y-axis.
    - cmap (str, optional): Colormap for the heatmap.
    - annot (bool, optional): Whether to annotate the heatmap with metric values.
    - fmt (str, optional): String formatting code for annotations.
    - output_dir (str, optional): Directory to save the plot.
    - filename (str, optional): Name of the saved plot file. If None, generated from metric and plot type.
    - **kwargs: Additional keyword arguments for Seaborn's heatmap.

    Returns:
    - None: Saves the plot to the specified directory.
    """
    if facet:
        unique_facets = data.coords[facet].values
        num_facets = len(unique_facets)
        plt.figure(figsize=(8 * num_facets, 6))
        for i, facet_val in enumerate(unique_facets, 1):
            plt.subplot(1, num_facets, i)
            subset = data.sel({facet: facet_val})[metric].to_dataframe().reset_index()
            pivot_table = subset.pivot(index=y, columns=x, values=metric)
            sns.heatmap(
                pivot_table,
                annot=annot,
                fmt=fmt,
                cmap=cmap,
                cbar=True,
                **kwargs
            )
            plt.title(f"{facet}: {facet_val}")
            plt.xlabel(xlabel or x)
            plt.ylabel(ylabel or y)
        plt.suptitle(title or f"{metric} Heatmap Faceted by {facet}", fontsize=16)
    else:
        plt.figure(figsize=(10, 8))
        subset = data[metric].to_dataframe().reset_index()
        pivot_table = subset.pivot(index=y, columns=x, values=metric)
        sns.heatmap(
            pivot_table,
            annot=annot,
            fmt=fmt,
            cmap=cmap,
            cbar=True,
            **kwargs
        )
        plt.title(title or f"{metric} Heatmap")
        plt.xlabel(xlabel or x)
        plt.ylabel(ylabel or y)

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filename = filename or f"{metric}_heatmap.png"

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def plot_bar(
    data: xr.Dataset,
    metric: str,
    x: str,
    hue: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    palette: str = "viridis",
    output_dir: str = "plots",
    filename: str = None,
    ci: float = 95,
    **kwargs
):
    """
    Generate a bar chart for a specified metric.

    **Usage**:
    Ideal for comparing average metric values across categories (e.g., algorithms, generators).

    Parameters:
    - data (xr.Dataset): Dataset containing the metric to plot.
    - metric (str): The metric variable name in the dataset.
    - x (str): The categorical dimension to plot on the x-axis.
    - hue (str, optional): Dimension for color encoding (e.g., 'Algorithm').
    - title (str, optional): Title of the plot.
    - xlabel (str, optional): Label for the x-axis.
    - ylabel (str, optional): Label for the y-axis.
    - palette (str, optional): Color palette for the plot.
    - output_dir (str, optional): Directory to save the plot.
    - filename (str, optional): Name of the saved plot file. If None, generated from metric and plot type.
    - ci (float, optional): Size of confidence intervals to draw around estimated values.
    - **kwargs: Additional keyword arguments for Seaborn's barplot.

    Returns:
    - None: Saves the plot to the specified directory.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=data.to_dataframe().reset_index(),
        x=x,
        y=metric,
        hue=hue,
        palette=palette,
        ci=ci,
        **kwargs
    )
    plt.title(title or f"{metric} Bar Chart")
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or metric)
    plt.legend(title=hue if hue else "")
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filename = filename or f"{metric}_bar_chart.png"

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def plot_box(
    data: xr.Dataset,
    metric: str,
    x: str,
    hue: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    palette: str = "viridis",
    output_dir: str = "plots",
    filename: str = None,
    **kwargs
):
    """
    Generate a box plot for a specified metric.

    **Usage**:
    Ideal for visualizing the distribution and variability of a metric across different categories.

    Parameters:
    - data (xr.Dataset): Dataset containing the metric to plot.
    - metric (str): The metric variable name in the dataset.
    - x (str): The categorical dimension to plot on the x-axis.
    - hue (str, optional): Dimension for color encoding (e.g., 'Algorithm').
    - title (str, optional): Title of the plot.
    - xlabel (str, optional): Label for the x-axis.
    - ylabel (str, optional): Label for the y-axis.
    - palette (str, optional): Color palette for the plot.
    - output_dir (str, optional): Directory to save the plot.
    - filename (str, optional): Name of the saved plot file. If None, generated from metric and plot type.
    - **kwargs: Additional keyword arguments for Seaborn's boxplot.

    Returns:
    - None: Saves the plot to the specified directory.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=data.to_dataframe().reset_index(),
        x=x,
        y=metric,
        hue=hue,
        palette=palette,
        **kwargs
    )
    plt.title(title or f"{metric} Box Plot")
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or metric)
    plt.legend(title=hue if hue else "")
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filename = filename or f"{metric}_box_plot.png"

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def plot_scatter(
    data: xr.Dataset,
    x_metric: str,
    y_metric: str,
    hue: str = None,
    size: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    palette: str = "viridis",
    size_palette: str = "viridis",
    output_dir: str = "plots",
    filename: str = None,
    **kwargs
):
    """
    Generate a scatter plot for two specified metrics.

    **Usage**:
    Ideal for examining the relationship between two numerical metrics (e.g., Relative Performance Ratio vs. Optimality Gap).

    Parameters:
    - data (xr.Dataset): Dataset containing the metrics to plot.
    - x_metric (str): The metric variable name for the x-axis.
    - y_metric (str): The metric variable name for the y-axis.
    - hue (str, optional): Dimension for color encoding (e.g., 'Algorithm').
    - size (str, optional): Dimension for size encoding (e.g., 'Generator').
    - title (str, optional): Title of the plot.
    - xlabel (str, optional): Label for the x-axis.
    - ylabel (str, optional): Label for the y-axis.
    - palette (str, optional): Color palette for the plot.
    - size_palette (str, optional): Color palette for size encoding.
    - output_dir (str, optional): Directory to save the plot.
    - filename (str, optional): Name of the saved plot file. If None, generated from metric and plot type.
    - **kwargs: Additional keyword arguments for Seaborn's scatterplot.

    Returns:
    - None: Saves the plot to the specified directory.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=data.to_dataframe().reset_index(),
        x=x_metric,
        y=y_metric,
        hue=hue,
        size=size,
        palette=palette,
        sizes=(20, 200),
        alpha=0.7,
        **kwargs
    )
    plt.title(title or f"{y_metric} vs {x_metric} Scatter Plot")
    plt.xlabel(xlabel or x_metric)
    plt.ylabel(ylabel or y_metric)
    plt.legend(title=hue if hue else "")
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filename = filename or f"{y_metric}_vs_{x_metric}_scatter_plot.png"

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()
