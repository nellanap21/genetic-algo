import creature
import numpy as np

class Population():
    def __init__(self, pop_size, gene_count):
        """
        Purpose: create a population of creatures 
        Input: 
            pop_size: the total size of the population
            gene_count: the number genes each creature will have
        """
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

    @staticmethod
    def select_parent_tournament(fitness_scores, tournament_size=3):
        """
        Selects one parent using tournament selection.

        Parameters:
            fitness_scores (list or np.ndarray):
                Fitness score for each creature. Higher is better.

            tournament_size (int):
                Number of random creatures competing in the tournament.

        Returns:
            int:
                Index of the winning parent.
        """
        # select tournament competitors
        competitors = np.random.choice(
            len(fitness_scores),
            size=tournament_size,
            replace=False
        )

        # choose the best from the competitors
        best_index = competitors[np.argmax([fitness_scores[i] for i in competitors])]

        return best_index