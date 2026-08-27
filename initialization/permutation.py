import random
from individuals.permutation import PermutationIndividual


def create_permutation_initializer(n_elements: int):
    def initializer() -> PermutationIndividual:
        return PermutationIndividual(random.sample(range(n_elements), n_elements))

    return initializer