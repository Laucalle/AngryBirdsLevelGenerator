import math
import os
from AngryBirdsGA import *
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA.LevelIndividual import LevelIndividual
import AngryBirdsGA.SeparatingAxisTheorem as SAT
import AngryBirdsGA.XmlHelpers as xml
import numpy as np
from collections import Counter
import subprocess

class Evolution:

    def __init__(self, game_path, write_path, read_path):
        self.population = []
        self.fitness = lambda population, worst_evaluated: \
            self.fitnessPopulationSkip(individuals=population,game_path=game_path, write_path=write_path,
                                       read_path=read_path, max_evaluated=worst_evaluated)
        self.selection = self.selectionTournament
        self.cross = self.crossMaintainCommon
        self.mutation = [ self.mutationBlockType,
                          self.mutationBlockRotation,
                          self.mutationBlockPositionX,
                          self.mutationBlockPositionY]
        self.replacement = self.elitistReplacement

    def initEvolution(self, population_size, initialization_method, fitness_params ):
        """ Sets the initial population and its fitness and returns it"""
        self.population = self.initPopulation(population_size, initialization_method)
        return self.fitness(self.population,*fitness_params)

    def runGeneration(self, fitness_params, selection_params, mutation_params, replacement_params):
        """ Runs a generation: selection, crossover, mutation and replacement. Returns the population and base penalty """
        assert self.population is not [], "Before executing a generation you need to initialize the evolution"
        parents = self.selection(*selection_params)
        children = self.cross(parents)
        for  mut,params in zip(self.mutation,mutation_params):
            mut(children,*params)
        fit_out = self.fitness(children, *fitness_params)
        for l in self.population:
            l.updateBaseFitness(fit_out)
        self.population = self.replacement(children, *replacement_params)

        return self.population, fit_out


    def initPopulation(self,number_of_individuals, initialization_method):
        """ Initializes the population with a number of LevelIndividual (number_of_individuals) using the initialization method """
        self.population = []

        for i in range(number_of_individuals):
            self.population.append(initialization_method(LevelIndividual([]),n_blocks=random.randint(MIN_B, MAX_B)))

        return self.population

    def selectionTournament(self, percentage_parents):
        """ Returns percentage_of_parents pairs of LevelIndividual from population selected with a binary tournament """
        parents = []
        for i in range(int(len(self.population) * percentage_parents) * 2):
            candidate_1, candidate_2 = random.sample(self.population, 2)
            parents.append(min(candidate_1, candidate_2, key=lambda x: x.fitness))
        return parents

    def crossSample(self, parents):
        """ Crossover operator. It samples the blocks from each two parents from the list of parents. One new individual per pair """
        children = []
        for i in range(0, len(parents), 2):
            child_n_blocks = min(len(parents[i].blocks()) + len(parents[i + 1].blocks()) // 2, MAX_B)
            child_blocks = random.sample(parents[i].blocks() + parents[i + 1].blocks(), child_n_blocks)
            children.append(LevelIndividual(child_blocks))
        return children

    def crossSampleNoDuplicate(self, parents):
        """ Crossover operator. It samples the blocks (without duplicates) from each two parents from the list of parents. One new individual per pair """
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

    def crossMaintainCommon(self, parents):
        """ Crossover operator. It blocks present in both parents pass on to the children, the rest are split between the two children """
        children = []
        for i in range(0, len(parents), 2):
            common = [x for x in parents[i].blocks() if x in parents[i + 1].blocks()]
            uncommon =[x for x in parents[i].blocks()+ parents[i+1].blocks() if x not in common ]
            random.shuffle(uncommon)
            children.append(LevelIndividual(common + uncommon[:len(uncommon)//2]))
            children.append(LevelIndividual(common + uncommon[len(uncommon)//2:]))
        return children


    def mutationBlockNumber(self,individuals, n_mutations, max_difference):
        """ Mutates n_mutations individuals and it adds or removes up to max_difference blocks """
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
        """ Mutates a percentage of individuals by changing the block type of one of their blocks"""
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.type = (block.type+random.choice([-1, 1]))%len(BLOCKS)

            indv_mut.updateBlock(block_i,block)

    def mutationBlockPositionX(self, individuals, percentage_mutations):
        """ Mutates a percentage of individuals by adding a value from [-1,0)(0,1] to the x coordinate of one of their blocks"""
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.x = block.x+random.choice([random.uniform(-1,-0.01),random.uniform(0.01,1)])

            indv_mut.updateBlock(block_i,block)

    def mutationBlockPositionY(self, individuals, percentage_mutations):
        """ Mutates a percentage of individuals by adding a value from [-1,0)(0,1] to the y coordinate of one of their blocks"""
        sample = random.sample(individuals, min(math.floor(len(individuals) * percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.y = block.y+random.choice([random.uniform(-1,-0.01),random.uniform(0.01,1)])

            indv_mut.updateBlock(block_i,block)

    def mutationBlockRotation(self, individuals, percentage_mutations):
        """ Mutates a percentage of individuals by adding 45 or -45 to the rotation of one of their blocks"""
        sample = random.sample(individuals,min(math.floor(len(individuals)*percentage_mutations), len(individuals)))
        for indv_mut in sample:
            block_i = random.randint(0, len(indv_mut.blocks()) - 1)
            block = BlockGene(type=indv_mut.blocks()[block_i].type,
                              pos=(indv_mut.blocks()[block_i].x, indv_mut.blocks()[block_i].y),
                              r=indv_mut.blocks()[block_i].rot)
            block.rot = (block.rot+random.choice([-1, 1]))%len(ROTATION)

            indv_mut.updateBlock(block_i,block)

    def elitistReplacement(self, new, n_new):
        """ Returns the n_best best individuals from both population and offspring(new) """
        return sorted((self.population + new), key=lambda a: a.fitness, reverse=False)[:n_new]

    def fitnessPopulationSkip(self,individuals, game_path, write_path, read_path, max_evaluated):
        """ Computes the fitness value for the individuals. It launches the simulation but skips levels with penalty """
        fill = len(str(len(individuals)))
        evaluated = []
        # generate xml for all potentially suitable levels
        for i in range(len(individuals)):
            individuals[i].calculatePreFitness()
            if individuals[i].fitness == 0:
                xml.writePlain(individuals[i],
                             os.path.join(write_path, "level_raw_" + str(i).zfill(fill) + ".txt"))
                
                evaluated.append(i)
        #run simulation 
        for i in evaluated:
            proc = subprocess.Popen([game_path, os.path.join(write_path, "level_raw_" + str(i).zfill(fill) + ".txt")], stdout = subprocess.PIPE)
            average_velocity = []
            # parse all files and update worst value obtained by in game evaluation
            while True:
                line = proc.stdout.readline()
                if line:
                    #print(repr(line))
                    average_velocity.append(float(line))
                else:
                    break
            individuals[i].calculateFitness(average_velocity)
            max_evaluated = max(individuals[i].fitness, max_evaluated)


        # to make sure all levels not evaluated in game have worse fitness value
        for i in range(len(individuals)):
            if i not in evaluated:
                individuals[i].base_fitness = max_evaluated
                individuals[i].fitness += max_evaluated
            else:
                individuals[i].base_fitness = -1  # mark in game evaluated levels

        return max_evaluated

def informationEntropy(population, prec):
    """ Returns Shannon's entropy on the fitness """
    c = Counter([round(p.fitness,prec) for p in population])
    k = 1
    for i in range(prec):
        k/=10
    k = len(population)
    h = - sum( [(f/k)*math.log(f/k,2) for e,f in c.most_common()])
    return h
