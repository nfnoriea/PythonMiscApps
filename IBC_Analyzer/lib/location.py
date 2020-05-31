import pandas as pd

# Get Location and BSC Data for Protocol


class Room(object):
    def __init__(self, bldg="", room_num="", use=""):
        self.bldg = bldg
        self.room_num = room_num
        self.use = use
        self.name = self.bldg + ' - ' + self.room_num

    def get_info(self):
        print(self.room_num + "  " + self.bldg)
        print("Use: ", self.use, "\n")

    def print_fancy(self):
        txt = ("<h5>Building</h5>" + self.bldg +
               "<h5>Room Number</h5>" + self.room_num +
               "<h5>Use</h5>" + self.use)
        return txt


class BSC(object):
    def __init__(self, btype="", manufacturer="", model_num="", serial_num="",
                 cert_date="", room=""):
        self.btype = btype
        self.manufacturer = manufacturer
        self.model_num = model_num
        self.serial_num = serial_num
        self.cert_date = cert_date
        self.room = room
        self.name = self.manufacturer + ' - ' + self.model_num

    def get_info(self):
        print(self.manufacturer + "\t" + self.model_num)
        print(self.btype + "\t Last Cert: ", self.cert_date)
        print("Room: ", self.room.room_num)
        print(self.room.bldg)
        print("Serial #: ", self.serial_num, "\n")

    def print_fancy(self):
        txt = ("<h5>Type</h5>" + self.btype +
               "<h5>Manufacturer</h5>" + self.manufacturer +
               "<h5>Model Number</h5>" + self.model_num +
               "<h5>Serial Number</h5>" + self.serial_num +
               "<h5>Certification Date</h5>" + self.cert_date)
        return txt


def create_locations(path):
    data = pd.read_csv(path + "Locations.csv")
    rooms = process_rooms(data)
    cabinets = process_bscs(data, rooms)
    return rooms, cabinets


def process_bscs(d, rooms):
    data_b = d.loc[d['Model Number'] != 'No Data']
    cabinets = []
    for i, row in data_b.iterrows():

        # Find the room of attached BSC
        bsc_room_num = row.loc['Lab Room Num']
        bsc_room_obj = None
        for r in rooms:
            if r.room_num == bsc_room_num:
                bsc_room_obj = r
                break
        b = BSC(row['Biosafety Cabinet Type'],
                row['Manufacture'],
                row['Model Number'],
                row['Serial Number'],
                row['Last Certification Dt'],
                bsc_room_obj)
        cabinets.append(b)
    return cabinets


def process_rooms(d):
    data_b = d.loc[d['Use Of Room'] != 'No Data']
    locs = []
    for i, row in data_b.iterrows():
        l = Room(row['Location Attributes.Building Name'],
                 row['Lab Room Num'],
                 row['Use Of Room'])
        locs.append(l)
    return locs
