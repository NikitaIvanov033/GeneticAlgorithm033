from dataclasses import dataclass
from typing import List
from core.individual import Individual


@dataclass
class PermutationIndividual(Individual):
    chromosome: List[int]

    def copy(self) -> 'PermutationIndividual':
        return PermutationIndividual(self.chromosome.copy())

    def __len__(self) -> int:
        return len(self.chromosome)

    def __str__(self) -> str:
        return " -> ".join(str(x) for x in self.chromosome)