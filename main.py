from ciclo_bbbc import mgp_bbbc
from clustering import big_crunch_kmeans  # o big_crunch_meanshift
from fitness_filtering import plot_fitness_evolution

if __name__ == "__main__":
    result = mgp_bbbc(
        pop_size=30,
        generations=30,
        clustering_fn=big_crunch_kmeans,
        clustering_param=5
    )
    plot_fitness_evolution(result)
