import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns

import os

import xarray as xr

from math import ceil


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
    percent: bool = False,
    **kwargs
):
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=data.to_dataframe().reset_index(),
        x=x,
        y=metric,
        hue=hue,
        style=style,
        palette=palette,
        marker="o",
        errorbar=None,
        **kwargs
    )
    if percent: plt.gca().yaxis.set_major_formatter(PercentFormatter(1, 0))
    plt.title(title or f"{metric} vs {x}")
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or metric)
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
    figsize: tuple = (8, 6),
    nrows: int = None,
    **kwargs
):
    x_order = data.coords[x].values
    y_order = data.coords[y].values

    if facet:
        unique_facets = data.coords[facet].values
        num_facets = len(unique_facets)
        nrows = nrows or num_facets
        ncols = ceil(num_facets / nrows)
        plt.figure(figsize=(figsize[0] * ncols, figsize[1] * nrows))
        for i, facet_val in enumerate(unique_facets, 1):
            plt.subplot(nrows, ncols, i)
            subset = data.sel({facet: facet_val})[metric].to_dataframe().reset_index()
            pivot_table = subset.pivot(index=y, columns=x, values=metric)
            pivot_table = pivot_table.reindex(index=y_order, columns=x_order)
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
        pivot_table = pivot_table.reindex(index=y_order, columns=x_order)
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
    percent: bool = False,
    **kwargs
):
    plt.figure(figsize=(14, 6))
    sns.barplot(
        data=data.to_dataframe().reset_index(),
        x=x,
        y=metric,
        hue=hue,
        palette=palette,
        errorbar=("ci", ci),
        **kwargs
    )
    if percent: plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.title(title or f"{metric} Bar Chart")
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or metric)
    plt.xticks(rotation=45, ha="right")
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
