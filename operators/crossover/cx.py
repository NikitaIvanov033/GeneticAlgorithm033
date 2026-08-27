from typing import List
import random
from core.config import GAConfig
from individuals.permutation import PermutationIndividual


def cx_crossover(
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
            child1, child2 = _cx(p1, p2)
            offspring.extend([child1, child2])
        else:
            offspring.extend([p1.copy(), p2.copy()])

    return offspring


def _cx(
        p1: PermutationIndividual,
        p2: PermutationIndividual
) -> tuple[PermutationIndividual, PermutationIndividual]:
    n = len(p1)

    if n < 2:
        return p1.copy(), p2.copy()

    child1 = [-1] * n
    child2 = [-1] * n

    pos_in_p2 = {value: idx for idx, value in enumerate(p2.chromosome)}

    visited = set()

    for start_pos in range(n):
        if start_pos in visited:
            continue

        current_pos = start_pos
        cycle = set()

        while current_pos not in cycle:
            cycle.add(current_pos)

            value = p1.chromosome[current_pos]

            next_pos = pos_in_p2[value]

            current_pos = next_pos

        if current_pos != start_pos:
            raise RuntimeError(
                f"CX: Cycle did not close properly. "
                f"Started at {start_pos}, ended at {current_pos}. "
                f"Cycle: {cycle}"
            )

        visited.update(cycle)

        if 0 in cycle:
            for pos in cycle:
                child1[pos] = p1.chromosome[pos]
                child2[pos] = p2.chromosome[pos]
        else:
            for pos in cycle:
                child1[pos] = p2.chromosome[pos]
                child2[pos] = p1.chromosome[pos]

    return PermutationIndividual(child1), PermutationIndividual(child2)