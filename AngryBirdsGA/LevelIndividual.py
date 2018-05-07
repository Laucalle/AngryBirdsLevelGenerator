from AngryBirdsGA import *
import AngryBirdsGA.SeparatingAxisTheorem as SAT

class LevelIndividual:

    def __init__(self, blocks):
        self.blocks = blocks
        self.fitness = float("inf")
        self.base_fitness = 0
        self.numberOverlappingBlocks()

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
