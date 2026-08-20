from dataclasses import dataclass
from typing import Optional

@dataclass
class GAConfig:
    population_size: int = 100
    max_generations: int = 1000
    mutation_rate: float = 0.01
    crossover_rate: float = 0.9
    elitism_count: int = 2
    # for some selection operators
    tournament_size: int = 3
    seed: Optional[int] = None