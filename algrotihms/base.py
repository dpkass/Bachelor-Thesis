import numpy as np

dtype = np.int64
dtype_max = np.iinfo(dtype).max


def inc(lst, i):
    tmp = list(lst)
    tmp[i] += 1
    return tuple(tmp)


class Solver:
    def __init__(self):
        self.n = None
        self.m = None

    def fit(self, n, m): pass

    def transform(self, y) -> int: pass

    def fit_transform(self, m, a) -> int:
        self.fit(len(a), m)
        return self.transform(a)


class DP(Solver):
    def __init__(self):
        super().__init__()
        self.dp = None

    def init_positions(self):
        root = tuple([0] * self.m)
        self.dp[root] = 0
        return [root]
