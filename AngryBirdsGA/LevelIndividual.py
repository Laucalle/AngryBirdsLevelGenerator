from AngryBirdsGA import *
import AngryBirdsGA.SeparatingAxisTheorem as SAT

class LevelIndividual:

    def __init__(self, blocks):
        self._blocks = blocks
        self.fitness = float("inf")
        self.base_fitness = 0
        self.n_overlapping = self._initOverlappingBlocks()

    def appendBlock(self, block):
        self._blocks.append(block)
        self.n_overlapping+=self._overlappinBlock(block)*2

    def tryAppendBlock(self, block):
        if not block in self._blocks and self._overlappinBlock(block)==0:
            self.appendBlock(block)
            return True
        else:
            return False

    def removeBlock(self, i):
        if 0 <= i < len(self._blocks):
            self.n_overlapping -= self._overlappinBlock(self._blocks[i])*2
            self._blocks.remove(self._blocks[i])

    def updateBlock(self, i, block):
        if 0 <= i < len(self._blocks):
            self.n_overlapping -= self._overlappinBlock(self._blocks[i]) * 2
            self._blocks[i] = block
            self.n_overlapping += self._overlappinBlock(block) * 2

    def blocks(self):
        return self._blocks

    def calculateFitness(self, avg_vel):
        # This doesn't take into account pigs, since they are added later
        if len(avg_vel)!=0 :
            self.fitness = sum(avg_vel) / len(avg_vel) + 100*(len(self._blocks)-len(avg_vel))
        else: # how do we penalize when all blocks are broken
            self.fitness =  100*(len(self._blocks)-len(avg_vel))

    def calculatePreFitness(self):
        self.fitness = 10*self.numberOverlappingBlocks()
        min_y = self.distanceToGround()
        self.fitness+= (10*min_y) if min_y>0.1 else 0

    def updateBaseFitness(self, new_base):
        if self.base_fitness > 0: # levels evaluated in game don't need  base
            raw_fitness= self.fitness - self.base_fitness
            self.base_fitness = new_base
            self.fitness = raw_fitness+ new_base

    def _overlappinBlock(self, block):
        vertices0 = block.corners()
        n_overlaps = 0
        for j in range(0, len(self._blocks)):
            vertices1 = self._blocks[j].corners()
            if block!=self._blocks[j] and SAT.sat(vertices0, vertices1):
                n_overlaps += 1
        return n_overlaps

    def _initOverlappingBlocks(self):
        n_overlapping=0
        for i in range(len(self._blocks)):
            n_overlapping+= self._overlappinBlock(self._blocks[i])
        return n_overlapping

    def numberOverlappingBlocks(self):
        return self.n_overlapping

    def distanceToGround(self):
        return abs(ABSOLUTE_GROUND - min(self._blocks, key=lambda b: b.y).y)

    def toString(self):
        #strblocks= '\n'.join([b.toString() for b in self._blocks])
        assert self.fitness > 0, "Fitness value is wrong: %r" % self.fitness
        return '\nFITNESS '+str(self.fitness)+'( base '+str(self.base_fitness)+')\n'#+strblocks
