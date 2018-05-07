import unittest
from AngryBirdsGA import BlockGene

class TestBlockGene(unittest.TestCase):

    def setUp(self):
        self.gene = BlockGene( 1, [0,0], 45)

    def test_should_initialize_gene_OK(self):
        self.assertIsInstance(self.gene,BlockGene, "Object created");


            
if __name__ == '__main__':
    unittest.main()
