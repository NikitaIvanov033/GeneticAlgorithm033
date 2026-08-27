from typing import List
from core.config import GAConfig
from individuals.permutation import PermutationIndividual
from .base import pair_wise_crossover


def cx_crossover(
        parents: List[PermutationIndividual],
        config: GAConfig
) -> List[PermutationIndividual]:
    return pair_wise_crossover(parents, config, _cx)


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