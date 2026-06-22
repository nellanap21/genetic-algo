import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np


class TestGA(unittest.TestCase):

    def testGA(self):
        pop = poplib.Population(pop_size=10, gene_count=3)
        sim = simlib.ThreadedSim(pool_size=8)

        for generation in range(10):
            sim.eval_population(pop, 2400)
            # iterate all creatures in population, get distance and save in array
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            fitmap = poplib.Population.get_fitness_map(fits)

            print(generation, np.max(fits), np.mean(fits))
            # make new generation
            new_gen = []
            for cid in range(len(pop.creatures)):
                p1_ind = poplib.Population.select_parent(fitmap)
                p2_ind = poplib.Population.select_parent(fitmap)
                dna = genlib.Genome.crossover(pop.creatures[p1_ind].dna,
                                            pop.creatures[p2_ind].dna)
                dna = genlib.Genome.point_mutate(dna, 0.1, 0.25)
                dna = genlib.Genome.grow_mutate(dna, 0.25)
                dna = genlib.Genome.shrink_mutate(dna, 0.25)
                cr = crlib.Creature(1)
                cr.set_dna(dna)
                new_gen.append(cr)
            pop.creatures = new_gen







if __name__ == "__main__":
    unittest.main()
