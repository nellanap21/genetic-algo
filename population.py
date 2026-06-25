import creature
import numpy as np

class Population():
    def __init__(self, pop_size, gene_count):
        self.creatures = [creature.Creature(gene_count=gene_count) for i in range(pop_size)]


    @staticmethod
    def get_fitness_map(fits):
        fitmap = []
        total = 0
        for f in fits:
            total = total + f
            fitmap.append(total)
        return fitmap

    @staticmethod
    def select_parent(fitmap):
        r = np.random.rand() # 0-1
        r = r * fitmap[-1] # scale to range of fitnesses
        for i in range (len(fitmap)): # iterate through fitnesses
            # NOTE: would be better if selected highest fitness?
            if r <= fitmap[i]: # select if fitness is big enough
                return i

