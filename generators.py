import numpy as np
from itertools import repeat


def constant(n):
    """
    Constant 1
    """
    return list(repeat(1, n))


def increasing(n):
    """
    +1 Increasing Weights
    """
    return range(1, n + 1)


def decreasing(n):
    """
    -1 Decreasing Weights
    """
    return increasing(n)[::-1]


def small_random(n, seed):
    """
    Small Random Weights
    """
    np.random.seed(seed)
    return np.random.randint(1, 101, size=n)


def small_span_large(n, seed):
    """
    Small Span Large Weights
    """
    return small_random(n, seed) + 10_000


def large_span_large(n, seed):
    """
    Large Span Large Weights
    """
    np.random.seed(seed)
    return np.random.randint(10_001, 1_000_001, size=n)


def low_then_high(n, seed):
    """
    Random Half Low, then Half High Weights
    e.g. [920, 912, 945, ..., 24, 94, 56]
    """
    a = small_random(n, seed)
    a[n // 2:] += 900
    return a


def high_then_low(n, seed):
    """
    Random Half High, then Half Low Weights
    e.g. [24, 94, 56, ..., 920, 912, 945]
    """
    return low_then_high(n, seed)[::-1]


def large_span_random_non_decreasing(n, seed):
    """
    Non-Decreasingly Sorted Large Span Random Weights
    """
    np.random.seed(seed)
    return np.sort(np.random.randint(1, 100_001, size=n))


def large_span_random_non_increasing(n, seed):
    """
    Non-Increasingly Sorted Large Span Random Weights
    """
    return large_span_random_increasing(n, seed)[::-1]


class Generator:
    def __init__(self, generator_function, name, is_random):
        self.gf = generator_function
        self.name = name
        self.is_random = is_random

    def __call__(self, n, seed=None):
        return self.gf(n, seed) if self.is_random else self.gf(n)


all = [(constant, "Constant", False),
       (increasing, "+1 Increasing", False),
       (decreasing, "-1 Decreasing", False),
       (small_random, "Random Small", True),
       (small_span_large, "Random Small Span Large", True),
       (large_span_large, "Random Large Span Large", True),
       (low_then_high, "Random Half Low, Half High", True),
       (high_then_low, "Random Half High, Half Low", True),
       (large_span_random_increasing,
        "Random Non-Decreasing Large Span", True),
       (large_span_random_decreasing,
        "Random Non-Increasing Large Span", True)]

generators = [Generator(*args) for args in all]
