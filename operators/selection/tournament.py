from typing import List, TypeVar
import random
from core.config import GAConfig
from operator import itemgetter

T = TypeVar('T')


def tournament_selection(
        population: List[T],
        fitness: List[float | int],
        config: GAConfig
) -> List[T]:
    selected: List[T] = []
    pop_size = config.population_size
    tournament_size = config.tournament_size

    for _ in range(pop_size):
        participants = random.sample(list(zip(population, fitness)), tournament_size)

        winner = min(participants, key=itemgetter(1))[0]

        selected.append(winner.copy())

    return selected