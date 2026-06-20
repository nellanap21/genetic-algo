import unittest
import genome
import numpy as np

class GenomeTest (unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertEqual(len(gene), 10)

    def testRandGeneIsNumpyArrays(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(20, 3)
        # print(data)
        self.assertIsNotNone(data)

    def testGeneSpecExist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link_length'])

    def testGeneSpecHasLinkLengthIndex(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link_length']["ind"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        #print(spec["link_length"])
        #print(spec["link_length"]["ind"])
        #print(gene[spec["link_length"]["ind"]])
        self.assertGreater(gene[spec["link_length"]["ind"]], 0)

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        #print(gene_dict)
        self.assertIn("link_recurrence", gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        print(genome_dicts)
        self.assertEqual(len(genome_dicts), 3)

unittest.main()