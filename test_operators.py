import unittest
import AngryBirdsGA.evolution as op
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA.LevelIndividual import LevelIndividual
import numpy as np
import unittest.mock as mock
import random

class TestOperator(unittest.TestCase):
    def setUp(self):
        self.population_mock_1 = [LevelIndividual([]),LevelIndividual([]),LevelIndividual([]),LevelIndividual([])]
        self.population_mock_2 = [LevelIndividual([]),LevelIndividual([]),LevelIndividual([]),LevelIndividual([])]
        for n in range(len(self.population_mock_1)):
            self.population_mock_1[n].fitness = n
        for n in range(len(self.population_mock_2)):
            self.population_mock_2[n].fitness =  n + len(self.population_mock_1)

        self.individual_1 = LevelIndividual([BlockGene(type=1, pos=[0,0], r=0),
                           BlockGene(type=1, pos=[0.42,0.42], r=0),
                           BlockGene(type=1, pos=[0.42,2.5], r=0),
                           BlockGene(type=13, pos=[0.5,1.5], r=0)])
        self.individual_2 = LevelIndividual([BlockGene(type=1, pos=[0,0], r=0),
                           BlockGene(type=1, pos=[0.42,0.42], r=0),
                           BlockGene(type=1, pos=[0.42,2.5], r=0),
                           BlockGene(type=13, pos=[0.8,2.0], r=0)])
        self.merged_blocks = [BlockGene(type=1, pos=[0,0], r=0),
                              BlockGene(type=1, pos=[0.42,0.42], r=0),
                              BlockGene(type=1, pos=[0.42,2.5], r=0),
                              BlockGene(type=13, pos=[0.5,1.5], r=0),
                              BlockGene(type=13, pos=[0.8,2.0], r=0)]


    def test_replacement(self):
        result = op.elitistReplacement(self.population_mock_1, self.population_mock_2, len(self.population_mock_1))
        self.assertEqual(result, self.population_mock_1, "Replacement working")

    def test_fitness(self): #???
        pass


    def test_merge_blocks(self):
        common = []
        merged = [x for x in self.individual_1.blocks() + self.individual_2.blocks() if
                  x not in common and (common.append(x) or True)]
        self.assertEqual(merged, self.merged_blocks, "Unique blocks line is working")

    def test_cross(self):
        blocks = random.sample(self.merged_blocks, len(self.individual_1.blocks()))
        with mock.patch('random.sample', lambda x,v: blocks):
            result = op.crossSampleNoDuplicate([self.individual_1, self.individual_2])[0]

        self.assertTrue(np.all(np.asarray([x for x in result.blocks() if x in blocks])))

    def test_mutation(self): #?
        pass

    def test_selection(self):
        parents = [[self.population_mock_1[0], self.population_mock_2[0]],
                   [self.population_mock_1[1],self.population_mock_1[2]]]
        with mock.patch('random.sample', lambda x,v: parents.pop(0)):
            result = op.selectionTournamentNoRepetition(self.population_mock_1+self.population_mock_2, 1)

        self.assertEqual([self.population_mock_1[0], self.population_mock_1[1]], result, "Selection tournament correct")


if __name__ == '__main__':
    unittest.main()
