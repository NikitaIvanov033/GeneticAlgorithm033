from dataclasses import dataclass
from typing import Optional

@dataclass
class GAConfig:
    population_size: int = 100
    max_generations: int = 100

    mutation_rate: float = 0.01
    crossover_rate: float = 0.9

    elitism_count: int = 2
    tournament_size: int = 3

    seed: Optional[int] = None

    def __post_init__(self):
        if self.seed is not None:
            import random
            random.seed(self.seed)