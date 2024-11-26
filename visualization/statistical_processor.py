import xarray as xr


def relative_performance_ratio(solutions, optimal):
    return solutions / optimal


def coefficient_of_variation(solutions):
    solutions = solutions.sel(generator=solutions.randomized)
    return solutions.std(dim="seed") / solutions.mean(dim="seed")


def relative_improvement(solutions):
    return -1 * solutions.diff(dim="m", label="lower") / solutions


def compute_all_metrics(solutions, optimal):
    rpr = relative_performance_ratio(solutions, optimal)
    cv = coefficient_of_variation(rpr)
    rel_imp = relative_improvement(solutions)

    return xr.Dataset({
        "Relative_Performance_Ratio": rpr.mean(dim="seed"),
        "Coefficient_of_Variation": cv.drop_vars("randomized"),
        "Relative_Improvement": rel_imp.mean(dim="seed"),
    })
