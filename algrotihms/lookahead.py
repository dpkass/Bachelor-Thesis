from collections import defaultdict

from algrotihms.base import DP, dtype_max


class Lookahead(DP):
    """
    Greedy with DP based lookahead.
    """

    def __init__(self, k):
        super(Lookahead, self).__init__()
        self.k = k
        self.__class__.__name__ = f"Lookahead {k}"

    def fit(self, n, m):
        self.n, self.m = n, m
        self.dp = defaultdict(lambda: dtype_max)

    def transform(self, a):
        self.init_positions()
        pos = self.positions[0]

        for i, ai in enumerate(a):
            self.positions = [pos]
            step_dp = self.step(ai)

            best = dtype_max
            for pos_option, target in step_dp.items():
                self.positions = [pos_option]
                dp = {pos_option: target}
                for w in a[i + 1:min(i + self.k, len(a))]: dp = self.step(w, dp)

                result = min(dp.values())
                if result < best:
                    pos = pos_option
                    best = result

            self.dp[pos] = step_dp[pos]

        return self.dp[pos]
