import numpy as np
from collections import defaultdict as dd
from queue import PriorityQueue as PQ

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

    def fit_transform(self, n, m, y) -> int:
        self.fit(n, m)
        return self.transform(y)


class DP(Solver):
    def __init__(self):
        super().__init__()
        self.dp = None

    def init_positions(self):
        root = tuple([0] * self.m)
        self.dp[root] = 0
        return [root]


class DP_MDIM(DP):
    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = np.full([n + 1 // i for i in range(1, m + 1)], dtype=dtype, fill_value=dtype_max)

    def transform(self, w):
        curr_positions = self.init_positions()
        next_positions = set()

        for wi in w:
            for pos in curr_positions:
                for j in range(self.m):
                    if pos[j - 1] > pos[j] or j == 0:
                        npos = inc(pos, j)
                        self.dp[npos] = min(self.dp[npos], self.dp[pos] + npos[j] * wi)
                        next_positions.add(npos)
            curr_positions = next_positions.copy()
            next_positions.clear()

        return self.dp, min(self.dp[i] for i in curr_positions)


class DP_DICT(DP):
    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = dd(lambda: dtype_max)

    def transform(self, w):
        curr_positions = self.init_positions()
        next_positions = set()

        next_values = dd(lambda: dtype_max)

        for wi in w:
            for pos in curr_positions:
                for j in range(self.m):
                    if pos[j - 1] > pos[j] or j == 0:
                        npos = inc(pos, j)
                        next_values[npos] = min(next_values[npos], self.dp[pos] + npos[j] * wi)
                        next_positions.add(npos)

            curr_positions = next_positions.copy()
            next_positions.clear()

            self.dp = next_values.copy()
            next_values.clear()

        return min(self.dp[i] for i in curr_positions)


class Greedy(Solver):
    def fit(self, n, m):
        self.n, self.m = n, m
        self.pq = PQ(maxsize=m)
        for _ in range(m): self.pq.put((0, 0))

    def transform(self, w):
        for wi in w:
            sum_wc, i = self.pq.get()
            i += 1
            sum_wc += wi * i
            self.pq.put((sum_wc, i))

        sum_wc = 0
        while not self.pq.empty():
            partial_sum, _ = self.pq.get()
            sum_wc += partial_sum

        return sum_wc


def run(wf, seed=0):
    np.random.seed(seed)
    w = wf()

    dp_dict = DP_DICT()
    greedy = Greedy()

    dp = dp_dict.fit_transform(n, m, w)
    gdy = greedy.fit_transform(n, m, w)

    return gdy / dp


run_mean = lambda w: sum(run(w, i) for i in range(10)) / 10

n = 150
m = 4

low = np.random.randint(0, 100, size=n // 2)
high = np.random.randint(900, 1000, size=n // 2)

w1 = lambda: range(n)  # 1.182, 1.260, 1.303
w2 = lambda: range(n)[::-1]  # 1
w3 = lambda: np.random.randint(0, 100, size=n)  # 1.199, 1.273, 1.316
w4 = lambda: np.random.randint(0, 100, size=n) + 10000  # 1.0007, 1.0009, 1.001
w5 = lambda: np.random.randint(10000, 1000000, size=n)  # 1.182, 1.261, 1.298
w6 = lambda: np.concatenate((low, high))  # 1.452, 1.830, 1.949
w7 = lambda: np.concatenate((high, low))  # 1.012, 1.014, 1.023
w8 = lambda: np.sort(np.random.randint(1, 100000, size=n))  # 1.180, 1.254, 1.299
w9 = lambda: np.sort(np.random.randint(1, 100000, size=n))[::-1]  # 1.0000005, 1.0000005, 1.000001
ws = [w1, w2, w3, w4, w5, w6, w7, w8, w9]

for w in ws: print(run_mean(w))

