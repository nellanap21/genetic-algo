from xml.dom.minidom import getDOMImplementation
import genome
from enum import Enum
import numpy as np

BODY_LENGTH = 1.5

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor():
    # self gives access to its own state
    def __init__(self, control_waveform, control_amp, control_freq, phase_offset=0):
        """
        Note: Not testing waveform, control_amp, control_freq for this experiment
        Leaving parameters for future experiments
        """
        self.motor_type = MotorType.SINE
        self.phase = 0
        self.phase_offset = phase_offset

    def get_output(self):
        # every time get_output is called, the phase of waveform changes
        self.phase = self.phase + .03

        output = np.sin(self.phase + self.phase_offset)
        return output

class Creature:
    def __init__(self, gene_count):
        """
        Purpose: Create a new creature by
        1. generating random genome
        2. creating links for body structure
        3. setting variables to track fitness
        """
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)

        # when the creature first is created, hard code the base leg values
        length_ind = self.spec["link_length"]["ind"]
        radius_ind = self.spec["link_radius"]["ind"]
        self.dna[:, length_ind] = .5
        self.dna[:, radius_ind] = .15

        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def set_dna(self, dna):
        """
        Purpose: Replace a creature's DNA with the one provided
        Inputs: new DNA
        Outputs: updated creature with reset distance
        """
        self.dna = dna
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def get_flat_links(self):
        """
        Purpose: Converts a creature's DNA into a list of links
        """
        if self.flat_links == None:
            gdicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        """
        Purpose: expands number of links by applying recurrence value
        """
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
        """
        Purpose: convert expanded links into URDF XML for pybullet
        """
        # make sure expanded links are available
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")

        # add for every link, add a <link> element
        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_element(adom))

        # for every link other than first, add a <joint> to existing link
        first = True
        for link in self.exp_links:
            if first: # skip the root node!
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))

        robot_tag.setAttribute("name", "climber") 
        return robot_tag.toprettyxml()

    def get_motors(self):
        """
        Create and return motors that control each joint
        Gives legs a sinusoidal movement using phase_offset
        """
        assert(self.exp_links != None), "creature: call get_exp_links before get_motors"

        # if no motors, make them
        if self.motors == None: 
            motors = []
            for i in range(1, len(self.exp_links)):
                l = self.exp_links[i]

                # map phase offset the location of <link> on the body
                phase_offset = l.joint_origin_xyz_3 * 2 * np.pi
                m = Motor(l.control_waveform, l.control_amp, l.control_freq, phase_offset)
                motors.append(m)
            self.motors = motors

        # if motors exists already, just return them
        return self.motors

    def update_position(self, pos):
        """
        Purpose: save creatures start and last position
        Also calculate creature's distance from mountain peak
        """
        # hard coded mountain peak value - update based on landscape
        mountain_peak = np.array([0.0, 0.0, 4.0])
        p = np.array(pos)
        self.dist = np.linalg.norm(p - mountain_peak)

        # updates the start_position and last_position variables
        if self.start_position == None:
            self.start_position = pos
        self.last_position = pos

    def get_distance_to_peak(self):
        """
        Purpose: getter function that returns creature's distance to peak
        """
        return self.dist
    
    def get_hdist_to_peak(self):
        """
        Purpose: compute creature's horizontal (x,y) distance to peak
        """
        if self.start_position == None or self.last_position == None:
            return 0
        p1 = np.array(self.last_position[:2]) # just x and y coords
        p2 = np.array([0,0])

        return np.linalg.norm(p1-p2)

    def get_vdist_to_peak(self):
        """
        Purpose: compute creature's vertical (z) distance to peak
        """
        if self.start_position == None or self.last_position == None:
            return 0
        
        # just z coord
        p1 = np.array(self.last_position[2]) 
        # hard coded mountain peak value - update based on environment
        p2 = np.array([4])

        return abs(p2 - p1)

    def get_distance_travelled(self):
        """
        Purpose: compute net distance travelled from start to last
        """
        if self.start_position == None or self.last_position == None:
            return 0
        
        p1 = np.array(self.start_position)
        p2 = np.array(self.last_position)
        
        return np.linalg.norm(p1-p2)


