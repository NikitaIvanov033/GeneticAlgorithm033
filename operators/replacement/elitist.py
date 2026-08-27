from typing import List, Tuple, TypeVar
from core.config import GAConfig
from operator import itemgetter
from itertools import chain

T = TypeVar('T')


def elitist_replacement(
    population: List[T],
    offspring: List[T],
    pop_fitness: List[float | int],
    off_fitness: List[float | int],
    config: GAConfig
) -> Tuple[List[T], List[float | int]]:
    combined = sorted(
        chain(zip(population, pop_fitness), zip(offspring, off_fitness)),
        key=itemgetter(1)
    )

    new_population = [ind for ind, _ in combined[:config.population_size]]
    new_fitness = [fit for _, fit in combined[:config.population_size]]

    return new_population, new_fitness