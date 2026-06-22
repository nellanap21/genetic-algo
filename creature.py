from xml.dom.minidom import getDOMImplementation
import genome
from enum import Enum
import numpy as np

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor():
    # self gives access to its own state
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
            self.motor_type = MotorType.SINE

        self.amp = control_amp
        self.freq = control_freq
        self.phase = 0

    def get_output(self):
        # every time get_output is called, the phase of waveform changes
        self.phase = (self.phase + self.freq) % (np.pi * 2)

        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1

        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)
        
        return output

class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
    
    def get_flat_links(self):
        if self.flat_links == None:
            gdicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        self.get_flat_links()
        if self.exp_links is not None:
            return self.exp_links
        
        exp_links = [self.flat_links[0]]
        genome.Genome.expandLinks(self.flat_links[0],
                                  self.flat_links[0].name,
                                  self.flat_links,
                                  exp_links)
        self.exp_links = exp_links
        return self.exp_links
    
    def to_xml(self):
        # NOTE: adding this assertion will break certain tests
        # assert(self.exp_links != None), "creature: call get_exp_links before to_xml"

        # make sure expanded links are available
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_element(adom))
        first = True
        for link in self.exp_links:
            if first: # skip the root node!
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))
        robot_tag.setAttribute("name", "pepe") # choose a name!
        return robot_tag.toprettyxml()


    def get_motors(self):
        assert(self.exp_links != None), "creature: call get_exp_links before get_motors"
        if self.motors == None:
            motors = []
            for i in range(1, len(self.exp_links)):
                l = self.exp_links[i]
                # assume the URDFLink has control_waveform
                # control_amp, and control_freq properties, read from genome
                m = Motor(l.control_waveform, l.control_amp, l.control_freq)
                motors.append(m)
            self.motors = motors
        return self.motors

    def update_position(self, pos):
        if self.start_position == None:
            self.start_position = pos
        else:
            self.last_position = pos

    def get_distance_travelled(self):
        p1 = np.array(self.start_position)
        p2 = np.array(self.last_position)
        return np.linalg.norm(p1-p2)


