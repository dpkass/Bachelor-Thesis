from algrotihms.base import Solver, decorate_sort

from sortedcontainers import SortedList


class BalancedSequentialInsert(Solver):
    """
    Distribute a set of jobs across multiple machines in a sequential manner, aiming to balance
    the total completion time across all machines.

    Process:
    1. Sort the jobs in non-increasing order based on their weights.
    2. Begin by inserting the highest-weighted job(s) onto the first machine.
    3. Sequentially, attempt to balance the load:
        - For each subsequent machine, add jobs until the completion time on the current machine
          exceeds that of the previous one.
        - Continue this process for all machines.
    4. If jobs remain after reaching the last machine, the algorithm will reset and try adding
    more jobs on the first machine.

    This method is a greedy heuristic that aims to minimize the overall imbalance in completion
    times across machines, making it particularly useful when the goal is to achieve an evenly
    distributed workload.

    Returns:
    - The target function across all machines once the jobs are distributed.
    """

    name = "Balanced Sequential Insert"

    def __init__(self):
        super().__init__()
        self.ms = None
        self.t = lambda vs: Solver.t(vs, lambda v: v[1])

    def fit(self, n, m):
        self.n, self.m = n, m
        self.ms = [SortedList() for _ in range(m)]

    def transform(self, a) -> int:
        a = decorate_sort(a)

        i = 1
        while not self.iterate(a, i): i += 1

        return sum(self.t(m) for m in self.ms)

    def iterate(self, a, i):
        self._reset()
        self.ms[0].update(a[:i])
        t_m0 = self.t(self.ms[0])

        for m in self.ms[1:]:
            while self.t(m) < t_m0 and i < self.n:
                m.add(a[i])
                i += 1

        return i == self.n

    def _reset(self):
        for m in self.ms: m.clear()
