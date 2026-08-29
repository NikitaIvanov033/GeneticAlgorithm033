"""
Core module: genetic algorithm core components.

Exports:
- GeneticAlgorithm: main algorithm class
- GAConfig: configuration dataclass
- Individual: protocol for individuals
- FitnessFunction, Initializer, SelectionOperator, etc.: type aliases
"""

from .algorithm import GeneticAlgorithm
from .config import GAConfig
from .individual import Individual
from .types import (
    FitnessFunction,
    Initializer,
    SelectionOperator,
    CrossoverOperator,
    MutationOperator,
    ReplacementOperator,
)

__all__ = [
    'GeneticAlgorithm',
    'GAConfig',
    'Individual',
    'FitnessFunction',
    'Initializer',
    'SelectionOperator',
    'CrossoverOperator',
    'MutationOperator',
    'ReplacementOperator',
]