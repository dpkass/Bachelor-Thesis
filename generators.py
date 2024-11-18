import numpy as np


def increasing(n):
    """
    +1 Increasing Weights

    :param n: Length of a
    :return: List of Weights a
    """
    return range(1, n + 1)


def decreasing(n):
    """
    -1 Decreasing Weights

    :param n: Length of a
    :return: List of Weights a
    """
    return increasing(n)[::-1]


def small_random(n, seed):
    """
    Small Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    np.random.seed(seed)
    return np.random.randint(1, 100, size=n)


def small_span_large(n, seed):
    """
    Small Span Large Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    return small_random(n, seed) + 100000


def large_span_large(n, seed):
    """
    Large Span Large Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    np.random.seed(seed)
    return np.random.randint(10000, 1000000, size=n)


def low_then_high(n, seed):
    """
    Random Half Low, then Half High Weights
    e.g. [920, 912, 945, ..., 24, 94, 56]

    :param n: Size of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    a = small_random(n, seed)
    a[n // 2:] += 900
    return a


def high_then_low(n, seed):
    """
    Random Half High, then Half Low Weights
    e.g. [24, 94, 56, ..., 920, 912, 945]

    :param n: Size of a, if even: |a| = n, else: |a| = n - 1
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    return low_then_high(n, seed)[::-1]


def large_span_random_increasing(n, seed):
    """
    Increasingly Sorted Large Span Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    np.random.seed(seed)
    return np.sort(np.random.randint(1, 100000, size=n))


def large_span_random_decreasing(n, seed):
    """
    Decreasingly Sorted Large Span Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of Weights a
    """
    return large_span_random_increasing(n, seed)[::-1]


class Generator:
    def __init__(self, generator_function, name, is_random):
        self.gf = generator_function
        self.name = name
        self.is_random = is_random

    def __call__(self, n, seed=None):
        return self.gf(n, seed) if self.is_random else self.gf(n)


all = [(increasing, "+1 Increasing Weights", False),
       (decreasing, "-1 Decreasing Weights", False),
       (small_random, "Small Random Weights", True),
       (small_span_large, "Small Span Large Weights", True),
       (large_span_large, "Large Span Large Weights", True),
       (low_then_high, "Random Half Low, then Half High Weights", True),
       (high_then_low, "Random Half High, then Half Low Weights", True),
       (large_span_random_increasing,
        "Increasingly Sorted Large Span Random Weights", True),
       (large_span_random_decreasing,
        "Decreasingly Sorted Large Span Random Weights", True)]

generators = [Generator(*args) for args in all]
