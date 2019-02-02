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

        self._broken_blocks_penalty = 100
        self._overlapping_penalty = 10
        self._distance_penalty = 10
        self._distance_threshold = 0.1

    def _initRandomBlock(self):
        """ Returns a randomly initialized BlockGene """
        return BlockGene(type=Random.randint(1, len(BLOCKS) - 1),
                         pos=(Random.uniform(MIN_X, MAX_X), Random.uniform(MIN_Y, MAX_Y)),
                         r=Random.randint(0, len(ROTATION) - 1))

    def _initDiscreteBlock(self):
        """ Returns a randomly initialized BlockGene positioned in the grid given by the smallest Block size """
        ny = floor((MAX_Y - MIN_Y) / SMALLEST_STEP)
        nx = floor((MAX_X - MIN_X) / SMALLEST_STEP)
        x = Random.randint(0, nx)
        y = Random.randint(0, ny)
        return BlockGene(type = Random.randint(1, len(BLOCKS)-1),
                         pos = (MIN_X + SMALLEST_STEP * x, MIN_Y + SMALLEST_STEP * y),
                         r = Random.randint(0, len(ROTATION) - 1))

    def initRandom(self, n_blocks):
        """ Populates the list of BlockGene with n_blocks random blocks """
        for n in range(n_blocks):
            block = self._initRandomBlock()
            self.appendBlock(block)
        return self

    def initNoOverlapping(self,n_blocks):
        """ Populates the list of BlockGene with n_blocks random blocks that do not overlap """
        while len(self._blocks) < n_blocks:
            block = self._initRandomBlock()
            self.tryAppendBlock(block)
        return self

    def initDiscrete(self,n_blocks):
        """ Populates the list of BlockGene with n_blocks random blocks using _initDiscreteBlock """
        for n in range(n_blocks):
            block = self._initDiscreteBlock()
            self.appendBlock(block)
        return self

    def initDiscreteNoOverlapping(self,n_blocks):
        """ Populates the list of BlockGene with n_blocks random blocks that do not overlap using _initDiscreteBlock """
        while len(self._blocks) < n_blocks:
            block = self._initDiscreteBlock()
            self.tryAppendBlock(block)
        return self


    def appendBlock(self, block):
        """ Adds the block to the list of BlockGene """
        self._blocks.append(block)
        self.n_overlapping+=self._overlappinBlock(block)*2

    def tryAppendBlock(self, block):
        """ Adds the block if it does not overlap with an existing one. Returns true if it was added """
        if not block in self._blocks and self._overlappinBlock(block)==0:
            self.appendBlock(block)
            return True
        else:
            return False

    def removeBlock(self, i):
        """ Removes the block in position i from the list of BlockGene """
        if 0 <= i < len(self._blocks):
            self.n_overlapping -= self._overlappinBlock(self._blocks[i])*2
            self._blocks.remove(self._blocks[i])

    def updateBlock(self, i, block):
        """ Changes the block in position i of the list of BlockGene with the one provided """
        if 0 <= i < len(self._blocks):
            self.n_overlapping -= self._overlappinBlock(self._blocks[i]) * 2
            self._blocks[i] = block
            self.n_overlapping += self._overlappinBlock(block) * 2

    def blocks(self):
        """ Returns the list of BlockGenes """
        return self._blocks

    def calculateFitness(self, avg_vel):
        """ Computes the fitness value given a list of average velocities """
        # This doesn't take into account pigs, since they are added later
        if len(avg_vel)!=0 :
            self.fitness = sum(avg_vel) / len(avg_vel) + self._broken_blocks_penalty*(len(self._blocks)-len(avg_vel))
        else:
            self.fitness =  self._broken_blocks_penalty*(len(self._blocks))

    def calculatePreFitness(self):
        """ Computes the penalty. It is formed by overlapping blocks and distance to the ground penalization """
        self.fitness = self._overlapping_penalty * self.numberOverlappingBlocks()
        min_y = self.distanceToGround()
        self.fitness+= (self._distance_penalty * min_y) if min_y > self._distance_threshold else 0

    def updateBaseFitness(self, new_base):
        """ Sets the base penalty if the LevelIndividual has never been evaluated in simulation """
        if self.base_fitness >= 0: # levels evaluated in game don't need  base
            raw_fitness= self.fitness - self.base_fitness
            self.base_fitness = new_base
            self.fitness = raw_fitness+ new_base

    def _overlappinBlock(self, block):
        """ Returns the number of blocks in the list of BlockGene that overlap with the provided one """
        vertices0 = block.corners()
        n_overlaps = 0
        for j in range(0, len(self._blocks)):
            vertices1 = self._blocks[j].corners()
            if block!=self._blocks[j] and SAT.sat(vertices0, vertices1):
                n_overlaps += 1
        return n_overlaps

    def _initOverlappingBlocks(self):
        """ Computes the number of overlapping in the list of BlockGene """
        n_overlapping=0
        for i in range(len(self._blocks)):
            n_overlapping+= self._overlappinBlock(self._blocks[i])
        return n_overlapping

    def numberOverlappingBlocks(self):
        """ Returns the number of overlapping blocks in the list of BlockGene. It does not compute it """
        return self.n_overlapping

    def distanceToGround(self):
        """ Returns the distance to the ground of the lowest block in the list of BlockGene """
        return abs(ABSOLUTE_GROUND - min(self._blocks, key=lambda b: b.y).y)

    def toString(self):
        return '\nFITNESS '+str(self.fitness)+'( base '+str(self.base_fitness)+')\n'#+strblocks
