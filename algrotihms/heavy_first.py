from algrotihms.base import Solver, decorate_sort

from sortedcontainers import SortedList


class HeavyFirst(Solver):
    """
    Decreasingly Sort a by weight then greedily insert to best position.
    """

    name = "Heavy First"

    def __init__(self):
        super().__init__()
        self.v = None
        self.t = lambda vs: Solver.t(vs, lambda v: v[1])

    def fit(self, n, m):
        self.n, self.m = n, m
        self.v = [SortedList() for _ in range(m)]

    def step(self, value):
        best_index = None
        best_diff = float('inf')

        for i, slist in enumerate(self.v):
            trial_list = SortedList(slist)
            trial_list.add(value)

            diff = self.t(trial_list) - self.t(slist)

            if diff < best_diff:
                best_diff = diff
                best_index = i

        self.v[best_index].add(value)

    def transform(self, a):
        for ai in decorate_sort(a): self.step(ai)
        return sum(self.t(machine) for machine in self.v)
