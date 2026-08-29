# Evolutionary Algorithm Framework

A flexible genetic algorithm framework written in Python. Designed for research and experimentation with evolutionary algorithms on discrete optimization problems, with a focus on the Traveling Salesman Problem (TSP).

## Features

- **Modular architecture** – pluggable operators for selection, crossover, mutation, and replacement.
- **Generic individual protocol** – supports binary strings, permutations, real‑valued vectors, and custom types.
- **Built‑in TSP support** – Euclidean distance, the berlin52 dataset, and reference optimal value.
- **Benchmark framework** – grid search over operator combinations and hyperparameters with progress bars.
- **Analysis tools** – automatic report generation, convergence plots, operator comparison, and heatmaps.
- **NumPy‑accelerated** – fast pairwise distance computation and vectorised fitness evaluation.

## Project Structure

```
GAN/
├── analysis/                    # Data analysis and cleaning
│   ├── clean_benchmark.py       # Remove duplicate rank‑selection runs
│   ├── split_benchmark.py       # Split CSV by population/generations
│   └── tsp/
│       └── analyze_tsp_benchmark.py  # Generate reports and plots
├── benchmarks/                  # Benchmarks
│   └── tsp/
│       ├── plan.txt             # Experiment plan
│       └── tsp_param_grid.py    # Grid search over parameters
├── core/                        # Core framework
│   ├── algorithm.py             # GeneticAlgorithm class
│   ├── config.py                # GAConfig dataclass
│   ├── individual.py            # Individual protocol
│   └── types.py                 # Type hints
├── experiments/                 # Experiment scripts
│   └── tsp.py                   # Run TSP with convergence plot
├── fitness/                     # Fitness functions
│   ├── combinatorial/
│   │   └── tsp.py               # TSP fitness (NumPy)
│   ├── continuous/              # (placeholder)
│   └── discrete/                # (placeholder)
├── individuals/                 # Individual implementations
│   └── permutation.py           # PermutationIndividual
├── initialization/              # Population initialisation
│   └── permutation.py           # Random permutation
├── operators/                   # Genetic operators
│   ├── crossover/               # PMX, OX, CX
│   ├── mutation/                # Swap
│   ├── replacement/             # Elitist, Generational
│   └── selection/               # Tournament, Rank
├── utils/                       # Utilities
│   ├── data_loader.py           # Load TSP data
│   ├── gui.py                   # GUI file chooser
│   └── paths.py                 # Path definitions
├── data/                        # Data files
│   ├── results/                 # Benchmark results (CSV)
│   └── tsp/                     # TSPLIB instances (berlin52.tsp)
├── tests/                       # Unit tests
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/NikitaIvanov033/GeneticAlgorithm033.git
cd evolutionary-framework
pip install -r requirements.txt
```

## Quick Start

Run the TSP example on the Berlin52 instance:

```bash
python experiments/tsp.py
```

This will execute the genetic algorithm with default settings, print the best route found, its length, the gap from the optimal value (7542), and display a convergence plot.

## Running Benchmarks and Analysing Results

1. **Run the grid search**  
   Launch the benchmark script:
   ```bash
   python benchmarks/tsp/tsp_param_grid.py
   ```
   Results are saved as CSV files in `data/results/`.

2. **Generate reports and plots**  
   Analyse the benchmark results and create visualisations:
   ```bash
   python analysis/tsp/analyze_tsp_benchmark.py
   ```
   Reports and figures are saved in `data/analysis/`.

## Configuration

All core parameters are managed via the `GAConfig` class in `core/config.py`. Example:

```python
from core.config import GAConfig

config = GAConfig(
    population_size=100,
    max_generations=300,
    mutation_rate=0.1,
    crossover_rate=0.9,
    seed=42
)
```

Operators are plugged in as functions that adhere to the type protocols defined in `core/types.py`.

## Extending the Framework

- To add a new individual type, implement the `Individual` protocol (see `core/individual.py`).
- Place new operators in the corresponding subdirectories under `operators/`.
- Add new fitness functions for other problems in the `fitness/` hierarchy.

## Requirements

The required packages are listed in `requirements.txt`:

- numpy
- matplotlib
- seaborn
- pandas
- tqdm

## License

...