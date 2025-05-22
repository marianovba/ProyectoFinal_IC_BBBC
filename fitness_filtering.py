import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import pdist, squareform

def compute_fitness(sim_result):
    T = sim_result["total_in"]
    M = sim_result["total_out"]
    E = sim_result["total_wait_time"]
    ME = sim_result["max_wait_time"]
    penalty_1 = 1 - (M / T) if T > 0 else 1
    return 0.95 * penalty_1 + 0.0009 * E + 0.00004 * ME

def distance_filtering(population, fitnesses, threshold):
    X = np.array(population, dtype=float)
    dist_matrix = squareform(pdist(X, metric='euclidean'))
    to_keep = [True] * len(population)
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if dist_matrix[i, j] < threshold:
                if fitnesses[i] < fitnesses[j]:
                    to_keep[j] = False
                else:
                    to_keep[i] = False
    return [ind for ind, keep in zip(population, to_keep) if keep]

def plot_fitness_evolution(history, title="MGP-BBBC Fitness Evolution"):
    generations = [entry["generation"] for entry in history]
    fitness_values = [entry["best_fitness"] for entry in history]
    plt.figure(figsize=(10, 5))
    plt.plot(generations, fitness_values, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_fitness_distribution(history_list, title="Distribución del Fitness"):
    all_data = []
    for gen_idx, generation in enumerate(history_list):
        for fit in generation:
            all_data.append({"Generación": gen_idx, "Fitness": fit})
    df = pd.DataFrame(all_data)
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Generación", y="Fitness", data=df)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_multiple_runs(runs, title="Comparación de ejecuciones"):
    plt.figure(figsize=(10, 6))
    for i, history in enumerate(runs):
        generations = [h["generation"] for h in history]
        fitness = [h["best_fitness"] for h in history]
        plt.plot(generations, fitness, label=f"Ejecución {i+1}")
    plt.title(title)
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
