import unittest
import population as poplib
import simulation as simlib

class TestGA(unittest.TestCase):

    def testGA(self):
        pop = poplib.Population(pop_size=10, gene_count=3)
        sim = simlib.ThreadedSim(pool_size=8)
        











unittest.main()