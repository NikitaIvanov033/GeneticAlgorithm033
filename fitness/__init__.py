"""
Fitness functions for various problems.

Submodules:
- combinatorial: TSP, VRP, scheduling, etc.
- discrete: OneMax, deceptive, etc.
- continuous: Sphere, Rastrigin, Rosenbrock, etc.
"""

from .combinatorial.tsp import create_tsp_fitness, compute_euclidean_distance_matrix

__all__ = [
    'create_tsp_fitness',
    'compute_euclidean_distance_matrix',
]