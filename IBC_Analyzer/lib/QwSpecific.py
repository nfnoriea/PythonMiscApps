from PySide2 import QtWidgets as Qw

"""
Safety Widget

(Detail Widget -> Agent Widget -> Safety Widget)
"""


class SafetyWidget(Qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.l_ppe = Qw.QLabel('<h4>PPE</h4>')
        self.l_equip = Qw.QLabel('<h4>Safety Equipment</h4>')
        self.l_spill = Qw.QLabel('<h4>Spill Procedure</h4>')
        self.l_addprac = Qw.QLabel('<h4>Additional Practices</h4>')
        self.l_sde = Qw.QLabel('<h4>Surface Decon</h4>')
        self.l_ede = Qw.QLabel('<h4>Equipment Decon</h4>')
        self.l_waste = Qw.QLabel('<h4>Waste</h4>')

        self.txt_ppe = Qw.QLineEdit()
        self.txt_ppe.setReadOnly(True)
        self.txt_equip = Qw.QLineEdit()
        self.txt_equip.setReadOnly(True)
        self.txt_spill = Qw.QLineEdit()
        self.txt_spill.setReadOnly(True)
        self.txt_addprac = Qw.QLineEdit()
        self.txt_addprac.setReadOnly(True)
        self.txt_sde = Qw.QLineEdit()
        self.txt_sde.setReadOnly(True)
        self.txt_ede = Qw.QLineEdit()
        self.txt_ede.setReadOnly(True)
        self.txt_waste = Qw.QLineEdit()
        self.txt_waste.setReadOnly(True)

        # LAYOUT
        lay = Qw.QVBoxLayout()

        lay1 = Qw.QHBoxLayout()
        lay1.addWidget(self.l_ppe)
        lay1.addWidget(self.txt_ppe)

        lay2 = Qw.QHBoxLayout()
        lay2.addWidget(self.l_equip)
        # lay2.addStretch()
        lay2.addWidget(self.txt_equip)

        lay3 = Qw.QHBoxLayout()
        lay3.addWidget(self.l_spill)
        # lay3.addStretch()
        lay3.addWidget(self.txt_spill)

        lay4 = Qw.QHBoxLayout()
        lay4.addWidget(self.l_addprac)
        # lay4.addStretch()
        lay4.addWidget(self.txt_addprac)

        lay5 = Qw.QHBoxLayout()
        lay5.addWidget(self.l_sde)
        # lay5.addStretch()
        lay5.addWidget(self.txt_sde)

        lay6 = Qw.QHBoxLayout()
        lay6.addWidget(self.l_ede)
        # lay6.addStretch()
        lay6.addWidget(self.txt_ede)

        lay7 = Qw.QHBoxLayout()
        lay7.addWidget(self.l_waste)
        # lay7.addStretch()
        lay7.addWidget(self.txt_waste)

        lay.addLayout(lay1)
        lay.addLayout(lay2)
        lay.addLayout(lay3)
        lay.addLayout(lay4)
        lay.addLayout(lay5)
        lay.addLayout(lay6)
        lay.addLayout(lay7)

        self.setLayout(lay)

        self.show()

    def set_data(self, agentitem):
        if not agentitem.is_agent():
            return
        s = agentitem.mydata.safety
        self.txt_ppe.setText(s.ppe)
        self.txt_equip.setText(s.safety_eq[0])
        self.txt_spill.setText(s.spill[0])
        self.txt_addprac.setText(s.addlpractice[0])
        self.txt_sde.setText(s.surface_de[0])
        self.txt_ede.setText(s.equip_de)
        self.txt_waste.setText(s.waste)

    def clear_data(self):
        self.txt_ppe.setText('')
        self.txt_equip.setText('')
        self.txt_spill.setText('')
        self.txt_addprac.setText('')
        self.txt_sde.setText('')
        self.txt_ede.setText('')
        self.txt_waste.setText('')
