import xarray as xr
from plotter import plot_heatmap, plot_bar, plot_line

interesting_rename_algos = {
    'DP': 'DP',
    'Least Loaded': 'Greedy',
    'Balanced Sequential Insert': 'BSI'
}

interesting_rename_gens = {
    '+1 Increasing': 'Non-Decreasing',
    '-1 Decreasing': 'Non-Increasing',
    'Random Small': 'Uniform Random',
    'Random Half Low, Half High': 'LoHi',
    'Random Half High, Half Low': 'HiLo',
}

interesting_algos_only = lambda ds: ds.sel(algorithm=list(interesting_rename_algos)).assign_coords(
    algorithm=list(interesting_rename_algos.values()))

interesting_gens_only = lambda ds: ds.sel(generator=list(interesting_rename_gens)).assign_coords(
    generator=list(interesting_rename_gens.values()))

interesting_only = lambda ds: interesting_algos_only(interesting_gens_only(ds))

random_only = lambda ds: ds.sel(generator=solutions.randomized)


def plot_relative_performance_ratio_heatmap_A_vs_G_per_m(metrics_ds: xr.Dataset, **kwargs):
    plot_heatmap(
        data=metrics_ds,
        metric="Relative_Performance_Ratio",
        x="generator",
        y="algorithm",
        facet="m",
        title="Relative Performance Ratio Heatmap (Algorithm vs Generator per Machine)",
        xlabel="Generator",
        ylabel="Algorithm",
        filename="RPR-HEAT-G-A-m.png",
        **kwargs
    )


def plot_relative_performance_ratio_heatmap_G_vs_m_per_A(metrics_ds: xr.Dataset, **kwargs):
    plot_heatmap(
        data=metrics_ds,
        metric="Relative_Performance_Ratio",
        x="m",
        y="generator",
        facet="algorithm",
        title="Relative Performance Ratio Heatmap (Generator vs Machines per Algorithm)",
        xlabel="Number of Machines (m)",
        ylabel="Generator",
        filename="RPR-HEAT-G-m-A.png",
        **kwargs
    )


def plot_variation_coefficient_bar_A_vs_G(metrics_ds: xr.Dataset, **kwargs):
    plot_bar(
        data=metrics_ds.sel(m=4),
        metric="Coefficient_of_Variation",
        x="generator",
        hue="algorithm",
        title="Variation Coefficient Bar Chart (Algorithm vs Generator)",
        xlabel="Generator",
        ylabel="Coefficient of Variation",
        filename="CV-BAR-A-G.png",
        **kwargs
    )


def plot_variation_coefficient_heatmap_A_vs_G_per_m(metrics_ds: xr.Dataset, **kwargs):
    plot_heatmap(
        data=metrics_ds,
        metric="Coefficient_of_Variation",
        x="generator",
        y="algorithm",
        facet="m",
        title="Variation Coefficient Heatmap (Algorithm vs Generator)",
        xlabel="Generator",
        ylabel="Algorithm",
        filename="CV-HEAT-A-G-m.png",
        **kwargs
    )


def plot_relative_improvement_line_A_vs_m(metrics_ds: xr.Dataset, **kwargs):
    plot_line(
        data=metrics_ds.mean("generator"),
        metric="Relative_Improvement",
        x="m",
        hue="algorithm",
        title="Relative Improvement from $m$ to $m+1$ Machines per Algorithm",
        xlabel="Number of Machines (m)",
        ylabel="Relative Improvement %",
        filename="RI-LINE-A-m.png",
        **kwargs
    )


def plot_all_metrics(metrics_ds: xr.Dataset, **kwargs):
    plot_relative_performance_ratio_heatmap_A_vs_G_per_m(metrics_ds, **kwargs)
    plot_relative_performance_ratio_heatmap_G_vs_m_per_A(metrics_ds, **kwargs)
    plot_variation_coefficient_bar_A_vs_G(random_only(metrics_ds), **kwargs)
    plot_variation_coefficient_heatmap_A_vs_G_per_m(random_only(metrics_ds), **kwargs)
    plot_relative_improvement_line_A_vs_m(interesting_algos_only(metrics_ds), **kwargs)


if __name__ == "__main__":
    from statistical_processor import compute_all_metrics

    solutions = xr.open_dataarray('./precomputed.nc')
    optimal_solution = solutions.sel(algorithm='DP')

    metrics_ds = compute_all_metrics(solutions, optimal_solution)

    plot_all_metrics(metrics_ds)
