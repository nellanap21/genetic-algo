import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import fitness as fitlib
import numpy as np

# genetic algorithm settings
POPULATION = 20
SIM_LENGTH = 1200
GENERATIONS = 10

# genome settings
GENE_COUNT = 3                  # Number of genes/limbs in creature
POINT_MUTATION_RATE = 0.1       # Percent chance of mutating a gene
POINT_MUTATION_AMOUNT = 0.01
GROW_RATE = 0.01               # discourage evolving extra limbs
SHRINK_RATE = 0.01              # removes accidental extra limbs


logs = ["generation,stage,best_fitness,mean_fitness,max_links,mean_links\n"]




def run_ga():
    pop = poplib.Population(pop_size=POPULATION, gene_count=GENE_COUNT)
    sim = simlib.ThreadedSim(pool_size=6)
    generations = GENERATIONS

    for generation in range(generations):
        # run the simulation
        sim.eval_population(pop, SIM_LENGTH)

        # calculate fitness scores
        fitness_scores = fitlib.Fitness.get_scores(pop)
        print(fitness_scores)
        links = [len(cr.get_expanded_links()) for cr in pop.creatures]
        logs.append(
            f"{generation},"
            f"{np.max(fitness_scores):.3f},"
            f"{np.mean(fitness_scores):.3f},"
            f"{np.max(links)},"
            f"{np.mean(links):.3f}\n"
        )

        fitmap = poplib.Population.get_fitness_map(fitness_scores)


        # ELITISM
        best_ind = np.argmax(fitness_scores)
        elite = crlib.Creature(1)
        elite.set_dna(np.copy(pop.creatures[best_ind].dna))

        # make new generation
        new_gen = []
        for cid in range(len(pop.creatures)):

            # roulette wheel selection
            # p1_ind = poplib.Population.select_parent(fitmap)
            # p2_ind = poplib.Population.select_parent(fitmap)

            # tournament style selection
            p1_ind = poplib.Population.select_parent_tournament(fitness_scores, tournament_size=3)
            p2_ind = poplib.Population.select_parent_tournament(fitness_scores, tournament_size=3)

            dna = genlib.Genome.crossover(pop.creatures[p1_ind].dna,
                                        pop.creatures[p2_ind].dna)
            dna = genlib.Genome.point_mutate(dna, POINT_MUTATION_RATE, POINT_MUTATION_AMOUNT)
            dna = genlib.Genome.grow_mutate(dna, GROW_RATE)
            dna = genlib.Genome.shrink_mutate(dna, SHRINK_RATE)
            cr = crlib.Creature(1)
            cr.set_dna(dna)
            new_gen.append(cr)
        
        # NOTE: replace the lowest with the elite
        new_gen[0] = elite # you are being replaced with elite
        # if generation % (generations / 10) == 0:
            #print(generation)
        csv_filename = f"elites/elite{generation}.csv"
        genlib.Genome.to_csv(elite.dna, csv_filename)
        pop.creatures = new_gen



if __name__ == "__main__":
    run_ga()

    filename = f"logs/gens_{GENERATIONS}_sim_{SIM_LENGTH}_pop_{POPULATION}_gene_{GENE_COUNT}.csv"
    with open(filename, "w") as f:
        f.writelines(logs)