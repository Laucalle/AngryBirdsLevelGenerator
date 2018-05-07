import unittest
from AngryBirdsGA.BlockGene import BlockGene

class TestBlockGene(unittest.TestCase):

    def setUp(self):
        self.gene = BlockGene( type=1, pos=[0,0], r=1)

    def test_should_initialize_gene_OK(self):
        self.assertIsInstance(self.gene, BlockGene, "Object created")

    def test_corners_cache(self):
        corners1 = self.gene.corners()
        corners2 = self.gene.corners()
        self.assertIs(corners1, corners2)
            
if __name__ == '__main__':
    unittest.main()
