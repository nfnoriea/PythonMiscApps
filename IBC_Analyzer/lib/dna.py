import pandas as pd

# Gets Protocol DNA Data


class Gene(object):
    def __init__(self, name="", func="", derive="", onco=""):
        self.name = name
        self.func = func
        self.derive = derive
        self.onco = onco

    def get_info(self):
        print(self.name)
        print("Function: ", self.func)
        print("Species derived from: ", self.derive)
        print("Oncogene: ", self.onco, "\n")


def create_genes(path):
    d = pd.read_csv(path + 'DNA.csv')
    pool = []
    for i, row in d.iterrows():
        g = Gene(row['r/sDna Name'],
                 row['r/sDna Function'],
                 row['Species/Organism Derived From'],
                 row['Oncogenic/Biohazardous Ind'])
        pool.append(g)
    return pool
