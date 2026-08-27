from core.config import GAConfig
from core.algorithm import GeneticAlgorithm
from fitness.combinatorial.tsp import compute_euclidean_distance_matrix, create_tsp_fitness
from initialization.permutation import create_permutation_initializer
from operators.crossover.pmx import pmx_crossover
from operators.mutation.swap import swap_mutation
from operators.replacement.elitist import elitist_replacement
from operators.selection.tournament import tournament_selection
from utils.data_loader import load_tsp_data

cities = load_tsp_data("data/tsp/berlin52.tsp")
n_cities = len(cities)
distance_matrix = compute_euclidean_distance_matrix(cities)

initializer = create_permutation_initializer(n_cities)
fitness_fn = create_tsp_fitness(distance_matrix)

config = GAConfig(
    population_size=100,
    max_generations=500,
    mutation_rate=0.02,
    crossover_rate=0.9,
    elitism_count=2,
    tournament_size=3,
    seed=42
)

ga = GeneticAlgorithm(
    config=config,
    fitness_fn=fitness_fn,
    selection=tournament_selection,
    crossover=pmx_crossover,
    mutation=swap_mutation,
    replacement=elitist_replacement,
    initializer=initializer
)