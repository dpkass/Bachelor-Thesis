from algrotihms import *

import xarray as xr


def compare():
    with xr.open_dataarray('../precomputed.nc') as solutions:
        bsi = solutions.sel(algorithm='Balanced Sequential Insert')
        bsipp = solutions.sel(algorithm='Balanced Sequential Insert++')
        print(bsi.where(bsipp > bsi, drop=True).coords)
        print(bsi.where(bsipp > bsi, drop=True).values.squeeze())
        print(bsipp.where(bsipp > bsi, drop=True).values.squeeze())


def local_compare():
    import generators
    import matplotlib.pyplot as plt

    alg = BalancedSequentialInsertPP()
    alg.fit(150, 2)

    faulty1 = generators.small_random(150, 5)
    faulty2 = generators.small_random(150, 8)

    for faulty in map(lambda x: generators.small_random(150, x), range(10)):
        alg.transform(faulty)
        plt.plot(range(len(alg.ctl)), alg.ctl)
        plt.show()

    # Not Unimodal :(


if __name__ == "__main__": local_compare()
