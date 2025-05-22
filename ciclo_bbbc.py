import random
from simulacion_trafico import GENOTYPE_LENGTH, simulate_traffic
from fitness_filtering import compute_fitness, distance_filtering

def generate_individual():
    return [random.choice([0, 1]) for _ in range(GENOTYPE_LENGTH)]

def generate_population(size):
    return [generate_individual() for _ in range(size)]

def big_bang(centers, generation, pop_size, mutation_prob=0.2):
    extent = 1.0 / (generation + 1)
    new_population = []
    per_center = max(1, pop_size // len(centers))
    
    for center in centers:
        for _ in range(per_center):
            child = []
            for gene in center:
                if random.random() < mutation_prob:
                    child.append(1-gene)
                else:
                    perturb = gene + random.uniform(-1, 1) * extent
                    child.append(int(round(min(1, max(0, perturb)))))
            new_population.append(child)

    while len(new_population) < pop_size:
        new_population.append(generate_individual())
    return new_population[:pop_size]

def mgp_bbbc(pop_size, generations, clustering_fn, clustering_param):
    population = generate_population(pop_size)
    archive = []
    history = []

    for generation in range(generations):
        sim_data = [(ind, simulate_traffic(ind)) for ind in population]
        fitnesses = [compute_fitness(res) for _, res in sim_data]

        if not archive:
            archive = [ind for ind, _ in sim_data]
        else:
            combined = archive + [ind for ind, _ in sim_data]
            combined_fitnesses = [compute_fitness(simulate_traffic(ind)) for ind in combined]
            filtered = distance_filtering(combined, combined_fitnesses, threshold=1.0)
            archive = sorted(filtered, key=lambda ind: compute_fitness(simulate_traffic(ind)))[:pop_size]

        archive_fitnesses = [compute_fitness(simulate_traffic(ind)) for ind in archive]
        centers = clustering_fn(archive, archive_fitnesses, clustering_param)
        population = big_bang(centers, generation, pop_size)
        best_fit = min(fitnesses)
        history.append({"generation": generation,
                        "best_fitness": min(fitnesses),
                        "all_fitness": fitnesses})

    return history
