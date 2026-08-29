"""
Combinatorial fitness functions.

Available:
- tsp: Traveling Salesman Problem
"""

from .tsp import create_tsp_fitness, compute_euclidean_distance_matrix

__all__ = [
    'create_tsp_fitness',
    'compute_euclidean_distance_matrix',
]