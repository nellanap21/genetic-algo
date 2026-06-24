import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation
import os

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
            # print(l.name) # correctly naming links at this point: 0, 1, 2
            self.assertEqual(len(names), 1)       

    def testLinkToXML(self):
        link = genome.URDFLink(name="A", parent_name="None", recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_link_element(adom)
        # print(xml_str)
        self.assertIsNotNone(xml_str)

    # test crossover
    def testXO(self):
        g1 = np.array([[1,2,3], [4,5,6], [7,8,9]])
        g2 = np.array([[10,11,12], [13,14,15], [16,17,18]])
        g3 = genome.Genome.crossover(g1, g2)
        self.assertEqual(len(g3), len(g1))

    # test point mutation
    def test_point(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        # print(g1)
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        # print(g2)
        self.assertFalse(np.array_equal(g1, g2))

    # ensure values have not gone out of range 0-1
    def test_point_range(self):
        g1 = np.array([[1.0], [0.0], [1.0], [0.0]])
        for i in range(100):
            g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
            self.assertLess(np.max(g2), 1.0)
            self.assertGreaterEqual(np.min(g2), 0.0)

    def test_shrink0(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1)
        #print(g1, g2)
        self.assertNotEqual(len(g1), len(g2))

    def test_shrink1(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should def. shrink as rate = 1
        self.assertEqual(len(g2), 1)

    def test_shrink2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=0.0)
        # should not shrink as rate = 0
        self.assertEqual(len(g2), 2)

    def test_shrink3(self):
        g1 = np.array([[1.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should not shrink if already len 1
        self.assertEqual(len(g2), 1)


    def test_grow0(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        # print(g1, g2)
        self.assertGreater(len(g2), len(g1))

    def test_grow1(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def test_grow2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=0)
        self.assertEqual(len(g2), len(g1))



    def test_tocsv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'temp/test.csv')
        self.assertTrue(os.path.exists('temp/test.csv'))

    def test_tocsv_content(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'temp/test.csv')
        expect = "1,2,3,\n"
        with open('temp/test.csv') as f:
            csv_str = f.read()
        self.assertEqual(csv_str, expect);

    def test_tocsv_content2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'temp/test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open('temp/test.csv') as f:
            csv_str = f.read()
        self.assertEqual(csv_str, expect);

    def test_from_csv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'temp/test.csv')    
        g2 = genome.Genome.from_csv('temp/test.csv')
        # print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))

    def test_from_csv2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'temp/test.csv')    
        g2 = genome.Genome.from_csv('temp/test.csv')
        # print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))









unittest.main()