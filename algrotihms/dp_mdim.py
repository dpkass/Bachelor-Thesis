import numpy as np

from math import ceil

from algrotihms.base import DP, dtype, dtype_max


class DP_MDIM(DP):
    """
    Normal DP with multidimensional array. Very Space intensive.
    """

    name = 'Multidimensional DP'

    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = np.full([ceil((n + 1) / i) for i in range(1, m + 1)], dtype=dtype, fill_value=dtype_max)

    def transform(self, a):
        self.init_positions()

        for ai in a:
            next_values = self.step(ai)
            for k, v in next_values.items(): self.dp[k] = v

        return min(self.dp[i] for i in self.positions)
