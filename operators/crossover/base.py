from typing import List, Callable, TypeVar
import random
from core.config import GAConfig

T = TypeVar('T')


def pair_wise_crossover(
    parents: List[T],
    config: GAConfig,
    crossover_fn: Callable[[T, T], tuple[T, T]]
) -> List[T]:
    offspring: List[T] = []
    pop_size = len(parents)

    for i in range(0, pop_size, 2):
        if i + 1 >= pop_size:
            offspring.append(parents[i].copy())
            break

        p1 = parents[i]
        p2 = parents[i + 1]

        if random.random() < config.crossover_rate:
            child1, child2 = crossover_fn(p1, p2)
            offspring.extend([child1, child2])
        else:
            offspring.extend([p1.copy(), p2.copy()])

    return offspring