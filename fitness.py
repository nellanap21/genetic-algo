

class Fitness():

    @staticmethod
    def get_scores(pop):
        """
        Purpose: calculate fitness score for each creature in population
        Input: population object with all creatures
        Outpu: list of fitness scores
        """
        scores = []

        for cr in pop.creatures:
            # compute horizontal distance to peak
            horizontal_dist = cr.get_hdist_to_peak()

            # compute final height at end of simulation
            final_height = cr.last_position[2]

            # weight the final height more than horizontal height
            score = 5.0 * final_height - 2.0 * horizontal_dist

            scores.append(score)

        return scores
    
