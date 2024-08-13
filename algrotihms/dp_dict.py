from collections import defaultdict

from algrotihms.base import DP, dtype_max


class DP_DICT(DP):
    """
    DP with dict. Less Space intensive, but a minimally higher complexity.
    """

    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = defaultdict(lambda: dtype_max)

    def transform(self, a):
        self.init_positions()
        for ai in a: self.dp = self.step(ai)
        return min(self.dp[i] for i in self.positions)
