from generators import generators as gs


def generate_seeded(g, n, seeds):
    """
    Generate Lists of Weights for given seeds. If it is not random generate
    just once.

    :param g: Supplier function (Generator), that generates a's
    :param n: Length of a's
    :param seeds: Reproducibility Seeds or Falsy if not random
    :return: List of generated a's
    """
    if not seeds: return [g(n)]

    return [g(n, seed) for seed in seeds]


def generate(n=150, seeds=range(10)):
    """
    Generate Lists of Weights for all generators and given seeds.

    :param n: Length of a's. Defaults to 150.
    :param seeds: Reproducibility Seeds. Defaults to [0, ..., 9]
    :return: List of tuples of Lists of a's and their description
    """
    return [(generate_seeded(g, n, seeds if is_random else None), desc)
            for (g, desc, is_random) in gs]
