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
                    sum(avg_vel) / len(self.blocks) + (math.sqrt(len(self.blocks) - cte.B) / (cte.MaxB - cte.B)))

def initPopulation(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        n_blocks = random.randint(cte.MinB, cte.MaxB)
        blocks = []
        for n in range(n_blocks):
            block = BlockGen(type = random.randint(1, len(cte.blocks)),
                             pos = (random.uniform(cte.MinX, cte.MaxX), random.uniform(cte.MinB, cte.MaxB)),
                             r = random.randint(0, len(cte.Rotation)))
            blocks.append(block)
        population.append(LevelIndv(blocks))

    FitnessPopulation(population,
                      game_path = os.path.join(os.path.dirname(os.getcwd()),'ablinux/ab_linux_build.x86_64'),
                      write_path = os.path.join(os.path.dirname(os.getcwd()),'ablinux/ab_linux_build_Data/StreamingAssets/Levels'),
                      read_path = os.path.join(os.path.dirname(os.getcwd()),'ablinux/ab_linux_build_Data/StreamingAssets/Output'))

    return population


def FitnessPopulation(population, game_path, write_path, read_path):
    # generate all xml
    for i in range(len(population)):
        xml.writeXML( population[i], os.path.join(write_path,"level-"+str(i)+".xml"))

    # run game
    os.system(game_path)

    # parse all xml
    for i in range(len(population)):
        averageVelocity = xml.readXML(os.path.join(read_path,"level-"+str(i)+".xml"))
        # assign fitness
        population[i].calculateFitness(averageVelocity)

def main():
    initPopulation(10)

if __name__ == "__main__":
    main()