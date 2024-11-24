from queue import PriorityQueue as PQ

from algrotihms.base import Solver


class LeastLoaded(Solver):
    """
    Always select least loaded machine.
    """

    name = "Least Loaded"

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
