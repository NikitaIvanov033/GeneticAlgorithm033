from typing import List, Optional, Callable, Tuple, TypeVar
from core.config import GAConfig
from core.individual import Individual
from core.types import FitnessFunction, Initializer, SelectionOperator, CrossoverOperator, MutationOperator, \
    ReplacementOperator

T = TypeVar('T', bound=Individual)


class GeneticAlgorithm:
    """
    Genetic Algorithm

    Minimize fitness function
    """

    def __init__(
            self,
            config: GAConfig,
            fitness_fn: FitnessFunction[T],
            selection: SelectionOperator[T],
            crossover: CrossoverOperator[T],
            mutation: MutationOperator[T],
            replacement: ReplacementOperator[T],
            initializer: Initializer[T],
            callback: Optional[Callable[[int, List[T], List[float], float], None]] = None
    ):
        self.config = config
        self.fitness_fn = fitness_fn
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.replacement = replacement
        self.initializer = initializer
        self.callback = callback

        self.population: List[T] = []
        self.fitness: List[float] = []
        self.best_individual: Optional[T] = None
        self.best_fitness: float = -float('inf')
        self.generation: int = 0
        self.history: List[float] = []

    def _initialize_population(self) -> List[T]:
        return [self.initializer() for _ in range(self.config.population_size)]

    def _evaluate_population(self, population: List[T]) -> List[float | int]:
        return [self.fitness_fn(individual) for individual in population]

    def _update_best(self, population: List[T], fitness: List[float | int]) -> None:
        if not fitness:
            return

        best_idx = max(range(len(fitness)), key=lambda individual: fitness[individual])
        current_best_fitness = fitness[best_idx]

        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_individual = population[best_idx].copy()

    def _log_generation(self) -> None:
        if self.callback is not None:
            self.callback(
                self.generation,
                self.population,
                self.fitness,
                self.best_fitness
            )

    def run(self) -> Tuple[Optional[T], float]:
        """
        Returns:
            Tuple[Optional[T], float]: best individual and best fitness
        """
        self.population = self._initialize_population()
        self.fitness = self._evaluate_population(self.population)
        self._update_best(self.population, self.fitness)
        self.history.append(self.best_fitness)
        self._log_generation()

        for gen in range(self.config.max_generations):
            self.generation = gen + 1

            parents = self.selection(self.population, self.fitness, self.config)

            offspring = self.crossover(parents, self.config)

            offspring = self.mutation(offspring, self.config)

            offspring_fitness = self._evaluate_population(offspring)

            self.population, self.fitness = self.replacement(
                self.population, offspring, self.fitness, offspring_fitness, self.config
            )

            self._update_best(self.population, self.fitness)
            self.history.append(self.best_fitness)

            self._log_generation()

        return self.best_individual, self.best_fitness

    def get_history(self) -> List[float]:
        return self.history.copy()