from core.config import GAConfig
import matplotlib.pyplot as plt
from core.algorithm import GeneticAlgorithm
from fitness.combinatorial.tsp import compute_euclidean_distance_matrix, create_tsp_fitness
from initialization.permutation import create_permutation_initializer
from operators.crossover.ox import ox_crossover
from operators.mutation.swap import swap_mutation
from operators.replacement.generational import generational_replacement
from operators.selection.tournament import create_tournament_selection
from utils.data_loader import load_tsp_data

cities = load_tsp_data("../data/tsp/berlin52.tsp")
n_cities = len(cities)
distance_matrix = compute_euclidean_distance_matrix(cities)

initializer = create_permutation_initializer(n_cities)
fitness_fn = create_tsp_fitness(distance_matrix)

config = GAConfig(
    population_size=100,
    max_generations=300,
    mutation_rate=0.2,
    crossover_rate=0.9,
    seed=42
)

ga = GeneticAlgorithm(
    config=config,
    fitness_fn=fitness_fn,
    selection=create_tournament_selection(5),
    crossover=ox_crossover,
    mutation=swap_mutation,
    replacement=generational_replacement,
    initializer=initializer
)

if __name__ == "__main__":
    best, best_fitness = ga.run()
    print(f"\nBest route: {best}")
    print(f"Best fitness: {best_fitness:.2f}")

    print(f"Gap: {((best_fitness - 7542) / 7542 * 100):.2f}%")

    plt.figure(figsize=(10, 6))
    plt.plot(ga.history, color='blue', linewidth=1.5)
    plt.axhline(y=7542, color='red', linestyle='--', linewidth=2, label='Optimal (7542)')
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Best Fitness (Tour Length)", fontsize=12)
    plt.title("Convergence Plot — Berlin52", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    plt.show()