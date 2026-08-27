from dataclasses import dataclass
from typing import Optional

@dataclass
class GAConfig:
    population_size: int = 100
    max_generations: int = 300

    mutation_rate: float = 0.1
    crossover_rate: float = 0.9

    seed: Optional[int] = None

    def __post_init__(self):
        if self.seed is not None:
            import random
            random.seed(self.seed)