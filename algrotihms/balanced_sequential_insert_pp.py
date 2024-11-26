from algrotihms.base import Solver, decorate_sort

from sortedcontainers import SortedList
from math import ceil


def ternary(a, lo, hi):
    while hi - lo > 2:
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3
        if a[mid1] < a[mid2]:
            hi = mid2
        else:
            lo = mid1
    return min([(a[lo], lo), (a[lo + 1], lo + 1), (a[hi], hi + 1)])


class CompletionTimeList:
    def __init__(self, t, ms, low, high):
        self.t = t
        self.ms = ms
        self.a = None
        self._cache = {}
        self.low, self.high = low, high
        self.len = high - low + 1

    def __len__(self):
        return self.len

    def accept(self, a):
        self.a = a

    def __getitem__(self, i):
        return self._cache[i] if i in self._cache else self._simulate(i)

    def __iter__(self):
        for i in range(self.low, self.high + 1): yield self[i]

    def _simulate(self, i):
        self._reset()

        self.ms[0].update(self.a[:i])
        t_m0 = self.t(self.ms[0])

        for m in self.ms[1:]:
            while self.t(m) < t_m0 and i < len(self.a):
                m.add(self.a[i])
                i += 1

        return sum(map(self.t, self.ms)) if i == len(self.a) else float('inf')

    def _reset(self):
        for m in self.ms:
            m.clear()


class BalancedSequentialInsertPP(Solver):
    name = "Balanced Sequential Insert++"

    def __init__(self):
        super().__init__()
        self.ms, self.ctl = None, None
        self.low, self.high = None, None
        self.t = lambda vs: Solver.t(vs, lambda v: v[1])

    def fit(self, n, m):
        self.low, self.high = 1, ceil(n / m)
        ms = [SortedList() for _ in range(m)]
        self.ctl = CompletionTimeList(self.t, ms, self.low, self.high)

    def transform(self, a) -> int:
        self.ctl.accept(decorate_sort(a))
        min_total_time, best_i = ternary(self.ctl, self.low, self.high)
        return min_total_time
