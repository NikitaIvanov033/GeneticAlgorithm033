import csv
import time
import random
import signal
import sys
from pathlib import Path
from datetime import datetime
from itertools import product
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Set

import numpy as np
from core.config import GAConfig
from core.algorithm import GeneticAlgorithm
from fitness.combinatorial.tsp import compute_euclidean_distance_matrix, create_tsp_fitness
from initialization.permutation import create_permutation_initializer
from operators.crossover.pmx import pmx_crossover
from operators.crossover.ox import ox_crossover
from operators.crossover.cx import cx_crossover
from operators.mutation.swap import swap_mutation
from operators.replacement.elitist import elitist_replacement
from operators.replacement.generational import generational_replacement
from operators.selection.tournament import create_tournament_selection
from operators.selection.rank import rank_selection
from utils.data_loader import load_tsp_data


@dataclass
class BenchmarkConfig:
    selection: str
    crossover: str
    mutation: str
    replacement: str

    population_size: int
    max_generations: int
    mutation_rate: float
    crossover_rate: float
    tournament_size: int

    seed: int
    run_id: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def config_key(self) -> str:
        return f"{self.selection}_{self.crossover}_{self.mutation}_{self.replacement}_{self.population_size}_{self.max_generations}_{self.mutation_rate}_{self.crossover_rate}_{self.tournament_size}"


def get_selection(name: str, tournament_size: int = 3):
    if name == 'tournament':
        return create_tournament_selection(tournament_size)
    elif name == 'rank':
        return rank_selection
    else:
        raise ValueError(f"Unknown selection: {name}")


def get_operator(name: str, op_type: str):
    operators = {
        'crossover': {
            'pmx': pmx_crossover,
            'ox': ox_crossover,
            'cx': cx_crossover,
        },
        'mutation': {
            'swap': swap_mutation,
        },
        'replacement': {
            'elitist': elitist_replacement,
            'generational': generational_replacement
        },
    }
    return operators[op_type][name]


def run_single_experiment(
        config: BenchmarkConfig,
        distance_matrix: List[List[float]],
        n_cities: int
) -> Dict[str, Any]:
    random.seed(config.seed)
    np.random.seed(config.seed)

    initializer = create_permutation_initializer(n_cities)
    fitness_fn = create_tsp_fitness(distance_matrix)

    selection_fn = get_selection(config.selection, config.tournament_size)
    crossover_fn = get_operator(config.crossover, 'crossover')
    mutation_fn = get_operator(config.mutation, 'mutation')
    replacement_fn = get_operator(config.replacement, 'replacement')

    ga_config = GAConfig(
        population_size=config.population_size,
        max_generations=config.max_generations,
        mutation_rate=config.mutation_rate,
        crossover_rate=config.crossover_rate,
        seed=config.seed,
    )

    ga = GeneticAlgorithm(
        config=ga_config,
        fitness_fn=fitness_fn,
        selection=selection_fn,
        crossover=crossover_fn,
        mutation=mutation_fn,
        replacement=replacement_fn,
        initializer=initializer,
    )

    start_time = time.perf_counter()
    best, best_fitness = ga.run()
    elapsed_time = time.perf_counter() - start_time

    result = config.to_dict()
    result.update({
        'best_fitness': best_fitness,
        'elapsed_time': elapsed_time,
        'history': ga.history,
        'best_individual': best,
    })

    return result

def run_benchmark(
        base_params: Dict[str, List],
        tournament_sizes: List[int] = None,
        n_runs: int = 50,
        data_path: str = None,
        results_dir: str = None,
        prefix: str = "benchmark",
) -> None:
    if data_path is None:
        data_path = str(BASE_DIR / "data" / "tsp" / "berlin52.tsp")
    if results_dir is None:
        results_dir = str(BASE_DIR / "data" / "results")

    coords = load_tsp_data(data_path)
    n_cities = len(coords)
    distance_matrix = compute_euclidean_distance_matrix(coords)

    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    pop_sizes = base_params.get('population_size', [100])
    gen_counts = base_params.get('max_generations', [300])

    rest_params = {k: v for k, v in base_params.items() if k not in ['population_size', 'max_generations']}
    rest_keys = list(rest_params.keys())
    rest_values = list(rest_params.values())
    rest_combinations = list(product(*rest_values))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for pop_size in pop_sizes:
        for max_gen in gen_counts:
            filename = f"{prefix}_{timestamp}_pop{pop_size}_gen{max_gen}.csv"
            csv_path = results_path / filename

            print(f"Population: {pop_size}, Generations: {max_gen}")
            print(f"Results file: {csv_path}")

            combinations = []
            for combo in rest_combinations:
                config = dict(zip(rest_keys, combo))
                if config['selection'] == 'tournament' and tournament_sizes:
                    for ts in tournament_sizes:
                        combinations.append({**config, 'tournament_size': ts})
                else:
                    combinations.append({**config, 'tournament_size': None})

            total_experiments = len(combinations) * n_runs
            print(f"  Configurations: {len(combinations)} × {n_runs} runs = {total_experiments}")

            with open(csv_path, 'w', newline='') as csvfile:
                fieldnames = [
                    'selection', 'crossover', 'mutation', 'replacement',
                    'population_size', 'max_generations', 'mutation_rate',
                    'crossover_rate', 'tournament_size',
                    'seed', 'run_id', 'best_fitness', 'elapsed_time'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                csvfile.flush()

                run_counter = 0

                for config_kwargs in combinations:
                    base_config = {
                        'selection': config_kwargs['selection'],
                        'crossover': config_kwargs['crossover'],
                        'mutation': config_kwargs['mutation'],
                        'replacement': config_kwargs['replacement'],
                        'population_size': pop_size,
                        'max_generations': max_gen,
                        'mutation_rate': config_kwargs['mutation_rate'],
                        'crossover_rate': config_kwargs['crossover_rate'],
                        'tournament_size': config_kwargs['tournament_size'],
                    }

                    print(f"\n  Config: {config_kwargs['selection']} + {config_kwargs['crossover']} + {config_kwargs['replacement']} | "
                          f"mut={config_kwargs['mutation_rate']} | ts={config_kwargs['tournament_size']}")

                    for run_id in range(n_runs):
                        run_counter += 1
                        seed = 42 + run_counter

                        config = BenchmarkConfig(
                            **base_config,
                            seed=seed,
                            run_id=run_id,
                        )

                        result = run_single_experiment(config, distance_matrix, n_cities)

                        row = {k: v for k, v in result.items() if k not in ['history', 'best_individual']}
                        writer.writerow(row)
                        csvfile.flush()

                        if run_counter % 10 == 0:
                            print(f"    Progress: {run_counter}/{total_experiments} runs")

            print(f"\nResults saved to: {csv_path}")


BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = str(BASE_DIR / "data" / "tsp" / "berlin52.tsp")
RESULTS_DIR = str(BASE_DIR / "data" / "results")

def main():
    param_grid = {
        'selection': ['tournament', 'rank'],
        'crossover': ['pmx', 'ox', 'cx'],
        'mutation': ['swap'],
        'replacement': ['elitist', 'generational'],
        'population_size': [50, 100],
        'max_generations': [100, 300, 500],
        'mutation_rate': [0.05, 0.1, 0.2],
        'crossover_rate': [0.7, 0.8, 0.9],
    }

    run_benchmark(
        base_params=param_grid,
        tournament_sizes=[3, 5, 10],
        n_runs=50,
        data_path=DATA_PATH,
        results_dir=RESULTS_DIR,
        prefix="benchmark",
    )


if __name__ == "__main__":
    main()