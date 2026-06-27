import pybullet as p
import numpy as np

class Fitness():
    def __init__(self):
        pass

    @staticmethod
    def get_scores(pop):
        scores = []

        for cr in pop.creatures:
            horizontal_dist = cr.get_hdist_to_peak()
            final_height = cr.last_position[2]
            score = 5.0 * final_height - 2.0 * horizontal_dist

            scores.append(score)

        return scores
    
