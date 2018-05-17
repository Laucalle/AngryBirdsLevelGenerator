import unittest
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA.LevelIndividual import LevelIndividual
from AngryBirdsGA import BLOCKS, ROTATION
import numpy as np
from math import sin, cos, radians

class TestLevelIndividual(unittest.TestCase):
    def setUp(self):
        self.block1 = BlockGene( type=1, pos=[0,0], r=0)
        self.block2 = BlockGene( type=2, pos=[0,0], r=1)
        self.individual = LevelIndividual([self.block1])
        self.blocklist1 = [BlockGene(type=1, pos=[0,0], r=0),
                           BlockGene(type=1, pos=[0.42,0.42], r=0),
                           BlockGene(type=1, pos=[0.42,2.5], r=0),
                           BlockGene(type=13, pos=[0.5,1.5], r=0)]
        self.individual2 = LevelIndividual(self.blocklist1)

    def test_should_initialize_individual_OK(self):
        self.assertIsInstance(self.individual, LevelIndividual, "Object created")

    def test_append_block(self):
        self.individual.appendBlock(self.block2)
        self.assertEqual(self.individual.blocks(), [self.block1,self.block2], "Block appended")

    def test_remove_block(self):
        self.individual.removeBlock(0)
        self.assertEqual(self.individual.blocks(), [], "Block removed")

    def test_update_block(self):
        self.individual.updateBlock(0,self.block2)
        self.assertEqual(self.individual.blocks(), [self.block2], "Block changed")

    def test_try_append_block_error(self):
        self.assertTrue(not self.individual.tryAppendBlock(self.block2) and self.individual.blocks() == [self.block1])

    def test_try_append_block_success(self):
        block = BlockGene( type=1, pos=[2,2], r=0)
        self.assertTrue(self.individual.tryAppendBlock(block) and self.individual.blocks() == [self.block1, block])

    def test_overlapping_blocks(self):
        self.assertEqual(self.individual2.numberOverlappingBlocks(), 6)

    def test_overlapping_blocks_update(self):
        self.individual2.updateBlock(3,BlockGene(type=5, pos =[0.5,1.5], r=0))
        self.assertEqual(self.individual2.numberOverlappingBlocks(), 2)

    def test_overlapping_blocks_remove(self):
        self.individual2.removeBlock(3)
        self.assertEqual(self.individual2.numberOverlappingBlocks(), 2)

    def test_overlapping_blocks_append(self):
        self.individual2.appendBlock(BlockGene(type=13, pos=[0.5, 1.5], r=2))
        self.assertEqual(self.individual2.numberOverlappingBlocks(), 8)

    def test_init_random_len(self):
        individual = LevelIndividual([]).initRandom(8)
        self.assertTrue(len(individual.blocks()) == 8)

    def test_init_discrete_len(self):
        individual = LevelIndividual([]).initDiscrete(8)
        self.assertTrue(len(individual.blocks()) == 8)

    def test_init_no_overlapping_len(self):
        individual = LevelIndividual([]).initNoOverlapping(8)
        self.assertTrue(len(individual.blocks()) == 8)

    def test_init_discrete_no_overlapping_len(self):
        individual = LevelIndividual([]).initDiscreteNoOverlapping(8)
        self.assertTrue(len(individual.blocks()) == 8)

    def test_init_no_overlapping(self):
        individual = LevelIndividual([]).initNoOverlapping(8)
        self.assertTrue(individual.numberOverlappingBlocks() == 0)

    def test_init_discrete_no_overlapping(self):
        individual = LevelIndividual([]).initDiscreteNoOverlapping(8)
        self.assertTrue(individual.numberOverlappingBlocks() == 0)

if __name__ == '__main__':
    unittest.main()
