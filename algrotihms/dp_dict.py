from collections import defaultdict as dd

from algrotihms.base import DP, dtype_max, inc


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
