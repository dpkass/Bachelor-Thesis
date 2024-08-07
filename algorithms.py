import numpy as np

from collections import defaultdict as dd
from queue import PriorityQueue as PQ

dtype = np.int64
dtype_max = np.iinfo(dtype).max

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


def inc(lst, i):
    tmp = list(lst)
    tmp[i] += 1
    return tuple(tmp)

class DP_MDIM(DP):
    """
    Normal DP with multidimensional array. Very Space intensive.
    """
    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = np.full([n + 1 // i for i in range(1, m + 1)], dtype=dtype, fill_value=dtype_max)

    def transform(self, a):
        curr_positions = self.init_positions()
        next_positions = set()

        for ai in a:
            for pos in curr_positions:
                for j in range(self.m):
                    if pos[j - 1] > pos[j] or j == 0:
                        npos = inc(pos, j)
                        self.dp[npos] = min(self.dp[npos], self.dp[pos] + npos[j] * ai)
                        next_positions.add(npos)
            curr_positions = next_positions.copy()
            next_positions.clear()

        return min(self.dp[i] for i in curr_positions)


class DP_DICT(DP):
    """
    DP with dict. Less Space intensive, but a minimally higher complexity.
    """
    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = dd(lambda: dtype_max)

    def transform(self, a):
        curr_positions = self.init_positions()
        next_positions = set()

        next_values = dd(lambda: dtype_max)

        for ai in a:
            for pos in curr_positions:
                for j in range(self.m):
                    if pos[j - 1] > pos[j] or j == 0:
                        npos = inc(pos, j)
                        next_values[npos] = min(next_values[npos], self.dp[pos] + npos[j] * ai)
                        next_positions.add(npos)

            curr_positions = next_positions.copy()
            next_positions.clear()

            self.dp = next_values.copy()
            next_values.clear()

        return min(self.dp[i] for i in curr_positions)


class Greedy(Solver):
    """
    Greedy. Linear complexity.
    """
    def fit(self, n, m):
        self.n, self.m = n, m
        self.pq = PQ(maxsize=m)
        for _ in range(m): self.pq.put((0, 0))

    def transform(self, a):
        for ai in a:
            sum_wc, i = self.pq.get()
            i += 1
            sum_wc += ai * i
            self.pq.put((sum_wc, i))

        sum_wc = 0
        while not self.pq.empty():
            partial_sum, _ = self.pq.get()
            sum_wc += partial_sum

        return sum_wc
