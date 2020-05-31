import pandas as pd

# Get Animal Data from Protocol


class Animal(object):
    def __init__(self, name="", iacuc="", shed="", route="", absl="",
                 transport="", freq="", total_doses="", max_dose="",
                 animal_species=""):
        self.name = name
        self.iacuc = iacuc
        self.shed = shed
        self.route = route
        self.absl = absl
        self.transport = transport
        self.freq = freq
        self.total_doses = total_doses
        self.max_dose = max_dose
        self.animal_species = animal_species

    def get_info(self):
        print(self.name)
        print("Animal: ", self.animal_species, "\t Shed? ", self.shed)
        print("Max Dose: ", self.max_dose, "\tNum Doses: ",
              self.total_doses, "\tFrequency: ", self.freq)
        print("Transport? ", self.transport, "\tIACUC: ", self.iacuc, "\n")

    def print_fancy(self):
        txt = ('<h4>Animal Species</h4>' + self.animal_species +
               '<h4>Agent</h4>' + self.name +
               '<h5>Shed?</h5>' + self.shed +
               '<h5>ABSL</h5>' + self.absl +
               '<h5>Frequency</h5>' + self.freq +
               '<h5>Total Doses</h5>' + self.total_doses +
               '<h5>Max Dose</h5>' + self.max_dose)
        return txt


def create_animals(path):
    d = pd.read_csv(path + 'Animals.csv')
    zoo = []
    for i, row in d.iterrows():
        a = Animal(row['Animal Risk Asses Agent Desc'],
                   row['IACUC Protocol Id2'],
                   row['Shed Ind'],
                   row['Route Of Admin'],
                   row['Animal Biosafety Level'],
                   row['Animal Transport Ind'],
                   row['Frequency'],
                   row['Total # of Doses'],
                   row['Max Dose'],
                   row['Animal Species'])
        zoo.append(a)
    return zoo
