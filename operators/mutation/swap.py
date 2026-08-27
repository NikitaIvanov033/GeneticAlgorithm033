from typing import List
import random
from core.config import GAConfig
from individuals.permutation import PermutationIndividual


def swap_mutation(
        offspring: List[PermutationIndividual],
        config: GAConfig
) -> List[PermutationIndividual]:
    for individual in offspring:
        if random.random() < config.mutation_rate:
            n = len(individual)
            if n > 1:
                i, j = random.sample(range(n), 2)

                individual.chromosome[i], individual.chromosome[j] = individual.chromosome[j], individual.chromosome[i]

    return offspring