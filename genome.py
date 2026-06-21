import numpy as np
import copy

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
            "link_length": {"scale":1},
            "link_radius": {"scale":1},
            "link_recurrence": {"scale":4},
            "link_mass": {"scale":1},
            "joint_type": {"scale":1},
            "joint_parent": {"scale":1},
            "joint_axis_xyz": {"scale":1},
            "joint_origin_rpy_1": {"scale": np.pi * 2}, 
            "joint_origin_rpy_2": {"scale": np.pi * 2}, 
            "joint_origin_rpy_3":{"scale": np.pi * 2}, 
            "joint_origin_xyz_1": {"scale": 1},
            "joint_origin_xyz_2": {"scale": 1},
            "joint_origin_xyz_3":{"scale": 1},
            "control_waveform": {"scale": 1},
            "control_amp": {"scale": 0.25},
            "control_freq":{"scale": 1}
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
        # tracks which child number we're creating
        sibling_ind = 1
        for c in children:
            for r in range(int(c.recur)):
                sibling_ind = sibling_ind + 1
                # create shallow copy of the child
                c_copy = copy.copy(c)  
                # attach to unique parent
                c_copy.parent_name = uniq_parent_name
                # give child unique name
                uniq_name = c_copy.name + str(len(exp_links))
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
        link_ind = 0
        parent_names = [str(link_ind)]
        links = []
        for gdict in gdicts:
            link_ind = link_ind + 1
            link_name = str(link_ind)
            parent_ind = gdict["joint_parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link_recurrence"]
            link = URDFLink(name=link_name, 
                            parent_name=parent_name, 
                            recur=recur+1,
                            link_length=gdict["link_length"],
                            link_radius=gdict["link_radius"],
                            link_mass=gdict["link_mass"],
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
            parent_names.append(link_name)
        return links
    

class URDFLink:
    # OOP - creating wrapper which contains all the data i need to represent a link
    # constructor which takes as its argument
    # itself the instance of the object plus
    # name, parent_name, recurrence level - assigns those
    def __init__(self, name, parent_name, recur, 
                 link_length=0.1,
                 link_radius=0.1,
                 link_mass=0.1,
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

