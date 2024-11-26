import xarray as xr


def relative_performance_ratio(solutions, optimal):
    return solutions / optimal


def standard_deviation(solutions):
    solutions = solutions.sel(generator=solutions.randomized)
    return solutions.std(dim="seed")


def relative_improvement(solutions):
    return -1 * solutions.diff(dim="m", label="lower") / solutions


def compute_all_metrics(solutions, optimal):
    rpr = relative_performance_ratio(solutions, optimal)
    std = standard_deviation(rpr)
    rel_imp = relative_improvement(solutions)

    return xr.Dataset({
        "Relative_Performance_Ratio": rpr.mean(dim="seed"),
        "Standard_Deviation": std.drop_vars("randomized"),
        "Relative_Improvement": rel_imp.mean(dim="seed"),
    })
