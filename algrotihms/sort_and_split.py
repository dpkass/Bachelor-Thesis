from algrotihms.base import Solver

from sortedcontainers import SortedList

import numpy as np


def partition(lst, m):
    ps = np.array_split(lst, m)
    ms = [SortedList(map(tuple, p)) for p in ps]
    return [[int(j[1]) for j in m] for m in ms]


class SimpleSortAndSplit(Solver):
    """
    Decreasingly Sort, then split into equally sized subarrays.
    """

    name = "Simple Sort & Split"

    def fit(self, n, m):
        self.n, self.m = n, m

    def transform(self, a):
        machines = partition(sorted(enumerate(a), key=lambda v: v[1]), self.m)
        return sum(Solver.t(m) for m in machines)
