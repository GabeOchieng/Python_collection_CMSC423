# Entropy Game Version 2
# No survival 

import sys
import re
import random
from random import randint
import math

nruns = 10
nyears = 100
num_offspring = 5
mutation_rate = 1. / 15
max_age = 10
max_population_size = 100


def mutate(nucleotide):
    nList = [nuc for nuc in 'ACGT' if nuc != nucleotide]
    return nList[randint(0,2)]


def reproduce(population, num_offspring, mutation_rate):
    new_population_list = []

    # populate new list with population 
    for organism in population:
        organism[0] += 1                            # increment parents' age
        new_population_list.append(organism)

    # run reproduction
    for organism in population:
        for i in range(num_offspring):
            nuc_list = list(organism[1])
            for j in range(len(nuc_list)):
                if random.uniform(0,1) <= (mutation_rate):
                    nuc_list[j] = mutate(nuc_list[j])
            new_organism = [0, ''.join(str(p) for p in nuc_list)]
            new_population_list.append(new_organism)
            
    return new_population_list


def remove_elders(population, max_age):
    population=filter(lambda x: x[0] < max_age, population)
    return population


def yearend(population, max_population_size):
    for organism in population:
        organism[0] += 1
    
    random.shuffle(population)
    new_population = population[:100]

    return new_population


def get_profile(motifs):
    prof = []
    for i in range(len(motifs[0][1])):
        col = ''.join(str([motifs[j][1][i] for j in xrange(len(motifs))]))
        prof.append([float(col.count(nuc))/float(len(col)) for nuc in 'ACGT'])
    return prof


def calculate_entropy(population):
    entropy = 0
    profile = get_profile(population)
    
    for col in profile:
        colProb = 0
        for prob in col:
            if prob != 0:
                colProb += (prob * (math.log(prob) / math.log(2)))
        entropy += (-1 * colProb)

    return entropy


entropies = []
for i in xrange(nruns):
    # age and sequence of primodial organism
    population = [[0, 'TCGTACGGTATT']]
    for j in xrange(nyears):
	# five new individuals per
	# individual in the population, with random mutations at each
        # position with given probability                                 
        population = reproduce(population, num_offspring, mutation_rate)

	# remove members of the population that are too old (10 years old)
        population = remove_elders(population, max_age)

        # increase the age of each individual and keep at most 100
        #  individuals, choose randomly if populations is larger that 100
        population = yearend(population, max_population_size)
    entropies.append(calculate_entropy(population))

print 'Years: ' + str(nyears)
print 'Entropy 2: ' + str(sum(entropies)/len(entropies))
