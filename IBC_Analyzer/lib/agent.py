import pandas as pd


class Safety_Info(object):
    def __init__(self, ppe="", safety_eq="", spill="", addlpractice="",
                 surface_de="", equip_de="", waste=""):
        self.ppe = ppe
        self.safety_eq = safety_eq,
        self.spill = spill,
        self.addlpractice = addlpractice,
        self.surface_de = surface_de,
        self.equip_de = equip_de
        self.waste = waste

    def get_info(self):
        print("PPE: ", self.ppe)
        print("Safety Equipment: ", self.safety_eq)
        print("Spill Procedure: ", self.spill)
        print("Additional Practices: ", self.addlpractice)
        print("Surface Decon: ", self.surface_de)
        print("Equip Decon: ", self.equip_de)
        print("Waste Disposal: ", self.waste)


def create_safety_data(data):
    ppe = sanitize_data(data['PPE List'])
    seq = sanitize_data(data['Safety Equipment List'])
    spill = sanitize_data(data['Spill Procedure'])
    addprac = sanitize_data(data['Addl Safety Practice Desc'])
    sde = sanitize_data(data['Work Surface Decon'])
    ede = sanitize_data(data['Equipment Decon'])
    waste = sanitize_data(data['Waste Disposal Method'])
    return Safety_Info(ppe, seq, spill, addprac, sde, ede, waste)


"""
Sanitize Raw Data from CSV for Qt Widget text-setting
"""


def sanitize_data(data):
    badchars = ['\'', '"', '\\', '(', ')', '*']
    clean = [char for char in data if char not in badchars]
    clean = ''.join(clean)
    clean = clean.replace('|', ', ')
    return clean


# Superclass Agent
# Contains Member Fields for Agent Name, Agent Type,
# all Safety Descriptions, and Administered to Hum/Animal

class Agent():
    def __init__(self, name, atype, safety, admin):
        self.name = name
        self.atype = atype
        self.safety = safety
        self.admin = admin

    def get_safety_info(self):
        return self.safety.get_info()

    def get_name(self):
        return self.name

    def get_type(self):
        return self.atype

    def is_administered(self):
        return (self.admin == 'Y')

    def is_selectagent(self):
        if hasattr(self, 'sa') and self.sa == 'Y':
            return True
        else:
            return False

    def get_riskgroup(self):
        if hasattr(self, 'rg'):
            if self.rg == 'RG1':
                return 1
            elif self.rg == 'RG2':
                return 2
            elif self.rg == 'RG3':
                return 3
            elif self.rg == 'RG4':
                return 4
            else:
                return None

        else:
            return None

    def print_fancy(self):
        return ('')


# Subclasses of Agent Corresponding to each IBC section

class Microbe(Agent):
    def __init__(self, name, atype, safety, admin,
                 rg="", sa="", abx="", attenuate=""):
        super().__init__(name, atype, safety, admin)
        self.rg = rg
        self.sa = sa
        self.abx = abx
        self.attenuate = attenuate

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("SA? ", self.sa, "\tRG: ", self.rg)
        print("Attenuated? ", self.attenuate)
        print("Abx Profile?", self.abx)
        print("Admin H/A?", self.admin)
        print()

    def print_fancy(self):
        txt = ("<h5>Attenuated</h5>" + self.attenuate +
               "<h5>Antibiotic Profile</h5>" + self.abx)
        return super().print_fancy() + txt


class ViralVector(Agent):
    def __init__(self, name, atype, safety, admin,
                 rg="", sa="", attenuate="", rc=""):
        Agent.__init__(self, name, "Viral Vector", safety, admin)
        self.rg = rg
        self.sa = sa
        self.attenuate = attenuate
        self.rc = rc

    def print_fancy(self):
        txt = ("<h5>Attenuated</h5>" + self.attenuate +
               "<h5>Replication Competant</h5>" + self.rc)
        return super().print_fancy() + txt

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("SA? ", self.sa, "\tRG: ", self.rg)
        print("Attenuated? ", self.attenuate)
        print("Replication Competent? ", self.rc)
        print("Admin H/A?", self.admin)
        print()


# Transfect Cells

class TFC(Agent):
    def __init__(self, name, atype, safety, admin, dna="", dna_func=""):
        Agent.__init__(self, name, "Transfected Cells", safety, admin)
        self.dna = dna
        self.dna_func = dna_func

    def print_fancy(self):
        txt = ("<h5>Source DNA</h5>" + self.dna +
               "<h5>DNA Function</h5>" + self.dna_func)
        return super().print_fancy() + txt

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("DNA: ", self.dna)
        print("DNA Function: ", self.dna_func)
        print("Admin H/A?", self.admin)
        print()


# Virally Transduced Cells

class VTC(Agent):
    def __init__(self, name, atype, safety, admin, dna="", dna_func="",
                 obtained="", test_method="", system="", hazards=""):
        Agent.__init__(self, name, "Virally Transduced Cells", safety, admin)
        self.dna = dna
        self.dna_func = dna_func
        self.obtained = obtained
        self.test_method = test_method
        self.system = system
        self.hazards = hazards

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("DNA: ", self.dna)
        print("Vector System: ", self.system)
        print("DNA Function: ", self.dna_func)
        print("Obtained from Others? ", self.obtained)
        print("Testing Method: ", self.test_method)
        print("Potential Hazards: ", self.hazards)
        print("Admin H/A?", self.admin)
        print()

    def print_fancy(self):
        txt = ("<h5>Source DNA</h5>" + self.dna +
               "<h5>DNA Function</h5>" + self.dna_func +
               "<h5>Obtained From Others?</h5>" + self.obtained +
               "<h5>Testing Method</h5>" + self.test_method +
               "<h5>Vector System</h5>" + self.system +
               "<h5>Other Hazards</h5>" + self.hazards)
        return super().print_fancy() + txt


# Transactive Peptides

class TAT(Agent):
    def __init__(self, name, atype, safety, admin, hazards=""):
        Agent.__init__(self, name, "Transactive Peptides", safety, admin)
        self.hazards = hazards

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("Potential Hazards: ", self.hazards)
        print("Admin H/A?", self.admin)
        print()

    def print_fancy(self):
        txt = ("<h5>Potential Hazards</h5>" + self.hazards)
        return super().print_fancy() + txt


# Infection Proteins

class InfProt(Agent):
    def __init__(self, name, atype, safety, admin):
        Agent.__init__(self, name, atype, safety, admin)

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("Admin H/A?", self.admin)
        print()


# Biological Toxins

class Toxin(Agent):
    def __init__(self, name, atype, safety, admin, sa="", stored_lab=""):
        Agent.__init__(self, name, "Biological Toxin", safety, admin)
        self.sa = sa
        self.stored_lab = stored_lab

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("SA? ", self.sa, "\tStorage in Lab: ", self.stored_lab)
        print("Admin H/A?", self.admin)
        print()

# Plasmid DNA


class DNA(Agent):
    def __init__(self, name, atype, safety, admin, promoter="", drug_res="",
                 hosts="", cell_types="", transfect=""):
        Agent.__init__(self, name, "Plasmid", safety, admin)
        self.promoter = promoter
        self.drug_res = drug_res
        self.hosts = hosts
        self.cell_types = cell_types
        self.transfect = transfect

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("Promoter: ", self.promoter)
        print("Resistance Markers: ", self.drug_res)
        print("Experiment Host: ", self.hosts)
        print("Transfected? ", self.transfect)
        if(self.transfect == "Y"):
            print("Transfected into: ", self.cell_types)
        print("Admin H/A?", self.admin)
        print()

    def print_fancy(self):
        txt = ("<h5>Promoter</h5>" + self.promoter +
               "<h5>Resistance Markers</h5>" + self.drug_res +
               "<h5>Experimental Host</h5>" + self.hosts +
               "<h5>Transfected</h5>" + self.transfect)
        return super().print_fancy() + txt

# Cultured Cell Lines
# Cultured Cells have no Ind for Admin to H/A


class CCells(Agent):

    def __init__(self, name, atype, safety):
        Agent.__init__(self, name, "Cultured Cells", safety, "N")

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print()


# CBTO harvested directly from humans
# IBC does not cover non-recombinant Material for Admin

class Human_Material(Agent):
    def __init__(self, name, atype, safety, admin, irb=""):
        Agent.__init__(self, name, "Human Material", safety, "N")
        self.irb = irb

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("No IRB: ", self.irb)
        print()

    def print_fancy(self):
        txt = ("<h5>IRB</h5>" + self.irb)
        return super().print_fancy() + txt

# CBTO Harvested from NHPs
# IBC does not cover non-recombinant Material for Admin


class NHP_Material(Agent):
    def __init__(self, name, atype, safety, admin="N"):
        Agent.__init__(self, name, "NHP Material", safety, "N")

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print()


# CBTO from biohazardous animals obtained from others
# IBC does not cover non-recombinant Material for Administration, so administer value
# is always 'N'
class Outside_Material(Agent):
    def __init__(self, name, atype, safety, admin="N"):
        Agent.__init__(self, name, "Material from Other", safety, "N")

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print(self.desc)
        print("Administerd to H/A?", self.admin)
        print()


class Other(Agent):
    # Other Agents
    def __init__(self, name, atype, safety, admin, bsl="", desc=""):
        Agent.__init__(self, name, "Other Agent", safety, admin)
        self.bsl = bsl
        self.desc = desc

    def get_info(self):
        print("(", self.atype, ")   ", self.name)
        print("Biosafety Level: ", self.bsl)
        print("Description: ", self.desc)
        print("Administerd to H/A?", self.admin)
        print()

    def print_fancy(self):
        txt = ("<h5>Biosafety Level</h5>" + self.bsl +
               "<h5>Description</h5>" + self.desc)
        return super().print_fancy() + txt


def create_agents(path):
    # Process raw data from csv file into a Dictionary where
    # the key is the agent type and the value is the list of
    # agent objects of that type associated with the protocol

    data = pd.read_csv(path + 'Agents.csv')
    # Get Microbes
    microbes = []
    mtypes = ['Bacteria', 'Virus', 'Fungus', 'Protozoa']
    data_m = data.loc[data['Agent Type'].isin(mtypes)]
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Microbe(row['Agent Name'],
                    row['Agent Type'],
                    safeinfo,
                    row['Human Animal Admin Ind'],
                    row['Agent Risk Group'],
                    row['Select Agent Ind'],
                    row['Antibiotic Sensitivity Characterization'],
                    row['Attenuation Ind'])
        microbes.append(m)

    # Get Viral Vectors
    vv = []
    data_m = data.loc[data['Agent Type'] == 'Viral Vector']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = ViralVector(row['Agent Name'],
                        row['Agent Type'],
                        safeinfo,
                        row['Human Animal Admin Ind'],
                        row['Agent Risk Group'],
                        row['Select Agent Ind'],
                        row['Attenuation Ind'],
                        row['Replication competent Ind'])
        vv.append(m)

    # Get Biological Toxins
    toxins = []
    data_m = data.loc[data['Agent Type'] == 'Toxin']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Toxin(row['Agent Name'],
                  row['Agent Type'],
                  safeinfo,
                  row['Human Animal Admin Ind'],
                  row['Select Agent Ind'],
                  row['Bio Toxin Stored In Lab'])

        toxins.append(m)

    # Get TFC and VTC
    tfcs = []
    vtcs = []
    data_m = data.loc[data['Cell Type'] != 'No Data']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        # Check if TFC
        if row['Vtc Viral Vector System Used'] == 'No Data':
            m = TFC(row['Cell Type'],
                    "Transfected Cells",
                    safeinfo,
                    row['Human Animal Admin Ind'],
                    row['Dna'],
                    row['Dna Function'])
            tfcs.append(m)
        else:
            m = VTC(row['Cell Type'],
                    "Virally Transduced Cells",
                    safeinfo,
                    row['Human Animal Admin Ind'],
                    row['Dna'],
                    row['Dna Function'],
                    row['Vtc Cells Obtained Ind'],
                    row['Vtc Testing Method Desc'],
                    row['Vtc Viral Vector System Used'],
                    row['Potential Hazards'])
            vtcs.append(m)

    # Get Infections Proteins
    infp = []
    data_m = data.loc[data['Infectious Proteins List'] != 'No Data']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = InfProt(row['Infectious Proteins List'],
                    "Infectious Protein",
                    safeinfo,
                    row['Human Animal Admin Ind'])
        infp.append(m)

    # Get TATs
    tats = []
    data_m = data.loc[data['Transactive Peptide List'] != 'No Data']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = TAT(row['Transactive Peptide List'],
                "Transactive Peptide",
                safeinfo,
                row['Human Animal Admin Ind'],
                row['Potential Hazards'])
        tats.append(m)

    # Get DNA
    plasmids = []
    data_m = data.loc[data['PVector Name'] != 'No Data']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = DNA(row['PVector Name'],
                "Plasmid Vector",
                safeinfo,
                row['Human Animal Admin Ind'],
                row['PVector Promoter'],
                row['PVector Drug Resistance Gene'],
                row['PVector Exper Hosts List'],
                row['PVector List Cell Types'],
                row['PVector Transfected Ind'])
        plasmids.append(m)

    # Get CCells
    ccs = []
    data_m = data.loc[data['CBTO Established Cell Lines Ind'] == 'Y']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = CCells(row['CBTO Established Cell Lines Desc'],
                   "Cultured Cells",
                   safeinfo)
        ccs.append(m)

    # Get Human Material
    HM = []
    data_m = data.loc[data['CBTO Harvested Human Ind'] == 'Y']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Human_Material(row['CBTO Harvested materials List'],
                           "Human Material",
                           safeinfo,
                           "N",
                           row['CBTO No Irb Desc'])
        HM.append(m)

    # Get NHP Material
    NHPM = []
    data_m = data.loc[data['CBTO NHP Harvested Ind'] == 'Y']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Human_Material(row['CBTO Harvested Nhum Mat List'],
                           "NHP Material",
                           safeinfo)
        NHPM.append(m)

    # Get Other Material
    OM = []
    data_m = data.loc[data['CBTO Biohazard Material from Others Ind'] == 'Y']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Outside_Material(row['CBTO Biohazard Material from Others Desc'])
        OM.append(m)

    # Get Other Hazards
    oag = []
    data_m = data.loc[data['Oth Agent Name'] != 'No Data']
    for i, row in data_m.iterrows():
        safeinfo = create_safety_data(row)
        m = Other(row['Oth Agent Name'],
                  "Other Agent",
                  safeinfo,
                  "N",
                  row['Oth Agent Biosafety Lvl'],
                  row['Oth Method Desc'])
        oag.append(m)

    # Now Create Master Dictionary of all Agents
    protocol_agents = {'microbe': microbes,
                       'vv': vv,
                       'tox': toxins,
                       'vtc': vtcs,
                       'tfc': tfcs,
                       'ip': infp,
                       'tat': tats,
                       'plasmid': plasmids,
                       'cc': ccs,
                       'hm': HM,
                       'nhpm': NHPM,
                       'om': OM,
                       'other': oag}
    return protocol_agents
