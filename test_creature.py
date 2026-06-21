import unittest
import creature 
import pybullet as p
import genome

class TestCreature(unittest.TestCase):
    def testCreatExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testExpLinks(self):
        c = creature.Creature(gene_count=3)
        links = c.get_flat_links()
        # for l in links:
        #     print(l.name)
        # print("=====")
        exp_links = c.get_expanded_links() # something is wrong in this function to give wrong names
        # for e in exp_links:
        #     print(e.name)
        # print(len(exp_links))
        self.assertGreaterEqual(len(exp_links), len(links))    

    def testToXMLNotNone(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        # print(xml_str)
        self.assertIsNotNone(xml_str)    

    def testLoadXML(self):
        c = creature.Creature(gene_count=20)
        xml_str = c.to_xml()
        with open('test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)

    def testRadial(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2, joint_origin_rpy_1=0.75, link_length=1.0)
        ]
        c = creature.Creature(gene_count=2)
        c.flat_links = links
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('test_radial.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" + xml_str)

unittest.main()