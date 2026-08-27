import numpy as np
from typing import List, Tuple
from individuals.permutation import PermutationIndividual


def compute_euclidean_distance_matrix(coords: List[Tuple[float, float]]) -> List[List[float]]:
    coords_np = np.array(coords)
    diff = coords_np[:, np.newaxis, :] - coords_np[np.newaxis, :, :]
    matrix = np.sqrt(np.sum(diff ** 2, axis=2))
    return matrix.tolist()


def create_tsp_fitness(distance_matrix: List[List[float]]):
    dist = np.array(distance_matrix)

    def tsp_fitness(individual: PermutationIndividual) -> float:
        route = np.array(individual.chromosome)
        total = np.sum(dist[route[:-1], route[1:]])
        total += dist[route[-1], route[0]]
        return float(total)

    return tsp_fitness