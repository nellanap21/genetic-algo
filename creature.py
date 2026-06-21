import genome

class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
    
    def get_flat_links(self):
        gdicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
        self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        self.get_flat_links()
        exp_links = []
        genome.Genome.expandLinks(self.flat_links[0],
                                  self.flat_links[0].name,
                                  self.flat_links,
                                  exp_links)
        self.exp_links = exp_links
        return self.exp_links