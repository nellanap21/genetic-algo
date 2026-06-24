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
        exp_links = c.get_expanded_links() 
        self.assertGreaterEqual(len(exp_links), len(links))    

    def testToXMLNotNone(self):
        c = creature.Creature(gene_count=2)      
        xml_str = c.to_xml()
        self.assertIsNotNone(xml_str)    

    def testLoadXML(self):
        c = creature.Creature(gene_count=20)
        xml_str = c.to_xml()

        with open('temp/test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('temp/test.urdf')
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
        with open('temp/test_radial.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" + xml_str)

    def testMotor(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

    def testMotorValPulse(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        # this has value of 0.1 coming into control_waveform
        # that means it should be a PULSE wave
        # self.phase is 0, so output should be 1
        self.assertEqual(m.get_output(), 1)

    def testMotorValSine(self):
        m = creature.Motor(0.6, 0.5, 0.5)
        m.get_output()
        m.get_output()

        self.assertGreater(m.get_output(), 0)


    def testCMotor(self):
        c = creature.Creature(gene_count = 4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls) - 1, len(ms))

unittest.main()