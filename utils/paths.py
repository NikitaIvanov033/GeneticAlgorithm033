from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"
ANALYSIS_DIR = DATA_DIR / "analysis"
TSP_DATA_DIR = DATA_DIR / "tsp"

BENCHMARK_DIR = BASE_DIR / "benchmarks"
EXPERIMENTS_DIR = BASE_DIR / "experiments"