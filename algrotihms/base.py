from collections import defaultdict
from typing import Iterable

import numpy as np

dtype = np.uint64
dtype_max = np.iinfo(dtype).max


def inc(it, i):
    tmp = list(it)
    tmp[i] += 1
    return tuple(tmp)


def w_sum(vs: Iterable[int | tuple], key=None) -> int:
    return sum(i * (key(n) if key else n) for i, n in enumerate(vs, 1))


class Solver:
    name = "Unknown"

    t = w_sum

    def __init__(self):
        self.n = None
        self.m = None

    def fit(self, n, m): pass

    def transform(self, y) -> int: pass

    def fit_transform(self, m, a) -> int:
        self.fit(len(a), m)
        return self.transform(a)


class DP(Solver):
    name = "DP"

    def __init__(self):
        super().__init__()
        self.dp = None
        self.positions = None

    def init_positions(self):
        root = tuple([0] * self.m)
        self.dp[root] = 0
        self.positions = [root]

    def step(self, ai, values=None, positions=None):
        if values is None: values = self.dp
        if positions is None: positions = self.positions

        next_values = defaultdict(lambda: dtype_max)
        next_positions = set()

        for pos in positions:
            for j in range(len(pos)):
                if pos[j] < pos[j - 1] or j == 0:
                    npos = inc(pos, j)
                    next_values[npos] = min(next_values[npos], values[pos] + npos[j] * ai)
                    next_positions.add(npos)

        positions[:] = list(next_positions)

        return next_values
