from typing import List
import random
from core.config import GAConfig
from individuals.permutation import PermutationIndividual
from .base import pair_wise_crossover


def pmx_crossover(
        parents: List[PermutationIndividual],
        config: GAConfig
) -> List[PermutationIndividual]:
    return pair_wise_crossover(parents, config, _pmx)


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