import numpy as np
import copy

BODY_LENGTH = 3
BODY_RADIUS = 0.2
LEG_LENGTH = BODY_LENGTH / 4
LEG_RADIUS = BODY_RADIUS / 4

class Genome():
    def __init__(self):
        pass

    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = np.array([Genome.get_random_gene(gene_length) for i in range(gene_count)])
        return genome # returns an array of genes
    
    @staticmethod
    def get_gene_spec():
        # allows you to pull value out of a gene by name
        gene_spec = {
            "link_shape": {"scale":1},
            "link_length": {"scale":0.75},
            "link_radius": {"scale":0.15},
            "link_recurrence": {"scale":1},
            "link_mass": {"scale":1},
            "joint_type": {"scale":1},
            "joint_parent": {"scale":1},
            "joint_axis_xyz": {"scale":1},
            "joint_origin_rpy_1": {"scale": np.pi}, 
            "joint_origin_rpy_2": {"scale": np.pi}, 
            "joint_origin_rpy_3":{"scale": np.pi}, 
            "joint_origin_xyz_1": {"scale": 1},
            "joint_origin_xyz_2": {"scale": 1},
            "joint_origin_xyz_3":{"scale": 1},
            "control_waveform": {"scale": 1},
            "control_amp": {"scale": 2.0},
            "control_freq":{"scale": 0.4}
        }

        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1

        return gene_spec
    
    @staticmethod
    def get_gene_dict(gene, spec):
        gene_dict = {}
        for key in spec.keys():
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gene_dict[key] = gene[ind] * scale

        return gene_dict
    
    @staticmethod
    def get_genome_dicts(genome, spec):
        genome_dicts = []
        for gene in genome:
            genome_dicts.append(Genome.get_gene_dict(gene, spec))
        return genome_dicts # returns array of dicts
    



    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        # flat links contains all link types (ABCD)
        # find every link whose parent is the current link
        children = [l for l in flat_links if l.parent_name == parent_link.name]

        # tracks sibling index for naming sibling links
        sibling_ind = 1 

        for c in children:
            for r in range(2):
                sibling_ind = sibling_ind + 1
                # create shallow copy of the child
                c_copy = copy.copy(c)  
                # attach to unique parent
                c_copy.parent_name = uniq_parent_name # should always be 0
                # give child unique name
                uniq_name = c_copy.name + str(len(exp_links))
                # print("exp: ", c.name, " -> " , uniq_name)
                c_copy.name = uniq_name
                # store sibling index
                c_copy.sibling_ind = sibling_ind
                # add to expanded list
                exp_links.append(c_copy)
                # recursively expand descendants
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)
    
    @staticmethod
    def genome_to_links(gdicts):
        # turns genome (array of dicts) int
        # array of links
        links = []        
        link_ind = int(0)
        parent_names = [str(link_ind)] # start with just number 0
        links_by_name = {}
        for gdict in gdicts:
            link_name = str(link_ind)

            # links can connect any previous link
            # parent_ind = gdict["joint_parent"] * len(parent_names)
            # parent_ind = min(parent_ind, len(parent_names) - 1) # to ensure parent_ind is not out or ange
            # parent_name = parent_names[int(parent_ind)]

            # links can only connect to first link
            if link_ind == 0:
                parent_name = "None"
            else:
                parent_name = "0"

            # set the parent link length
            if not links_by_name:
                parent_length = 0.0
            else:
                parent_length = links_by_name[parent_name].link_length

            # first link (the body) has set dimensions
            if link_ind == 0:
                link_length = BODY_LENGTH
                link_radius = BODY_RADIUS
            else:   # Fixed leg length
                link_length = LEG_LENGTH #gdict["link_length"]
                link_radius = LEG_RADIUS #gdict["link_radius"]

            recur = gdict["link_recurrence"]
            link = URDFLink(name=link_name, 
                            parent_name=parent_name, 
                            recur=recur+1,
                            link_length=link_length,
                            link_radius=link_radius,
                            link_mass=gdict["link_mass"],
                            parent_length=parent_length,
                            joint_type=gdict["joint_type"],
                            joint_parent=gdict["joint_parent"],
                            joint_axis_xyz=gdict["joint_axis_xyz"],
                            joint_origin_rpy_1=gdict["joint_origin_rpy_1"],
                            joint_origin_rpy_2=gdict["joint_origin_rpy_2"],
                            joint_origin_rpy_3=gdict["joint_origin_rpy_3"],
                            joint_origin_xyz_1=gdict["joint_origin_xyz_1"],
                            joint_origin_xyz_2=gdict["joint_origin_xyz_2"],
                            joint_origin_xyz_3=gdict["joint_origin_xyz_3"],
                            control_waveform=gdict["control_waveform"],
                            control_amp=gdict["control_amp"],
                            control_freq=gdict["control_freq"])
            links.append(link)
            links_by_name[link_name] = link
            if link_ind != 0: # don't re-add the first link
                parent_names.append(link_name)
            link_ind = int(link_ind) + 1

        # now fix the first link so it links to nothing
        links[0].parent_name = "None"

        return links
    
    @staticmethod
    def crossover(g1, g2):
        """
        g1 and g2 are raw dna data - list of lists of floats
        """
        xo = np.random.randint(len(g1))
        if xo == 0:
            return g2
        if xo == len(g1) - 1:
            return g1
        if xo > len(g2):
            xo = len(g2) - 1
        g3 = np.concatenate((g1[0:xo], g2[xo:]))
        return g3

    @staticmethod
    def point_mutate(genes, rate, amount):
        """
        Randomly mutates values within genome
        Inputs
        genes:  the genome to mutate
        rate:   probability 0-1 each gene will be mutated
        amount: max magnitude of the mutation. value is adjusted to be 
                random amount between -amount/2 and +amount/2
        Outputs
        copy of genome with random point mutations
        """
        new_genes = copy.copy(genes)
        for gene in new_genes:
            # if rate is high, the more likely to mutate
            if np.random.rand() < rate:
                ind = np.random.randint(len(gene)) # choose one gene

                # these next two lines are from videos
                r = (np.random.rand() - 0.5) * amount
                gene[ind] = gene[ind] + r
                gene[ind] = np.clip(gene[ind], 0, 1)
                # take the current value, multiply by random 0-1, multiply by amount
                # gene[ind] = gene[ind] * np.random.rand() * amount
        return new_genes

    @staticmethod
    def shrink_mutate(genes, rate):
        if len(genes) == 1:
            return genes
        if np.random.rand() < rate:
            # NOTE: adjust so that it cna remove first gene?
            ind = np.random.randint(len(genes))
            genes = np.delete(genes, ind, 0)
        return genes

    @staticmethod
    def grow_mutate(genes, rate):
        if np.random.rand() < rate:
            gene = Genome.get_random_gene(len(genes[0]))
            genes = np.append(genes, [gene], axis=0)
        return genes

    @staticmethod
    def to_csv(dna, csv_file):
        csv_str = ""
        for gene in dna:
            for val in gene:
                csv_str = csv_str + str(val) + ","
            csv_str = csv_str + '\n'

        with open(csv_file, 'w') as f:
            f.write(csv_str)

    @staticmethod
    def from_csv(filename):
        csv_str = ''
        # read whole file into string
        with open(filename) as f:
            csv_str = f.read()

        dna = []
        lines = csv_str.split('\n') # split into lines
        for line in lines:
            vals = line.split(',') # split into values
            gene = [float(v) for v in vals if v!= '']
            if len(gene) > 0:
                dna.append(gene)
        return dna







class URDFLink:
    def __init__(self, name, parent_name, recur, 
                 link_length=0.1,
                 link_radius=0.1,
                 link_mass=0.1,
                 parent_length=0.5,
                 joint_type=0.1,
                 joint_parent=0.1,
                 joint_axis_xyz=0.1,
                 joint_origin_rpy_1=0.1,
                 joint_origin_rpy_2=0.1,
                 joint_origin_rpy_3=0.1,                                  
                 joint_origin_xyz_1=0.1,
                 joint_origin_xyz_2=0.1,
                 joint_origin_xyz_3=0.1,
                 control_waveform=0.1,
                 control_amp=0.1,
                 control_freq=0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.parent_length = parent_length
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3       
        self.joint_origin_xyz_1 = joint_origin_xyz_1         
        self.joint_origin_xyz_2 = joint_origin_xyz_2         
        self.joint_origin_xyz_3 = joint_origin_xyz_3         
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq

        self.sibling_ind = 1

    def to_link_element(self, adom):
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)
        
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))
        orig_tag = adom.createElement("origin")
        orig_tag.setAttribute("xyz", f"0 0 {self.link_length / 2}") # set origin to one end of the link

        coll_tag = adom.createElement("collision")
        c_geom_tag = adom.createElement("geometry")
        c_cyl_tag = adom.createElement("cylinder")
        c_orig_tag = adom.createElement("origin")
        c_cyl_tag.setAttribute("length", str(self.link_length))
        c_cyl_tag.setAttribute("radius", str(self.link_radius))
        c_orig_tag.setAttribute("xyz", f"0 0 {self.link_length / 2}")
        
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")

        # pi r^2 * height
        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        r = self.link_radius
        h = self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx", f"{(1/12) * mass * (3*r*r + h*h)}")
        inertia_tag.setAttribute("iyy", f"{(1/12) * mass * (3*r*r + h*h)}")
        inertia_tag.setAttribute("izz", f"{0.5 * mass * r * r}")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyz", "0")
        inertia_orig_tag = adom.createElement("origin")
        inertia_orig_tag.setAttribute("xyz", f"0 0 {self.link_length / 2}")
        inertia_orig_tag.setAttribute("rpy", "0 0 0")

        # set hierarchy
        link_tag.appendChild(vis_tag)
        vis_tag.appendChild(geom_tag)
        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(orig_tag)

        link_tag.appendChild(coll_tag)
        coll_tag.appendChild(c_geom_tag)
        c_geom_tag.appendChild(c_cyl_tag)
        coll_tag.appendChild(c_orig_tag)

        link_tag.appendChild(inertial_tag)
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)
        inertial_tag.appendChild(inertia_orig_tag)
        
        return link_tag

    def to_joint_element(self, adom):
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)
        joint_tag.setAttribute("type", "revolute")
        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link", self.name)

        # controls axis of rotation x, y, or z
        axis_tag = adom.createElement("axis")
        axis_tag.setAttribute("xyz", "1 0 0")
        
        # controls how much joint bends
        limit_tag = adom.createElement("limit")
        limit_tag.setAttribute("upper", "1.2")
        limit_tag.setAttribute("lower", "-1.2")

        # transform from the parent link to the child link 
        # joint is located at the origin of the child link
        orig_tag = adom.createElement("origin")

        # Position of the leg along the body
        z_pos = self.parent_length * self.joint_origin_xyz_3
        body_quarter = self.parent_length / 4

        # Left/right side of body
        #side = 1 if self.sibling_ind % 2 == 0 else -1

        pitch = 1.5 if self.sibling_ind % 2 == 0 else -1.5
        j_origin_x = BODY_RADIUS if self.sibling_ind % 2 == 0 else -BODY_RADIUS

        # roll, pitch, yaw of joint
        #if z_pos < body_quarter or z_pos > body_quarter * 3:
        if z_pos < body_quarter * 2:
            orig_tag.setAttribute("rpy", f"{abs(pitch)} 0 0")
        else:
            orig_tag.setAttribute("rpy", f"0 {pitch} 0")

        # NOTE: fix so joint is at the end of parent joint
        orig_tag.setAttribute("xyz", f"{j_origin_x} 0 {self.parent_length * self.joint_origin_xyz_3}")

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(orig_tag)
        return joint_tag

