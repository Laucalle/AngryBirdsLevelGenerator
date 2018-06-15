from math import floor
from AngryBirdsGA import *
import AngryBirdsGA.SeparatingAxisTheorem as SAT
from AngryBirdsGA.BlockGene import BlockGene

class LevelIndividual:

    def __init__(self, blocks):
        self._blocks = blocks
        self.fitness = None
        self.base_fitness = 0
        self.n_overlapping = self._initOverlappingBlocks()
        self.broken_penalty = 0

        self._broken_blocks_penalty = 100
        self._overlapping_penalty = 10
        self._distance_penalty = 10
        self._distance_threshold = 0.1

    def _initRandomBlock(self):
        return BlockGene(type=Random.randint(1, len(BLOCKS) - 1),
                         pos=(Random.uniform(MIN_X, MAX_X), Random.uniform(MIN_Y, MAX_Y)),
                         r=Random.randint(0, len(ROTATION) - 1))

    def _initDiscreteBlock(self):
        ny = floor((MAX_Y - MIN_Y) / SMALLEST_STEP)
        nx = floor((MAX_X - MIN_X) / SMALLEST_STEP)
        x = Random.randint(0, nx)
        y = Random.randint(0, ny)
        return BlockGene(type = Random.randint(1, len(BLOCKS)-1),
                         pos = (MIN_X + SMALLEST_STEP * x, MIN_Y + SMALLEST_STEP * y),
                         r = Random.randint(0, len(ROTATION) - 1))

    def initRandom(self, n_blocks):
        for n in range(n_blocks):
            block = self._initRandomBlock()
            self.appendBlock(block)
        return self

    def initNoOverlapping(self,n_blocks):
        while len(self._blocks) < n_blocks:
            block = self._initRandomBlock()
            self.tryAppendBlock(block)
        return self

    def initDiscrete(self,n_blocks):
        for n in range(n_blocks):
            block = self._initDiscreteBlock()
            self.appendBlock(block)
        return self

    def initDiscreteNoOverlapping(self,n_blocks):
        while len(self._blocks) < n_blocks:
            block = self._initDiscreteBlock()
            self.tryAppendBlock(block)
        return self


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
        self.broken_penalty = self._broken_blocks_penalty*(len(self._blocks)-len(avg_vel))
        if len(avg_vel)!=0 :
            #assert sum(avg_vel) / len(avg_vel) > 0, "Negative velocity %r" % avg_vel
            #assert self._broken_blocks_penalty*(len(self._blocks)-len(avg_vel))>= 0, "More blocks than expected, %r expected %r" % (len(self._blocks),len(avg_vel))
            self.fitness = sum(avg_vel) / len(avg_vel) + self._broken_blocks_penalty*(len(self._blocks)-len(avg_vel))
        else: # how do we penalize when all blocks are broken
            self.fitness =  self._broken_blocks_penalty*(len(self._blocks))

    def calculatePreFitness(self):
        self.fitness = self._overlapping_penalty * self.numberOverlappingBlocks()
        min_y = self.distanceToGround()
        self.fitness+= (self._distance_penalty * min_y) if min_y > self._distance_threshold else 0

    def updateBaseFitness(self, new_base):
        if self.base_fitness >= 0: # levels evaluated in game don't need  base
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
        return '\nFITNESS '+str(self.fitness)+'( base '+str(self.base_fitness)+')\n'#+strblocks
