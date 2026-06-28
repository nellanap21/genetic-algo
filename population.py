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
    def select_parent_tournament(fitness_scores, tournament_size=3):
        """
        Purpose: selects one parent using tournament selection
        Input:
            fitness_scores: fitness score for each creature
            tournament_size: number of random creatures in contest
        Output: index of winner
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