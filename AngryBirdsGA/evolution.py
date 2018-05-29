import math
import os
from AngryBirdsGA import *
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA.LevelIndividual import LevelIndividual
import AngryBirdsGA.SeparatingAxisTheorem as SAT
import AngryBirdsGA.XMLHelpers as xml
import numpy as np
from collections import Counter

class Evolution:

    def __init__(self, game_path, write_path, read_path):
        self.population = []
        self.fitness = lambda population, worst_evaluated: \
            self.fitnessPopulationSkip(individuals=population,game_path=game_path, write_path=write_path,
                                       read_path=read_path, max_evaluated=worst_evaluated)
        self.selection = self.selectionTournament
        self.cross = self.crossSampleNoDuplicate
        self.mutation = [ self.mutationBlockType,
                          self.mutationBlockRotation,
                          self.mutationBlockPositionX,
                          self.mutationBlockPositionY]
        self.replacement = self.elitistReplacement


    def registerSelection(self, selection):
        self.selection = selection

    def registerCross(self, cross):
        self.cross = cross

    def initEvolution(self, population_size, initialization_method, fitness_params ):
        assert self.fitness is not None, "Fitness function required"
        self.population = self.initPopulation(population_size, initialization_method)
        return self.fitness(self.population,*fitness_params)

    def runGeneration(self, fitness_params, selection_params, mutation_params, replacement_params):
        assert self.population is not [], "Before executing a generation you need to initialize the evolution"
        assert self.selection is not None, "Selection function required"
        assert self.mutation is not None, "Mutation(s) function required"
        assert self.replacement is not None, "Replacement function required"
        assert self.cross is not None, "Cross function required"
        parents = self.selection(*selection_params)
        children = self.cross(parents)
        for  mut,params in zip(self.mutation,mutation_params):
            mut(children,*params)
        fit_out = self.fitness(children, *fitness_params)
        self.population = self.replacement(children, *replacement_params)

        return self.population, fit_out


    def initPopulation(self,number_of_individuals, initialization_method):
        self.population = []

        for i in range(number_of_individuals):
            self.population.append(initialization_method(LevelIndividual([]),n_blocks=random.randint(MIN_B, MAX_B)))

        return self.population

    def selectionTournament(self, percentage_parents):
        parents = []
        for i in range(int(len(self.population) * percentage_parents) * 2):
            candidate_1, candidate_2 = random.sample(self.population, 2)
            parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))
        return parents

    def crossSample(self, parents):
        children = []
        for i in range(0, len(parents), 2):
            child_n_blocks = min(len(parents[i].blocks()) + len(parents[i + 1].blocks()) // 2, MAX_B)
            child_blocks = random.sample(parents[i].blocks() + parents[i + 1].blocks(), child_n_blocks)
            children.append(LevelIndividual(child_blocks))
        return children

    def crossSampleNoDuplicate(self, parents):
        children = []
        for i in range(0, len(parents), 2):
            common = []
            # fast way of have unique elements in a list of un-hashable objects. If x is not in common, append evaluates and returns None, which evaluates false
            merged = [x for x in parents[i].blocks() + parents[i + 1].blocks() if
                      x not in common and (common.append(x) or True)]
            child_n_blocks = min(len(merged), min(len(parents[i].blocks()) + len(parents[i + 1].blocks()) // 2, MAX_B))
            assert len(merged) >= child_n_blocks, "Length is %r but the mean is %r" % (len(merged), child_n_blocks)
            child_blocks = random.sample(merged, child_n_blocks)
            children.append(LevelIndividual(child_blocks))
        return children

    def mutationBlockNumber(self,individuals, n_mutations, max_difference):
        for a in range(n_mutations):
            n_blocks = random.randint(-max_difference, max_difference)
            indv_mut = individuals[random.randint(0, len(individuals)-1)]

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

    def mutationBlockType(self,individuals, percentage_mutations):
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.type = (block.type+random.choice([-1, 1]))%len(BLOCKS)

            indv_mut.updateBlock(block_i,block)

    def mutationBlockPositionX(self, individuals, percentage_mutations):
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.x = block.x+random.choice([random.uniform(-1,-0.01),random.uniform(0.01,1)])

            indv_mut.updateBlock(block_i,block)

    def mutationBlockPositionY(self, individuals, percentage_mutations):
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.y = block.y+random.choice([random.uniform(-1,-0.01),random.uniform(0.01,1)])

            indv_mut.updateBlock(block_i,block)

    def mutationBlockRotation(self, individuals, percentage_mutations):
        sample = random.sample(individuals,min(math.floor(len(individuals)*percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.rot = (block.rot+random.choice([-1, 1]))%len(ROTATION)

            indv_mut.updateBlock(block_i,block)

    def elitistReplacement(self, new, n_new):
        return sorted((self.population + new), key=lambda a: a.fitness, reverse=False)[:n_new]

    def fitnessPopulationSkip(self,individuals, game_path, write_path, read_path, max_evaluated):

        fill = len(str(len(individuals)))
        evaluated = []
        # generate xml for all potentially suitable levels
        for i in range(len(individuals)):
            individuals[i].calculatePreFitness()
            if individuals[i].fitness == 0:
                xml.writeXML(individuals[i],
                             os.path.join(write_path, "level-" + str(len(evaluated)).zfill(fill) + ".xml"))
                evaluated.append(i)

        # run game
        if len(evaluated) > 0:
            print("Run Game")
            os.system(game_path)

        # parse all xml and update worst value obtained by in game evaluation
        for i in range(len(evaluated)):
            average_velocity = xml.readXML(os.path.join(read_path, "level-" + str(i) + ".xml"))
            # assign fitness
            individuals[evaluated[i]].calculateFitness(average_velocity)
            max_evaluated = max(individuals[evaluated[i]].fitness, max_evaluated)

        # to make sure all levels not evaluated in game have worse fitness value
        for i in range(len(individuals)):
            if i not in evaluated:
                individuals[i].base_fitness = max_evaluated
                individuals[i].fitness += max_evaluated
            else:
                individuals[i].base_fitness = -1  # mark in game evaluated levels

        return max_evaluated


#
# def initPopulationCheckOverlapping(number_of_individuals):
#     population = []
#
#     for i in range(number_of_individuals):
#         population.append(LevelIndividual([]).initNoOverlapping(n_blocks=Random.randint(MIN_B, MAX_B)))
#
#     return population

# def initPopulationDiscretePos(number_of_individuals):
#     population = []
#     for i in range(number_of_individuals):
#         population.append(LevelIndividual([]).initDiscrete(n_blocks = Random.randint(MIN_B, MAX_B)))
#
#     return population
#
# def initPopulationCheckOverlappingDiscretePos(number_of_individuals):
#     population = []
#
#     print("Initializing population 0/" + str(number_of_individuals) + "\r", end="", flush=True)
#     for i in range(number_of_individuals):
#         print("Initializing population " + str(i) + "/" + str(number_of_individuals)+ "\r", end="", flush=True)
#         population.append(LevelIndividual([]).initDiscreteNoOverlapping(n_blocks = Random.randint(MIN_B, MAX_B)))
#
#     print("Initializing population completed")
#     return population


# def fitnessPopulation(population, game_path, write_path, read_path):
#     # generate all xml
#     for i in range(len(population)):
#         xml.writeXML(population[i], os.path.join(write_path, "level-"+str(i)+".xml"))
#
#     # run game
#     os.system(game_path)
#
#     # parse all xml
#     for i in range(len(population)):
#         averageVelocity = xml.readXML(os.path.join(read_path,"level-"+str(i)+".xml"))
#         # assign fitness
#         population[i].calculateFitness(averageVelocity)



def informationEntropy(population, prec):
    c = Counter([round(p.fitness,prec) for p in population])
    k = 1
    for i in range(prec):
        k/=10
    #k = round((max(population, key=lambda x: x.fitness).fitness - min(population, key=lambda x: x.fitness).fitness)/k)
    k = len(population)
    h = - sum( [(f/k)*math.log(f/k,2) for e,f in c.most_common()])
    return h
