# now that this is threaded, do not run in ipython
# command: python test_simulation.py

import unittest
import simulation
import creature
import os
import population

class TestSim(unittest.TestCase):
    
    def testSimExists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)

    def testSimId(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.physicsClientId)

    def testRun(self):
        sim = simulation.Simulation()
        # cr = creature.Creature(gene_count = 3)
        self.assertIsNotNone(sim.run_creature)

    def testRunXML(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        self.assertTrue(os.path.exists('temp/temp0.urdf'))

    def testPos(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        self.assertNotEqual(cr.start_position, cr.last_position)

    def testDist(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        dist = cr.get_distance_to_peak()
        self.assertGreater(dist, 0)        

    # tests threaded simulation
    def testProc(self):
        pop = population.Population(pop_size=20, gene_count=3)
        tsim = simulation.ThreadedSim(pool_size=4)
        tsim.eval_population(pop, 2400)
        dists = [cr.get_distance_to_peak() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

# multiprocessing uses spawn, so every child process imports your module fresh
# without if statement, every worker process starts the test runner again.
if __name__ == "__main__":
    unittest.main()