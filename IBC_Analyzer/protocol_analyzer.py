#!/usr/bin/python3

from PySide2 import QtWidgets as Qw
from lib import protocol as Protocol
from lib import QwDetail as Dw
from lib import QwProtocol as Pw
import sys


# Master Gui Container for All Widgets
class MainGUI(Qw.QMainWindow):
    # Initialize
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_widget = None
        self.protocol = None
        self.loc_widget = None
        self.create_ui()

    # Create UI
    def create_ui(self):
        # MENU BAR WIDGET
        bar = self.menuBar()
        file_bar = bar.addMenu('File')

        # MENU BAR - ACTIONS
        open_action = Qw.QAction('&Open', self)
        quit_action = Qw.QAction('&Quit', self)
        clear_action = Qw.QAction('&Clear', self)
        file_bar.addAction(open_action)
        file_bar.addAction(clear_action)
        file_bar.addAction(quit_action)
        file_bar.triggered.connect(self.menu_respond)

        # WIDGETS
        self.main = MainWindow(self)
        self.setCentralWidget(self.main)

        # SIGNALS FOR AGENT BUTTONS/INDICATORS
        self.agent_button_actions()
        self.admin_button_actions()
        self.main.protocol_widget.pinfo.b_bsc.clicked.connect(
            lambda: self.main.detail_widget.set_list_data('BSC'))
        self.main.protocol_widget.pinfo.b_rooms.clicked.connect(
            lambda: self.main.detail_widget.set_list_data('Rooms'))

        # WINDOW SETTINGS
        self.setWindowTitle('IBC Protocol Analyzer')
        self.resize(1600, 800)
        self.show()

    def menu_respond(self, action):
        signal = action.text()
        if signal == '&Quit':
            Qw.qApp.quit()
        elif signal == '&Open':
            self.load_widget = LoadData(self)
            self.load_widget.b_load.clicked.connect(self.load_protocol)
        elif signal == '&Clear':
            self.clear_info()
        else:
            print("Error in Menu Response")

    # Agent Indicator Button Signals
    def agent_button_actions(self):
        self.main.protocol_widget.agent_indicators.microbe.clicked.connect(
            lambda: self.button_actions('microbe'))
        self.main.protocol_widget.agent_indicators.vv.clicked.connect(
            lambda: self.button_actions('vv'))
        self.main.protocol_widget.agent_indicators.vtc.clicked.connect(
            lambda: self.button_actions('vtc'))
        self.main.protocol_widget.agent_indicators.tfc.clicked.connect(
            lambda: self.button_actions('tfc'))
        self.main.protocol_widget.agent_indicators.tox.clicked.connect(
            lambda: self.button_actions('tox'))
        self.main.protocol_widget.agent_indicators.ip.clicked.connect(
            lambda: self.button_actions('ip'))
        self.main.protocol_widget.agent_indicators.tat.clicked.connect(
            lambda: self.button_actions('tat'))
        self.main.protocol_widget.agent_indicators.plasmid.clicked.connect(
            lambda: self.button_actions('plasmid'))
        self.main.protocol_widget.agent_indicators.cc.clicked.connect(
            lambda: self.button_actions('cc'))
        self.main.protocol_widget.agent_indicators.hm.clicked.connect(
            lambda: self.button_actions('hm'))
        self.main.protocol_widget.agent_indicators.nhpm.clicked.connect(
            lambda: self.button_actions('nhpm'))
        self.main.protocol_widget.agent_indicators.om.clicked.connect(
            lambda: self.button_actions('om'))

    def button_actions(self, agent):
        if self.protocol is None:
            pass
        else:
            self.main.detail_widget.set_list_data(agent)
            self.main.protocol_widget.agent_indicators.select_button(agent)

    # Load Protocol Data
    def load_protocol(self):
        self.protocol = self.load_widget.protocol
        self.main.protocol_widget.set_data(self.protocol)
        self.main.detail_widget.set_protocol(self.protocol)

    # Clear All Protocol Data
    def clear_info(self):
        self.main.protocol_widget.clear_data()
        self.main.detail_widget.clear_all()

    # SIGNALS for Administered Buttons
    def admin_button_actions(self):
        self.main.protocol_widget.admin_indicators.animal_ind.clicked.connect(
            lambda: (self.main.detail_widget.set_list_data('Animal')))

        # Unselect any Selected Agent buttons
        self.main.protocol_widget.admin_indicators.animal_ind.clicked.connect(
            lambda: self.main.protocol_widget.agent_indicators.activate())

        # Clear Data (Doesnt clear list)
        self.main.protocol_widget.admin_indicators.animal_ind.clicked.connect(
            lambda: self.main.detail_widget.clear_data())


"""
Load Data Widget
(Menu Bar)
"""


class LoadData(Qw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.protocol = None

    def init_ui(self):
        # Widgets
        self.l1 = Qw.QLabel('Load Protocol:')
        self.lbl_id = Qw.QLabel(self)
        self.edit = Qw.QLineEdit(self)
        self.b_load = Qw.QPushButton("Load")
        self.b_canc = Qw.QPushButton("Cancel")

        # Signals
        self.b_load.clicked.connect(self.load_data)
        self.b_canc.clicked.connect(lambda: self.close())

        # Layout
        lay1 = Qw.QHBoxLayout()
        lay1.addWidget(self.l1)
        lay1.addWidget(self.lbl_id)

        b_lay = Qw.QHBoxLayout()
        b_lay.addWidget(self.b_load)
        b_lay.addWidget(self.b_canc)

        layout = Qw.QVBoxLayout()
        layout.addLayout(lay1)
        layout.addWidget(self.edit)

        layout.addLayout(b_lay)
        self.setLayout(layout)

        self.show()

    def load_data(self):
        path = './test_data/' + self.edit.text() + '/'
        self.lbl_id.setText(path)
        # Create Data
        data = Protocol.create_protocol(path)

        # Check for Errors in Loading Data
        if data is not None:
            self.protocol = data
            self.close()
        else:
            self.lbl_status.setText('Error! Could not Load Data.')


"""
Main Window Widget
"""


class MainWindow(Qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        # WIDGETS
        self.protocol_widget = Pw.ProtocolWidget(self)
        self.detail_widget = Dw.DetailWidget(self)

        # LAYOUTS
        lay = Qw.QVBoxLayout()
        lay.addWidget(self.protocol_widget)
        lay.addWidget(self.detail_widget)

        # ACTIONS
        self.setLayout(lay)
        self.show()


"""
RUN PROGRAM
"""
if __name__ == '__main__':
    app = Qw.QApplication()
    main = MainGUI()
    sys.exit(app.exec_())
