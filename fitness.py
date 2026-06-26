import pybullet as p
import numpy as np

class Fitness():
    def __init__(self):
        pass

    @staticmethod
    def get_scores(pop):
        scores = []

        for cr in pop.creatures:
            hdist = cr.get_hdist_to_peak()
            height = cr.last_position[2]
            score = 5.0 * height + 2.0 * (6 - hdist)

            scores.append(score)

        return scores
    
