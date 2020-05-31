from PySide2 import QtWidgets as Qw

"""
Detail Widget
     The container widget which holds all subwidgets in the primary window.
     This widget controls all signals for selecting list items and functions
     to load and clear list items
"""


class DetailWidget(Qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.protocol = None

        # WIDGETS
        # Name Widget
        self.name = Qw.QLabel()
        self.name.setWordWrap(True)

        # Special Agent Widget
        self.specialBox = Qw.QTextEdit(self)
        self.specialBox.setReadOnly(True)

        # Detail Box
        self.detailBox = Qw.QTextEdit(self)
        self.detailBox.setReadOnly(True)

        # Item List
        self.itemlist = Qw.QListWidget(self)
        self.itemlist.setMaximumHeight(180)

        self.basicInfoBox = BasicInfo(self)

        # Layout
        self.leftcol = Qw.QVBoxLayout()
        self.leftcol.addWidget(self.name)
        self.leftcol.addWidget(self.basicInfoBox)
        self.leftcol.addWidget(self.specialBox)

        self.rightcol = Qw.QVBoxLayout()
        self.rightcol.addWidget(self.itemlist)
        self.rightcol.addWidget(self.detailBox)

        self.layout = Qw.QHBoxLayout(self)
        self.layout.addLayout(self.leftcol)
        self.layout.addLayout(self.rightcol)

        self.setLayout(self.layout)
        self.show()

        # Signals
        self.itemlist.itemSelectionChanged.connect(self.clear_data)
        self.itemlist.itemClicked.connect(self.set_clicked_data)
        self.itemlist.itemActivated.connect(self.set_clicked_data)

    def set_clicked_data(self, item):
        self.name.setText('<h2 style="color:blue">' + item.name + '</h2>')
        self.detailBox.setHtml(item.mydata.print_fancy())
        self.basicInfoBox.set_data(item)
        # Call Special Box Widget

    def set_specialBox(self, newwidget=None):
        return
        self.leftcol.removeWidget(self.specialBox)
        self.specialBox = Qw.QLabel('Yay!!')
        self.leftcol.addWidget(self.specialBox)
        self.leftcol.addWidget(self.specialBox)

    def set_protocol(self, protocol):
        self.protocol = protocol
        self.set_specialBox()

    def clear_data(self):
        self.name.setText('')
        self.detailBox.clear()

    def clear_list(self):
        self.itemlist.clear()

    def clear_all(self):
        self.clear_data()
        self.clear_list()

    def set_list_data(self, obj_type):
        if self.protocol is None:
            return
        self.itemlist.clear()
        items = []
        if obj_type == 'Animal':
            items = self.protocol.animals
        elif obj_type == 'BSC':
            items = self.protocol.cabinets
        elif obj_type == 'Rooms':
            items = self.protocol.rooms
        elif obj_type == 'Genes':
            items = self.protocol.genes
        else:
            items = self.protocol.agent_list[obj_type]
        for i in items:
            self.itemlist.addItem(IBCListItem(i.name, i))


"""
Wrapper List Item Widget
"""


class IBCListItem(Qw.QListWidgetItem):
    def __init__(self, name, mydata, parent=None):
        super().__init__(name, parent)
        self.mydata = mydata
        self.name = name

    def is_agent(self):
        return (hasattr(self.mydata, 'atype'))

    def is_animal(self):
        return (hasattr(self.mydata, 'animal_species'))

    def is_room(self):
        return (hasattr(self.mydata, 'bldg'))

    def is_bsc(self):
        return (hasattr(self.mydata, 'btype'))

    def is_gene(self):
        return (hasattr(self.mydata, 'onco'))


class BasicInfo(Qw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.l_rg = Qw.QLabel()
        self.l_sa = Qw.QLabel()
        self.l_admin = Qw.QLabel()

        self.clear_data()

        # LAYOUT
        lblay = Qw.QHBoxLayout()
        lblay.addWidget(self.l_rg)
        lblay.addWidget(self.l_admin)
        lblay.addWidget(self.l_sa)

        self.setLayout(lblay)

        self.show()

    def clear_data(self):
        self.l_rg.setText('<h3 style="color:gray">No Risk Group</h3>')
        self.l_admin.setText('<h5 style="color:gray">Not Admin</h5>')
        self.l_sa.setText('<h5 style="color:gray">Not SA </h5>')

    def set_data(self, agentitem):
        self.clear_data()
        if not agentitem.is_agent():
            return
        agent = agentitem.mydata
        if agent.is_administered():
            self.l_admin.setText('<h5 style="color:red"> Administered </h5>')
        rg = agent.get_riskgroup()
        if rg is not None:
            if rg == 1:
                self.l_rg.setText('<h3 style="color:green">RG1</h3>')
            elif rg == 2:
                self.l_rg.setText('<h3 style="color:orange">RG2</h3>')
            elif rg == 3:
                self.l_rg.setText('<h3 style="color:red">RG3</h3>')
        if agent.is_selectagent():
            self.l_sa.setText('<h5 style="color:red"> SA </h5>')
