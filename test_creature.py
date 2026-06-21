import unittest
import creature 
import pybullet as p

class TestCreature(unittest.TestCase):
    def testCreatExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testExpLinks(self):
        for i in range(20):
            c = creature.Creature(gene_count=25)
            links = c.get_flat_links()
            exp_links = c.get_expanded_links()
            # print(len(exp_links))
            self.assertGreaterEqual(len(exp_links), len(links))    

    def testToXMLNotNone(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        print(xml_str)
        self.assertIsNotNone(xml_str)    


unittest.main()