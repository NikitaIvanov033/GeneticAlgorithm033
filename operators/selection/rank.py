from typing import List, TypeVar
import random
from core.config import GAConfig
from operator import itemgetter

T = TypeVar('T')


def rank_selection(
    population: List[T],
    fitness: List[float | int],
    config: GAConfig
) -> List[T]:
    pop_size = config.population_size

    sorted_pairs = sorted(
        list(zip(population, fitness)),
        key=itemgetter(1)
    )

    ranks = [pop_size - i for i in range(pop_size)]

    total_rank = sum(ranks)
    probabilities = [r / total_rank for r in ranks]

    indices = random.choices(range(pop_size), weights=probabilities, k=pop_size)
    selected = [sorted_pairs[idx][0].copy() for idx in indices]

    return selected