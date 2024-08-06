import numpy as np

low = lambda n: np.random.randint(0, 100, size=n)
high = lambda n: np.random.randint(900, 1000, size=n)


def increasing(n):
    """
    +1 Increasing Weights

    :param n: Length of a
    :return: List of weights a
    """
    return range(n)


def decreasing(n):
    """
    -1 Decreasing Weights

    :param n: Length of a
    :return: List of weights a
    """
    return range(n)[::-1]


def small_random(n, seed):
    """
    Small Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.random.randint(0, 100, size=n)


def small_span_large(n, seed):
    """
    Small Span Large Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.random.randint(0, 100, size=n) + 10000


def large_span_large(n, seed):
    """
    Large Span Large Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.random.randint(10000, 1000000, size=n)


def low_then_high(n, seed):
    """
    Random Half Low, then Half High Weights
    e.g. [920, 912, 945, ..., 24, 94, 56]

    :param n: Size of a, if even: |a| = n, else: |a| = n - 1
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.concatenate([low(n // 2), high(n // 2)])


def high_then_low(n, seed):
    """
    Random Half High, then Half Low Weights
    e.g. [24, 94, 56, ..., 920, 912, 945]

    :param n: Size of a, if even: |a| = n, else: |a| = n - 1
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.concatenate([high(n // 2), low(n // 2)])


def large_random_increasing(n, seed):
    """
    Increasingly Sorted Large Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.sort(np.random.randint(1, 100000, size=n))


def large_random_decreasing(n, seed):
    """
    Decreasingly Sorted Large Random Weights

    :param n: Length of a
    :param seed: Reproducibility seed
    :return: List of weights a
    """
    np.random.seed(seed)
    return np.sort(np.random.randint(1, 100000, size=n))[::-1]


generators = [(increasing, "+1 Increasing Weights", False),
              (decreasing, "-1 Decreasing Weights", False),
              (small_random, "Small Random Weights", True),
              (small_span_large, "Small Span Large Weights", True),
              (large_span_large, "Large Span Large Weights", True),
              (low_then_high, "Random Half Low, then Half High Weights", True),
              (high_then_low, "Random Half High, then Half Low Weights", True),
              (large_random_increasing,
               "Increasingly Sorted Large Random Weights", True),
              (large_random_decreasing,
               "Decreasingly Sorted Large Random Weights", True)]
