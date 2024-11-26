import xarray as xr
import numpy as np
from plotter import plot_heatmap, plot_bar, plot_line

interesting_algos = ['Least Loaded',
                     'Simple Sort & Split',
                     'Balanced Sequential Insert',
                     'Balanced Sequential Insert++']

algos_order = [
    'DP',
    'Least Loaded',
    'Heavy First',
    'Lookahead 5',
    'Lookahead 15',
    'Simple Sort & Split',
    'Balanced Sequential Insert',
    'Balanced Sequential Insert++'
]

rename_algos = {
    'DP': 'DP',
    'Least Loaded': 'Greedy',
    'Heavy First': 'Greedy',
    'Lookahead 5': 'L5',
    'Lookahead 15': 'L15',
    'Simple Sort & Split': 'S&S',
    'Balanced Sequential Insert': 'BSI',
    'Balanced Sequential Insert++': 'BSI++'
}

interesting_gens = [
    '+1 Increasing',
    '-1 Decreasing',
    'Random Small',
    'Random Half Low, Half High',
    'Random Half High, Half Low'
]

gens_order = [
    'Constant',
    'Random Small Span Large',
    '+1 Increasing',
    'Random Non-Decreasing Large Span',
    '-1 Decreasing',
    'Random Non-Increasing Large Span',
    'Random Small',
    'Random Large Span Large',
    'Random Half Low, Half High',
    'Random Half High, Half Low'
]

rename_gens = {
    'Constant': 'Constant',
    'Random Small Span Large': 'Constant',
    '+1 Increasing': 'Non-Decreasing',
    'Random Non-Decreasing Large Span': 'Non-Decreasing',
    '-1 Decreasing': 'Non-Increasing',
    'Random Non-Increasing Large Span': 'Non-Decreasing',
    'Random Small': 'Uniform Random',
    'Random Large Span Large': 'Uniform Random',
    'Random Half Low, Half High': 'LoHi',
    'Random Half High, Half Low': 'HiLo',
}


def sel_rename(ds, key, sel, rename):
    return ds.sel({key: sel}).assign_coords({key: [rename[x] for x in sel]})


def sel_algos(ds, sel): return sel_rename(ds, "algorithm", sel, rename_algos)


def sel_gens(ds, sel): return sel_rename(ds, "generator", sel, rename_gens)


def interesting_only(ds):
    return sel_algos(sel_gens(ds, interesting_gens), interesting_algos).drop_sel(m=1)


def random_only(ds): return ds.sel(generator=ds.randomized)


# Plotting functions
def plot_relative_performance_ratio_heatmap_G_vs_A_per_m(metrics_ds, **kwargs):
    plot_heatmap(
        data=metrics_ds.sel(m=[2, 4, 6]),
        metric="Relative_Performance_Ratio",
        x="algorithm",
        y="generator",
        facet="m",
        title="Relative Performance Ratio",
        xlabel="Algorithm",
        ylabel="Generator",
        nrows=1,
        filename="RPR-HEAT-G-A-m.png",
        **kwargs
    )


def plot_relative_performance_ratio_line_G_vs_A_per_m_interesting(metrics_ds, **kwargs):
    filtered_ds = interesting_only(metrics_ds).sel(m=[3, 4, 5])
    plot_line(
        data=filtered_ds,
        metric="Relative_Performance_Ratio",
        x="generator",
        hue="algorithm",
        style="m",
        title="Relative Performance Ratio",
        xlabel="Generator",
        ylabel="Relative Performance Ratio",
        filename="RPR-LINE-G-A-m-INTERESTING.png",
        **kwargs
    )


def plot_relative_performance_ratio_heatmap_G_vs_m_per_A_interesting(metrics_ds, **kwargs):
    filtered_ds = interesting_only(metrics_ds)
    plot_heatmap(
        data=filtered_ds,
        metric="Relative_Performance_Ratio",
        x="m",
        y="generator",
        facet="algorithm",
        title="Relative Performance Ratio",
        xlabel="Number of Machines (m)",
        ylabel="Generator",
        filename="RPR-HEAT-G-m-A-INTERESTING.png",
        nrows=1,
        figsize=(5, 3),
        **kwargs
    )


def plot_standard_deviation_bar_G_vs_A(metrics_ds, **kwargs):
    plot_bar(
        data=metrics_ds.sel(m=3).drop_sel(algorithm="DP"),
        metric="Standard_Deviation",
        x="generator",
        hue="algorithm",
        title="Standard Deviation of RPR ($m=5$)",
        xlabel="Generator",
        ylabel="Standard Deviation",
        filename="RPR_STD-BAR-G-A.png",
        percent=True,
        **kwargs
    )


def plot_relative_improvement_line_A_vs_m(metrics_ds, **kwargs):
    plot_line(
        data=metrics_ds.mean("generator").assign_coords(m=[f"${int(m)}\\rightarrow{int(m + 1)}$"
                                                           for m in metrics_ds.coords["m"]]),
        metric="Relative_Improvement",
        x="m",
        hue="algorithm",
        title="Relative Improvement from $m-1$ to $m$ Machines",
        xlabel="Number of Machines (m)",
        ylabel="Relative Improvement",
        filename="RI-LINE-A-m.png",
        percent=True,
        **kwargs
    )


def plot_all_metrics(metrics_ds, **kwargs):
    plot_relative_performance_ratio_heatmap_G_vs_A_per_m(metrics_ds, **kwargs)
    plot_relative_performance_ratio_heatmap_G_vs_m_per_A_interesting(metrics_ds, **kwargs)
    plot_relative_performance_ratio_line_G_vs_A_per_m_interesting(metrics_ds, **kwargs)
    plot_standard_deviation_bar_G_vs_A(random_only(metrics_ds), **kwargs)
    plot_relative_improvement_line_A_vs_m(sel_algos(metrics_ds, interesting_algos), **kwargs)


if __name__ == "__main__":
    from statistical_processor import compute_all_metrics

    solutions = xr.open_dataarray('./precomputed.nc')
    optimal_solution = solutions.sel(algorithm='DP')

    metrics_ds = compute_all_metrics(solutions, optimal_solution).reindex(algorithm=algos_order,
                                                                          generator=gens_order)

    plot_all_metrics(metrics_ds)
