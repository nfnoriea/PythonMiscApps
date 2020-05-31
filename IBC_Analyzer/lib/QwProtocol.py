from PySide2 import QtWidgets as Qw
from PySide2 import QtGui as Qg
import os


"""
Info Widget
Widget Container for all protcol information and hazard indicators

(MainGUI-> Main Window Widget -> Info Widget)
"""


class ProtocolWidget(Qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pinfo = PInfo(self)
        self.admin_indicators = AdminIndicator(self)
        self.agent_indicators = AgentIndicators(self)

        # LAYOUT
        layout = Qw.QHBoxLayout()
        layout.addWidget(self.pinfo)
        layout.addWidget(self.admin_indicators)
        layout.addWidget(self.agent_indicators)
        self.setLayout(layout)

        # ACTIONS
        self.show()

    def set_data(self, protocol):
        self.pinfo.set_data(protocol)
        self.admin_indicators.set_data(protocol)
        self.agent_indicators.set_data(protocol)

    def clear_data(self):
        self.pinfo.clear_data()
        self.admin_indicators.clear_data()
        self.agent_indicators.clear_data()


# InfoWidget SubWidget - Agent Hazard Indicators


class AgentIndicators(Qw.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Agents')

        # Create Dictionary Of Agent PushButtons
        self.buttons = {}
        idir = (os.path.dirname(os.path.abspath(__file__)) + '/images/')
        self.microbe = AgentButton('microbe', idir)
        self.buttons['microbe'] = self.microbe
        self.vv = AgentButton('vv', idir)
        self.buttons['vv'] = self.vv
        self.vtc = AgentButton('vtc', idir)
        self.buttons['vtc'] = self.vtc
        self.tfc = AgentButton('tfc', idir)
        self.buttons['tfc'] = self.tfc
        self.tox = AgentButton('tox', idir)
        self.buttons['tox'] = self.tox
        self.ip = AgentButton('ip', idir)
        self.buttons['ip'] = self.ip
        self.tat = AgentButton('tat', idir)
        self.buttons['tat'] = self.tat
        self.plasmid = AgentButton('plasmid', idir)
        self.buttons['plasmid'] = self.plasmid
        self.cc = AgentButton('cc', idir)
        self.buttons['cc'] = self.cc
        self.hm = AgentButton('hm', idir)
        self.buttons['hm'] = self.hm
        self.nhpm = AgentButton('nhpm', idir)
        self.buttons['nhpm'] = self.nhpm
        self.om = AgentButton('om', idir)
        self.buttons['om'] = self.om

        # LAYOUT
        lay = Qw.QGridLayout()
        lay.addWidget(self.microbe, 0, 0)
        lay.addWidget(self.vv, 0, 1)
        lay.addWidget(self.vtc, 0, 2)
        lay.addWidget(self.tfc, 0, 3)
        lay.addWidget(self.tox, 1, 0)
        lay.addWidget(self.ip, 1, 1)
        lay.addWidget(self.tat, 1, 2)
        lay.addWidget(self.plasmid, 1, 3)
        lay.addWidget(self.cc, 2, 0)
        lay.addWidget(self.hm, 2, 1)
        lay.addWidget(self.nhpm, 2, 2)
        lay.addWidget(self.om, 2, 3)
        lay.setHorizontalSpacing(0)
        lay.setVerticalSpacing(0)
        self.setLayout(lay)
        self.show()

    def set_data(self, protocol):
        r = protocol.risks
        ag = protocol.agent_list
        if r['micro']:
            self.microbe.in_protocol = True
        if r['vv']:
            self.vv.in_protocol = True
        if r['vtc']:
            self.vtc.in_protocol = True
        if r['tfc']:
            self.tfc.in_protocol = True
        if r['tox']:
            self.tox.in_protocol = True
        if r['infp']:
            self.ip.in_protocol = True
        if r['tat']:
            self.tat.in_protocol = True
        if r['dna']:
            self.plasmid.in_protocol = True
        if len(ag['cc']) > 0:
            self.cc.in_protocol = True
        if len(ag['hm']) > 0:
            self.hm.in_protocol = True
        if len(ag['nhpm']) > 0:
            self.nhpm.in_protocol = True
        if (len(ag['om']) + len(ag['other']) > 0):
            self.om.in_protocol = True
        self.activate()

    # Activate de-selects all buttons
    def activate(self):
        for b in self.buttons:
            self.buttons[b].set()

    def clear_data(self):
        for b in self.buttons:
            self.buttons[b].in_protocol = False

    def select_button(self, agent):
        self.activate()
        if self.buttons[agent].in_protocol:
            self.buttons[agent].select()


class AgentButton(Qw.QPushButton):
    def __init__(self, name, idir, parent=None):
        super().__init__(parent)

        self.name = name
        self.in_protocol = False
        self.off_img = Qg.QPixmap(idir + self.name + '_off.png')
        self.on_img = Qg.QPixmap(idir + self.name + '_on.png')
        self.set_img = Qg.QPixmap(idir + self.name + '_set.png')
        self.setFixedSize(self.off_img.rect().size())
        self.setIconSize(self.off_img.rect().size())
        self.set()

    def select(self):
        self.setIcon(self.set_img)

    def set(self):
        if self.in_protocol:
            self.setIcon(self.on_img)
        else:
            self.setIcon(self.off_img)


"""
Protocol Indicators Widget (Administered Widget)
"""


class AdminIndicator(Qw.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Administered to')

        # WIDGETS
        img_dir = (os.path.dirname(os.path.abspath(__file__)) + '/images/')

        self.animal_ind = Qw.QPushButton(self)
        self.human_ind = Qw.QPushButton(self)

        # Load Image Data for Indicators

        self.animal_off = Qg.QPixmap(img_dir + 'animal_off.png')
        self.human_off = Qg.QPixmap(img_dir + 'human_off.png')
        self.animal_on = Qg.QPixmap(img_dir + 'animal_on.png')
        self.human_on = Qg.QPixmap(img_dir + 'human_on.png')

        # Set Buttons to Image Size and Set Icon Size to Button Size
        self.animal_ind.setFixedSize(self.animal_off.rect().size())
        self.human_ind.setFixedSize(self.human_off.rect().size())

        self.animal_ind.setIconSize(self.animal_off.rect().size())
        self.human_ind.setIconSize(self.human_off.rect().size())

        # Set Default 'Off' Images
        self.animal_ind.setIcon(self.animal_off)
        self.human_ind.setIcon(self.human_off)

        # LAYOUT
        lay = Qw.QVBoxLayout()
        lay.addWidget(self.animal_ind)
        lay.addWidget(self.human_ind)
        self.setLayout(lay)

        self.show()

    def set_data(self, protocol):
        if protocol.special_risks['Animal Use']:
            self.animal_ind.setIcon(self.animal_on)
        else:
            self.animal_ind.setIcon(self.animal_off)
        if protocol.special_risks['Human Use']:
            self.human_ind.setIcon(self.human_on)
        else:
            self.human_ind.setIcon(self.human_off)

    def clear_data(self):
        self.animal_ind.setIcon(self.animal_off)
        self.human_ind.setIcon(self.human_off)


"""
Protocol Information Widget

(Info Widget -> PInfo Widget)
"""


class PInfo(Qw.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Protocol Information')

        # WIDGETS
        self.l_prid = Qw.QLabel()
        self.l_prid.setText('<b>Protocol ID</b>')
        self.l_name = Qw.QLabel('<b>Protocol Name</b>')
        self.l_pi = Qw.QLabel('<b>P.I.</b>')
        self.le_prid = Qw.QLineEdit('')
        self.le_name = Qw.QLineEdit('')
        self.le_pi = Qw.QLineEdit('')
        self.le_prid.setReadOnly(True)
        self.le_name.setReadOnly(True)
        self.le_pi.setReadOnly(True)

        self.b_bsc = Qw.QPushButton('Cabinets')
        self.b_rooms = Qw.QPushButton('Rooms')

        # LAYOUT

        lay = Qw.QGridLayout()
        lay.addWidget(self.l_prid, 0, 0)
        lay.addWidget(self.l_name, 1, 0)
        lay.addWidget(self.l_pi, 2, 0)
        lay.addWidget(self.le_prid, 0, 1)
        lay.addWidget(self.le_name, 1, 1)
        lay.addWidget(self.le_pi, 2, 1)

        lay2 = Qw.QVBoxLayout()
        lay2.addWidget(self.b_bsc)
        lay2.addWidget(self.b_rooms)

        layout = Qw.QHBoxLayout()
        layout.addLayout(lay)
        layout.addLayout(lay2)

        self.setLayout(layout)
        self.show()

    def set_data(self, protocol):
        self.le_prid.setText(protocol.protocol_id)
        self.le_name.setText(protocol.name)
        self.le_pi.setText(protocol.pi)

    def clear_data(self):
        self.le_prid.setText('')
        self.le_name.setText('')
        self.le_pi.setText('')
