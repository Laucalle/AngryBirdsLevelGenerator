import math
import constants as cte
import random
import xml_helpers as xml
import os
import numpy as np
import SeparatingAxisTheorem as SAT


class BlockGen:
    def __init__(self, type, pos, r):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.rot = r
        self.mat = 0

    def corners(self):
        dims = cte.blocks[str(self.type)]
        sinA = math.sin(math.radians(int(cte.Rotation[self.rot])))
        cosA = math.cos(math.radians(int(cte.Rotation[self.rot])))

        p_1 = np.array([cosA*dims[0] - sinA*dims[1] + self.x, cosA*dims[1] - sinA*dims[0] + self.y])

        p_2 = np.array([cosA*dims[0] - sinA*(-dims[1]) + self.x, cosA*(-dims[1]) - sinA*dims[0] + self.y])

        p_3 = np.array([cosA*(-dims[0]) - sinA*(-dims[1]) + self.x, cosA*(-dims[1]) - sinA*(-dims[0]) + self.y])

        p_4 = np.array([cosA*(-dims[0]) - sinA*dims[1] + self.x, cosA*dims[1] - sinA*(-dims[0]) + self.y])

        return [p_1,p_2,p_3,p_4]


class LevelIndv:

    def __init__(self, blocks):
        self.blocks = blocks
        self.fitness = float("inf")

    def calculateFitness(self, avg_vel):
        # This doesn't take into account pigs, since they are added later
        if len(avg_vel)!=0 :
            self.fitness = sum(avg_vel) / len(avg_vel) + (len(self.blocks)-len(avg_vel))
        else: # how do we penalize when all blocks are broken
            self.fitness =  100*(len(self.blocks)-len(avg_vel))

    def NumberOverlapingBlocks(self):
        n_overlaping=0
        for i in range(len(self.blocks)):
            vertices0 = self.blocks[i].corners()
            for j in range(i+1,len(self.blocks)):
                vertices1 = self.blocks[j].corners()
                if SAT.sat(vertices0, vertices1):
                    n_overlaping+=1
        return n_overlaping


def initPopulation(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        for n in range(n_blocks):
            block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (random.uniform(cte.MinX, cte.MaxX), random.uniform(cte.MinY, cte.MaxY)),
                             r = random.randint(0, len(cte.Rotation)-1))
            blocks.append(block)
        population.append(LevelIndv(blocks))

    return population

def initPopulationCheckOverlapping(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        while len(blocks)<n_blocks:
            overlaps = False
            block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (random.uniform(cte.MinX, cte.MaxX), random.uniform(cte.MinY, cte.MaxY)),
                             r = random.randint(0, len(cte.Rotation)-1))
            vertices0 = block.corners()
            b=0
            while (not overlaps) and b <len(blocks):
                vertices1 = blocks[b].corners()
                overlaps =  SAT.sat(vertices0,vertices1)
                b=b+1
            if not overlaps:
                blocks.append(block)
        population.append(LevelIndv(blocks))

    return population


def initPopulationFixedPos(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        for n in range(n_blocks):
            block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (cte.MinX + ((cte.MaxX-cte.MinX)/5) * (n%5), cte.MinY + ((cte.MaxY-cte.MinY)/5) * (n // 5)),
                             r = random.randint(0, len(cte.Rotation)-1))
            blocks.append(block)
        population.append(LevelIndv(blocks))

    return population


def initPopulationCheckOverlappingDiscretePos(number_of_individuals):
    population = []
    ny = math.floor((cte.MaxY - cte.MinY)/cte.SmallestStep)
    nx = math.floor((cte.MaxX - cte.MinX)/cte.SmallestStep)

    print("Initializing population 0/" + str(number_of_individuals) + "\r", end="", flush=True)
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        print("Initializing population " + str(i) + "/" + str(number_of_individuals)+ "\r", end="", flush=True)
        while len(blocks)<n_blocks:
            overlaps = False
            x = random.randint(0, nx)
            y = random.randint(0, ny)
            block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (cte.MinX + cte.SmallestStep * x, cte.MinY + cte.SmallestStep * y),
                             r = random.randint(0, len(cte.Rotation)-1))
            vertices0 = block.corners()
            b=0
            while (not overlaps) and b <len(blocks):
                vertices1 = blocks[b].corners()
                overlaps =  SAT.sat(vertices0,vertices1)
                b=b+1
            if not overlaps:
                blocks.append(block)
        population.append(LevelIndv(blocks))
    print("Initializing population completed")
    return population


def FitnessPopulation(population, game_path, write_path, read_path):
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

# NOT WORKING YET
def FitnessPopulationSkip(population, game_path, write_path, read_path):
    # generate all xml
    evaluated= []
    for i in range(len(population)):
        print("Calculating fitness of "+ str(i)+ "/"+str(len(population))+ " with size of " + str(len(population[i].blocks)) +"\r", end="")
        population[i].fitness = 10*population[i].NumberOverlapingBlocks()
        min_y = abs(cte.absolute_ground-min(population[i].blocks, key=lambda b: b.y).y)
        population[i].fitness+= (10*min_y) if min_y>0.1 else 0
        if population[i].fitness == 0:
            xml.writeXML(population[i], os.path.join(write_path, "level-"+str(len(evaluated))+".xml"))
            evaluated.append(i)

    # run game
    if len(evaluated)>0:
        print( "Run Game" )
        os.system(game_path)

    max_evaluated = 0
    # parse all xml
    for i in range(len(evaluated)):
        averageVelocity = xml.readXML(os.path.join(read_path,"level-"+str(i)+".xml"))
        # assign fitness
        population[evaluated[i]].calculateFitness(averageVelocity)
        max_evaluated = max(population[evaluated[i]].fitness, max_evaluated)

    # to make sure all levels not evaluated in game have worse fitness value
    for i in range(len(population)):
        if i not in evaluated:
            population[i].fitness+=max_evaluated


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
        child_n_blocks = min(len(parents[i].blocks) + len(parents[i+1].blocks)//2, cte.MaxB)
        child_blocks = random.sample(parents[i].blocks+parents[i+1].blocks, child_n_blocks)
        children.append(LevelIndv(child_blocks))
    return children


def mutationBlockNumber(population, n_mutations, max_difference):
    for _ in range(n_mutations):
        n_blocks = random.randint(-max_difference, max_difference)
        indv_mut = population[random.randint(0, len(population)-1)]

        if(n_blocks>0):

            ny = math.floor((cte.MaxY - cte.MinY) / cte.SmallestStep)
            nx = math.floor((cte.MaxX - cte.MinX) / cte.SmallestStep)
            for _ in range(n_blocks):
                x = random.randint(0, nx)
                y = random.randint(0, ny)
                block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (cte.MinX + cte.SmallestStep * x, cte.MinY + cte.SmallestStep * y),
                             r = random.randint(0, len(cte.Rotation)-1))
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
            block.type = random.randint(1, len(cte.blocks)-1)
        elif(p == 1):
            block.x = random.uniform(cte.MinX, cte.MaxX)
        elif(p == 2):
            block.y = random.uniform(cte.MinB, cte.MaxB)
        elif(p == 3):
            block.rot = random.randint(0, len(cte.Rotation)-1)


def cleanInputOutput(input_path, output_path):
    for f in os.listdir(input_path):
        os.remove(os.path.join(input_path,f))
    for f in os.listdir(output_path):
        os.remove(os.path.join(output_path,f))

def main():
    #game_path = os.path.join(os.path.dirname(os.getcwd()), 'ablinux/ab_linux_build.x86_64')
    game_path = os.path.join(os.path.dirname(os.getcwd()), 'abwin/win_build.exe')
    write_path = os.path.join(os.path.dirname(os.getcwd()),
                              'abwin/win_build_Data/StreamingAssets/Levels')
    #                          'ablinux/ab_linux_build_Data/StreamingAssets/Levels')
    read_path = os.path.join(os.path.dirname(os.getcwd()),
                             'abwin/win_build_Data/StreamingAssets/Output')
    #                         'ablinux/ab_linux_build_Data/StreamingAssets/Output')
    population_size = 100
    number_of_generations = 100
    number_of_parents = math.floor(0.5*population_size)
    number_of_mutations = math.floor((number_of_parents//2)*0.3)

    population = initPopulationCheckOverlappingDiscretePos(population_size)

    # clean directory (input and output)
    cleanInputOutput(write_path,read_path)

    FitnessPopulationSkip(population, game_path=game_path, write_path=write_path, read_path=read_path)

    for generation in range(number_of_generations):
        print("Generation " + str(generation) + "/" + str(number_of_generations))
        # Select parents
        parents = selectionTournament(population, number_of_parents)
        # generate children
        children = crossSample(parents)
        # mutate children
        mutationBlockProperties(children,number_of_mutations)

        cleanInputOutput(write_path, read_path)
        # evaluate children
        FitnessPopulationSkip(children, game_path=game_path, write_path=write_path, read_path=read_path)
        # replace generation
        population = sorted((children+parents), key=lambda x: x.fitness, reverse = True)[:population_size]

    best_individual = min(population, key=lambda x: x.fitness)

    print("DONE: best-> "+str(best_individual.fitness)+ " avg -> "+ str( sum(map(lambda x: x.fitness, population))/len(population) ) + " worst -> " + str(max(population, key=lambda x: x.fitness).fitness))

    xml.writeXML(best_individual, os.path.join(os.path.dirname(os.getcwd()),
                              'abwin/level-0.xml'))

if __name__ == "__main__":
    main()