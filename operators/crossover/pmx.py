from typing import List
import random
from core.config import GAConfig
from individuals.permutation import PermutationIndividual


def pmx_crossover(
        parents: List[PermutationIndividual],
        config: GAConfig
) -> List[PermutationIndividual]:
    offspring = []
    pop_size = len(parents)

    for i in range(0, pop_size, 2):
        if i + 1 >= pop_size:
            offspring.append(parents[i].copy())
            break

        p1 = parents[i]
        p2 = parents[i + 1]

        if random.random() < config.crossover_rate:
            child1, child2 = _pmx(p1, p2)
            offspring.extend([child1, child2])
        else:
            offspring.extend([p1.copy(), p2.copy()])

    return offspring


def _pmx(
        p1: PermutationIndividual,
        p2: PermutationIndividual
) -> tuple[PermutationIndividual, PermutationIndividual]:
    n = len(p1)

    if n < 2:
        return p1.copy(), p2.copy()

    a, b = sorted(random.sample(range(n), 2))

    child1 = [-1] * n
    child2 = [-1] * n

    child1[a:b] = p1.chromosome[a:b]
    child2[a:b] = p2.chromosome[a:b]

    for i in range(n):
        if a <= i < b:
            continue

        val = p2.chromosome[i]

        while val in child1:
            pos_p1 = p1.chromosome.index(val)
            val = p2.chromosome[pos_p1]

        child1[i] = val

    for i in range(n):
        if a <= i < b:
            continue

        val = p1.chromosome[i]

        while val in child2:
            pos_p2 = p2.chromosome.index(val)
            val = p1.chromosome[pos_p2]

        child2[i] = val

    return PermutationIndividual(child1), PermutationIndividual(child2)