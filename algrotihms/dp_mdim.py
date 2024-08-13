import numpy as np

from algrotihms.base import DP, dtype, dtype_max, inc


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
