import math
import random
import os
from AngryBirdsGA import *
from AngryBirdsGA.BlockGene import BlockGene
import AngryBirdsGA.SeparatingAxisTheorem as SAT
import AngryBirdsGA.XMLHelpers as xml
import numpy as np

class LevelIndividual:

    def __init__(self, blocks):
        self.blocks = blocks
        self.fitness = float("inf")
        self.base_fitness = 0

    def calculateFitness(self, avg_vel):
        # This doesn't take into account pigs, since they are added later
        if len(avg_vel)!=0 :
            self.fitness = sum(avg_vel) / len(avg_vel) + 100*(len(self.blocks)-len(avg_vel))
        else: # how do we penalize when all blocks are broken
            self.fitness =  100*(len(self.blocks)-len(avg_vel))

    def calculatePreFitness(self):
        self.fitness = 10*self.numberOverlappingBlocks()
        min_y = self.distanceToGround()
        self.fitness+= (10*min_y) if min_y>0.1 else 0

    def updateBaseFitness(self, new_base):
        if self.base_fitness > 0: # levels evaluated in game don't need  base
            raw_fitness= self.fitness - self.base_fitness
            self.base_fitness = new_base
            self.fitness = raw_fitness+ new_base

    def numberOverlappingBlocks(self):
        n_overlapping=0
        for i in range(len(self.blocks)):
            vertices0 = self.blocks[i].corners()
            for j in range(i+1,len(self.blocks)):
                vertices1 = self.blocks[j].corners()
                if SAT.sat(vertices0, vertices1):
                    n_overlapping+=1
        return n_overlapping

    def distanceToGround(self):
        return abs(ABSOLUTE_GROUND - min(self.blocks, key=lambda b: b.y).y)

    def toString(self):
        #strblocks= '\n'.join([b.toString() for b in self.blocks])
        assert self.fitness > 0, "Fitness value is wrong: %r" % self.fitness
        return '\nFITNESS '+str(self.fitness)+'( base '+str(self.base_fitness)+')\n'#+strblocks


def initPopulation(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(MIN_B, MAX_B)
        blocks = []
        for n in range(n_blocks):
            block = BlockGene(type = random.randint(1, len(blocks)-1),
                              pos = (random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)),
                              r = random.randint(0, len(ROTATION) - 1))
            blocks.append(block)
        population.append(LevelIndividual(blocks))

    return population


def initPopulationCheckOverlapping(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(MIN_B, MAX_B)
        blocks = []
        while len(blocks)<n_blocks:
            overlaps = False
            block = BlockGene(type = random.randint(1, len(blocks)-1),
                              pos = (random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)),
                              r = random.randint(0, len(ROTATION) - 1))
            vertices0 = block.corners()
            b=0
            while (not overlaps) and b <len(blocks):
                vertices1 = blocks[b].corners()
                overlaps =  SAT.sat(vertices0,vertices1)
                b=b+1
            if not overlaps:
                blocks.append(block)
        population.append(LevelIndividual(blocks))

    return population


def initPopulationFixedPos(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(MIN_B, MAX_B)
        blocks = []
        for n in range(n_blocks):
            block = BlockGene(type = random.randint(1, len(blocks)-1),
                              pos = (MIN_X + ((MAX_X - MIN_X) / 5) * (n % 5), MIN_Y + ((MAX_Y - MIN_Y) / 5) * (n // 5)),
                              r = random.randint(0, len(ROTATION) - 1))
            blocks.append(block)
        population.append(LevelIndividual(blocks))

    return population


def initPopulationCheckOverlappingDiscretePos(number_of_individuals):
    population = []
    ny = math.floor((MAX_Y - MIN_Y) / SMALLEST_STEP)
    nx = math.floor((MAX_X - MIN_X) / SMALLEST_STEP)

    print("Initializing population 0/" + str(number_of_individuals) + "\r", end="", flush=True)
    for i in range(number_of_individuals):
        n_blocks = random.randint(MIN_B, MAX_B)
        blocks = []
        print("Initializing population " + str(i) + "/" + str(number_of_individuals)+ "\r", end="", flush=True)
        while len(blocks)<n_blocks:
            overlaps = False
            x = random.randint(0, nx)
            y = random.randint(0, ny)
            block = BlockGene(type = random.randint(1, len(BLOCKS)-1),
                              pos = (MIN_X + SMALLEST_STEP * x, MIN_Y + SMALLEST_STEP * y),
                              r = random.randint(0, len(ROTATION) - 1))
            vertices0 = block.corners()
            b=0
            while (not overlaps) and b <len(blocks):
                vertices1 = blocks[b].corners()
                overlaps =  SAT.sat(vertices0,vertices1)
                b=b+1
            if not overlaps:
                blocks.append(block)
        population.append(LevelIndividual(blocks))
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
    evaluated= []
    for i in range(len(population)):
        print("Calculating fitness of "+ str(i)+ "/"+str(len(population))+ " with size of " + str(len(population[i].blocks)) +"\r", end="")
        population[i].calculatePreFitness()
        if population[i].fitness == 0:
            xml.writeXML(population[i], os.path.join(write_path, "level-"+str(len(evaluated))+".xml"))
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


def crossSample(parents):
    children = []
    for i in range(0,len(parents), 2):
        child_n_blocks = min(len(parents[i].blocks) + len(parents[i+1].blocks) // 2, MAX_B)
        child_blocks = random.sample(parents[i].blocks+parents[i+1].blocks, child_n_blocks)
        children.append(LevelIndividual(child_blocks))
    return children


def mutationBlockNumber(population, n_mutations, max_difference):
    for _ in range(n_mutations):
        n_blocks = random.randint(-max_difference, max_difference)
        indv_mut = population[random.randint(0, len(population)-1)]

        if(n_blocks>0):

            ny = math.floor((MAX_Y - MIN_Y) / SMALLEST_STEP)
            nx = math.floor((MAX_X - MIN_X) / SMALLEST_STEP)
            for _ in range(n_blocks):
                x = random.randint(0, nx)
                y = random.randint(0, ny)
                block = BlockGene(type = random.randint(1, len(BLOCKS) - 1),
                                  pos = (MIN_X + SMALLEST_STEP * x, MIN_Y + SMALLEST_STEP * y),
                                  r = random.randint(0, len(ROTATION) - 1))
                indv_mut.blocks.append(block)
        else:
            for _ in range(-n_blocks):
                block = indv_mut.blocks[random.randint(0,len(indv_mut.blocks)-1)]
                indv_mut.blocks.remove(block)


def mutationBlockProperties(population, n_mutations):
    for _ in range(n_mutations):
        indv_mut = population[random.randint(0, len(population) - 1)]
        p = random.randint(0,3)
        block = indv_mut.blocks[random.randint(0, len(indv_mut.blocks) - 1)]
        if(p == 0):
            block.type = random.randint(1, len(BLOCKS) - 1)
        elif(p == 1):
            block.x = random.uniform(MIN_X, MAX_X)
        elif(p == 2):
            block.y = random.uniform(MIN_B, MAX_B)
        elif(p == 3):
            block.rot = random.randint(0, len(ROTATION) - 1)


def cleanDirectory(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path,f))


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
        parents = selectionTournament(population, number_of_parents)
        # generate children
        children = crossSample(parents)
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

        print("DONE: best-> " + str(population[0].fitness) + " avg -> " + str(
            sum(map(lambda x: x.fitness, population)) / len(population)) + " worst -> " + str(
            max(population, key=lambda x: x.fitness).fitness))

        f = open(os.path.join(os.path.dirname(os.getcwd()), 'tfgLogs/log.txt'), 'a')
        f.write("----------------------------------------------Generation " + str(generation) + "/" + str(number_of_generations)+ "----------------------------------------------")
        for i in population:
            f.write(i.toString())
        f.close()

    best_individual = min(population, key=lambda x: x.fitness)

    print("DONE: best-> "+str(best_individual.fitness)+ " avg -> "+ str( sum(map(lambda x: x.fitness, population))/len(population) ) + " worst -> " + str(max(population, key=lambda x: x.fitness).fitness))

    xml.writeXML(best_individual, os.path.join(os.path.dirname(os.getcwd()),
                                               'abwin/level-0.xml'))

if __name__ == "__main__":
    main()
