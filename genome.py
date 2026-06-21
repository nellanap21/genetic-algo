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
            gene_dict[key] = gene[spec[key]["ind"]]

        return gene_dict
    
    @staticmethod
    def get_genome_dicts(dna, spec):
        genome_dicts = []
        for gene in dna:
            genome_dicts.append(Genome.get_gene_dict(gene, spec))
        return genome_dicts # returns array of dicts
    
    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        # flat links contains all link types (ABCD)
        # filter for those with the parent == parent_link.name
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        for c in children:
            for r in range(c.recur):
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                exp_links.append(c_copy)
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)
    
class URDFLink:
    # OOP - creating wrapper which contains all the data i need to represent a link
    # constructor which takes as its argument
    # itself the instance of the object plus
    # name, parent_name, recurrence level - assigns those
    def __init__(self, name, parent_name, recur):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur