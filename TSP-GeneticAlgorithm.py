import math
import random
import statistics

# --------------------- Genetic Algorithm Parameters ------------------------- #

NBGENOME = 200
NBGEN = 200
MUTRATE = 0.05

# ------------------------- Problem's functions -------------------------------#

cities = [[60, 200],
          [180, 200],
          [80, 180],
          [140, 180],
          [20, 160],
          [100, 160],
          [200, 160],
          [140, 140],
          [40, 120],
          [100, 120],
          [180, 100]]

nbcities = len(cities)

def city(i):
    return cities[i][0], cities[i][1]

def dist(v1, v2):
    return math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

def randomGen():
    init = range(nbcities)
    gen = random.sample(init, nbcities)
    return gen

def fitness(genome):
    res = 0
    for i in range(len(genome) - 1):
        res += dist(city(genome[i]), city(genome[i + 1]))
    return -res

# ----------------------- Genetic Functions -----------------------------------#

# Initiates a random population
def randomPop():
    population = [randomGen() for _ in range(NBGENOME)]
    return population


# Returns the best genome of a population
def bestgenome(population):
    temp = fitnessPop(population)
    return population[temp.index(max(temp))]


# Returns the fitness of the best genome of the population
def bestfitness(population):
    temp = fitnessPop(population)
    return max(temp)


# Computes the fitness function of a genome
def fitnessGA(genome):
    return fitness(genome)


# Computes the fitness of each genome of the population
def fitnessPop(population):
    temp = list(map(fitnessGA, population))
    return temp


# Crossover function in the population
# used theory : PMX
def crossover(population):
    temp = []
    for k in range(len(population) // 2):
        p1, p2 = population[2 * k], population[2 * k + 1]
        off1 = list(p1)
        for i in range(len(off1) // 2):
            j = off1.index(p2[i])
            off1[i], off1[j] = off1[j], off1[i]

        off2 = list(p2)
        for i in range(len(off2) // 2):
            j = off2.index(p1[i])
            off2[i], off2[j] = off2[j], off2[i]

        temp.append(off1)
        temp.append(off2)
    return temp


# Selection function to keep the best genomes
# used theory : RWS (Roulet Wheel Selection)
def selection(population,neg):
    temp = []

    fitness = fitnessPop(population)
    #print(*fitness,sep='\n')
    if neg == True:
        m = min(fitness)
        fitness = [- m + i for i in fitness]
    #print(*fitness,sep='\n')
    sumfit = sum(fitness)
    for _ in range(len(population)):
        G = random.randrange(0, int(sumfit))
        res = 0
        i = 0
        while (res < G):
            res += fitness[i]
            i += 1
        #print(i-1)
        temp.append(population[i-1])
    return temp


# Population Mutation
def mutatePop(population):
    return [mutate(i) for i in population]


# Genome Mutation
def mutate(genome):
    temp = genome
    gensize = len(genome)
    for i in range(gensize):
        if (random.randrange(0, 100) / 100) <= MUTRATE:
            j = i
            while j == i:
                j = random.randint(0, gensize - 1)
            temp[i], temp[j] = temp[j], temp[i]
    return temp


# ------------------------------- Main --------------------------------------- #

pop = randomPop()
bestfit = fitness(pop[0])

for i in range(NBGEN):
    pop = selection(pop, True)
    pop = crossover(pop)
    pop = mutatePop(pop)
    bestfit = max(bestfit,bestfitness(pop))
    #print("Generation (" + str(i+1) +
    #      ") BestGenom : " + str(bestgenome(pop)) +
    #      " Fitness : " + str(bestfitness(pop)) +
    #      " Best : " + str(bestfit))

print("best found minimal distance : ",-bestfit)
