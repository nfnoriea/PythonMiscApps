import pandas as pd
from lib import agent as ag
from lib import location as loc
from lib import dna as pdna
from lib import animal as animal
import os.path


def create_protocol(path):
    if not os.path.exists(path):
        return None

    info = pd.read_csv(path + 'Info.csv')

    # Process Info Data
    # Create DURC Indicators
    durc = {'enhance harm':
            (info['Enhances Harmful Conseq Ind'] == 'Y').bool(),
            'disrupt immunity':
            (info['Disrupts Immunity Ind'] == 'Y').bool(),
            'confer resistance':
            (info['Confers Resist Ind'] == 'Y').bool(),
            'increase dissemination':
            (info['Increases Dissemination Ind'] == 'Y').bool(),
            'alter tropism': (info['Alters Tropism Ind'] == 'Y').bool(),
            'enhance susceptibility':
            (info['Enhances Susceptibility Ind'] == 'Y').bool(),
            'reconstitute extinct':
            (info['Reconstitutes Extinct Agent Ind'] == 'Y').bool()}
    # Create Agent Indicators

    risks = {'micro': (info['Microorganisms Ind'] == 'Y').bool(),
             'vv': (info['Viral Vectors Ind'] == 'Y').bool(),
             'tfc': (info['Transfected Cells Ind'] == 'Y').bool(),
             'vtc': (info['Virally Transduced Cells Ind'] == 'Y').bool(),
             'tat': (info['Transactive Peptides Ind'] == 'Y').bool(),
             'infp': (info['Infectious Proteins Ind'] == 'Y').bool(),
             'tox': (info['Biological Toxins Ind'] == 'Y').bool(),
             'cbto': (info['Cells Blood Tissues Organs Ind'] == 'Y').bool(),
             'plants': (info['Plants Ind'] == 'Y').bool(),
             'dna': (info['Recom Synthetic Dna Based Ind'] == 'Y').bool(),
             'other': (info['Oth Risk Assesment Risk Ind'] == 'Y').bool()}
    # Create Special Risk Indicators
    special_risks = {
        'Human Use': (info['Administered Humans Ind'] == 'Y').bool(),
        'Animal Use': (info['Administered V Animals Ind'] == 'Y').bool(),
        'N/A Use': (info['Administered N/A Ind'] == 'Y').bool(),
        'Large Scale': (info['Large Scale Research Ind'] == 'Y').bool(),
        'Environmental Release':
        (info['Experiments Release Env Ind'] == 'Y').bool(),
        'Genome Editing':
        (info['Genome Editing Technology Ind'] == 'Y').bool()}

    pid = info.iloc[0]['Protocol ID']
    pname = info.iloc[0]['Protocol Name']
    investigator = info.iloc[0]['PI Full Name']

    agents = ag.create_agents(path)
    rooms, cabinets = loc.create_locations(path)
    genes = pdna.create_genes(path)
    animals = animal.create_animals(path)

    return Protocol(pid, pname, investigator, risks, special_risks,
                    durc, agents, genes, rooms, cabinets, animals)


class Protocol(object):
    def __init__(self, protocol_id="", name="", pi="",
                 risks="", special_risks="", durc="", agent_list="",
                 genes="", rooms="", cabinets="", animals=""):
        self.protocol_id = protocol_id
        self.name = name
        self.pi = pi
        self.risks = risks
        self.special_risks = special_risks
        self.durc = durc
        self.agent_list = agent_list
        self.genes = genes
        self.rooms = rooms
        self.cabinets = cabinets
        self.animals = animals

    def get_agentlist(self):
        return self.agent_list

    def get_genes(self):
        return self.genes

    def get_cabinets(self):
        return self.cabinets

    def get_rooms(self):
        return self.rooms

    def get_animals(self):
        return self.animals

    def print_durc(self, all=True):
        print("Dual Use Research of Concern")
        print("----------------------------")
        if all:
            for k, v in self.durc.items():
                print('[', ('X' if v else ' '), ']  ',
                      format(k))
        else:
            for k, v in self.durc.items():
                if(v):
                    print(format(k))

    def get_info(self):
        print(self.protocol_id + self.name + self.pi+'\n')
        for k, v in self.durc.items():
            print(format(k) + "\t\t" + format(v))
        for k, v in self.risks.items():
            print(format(k) + "\t" + format(v))
        for k, v in self.special_risks.items():
            print(format(k) + "\t" + format(v))

    def print_all(self):
        print("\n****\nALL AGENTS\n****\n\nAgents")
        for v in self.agent_list.values():
            for a in v:
                a.get_info()
        print("\n\nDNA")
        for g in self.genes:
            g.get_info()
        print("\n\nRoom Locations")
        for r in self.rooms:
            r.get_info()
        print("\n\nBiosafet Cabinets")
        for b in self.cabinets:
            b.get_info()
        print("\n\nAnimal Administration")
        for a in self.animals:
            a.get_info()

    def print_agent_nums(self):
        total = 0
        nums = []
        for k, v in self.agent_list.items():
            t = len(v)
            total += t
            nums.append(t)
        print("Microbes: ", nums[0])
        print("Viral Vectors: ", nums[1])
        print("Virally Transduced Cells: ", nums[2])
        print("Transfected Cells: ", nums[3])
        print("Biological Toxins: ", nums[4])
        print("Infectious Proteins: ", nums[5])
        print("Transactive Peptides: ", nums[6])
        print("Plasmids: ", nums[7])
        print("Cultured Cells: ", nums[8])
        print("Human Material: ", nums[9])
        print("NHP Material: ", nums[10])
        print("Outside Material: ", nums[11])
        print("Other Agents: ", nums[12])
        print("-------------")
        print("Total: ", total)

    def print_agents(self, atype):
        if(atype == "" or atype is None):
            print("Agent Abbreviations:")
            print("[ Microbe, VV, VTC, FTC, Toxin, IP, DNA, CC, HM, NHPM, OM, Other]")
        else:
            for x in self.agent_list[atype]:
                x.get_info()
                print()
