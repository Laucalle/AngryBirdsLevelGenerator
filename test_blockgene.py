import unittest
from AngryBirdsGA.BlockGene import BlockGene
from AngryBirdsGA import BLOCKS, ROTATION
import numpy as np
from math import sin, cos, radians

class TestBlockGene(unittest.TestCase):

    def setUp(self):
        self.gene = BlockGene( type=1, pos=[0,0], r=1)
        self.gene1 = BlockGene( type=2, pos=[0,0], r=0)

    def test_should_initialize_gene_OK(self):
        self.assertIsInstance(self.gene, BlockGene, "Object created")

    def test_equals(self):
        self.assertTrue(self.gene == BlockGene( type=1, pos=[0,0], r=1))

    def test_corners_cache(self):
        corners1 = self.gene.corners()
        corners2 = self.gene.corners()
        self.assertIs(corners1, corners2, "Corners are cached")

    def test_corners_calculation_0(self):
        dims = [BLOCKS[str(self.gene1.type)][0] / 2, BLOCKS[str(self.gene1.type)][1] / 2]
        corners = [np.asarray([dims[0],dims[1]]), np.asarray([+dims[0],-dims[1]]),
                   np.asarray([-dims[0],-dims[1]]), np.asarray([-dims[0],+dims[1]])]
        #self.assertCountEqual(corners, gene1.corners())
        self.assertTrue( (np.asarray(corners) == np.asarray(self.gene1.corners())).all() )

    def test_corners_calculation_1(self):

        dims = [BLOCKS[str(self.gene.type)][0] / 2, BLOCKS[str(self.gene.type)][1] / 2]
        sinA = sin(radians(int(ROTATION[1])))
        cosA = cos(radians(int(ROTATION[1])))
        corners = [np.asarray([+ dims[0] * cosA - dims[1] * sinA, + dims[1] * cosA + dims[0] * sinA]),
                   np.asarray([+ dims[0] * cosA + dims[1] * sinA, - dims[1] * cosA + dims[0] * sinA]),
                   np.asarray([- dims[0] * cosA + dims[1] * sinA, - dims[1] * cosA - dims[0] * sinA]),
                   np.asarray([- dims[0] * cosA - dims[1] * sinA, + dims[1] * cosA - dims[0] * sinA])]
        print(corners)
        print(self.gene.corners())
        self.assertTrue( (np.asarray(corners) == np.asarray(self.gene.corners())).all() )

if __name__ == '__main__':
    unittest.main()
