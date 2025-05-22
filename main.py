from ciclo_bbbc import mgp_bbbc
from clustering import big_crunch_kmeans
from fitness_filtering import plot_fitness_evolution
from analisis import analizar_resultados

if __name__ == "__main__":
    runs = []

    for i in range(5):  # Ejecutar múltiples corridas
        result = mgp_bbbc(
            pop_size=100,
            generations=50,
            clustering_fn=big_crunch_kmeans,
            clustering_param=5
        )
        runs.append(result)
        plot_fitness_evolution(result, title=f"Evolución del Fitness - Ejecución {i+1}")

    analizar_resultados(runs)
