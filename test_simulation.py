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
        self.assertTrue(os.path.exists('temp.urdf'))

    def testPos(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        self.assertNotEqual(cr.start_position, cr.last_position)

    def testDist(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        dist = cr.get_distance_travelled()
        self.assertGreater(dist, 0)        

    def testPop(self):
        # create population
        pop = population.Population(pop_size=10, gene_count=3)
        # create simulation
        sim = simulation.Simulation()
        # iterate over creatures and run in simulation
        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)


unittest.main()        