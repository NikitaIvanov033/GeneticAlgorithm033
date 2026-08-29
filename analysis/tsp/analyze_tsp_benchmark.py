import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from utils import select_csv_files
from utils.paths import BASE_DIR, RESULTS_DIR
from tqdm import tqdm

OPTIMAL = 7542.0

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (12, 8)


def load_selected_files(files: list) -> pd.DataFrame:
    if not files:
        raise ValueError("No files selected.")

    print(f"\nLoading {len(files)} file(s)...")
    dfs = []
    for f in tqdm(files, desc="Loading files"):
        df = pd.read_csv(f)
        dfs.append(df)
        print(f"  {Path(f).name}: {len(df)} rows")

    df = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal: {len(df)} rows")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['gap'] = ((df['best_fitness'] - OPTIMAL) / OPTIMAL) * 100
    df['config_key'] = df.apply(
        lambda r: f"{r['selection']}_{r['crossover']}_{r['replacement']}_{r['mutation_rate']}_{r['tournament_size']}_{r['population_size']}_{r['max_generations']}_{r['crossover_rate']}",
        axis=1
    )
    return df


def aggregate_results(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = [
        'selection', 'crossover', 'mutation', 'replacement',
        'population_size', 'max_generations', 'mutation_rate',
        'crossover_rate', 'tournament_size'
    ]

    agg = df.groupby(group_cols).agg({
        'best_fitness': ['mean', 'std', 'min', 'max', 'count'],
        'gap': ['mean', 'std', 'min'],
        'elapsed_time': ['mean', 'std']
    }).round(2)

    agg.columns = ['_'.join(col).strip() for col in agg.columns.values]
    agg = agg.sort_values('best_fitness_mean').reset_index()
    return agg


def top_configurations(df_agg: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    cols = [
        'selection', 'crossover', 'replacement',
        'mutation_rate', 'tournament_size',
        'population_size', 'max_generations', 'crossover_rate',
        'best_fitness_mean', 'best_fitness_std',
        'gap_mean', 'elapsed_time_mean'
    ]
    return df_agg.nsmallest(n, 'best_fitness_mean')[cols]


def plot_operator_comparison(df: pd.DataFrame, output_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ax = axes.flatten()

    for i, (op, col) in enumerate([
        ('Selection', 'selection'),
        ('Crossover', 'crossover'),
        ('Replacement', 'replacement'),
        ('Tournament size', 'tournament_size')
    ]):
        if col == 'tournament_size':
            data = df[df['selection'] == 'tournament']
        else:
            data = df

        sns.boxplot(data=data, x=col, y='best_fitness', ax=ax[i])
        ax[i].set_title(f'Comparison: {op}', fontsize=14)
        ax[i].set_xlabel(op)
        ax[i].set_ylabel('Best fitness')
        ax[i].grid(True, alpha=0.3)
        ax[i].axhline(y=OPTIMAL, color='red', linestyle='--', linewidth=1.5, label='Optimal')
        ax[i].legend()

    plt.tight_layout()
    plt.savefig(output_dir / 'operator_comparison.png', dpi=150)
    plt.close()


def plot_heatmap_mutation_tournament(df: pd.DataFrame, output_dir: Path) -> None:
    data = df[df['selection'] == 'tournament']

    pivot = data.pivot_table(
        index='mutation_rate',
        columns='tournament_size',
        values='best_fitness',
        aggfunc='mean'
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r',
                linewidths=0.5, square=True)
    plt.title('Mutation rate x Tournament size', fontsize=14)
    plt.xlabel('Tournament size')
    plt.ylabel('Mutation rate')
    plt.tight_layout()
    plt.savefig(output_dir / 'heatmap_mutation_tournament.png', dpi=150)
    plt.close()


def plot_parameter_effects(df: pd.DataFrame, output_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.boxplot(data=df, x='mutation_rate', y='best_fitness', ax=axes[0])
    axes[0].set_title('Mutation rate influence', fontsize=14)
    axes[0].set_xlabel('Mutation rate')
    axes[0].set_ylabel('Best fitness')
    axes[0].axhline(y=OPTIMAL, color='red', linestyle='--', linewidth=1.5)

    sns.boxplot(data=df, x='crossover_rate', y='best_fitness', ax=axes[1])
    axes[1].set_title('Crossover rate influence', fontsize=14)
    axes[1].set_xlabel('Crossover rate')
    axes[1].set_ylabel('Best fitness')
    axes[1].axhline(y=OPTIMAL, color='red', linestyle='--', linewidth=1.5)

    plt.tight_layout()
    plt.savefig(output_dir / 'parameter_effects.png', dpi=150)
    plt.close()


def generate_report(df: pd.DataFrame, df_agg: pd.DataFrame, output_dir: Path) -> None:
    top5 = top_configurations(df_agg, 5)

    by_selection = df.groupby('selection')['best_fitness'].agg(['mean', 'std']).round(2).sort_values('mean')
    by_crossover = df.groupby('crossover')['best_fitness'].agg(['mean', 'std']).round(2).sort_values('mean')
    by_replacement = df.groupby('replacement')['best_fitness'].agg(['mean', 'std']).round(2).sort_values('mean')

    by_mutation_rate = df.groupby('mutation_rate')['best_fitness'].agg(['mean', 'std']).round(2)
    by_crossover_rate = df.groupby('crossover_rate')['best_fitness'].agg(['mean', 'std']).round(2).sort_values('mean')

    lines = [
        f"Total runs: {len(df)}",
        f"Configurations: {len(df_agg)}",
        f"Optimal: {OPTIMAL}",
        "",
        "Top 5 configurations:",
        top5.to_string(index=False),
        "",
        by_selection.to_string(),
        "",
        by_crossover.to_string(),
        "",
        by_replacement.to_string(),
        "",
        by_mutation_rate.to_string(),
        "",
        by_crossover_rate.to_string(),
        f"Graphs: {output_dir}",
        f"Tables: {output_dir}",
    ]

    with open(output_dir / 'report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print('\n'.join(lines))


def main():
    print("Benchmark Analysis")

    files = select_csv_files(RESULTS_DIR)
    if not files:
        print("No files selected. Exiting.")
        return

    base_name = Path(files[0]).stem
    OUTPUT_DIR = BASE_DIR / "data" / "analysis" / base_name
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_selected_files(files)
    df = add_derived_columns(df)

    df_agg = aggregate_results(df)
    print(f"Unique configurations: {len(df_agg)}")

    plot_operator_comparison(df, OUTPUT_DIR)
    plot_heatmap_mutation_tournament(df, OUTPUT_DIR)
    plot_parameter_effects(df, OUTPUT_DIR)

    generate_report(df, df_agg, OUTPUT_DIR)

    df_agg.to_csv(OUTPUT_DIR / 'full_aggregated.csv', index=False)
    top_configurations(df_agg, 20).to_csv(OUTPUT_DIR / 'top_configs.csv', index=False)

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()