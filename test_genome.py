import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation


class GenomeTest (unittest.TestCase):
    def testClassExists(self):
        # digging into the Genome class of genome module
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
        # print(genome_dicts)
        self.assertEqual(len(genome_dicts), 3)

    def testFlatLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        self.assertIsNotNone(links)



    def testExpandLinks1(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2)          
        ]
        exp_links = [links[0]]
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links)
        self.assertEqual(len(exp_links), 3)

    def testExpandLinks2(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        exp_links = [links[0]]
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links) 
        names = [l.name+"-parent-is-"+l.parent_name for l in exp_links]
        # print(names)
        self.assertEqual(len(exp_links), 6)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)        
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links), 3)

    def testGetLinksUniqueNames(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)        
        links = genome.Genome.genome_to_links(genome_dicts)
        # check that each link's name only appears once
        for l in links:
            names = [link.name for link in links if link.name == l.name] 
            self.assertEqual(len(names), 1)       

    def testLinkToXML(self):
        link = genome.URDFLink(name="A", parent_name="None", recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_link_element(adom)
        # print(xml_str)
        self.assertIsNotNone(xml_str)

unittest.main()