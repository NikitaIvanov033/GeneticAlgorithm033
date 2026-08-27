from typing import List
import random
from core.config import GAConfig
from individuals.permutation import PermutationIndividual


def ox_crossover(
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
            child1, child2 = _ox(p1, p2)
            offspring.extend([child1, child2])
        else:
            offspring.extend([p1.copy(), p2.copy()])

    return offspring


def _ox(
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

    elements_from_p2 = [x for x in p2.chromosome if x not in child1]

    pos = b
    for val in elements_from_p2:
        while child1[pos % n] != -1:
            pos += 1
        child1[pos % n] = val
        pos += 1

    elements_from_p1 = [x for x in p1.chromosome if x not in child2]

    pos = b
    for val in elements_from_p1:
        while child2[pos % n] != -1:
            pos += 1
        child2[pos % n] = val
        pos += 1

    return PermutationIndividual(child1), PermutationIndividual(child2)