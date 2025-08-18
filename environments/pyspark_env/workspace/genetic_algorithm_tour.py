import random

POPULATION_SIZE = 50
LEN_CHROMOSOME = 10
# distance matrix needs to be in function of the time
def fitness_f():
    pass

def crossover(chromosome_1, chromosome_2):
    """
    Apply ordered crossover
    """
    idx1, idx2 = sorted(random.sample(range(LEN_CHROMOSOME), 2))
    slice1 = chromosome_1[idx1:idx2]
    slice2 = chromosome_2[idx1:idx2]

    chromosome_1 = chromosome_1[idx2:] + chromosome_1[:idx2]
    chromosome_2 = chromosome_2[idx2:] + chromosome_2[:idx2]
    temp1 = [e for e in chromosome_1 if not e in slice2]
    temp2 = [e for e in chromosome_2 if not e in slice1]

    child1, child2 = [], []

    child1.extend(temp1[LEN_CHROMOSOME-idx2:])
    child1.extend(slice2)
    child1.extend(temp1[:LEN_CHROMOSOME-idx2])

    child2.extend(temp2[LEN_CHROMOSOME - idx2:])
    child2.extend(slice1)
    child2.extend(temp2[:LEN_CHROMOSOME - idx2])
    return child1, child2

def mutation(chromosome):
    idx1, idx2 = sorted(random.sample(range(LEN_CHROMOSOME), 2))
    tmp_gene = chromosome[idx1]
    chromosome[idx1] = chromosome[idx2]
    chromosome[idx2] = tmp_gene
    return chromosome


def genetic_algorithm()