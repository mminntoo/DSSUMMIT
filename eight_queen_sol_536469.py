'''' Solution for 8 queen problem
Step 1: A random chromosome is generated
Step 2: Fitness value of the chromosome is calculated
Step 3: If fitness is not equal to Fmax
Step 4: Reproduce (crossover) new chromosome from 2 randomly selected best chromosomes
Step 5: Mutation may take place
Step 6: New chromosome added to population
Repeat Step 2 to 6 until a chromosome (solution) with Fitness value = Fmax is found
'''
import random

def random_chromosome():
    ''' random chromosome allocation '''
    return [ random.randint(0, 7 ) for _ in range(8) ]

def fitness(chromosome):
    ''' to check the fitness of a chromosome / an iteration'''
    horizontal_collisions = sum([chromosome.count(q)-1 for q in chromosome])/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))



def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Errored"

def reproduce(x, y):
    '''cross_over between two chromosomes'''
    c = random.randint(0, 7)
    return x[0:c] + y[c:8]

def mutate(x):
    '''randomly changing the value of a random index of a chromosome'''

    c = random.randint(0, 7)
    m = random.randint(0, 7)
    x[c] = m
    return x

def genetic_queen(population, fitness, generation):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child, generation)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population

def print_chromosome(chrom, generation):
    print("Generation = {} Chromosome = {}  Fitness = {}"
        .format(generation, str(chrom), fitness(chrom)))

if __name__ == "__main__":
    '''main function to check for the right sequence based on max fitness  i.e. 28'''
    maxFitness = (8*7)/2
    population = [random_chromosome() for _ in range(123)]

    generation = 1

    while not maxFitness in [fitness(chrom) for chrom in population]:

        population = genetic_queen(population, fitness, generation)
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    chrom_out = []

    for chrom in population:
        if fitness(chrom) == maxFitness:
            print("One of the solutions : ")
            chrom_out = chrom
            print_chromosome(chrom,generation-1)
