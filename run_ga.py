import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np



def run_ga():
    pop = poplib.Population(pop_size=10, gene_count=3)
    sim = simlib.ThreadedSim(pool_size=8)
    generations = 100

    for generation in range(generations):
        sim.eval_population(pop, 2400)
        # iterate all creatures in population, get distance and save in array
        if generation < generations / 2:
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            fitness_scores = fits
            print(
                generation, 
                "stage: walking",
                "fittest: ", np.round(np.max(fits), 3), 
                "mean:", np.round(np.mean(fits), 3), 
            )
        else:
            fits = [cr.get_distance_to_peak() for cr in pop.creatures]
            fitness_scores = [1.0 / (1.0 + f) for f in fits]
            print(
                generation, 
                "stage: climbing",
                "fittest: ", np.round(np.min(fits), 3), 
                "mean:", np.round(np.mean(fits), 3), 
            )

        fitmap = poplib.Population.get_fitness_map(fitness_scores)


        # ELITISM
        best_ind = np.argmax(fitness_scores)
        elite = crlib.Creature(1)
        elite.set_dna(np.copy(pop.creatures[best_ind].dna))

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
        
        # NOTE: replace the lowest with the elite
        new_gen[0] = elite # you are being replaced with elite
        if generation % 10 == 0:
            csv_filename = f"elites/elite{generation}.csv"
            genlib.Genome.to_csv(elite.dna, csv_filename)
        pop.creatures = new_gen

if __name__ == "__main__":
    run_ga()
