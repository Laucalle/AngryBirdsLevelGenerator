import math
import random
import os
from AngryBirdsGA import *
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA.LevelIndividual import LevelIndividual
import AngryBirdsGA.SeparatingAxisTheorem as SAT
import AngryBirdsGA.XMLHelpers as xml
import numpy as np
from collections import Counter

def initPopulation(number_of_individuals):
    population = []

    for i in range(number_of_individuals):
        population.append(LevelIndividual([]).initRandom(n_blocks=random.randint(MIN_B, MAX_B)))

    return population

def initPopulationCheckOverlapping(number_of_individuals):
    population = []

    for i in range(number_of_individuals):
        population.append(LevelIndividual([]).initNoOverlapping(n_blocks=random.randint(MIN_B, MAX_B)))

    return population

def initPopulationFixedPos(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        population.append(LevelIndividual([]).initDiscrete(n_blocks = random.randint(MIN_B, MAX_B)))

    return population

def initPopulationCheckOverlappingDiscretePos(number_of_individuals):
    population = []

    print("Initializing population 0/" + str(number_of_individuals) + "\r", end="", flush=True)
    for i in range(number_of_individuals):
        print("Initializing population " + str(i) + "/" + str(number_of_individuals)+ "\r", end="", flush=True)
        population.append(LevelIndividual([]).initDiscreteNoOverlapping(n_blocks = random.randint(MIN_B, MAX_B)))

    print("Initializing population completed")
    return population


def fitnessPopulation(population, game_path, write_path, read_path):
    # generate all xml
    for i in range(len(population)):
        xml.writeXML(population[i], os.path.join(write_path, "level-"+str(i)+".xml"))

    # run game
    os.system(game_path)

    # parse all xml
    for i in range(len(population)):
        averageVelocity = xml.readXML(os.path.join(read_path,"level-"+str(i)+".xml"))
        # assign fitness
        population[i].calculateFitness(averageVelocity)

def fitnessPopulationSkip(population, game_path, write_path, read_path, max_evaluated):
    # generate all xml
    fill = len(str(len(population)))
    evaluated= []
    for i in range(len(population)):
        print("Calculating fitness of "+ str(i)+ "/"+str(len(population))+ " with size of " + str(len(population[i].blocks())) +"\r", end="")
        population[i].calculatePreFitness()
        if population[i].fitness == 0:
            xml.writeXML(population[i], os.path.join(write_path, "level-"+str(len(evaluated)).zfill(fill)+".xml"))
            evaluated.append(i)

    # run game
    if len(evaluated)>0:
        print( "Run Game" )
        os.system(game_path)


    # parse all xml
    for i in range(len(evaluated)):
        averageVelocity = xml.readXML(os.path.join(read_path,"level-"+str(i)+".xml"))
        # assign fitness
        population[evaluated[i]].calculateFitness(averageVelocity)
        max_evaluated = max(population[evaluated[i]].fitness, max_evaluated)

    # to make sure all levels not evaluated in game have worse fitness value
    for i in range(len(population)):
        if i not in evaluated:
            population[i].base_fitness = max_evaluated
            population[i].fitness+=max_evaluated

    return max_evaluated


def selectionTournament(population,n_tournaments):
    parents = []
    for i in range(n_tournaments):
        candidate_1 = population[random.randint(0,len(population)-1)]
        candidate_2 = population[random.randint(0,len(population)-1)]
        parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))

        candidate_1 = population[random.randint(0,len(population)-1)]
        candidate_2 = population[random.randint(0,len(population)-1)]
        parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))
    return parents

def selectionTournamentNoRepetition(population,n_tournaments):
    parents = []
    for i in range(n_tournaments):
        candidate_1, candidate_2  = random.sample(population,2)
        parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))

        candidate_1, candidate_2  = random.sample(population,2)
        parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))
    return parents


def crossSample(parents):
    children = []
    for i in range(0,len(parents), 2):
        child_n_blocks = min(len(parents[i].blocks()) + len(parents[i+1].blocks()) // 2, MAX_B)
        child_blocks = random.sample(parents[i].blocks()+parents[i+1].blocks(), child_n_blocks)
        children.append(LevelIndividual(child_blocks))
    return children

def crossSampleNoDuplicate(parents):
    children = []
    for i in range(0,len(parents), 2):
        common = []
        #fast way of have unique elements in a list of unhashable objects. If x is not in common, append evaluates and returns None, which evaluates false
        merged = [x for x in parents[i].blocks()+parents[i+1].blocks() if x not in common and (common.append(x) or True)]
        child_n_blocks = min(len(merged),min(len(parents[i].blocks()) + len(parents[i+1].blocks()) // 2, MAX_B))
        assert len(merged)>=child_n_blocks, "Lenght is %r but the mean is %r" % (len(merged),child_n_blocks)
        child_blocks = random.sample(merged, child_n_blocks)
        children.append(LevelIndividual(child_blocks))
    return children


def mutationBlockNumber(population, n_mutations, max_difference):
    for a in range(n_mutations):
        n_blocks = random.randint(-max_difference, max_difference)
        indv_mut = population[random.randint(0, len(population)-1)]

        if(n_blocks>0):

            ny = math.floor((MAX_Y - MIN_Y) / SMALLEST_STEP)
            nx = math.floor((MAX_X - MIN_X) / SMALLEST_STEP)
            for b in range(n_blocks):
                x = random.randint(0, nx)
                y = random.randint(0, ny)
                block = BlockGene(type = random.randint(1, len(BLOCKS) - 1),
                                  pos = (MIN_X + SMALLEST_STEP * x, MIN_Y + SMALLEST_STEP * y),
                                  r = random.randint(0, len(ROTATION) - 1))
                indv_mut.appendBlock(block)
        else:
            for b in range(-n_blocks):
                indv_mut.removeBlock(random.randint(0,len(indv_mut.blocks())-1))

def mutationBlockProperties(population, n_mutations):
    for _ in range(n_mutations):
        indv_mut = population[random.randint(0, len(population) - 1)]
        p = random.randint(0,3)
        block_i = random.randint(0, len(indv_mut.blocks()) - 1)
        block = BlockGene(type=indv_mut.blocks()[block_i].type,
                          pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].x),
                          r=indv_mut.blocks()[block_i].rot)
        if p == 0:
            block.type = random.randint(1, len(BLOCKS) - 1)
        elif p == 1:
            block.x = random.uniform(MIN_X, MAX_X)
        elif p == 2:
            block.y = random.uniform(MIN_B, MAX_B)
        elif p == 3:
            block.rot = random.randint(0, len(ROTATION) - 1)

        indv_mut.updateBlock(block_i,block)


def cleanDirectory(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path,f))

def informationEntropy(population, prec):
    c = Counter([round(p.fitness,prec) for p in population])
    k = 1
    for i in range(prec):
        k/=10
    #k = round((max(population, key=lambda x: x.fitness).fitness - min(population, key=lambda x: x.fitness).fitness)/k)
    k = len(population)
    h = - sum( [(f/k)*math.log(f/k,2) for e,f in c.most_common()])
    return h

def main():
    #game_path = os.path.join(os.path.dirname(os.getcwd()), 'ablinux/ab_linux_build.x86_64')
    project_root = os.path.dirname(os.getcwd())
    game_path = os.path.join(os.path.dirname(project_root), 'abwin/win_build.exe')
    write_path = os.path.join(os.path.dirname(project_root),
                              'abwin/win_build_Data/StreamingAssets/Levels')
    #                          'ablinux/ab_linux_build_Data/StreamingAssets/Levels')
    read_path = os.path.join(os.path.dirname(project_root),
                             'abwin/win_build_Data/StreamingAssets/Output')
    #                         'ablinux/ab_linux_build_Data/StreamingAssets/Output')
    log_path = os.path.join(os.path.dirname(project_root), 'tfgLogs/log.txt')
    population_size = 100
    number_of_generations = 100
    number_of_parents = math.floor(0.5*population_size)
    number_of_mutations = math.floor((number_of_parents//2)*0.3)

    population = initPopulationCheckOverlappingDiscretePos(population_size)

    # clean directory (input and output)
    cleanDirectory(write_path)
    cleanDirectory(read_path)
    if os.path.isfile(log_path):
        os.remove(log_path)

    max_evaluated = fitnessPopulationSkip(population, game_path=game_path, write_path=write_path, read_path=read_path, max_evaluated=0)

    for generation in range(number_of_generations):
        print("Generation " + str(generation) + "/" + str(number_of_generations))
        # Select parents
        parents = selectionTournamentNoRepetition(population, number_of_parents)
        # generate children
        children = crossSampleNoDuplicate(parents)
        # mutate children
        mutationBlockProperties(children,number_of_mutations)

        cleanDirectory(write_path)
        cleanDirectory(read_path)
        # evaluate children
        max_evaluated = fitnessPopulationSkip(children, game_path=game_path, write_path=write_path, read_path=read_path, max_evaluated=max_evaluated)
        # replace generation
        for i in population+children:
            i.updateBaseFitness(max_evaluated)
        population = sorted((children+parents), key=lambda x: x.fitness, reverse = False)[:population_size]

        print("ENTROPY " + str(informationEntropy(population, 4)) + " best-> " + str(population[0].fitness) + " avg -> " + str(
            sum(map(lambda x: x.fitness, population)) / len(population)) + " worst -> " + str(
            max(population, key=lambda x: x.fitness).fitness))

        f = open(os.path.join(os.path.dirname(project_root), 'tfgLogs/log.txt'), 'a')
        f.write("----------------------------------------------Generation " + str(generation) + "/" + str(number_of_generations)+ "----------------------------------------------")
        for level in population:
            f.write(level.toString())
        f.close()

    best_individual = min(population, key=lambda x: x.fitness)

    print("DONE: best-> "+str(best_individual.fitness)+ " avg -> "+ str( sum(map(lambda x: x.fitness, population))/len(population) ) + " worst -> " + str(max(population, key=lambda x: x.fitness).fitness))

    xml.writeXML(best_individual, os.path.join(os.path.dirname(project_root),
                                               'abwin/level-0.xml'))

if __name__ == "__main__":
    main()
