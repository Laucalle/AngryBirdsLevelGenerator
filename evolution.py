import math
import constants as cte
import random
import xml_helpers as xml
import os


class BlockGen:
    def __init__(self, type, pos, r):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.rot = r
        self.mat = 0


class LevelIndv:

    def __init__(self, blocks):
        self.blocks = blocks
        self.fitness = float("inf")

    def calculateFitness(self, avg_vel):
        # This doesn't take into account pigs, since they are added later
        self.fitness = 1.0 / 3 * (
                sum(avg_vel) / len(self.blocks) +
                (math.sqrt((len(self.blocks) - cte.B)*(len(self.blocks) - cte.B)) / (cte.MaxB - cte.B)))


def initPopulation(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        for n in range(n_blocks):
            block = BlockGen(type = random.randint(1, len(cte.blocks)-1),
                             pos = (random.uniform(cte.MinX, cte.MaxX), random.uniform(cte.MinB, cte.MaxB)),
                             r = random.randint(0, len(cte.Rotation)-1))
            blocks.append(block)
        population.append(LevelIndv(blocks))

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

def main():
    population_size = 10
    number_of_generations = 10
    number_of_parents = math.floor(0.5*population_size)

    population = initPopulation(population_size)

    FitnessPopulation(population,
                      game_path=os.path.join(os.path.dirname(os.getcwd()), 'ablinux/ab_linux_build.x86_64'),
                      write_path=os.path.join(os.path.dirname(os.getcwd()),
                                              'ablinux/ab_linux_build_Data/StreamingAssets/Levels'),
                      read_path=os.path.join(os.path.dirname(os.getcwd()),
                                             'ablinux/ab_linux_build_Data/StreamingAssets/Output'))

    best_individual = min(population, key=lambda x: x.fitness)

    for i in population:
        print(i.fitness)
    for generation in range(number_of_generations):
        # Select parents
        parents = selectionTournament(population, number_of_parents)
    # generate children
    # mutate children
    # evaluate childres
    # replace generation

if __name__ == "__main__":
    main()