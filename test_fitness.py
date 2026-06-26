import unittest
import fitness
import population 
import simulation

class TestFitness(unittest.TestCase):

    def testFitnessExists(self):
        fit = fitness.Fitness()
        self.assertIsNotNone(fit)

    def testGetScores(self):
        pop = population.Population(pop_size=10, gene_count=3)
        tsim = simulation.ThreadedSim(pool_size=4)
        tsim.eval_population(pop, 2400)
        scores = fitness.Fitness.get_scores(pop)
        self.assertIsNotNone(scores)

if __name__ == "__main__":
    unittest.main()