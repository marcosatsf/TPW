import random
import math
from datetime import datetime, timedelta

# distance matrix needs to be in function of the time
def fitness_function(individual, predicted_map, allele_map, init_t):
    time_now = init_t
    sum_fitness = 0
    # e.g: time_now : [(0.9786283937096293, 10.0),
    #                  (3.0059052871456076, 50.0),
    #                  (0.8060600673978527, 10.0),
    #                  (5.277188476128824, 40.0)]
    # e.g. of a hypothetical individual gene ['YC', 'HI', 'BC', 'NE']
    # First node is 'YC' so get from
    # allele_map : {'HI': ('Avatar Flight of Passage', 0),
    #  'NE': ('DINOSAUR', 1),
    #  'YC': ('Expedition Everest - Legend of the Forbidden Mountain', 2),
    #  'BC': ("Na'vi River Journey", 3)} the coordinate to find its respective weight
    # Here we should take coordinate 2 for 'YC'
    last_node = None
    for e in individual:
        if not last_node:
            last_node = e
            continue

        try:
            # print(time_now, allele_map[e][1], predicted_map[time_now][allele_map[last_node][1]][allele_map[e][1]])
            weight_result, time_passed = predicted_map[time_now][allele_map[last_node][1]][allele_map[e][1]]
        except KeyError:
            weight_result, time_passed = math.inf, 60*24*10
        sum_fitness += weight_result
        time_now += timedelta(minutes=time_passed)
        last_node = e
    return sum_fitness


def crossover(chromosome_1, chromosome_2):
    """
    Apply ordered crossover
    """
    len_chromosome = len(chromosome_1)
    idx1, idx2 = sorted(random.sample(range(len_chromosome), 2))
    slice1 = chromosome_1[idx1:idx2]
    slice2 = chromosome_2[idx1:idx2]

    chromosome_1 = chromosome_1[idx2:] + chromosome_1[:idx2]
    chromosome_2 = chromosome_2[idx2:] + chromosome_2[:idx2]
    temp1 = [e for e in chromosome_1 if not e in slice2]
    temp2 = [e for e in chromosome_2 if not e in slice1]

    child1, child2 = [], []

    child1.extend(temp1[len_chromosome-idx2:])
    child1.extend(slice2)
    child1.extend(temp1[:len_chromosome-idx2])

    child2.extend(temp2[len_chromosome - idx2:])
    child2.extend(slice1)
    child2.extend(temp2[:len_chromosome - idx2])
    return child1, child2


def mutation(chromosome):
    len_chromosome = len(chromosome)
    idx1, idx2 = sorted(random.sample(range(len_chromosome), 2))
    tmp_gene = chromosome[idx1]
    chromosome[idx1] = chromosome[idx2]
    chromosome[idx2] = tmp_gene
    return chromosome


# Create an individual with permutation encoding
def create_individual(code_map):
    # e.g. of a hypothetical individual gene ['YC', 'HI', 'BC', 'NE']
    return random.sample(code_map, k=len(code_map))


# Crossover operation
# def crossover(parent1, parent2):
#     point = random.randint(1, len(parent1) - 1)
#     child1 = parent1[:point] + parent2[point:]
#     child2 = parent2[:point] + parent1[point:]
#     return child1, child2

# Mutation operation
# def mutate(individual, mutation_rate):
#     for i in range(len(individual)):
#         if random.random() < mutation_rate:
#             individual[i] = 1 - individual[i]
#     return individual


# Selection operation: Elitism
def selection(fitnesses:list, n_th: int):
    n_th_value = sorted(fitnesses)[n_th]
    return fitnesses.index(n_th_value)


# Genetic Algo.
def genetic_algorithm(pop_size, num_generations, allele_map, predicted_map, crossover_rate, mutation_rate):
    # Initialize pop
    code_map_list = [e[0] for e in sorted(allele_map.items(), key=lambda al:al[1][1])]
    print(code_map_list)
    # Get initial time
    initial_time = min([t for t in predicted_map.keys()])
    print(initial_time)
    population = [create_individual(code_map_list) for _ in range(pop_size)]
    print(population)
    for generation in range(num_generations):
        # Evaluate fitness
        fitnesses = [fitness_function(ind, predicted_map, allele_map, initial_time) for ind in population]

        # Create new population
        new_population = []
        while len(new_population) < pop_size:
            for p in range(2):
                idx = selection(fitnesses, p)
                match p:
                    case 0: parent1 = population[idx]
                    case 1: parent2 = population[idx]

            # Apply crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            # Apply mutation
            if random.random() < mutation_rate:
                child1 = mutation(child1)
                child2 = mutation(child2)

            new_population.extend([child1, child2])

        # Update population
        population = new_population[:pop_size]

        # Print best individual in the current generation
        best_fitness = selection(fitnesses, 0)
        print(fitnesses, best_fitness, population, sep=' | ')
        best_individual = population[best_fitness]
        print(f"Generation {generation+1}:")
        print(f"Best Fitness to f(r, q, d) = {best_fitness}")
        print(f"Best individual is {best_individual}")

    # Return best individual and its fitness
    return best_individual, best_fitness