from fitness_filtering import plot_multiple_runs, plot_fitness_distribution

def analizar_resultados(runs):
    # Comparación entre ejecuciones
    plot_multiple_runs(runs, title="Comparación entre ejecuciones")

    # Recolectar todos los fitness por generación
    generations = len(runs[0])
    grouped_history = [[] for _ in range(generations)]
    for run in runs:
        for g in range(generations):
            grouped_history[g].append(run[g]["best_fitness"])

    plot_fitness_distribution(grouped_history, title="Distribución del Fitness por Generación")