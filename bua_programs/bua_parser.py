#!/usr/bin/python3

import requests, codecs, os, pprint
from lxml import etree, html
from io import StringIO, BytesIO
import pandas as pd
import bua_tables as btbl

class BUA:
    def __init__(self, bua_id, html):
                
        self.id = bua_id
        self.name = str(bua_id)
        self.tables = []        # html tables read by pandas
        self.table_list = []  # the table number from tables[] with the table type identified by program
        self.data = {}          # will store dataframes here
        self.risks = []         # store biohazard risks
        self.processed = False
        if len(html) < 4000:
            print("** Warning ** BUA #" + self.name +
                  " is empty! Check BUA id.")
        else:
            self.tables = pd.read_html(html)
            self.tables = [x.fillna('') for x in self.tables]

    def process(self):
        if self.tables:
            self.process_basic()
            self.process_locations()
            self.process_risks()
        self.processed = True
                
    def process_basic(self):
        if self.processed:
            return
        t2 = btbl.get_table2(self)
        t4 = btbl.get_table4(self)
        t5 = btbl.get_table5(self)
        t6 = btbl.get_table6(self)
        df = t2.join(t4)
        df = df.join(t5)
        df = df.join(t6)
        
        self.get_risks(t6)
        self.data['basic'] = df
        self.table_list.append('2,4,5,6 - Basic Data')

    def process_locations(self):
        if self.processed:
            return
        # table 3
        t3df = self.tables[3].copy()
        t3df['id'] = self.name
        self.data['locations'] = t3df
        self.table_list.append("3 - locations")
        
    def process_risks(self):
        if self.processed:
            return
        i = 7   # starting index by default. tables 2-6 are 'basic info'
        num_risks = len(self.risks)
        num_processed = 0
        if num_risks == 0:
            btbl.get_controls_ack(self,i)
            return
        # each loop get the agent list in the first table and questions in
        # the second table. the biohazards are always in order:
        # human, plants, rDNA, tg plants, animals, inverts, hsc
        
        while num_processed < num_risks:
            risk_name = self.risks[num_processed]
            self.table_list.append((str(i) + " - " + risk_name + " list"))

            # if the risk is human stem cells, determine if there are
            # 1 or two external tables
            # check for 'Cell Type' in the columns labels of table to
            # determine if an hsc agent list
            
            risk_list_df = btbl.get_risk_list(self, i)
            i = i + 1
            
            if risk_name == 'stem cells':    
                # check for hsc second table
                if 'Cell Type' in self.tables[i].columns:
                    # process second table view
                    hsc2_df = btbl.get_risk_list(self, i)
                    risk_list_df = risk_list_df.merge(hsc2_df, how='outer').fillna('')
                    i = i + 1

            listname = risk_name + '_list'
            self.data[listname] = risk_list_df

            qsname = risk_name + '_questions'

            # only one protocol has no question part for the human stem cells
            if risk_name == 'stem cells' and self.name == '2017003101':
                num_processed = num_processed + 1
            else:
                self.table_list.append((str(i) + " - " + risk_name + " questions"))
                risk_q_df = btbl.get_risk_qs(self, risk_name, i)
                i = i + 1
                self.data[qsname] = risk_q_df    
                num_processed = num_processed + 1
            
        self.table_list.append((str(i) + " - controls"))
        self.table_list.append((str(i+1) + " - acknowledgement"))
        btbl.get_controls_ack(self,i)


    def check_risk(self, table, start, finish, name):
        for i in range(start, finish):
            data = str(table.iloc[0,i])
            if data == "True":
                self.risks.append(name)
                break
            

    def get_risks(self, t6):
        self.check_risk(t6, 0, 5, "human")
        self.check_risk(t6, 5, 9, "plants")
        self.check_risk(t6, 9, 12, "rDNA")
        self.check_risk(t6, 12, 17, "transgenic plants")
        self.check_risk(t6, 17, 23, "animals")
        self.check_risk(t6, 23, 28, "inverts")
        self.check_risk(t6, 28, 29, "stem cells")
        self.check_first_view()

    def check_first_view(self):
        # this is called because the bua html will force the 
        # human/animal infectious agents view even if human or
        # animal isnt checked UNLESS infectious plants is checked
        # if only rDNA is checked then no human or plant view

        # if no risks, add human risk view
        if len(self.risks) == 0:
            self.risks = ['human']
            return

        if 'human' in self.risks:
            return
        
        # if animals checked but not human, add human
        if 'animals' in self.risks and 'rDNA' not in self.risks:
            # if animals in but not human, add human view
            oldr = self.risks
            newr = ['human'] + oldr
            self.risks = newr
            return

        if 'rDNA' in self.risks:
            if len(self.risks) == 1:
                if self.name[3] == '9' or len(self.name) > 8:
                    self.risks = ['human', 'rDNA']

        if 'stem cells' in self.risks and len(self.risks) == 1:
            self.risks = ['human', 'stem cells']
        

    def __str__(self):
        s = ("BUA: " + self.name + "\nProcessed: " + str(self.processed) +
             "\nRisks: ")
        r = pprint.pformat(self.risks)
        k = "\nData: ["
        k += ", ".join(self.data)
        k += ']'
        return (s + r + k)

def create_bua_list(csv_file='buas.csv'):
    # assuming that excel file with single column is saved as CSV
    x = pd.read_csv(csv_file, header=None)
    li = x[0].values.tolist()
    v1 = []
    v2 = []
    for bua in li:
        bua = bua.replace('-','')
        if bua[4] == '0':
            v1.append(bua)
        else:
            v2.append(bua)
    v1len = str(len(v1))
    v2len = str(len(v2))
    print("Found " + v1len + " v1 BUAs.")
    print("Found " + v2len + " v2 BUAs.")
    bua_list = []
    for b in v1:
        bua_list.append(create_bua(b))
    return bua_list
        
        
def combine_buas(bua_list):
    print("Combining BUAs...")
    df = {}
    cnt = 0
    for b in bua_list:
        # print("Dataframe bua_list[" + str(cnt) + "]")        
        # print("Adding BUA " + b.name)
        for keyname in b.data.keys():
            str_df = b.data[keyname].applymap(str)
            # print("Adding " + keyname)
            if keyname in df.keys():
                df[keyname] = df[keyname].merge(str_df, how='outer').fillna('')
            else:
                df[keyname] = str_df
        cnt = cnt + 1
    print("Combined " + str(cnt) + " buas.")
    return df

def to_csv(bua_list, select="all"):
    df = combine_buas(bua_list)
    pathf = 'csv'
    if not os.path.exists(pathf):
        os.mkdir(pathf)
    if select == "all":
        for keyname in df.keys():
            path = pathf + '/' + keyname + '.csv'
            df[keyname].to_csv(path)
    else:
        path = pathf + '/' + select + '.csv'
        if select not in df.keys():
            print("Cant write " + select + " to CSV. Does not Exist.")
        else:
            df[select].to_csv(path)
    print("Wrote CSVs to file.")
        

def create_buas(bua_list):
    blist = []
    for b in bua_list:
        blist.append(create_bua(b))
    return blist
        
def create_bua(bua_id, force_create=False):
    path = 'html/' + str(bua_id) + '.html'
    if os.path.exists(path) and not force_create:
        with open(path, 'r') as f:
            data = f.read()
        return BUA(bua_id, data)
    
    ucr_prefix = ("https://research.ucr.edu/" +
                  "OrPortal/Forms/Compliance/IBC/BUA/" +
                  "Print.asp?Project_Number=")
    link = ucr_prefix + str(bua_id)
    response = requests.get(link)
    if(response.status_code != 200):
        print("Error retreiving html from link (" +
              str(response.status_code) + ")\n" + link)
        return 0
    data = response.text
    # process all broken BUA links 
    no_text = ("<img src=\'/appAsp/images/CheckBox.gif\'>Yes&nbsp;&nbsp;&nbsp;" +
               "<img src=\'/appAsp/images/CheckedBox.gif\'>No")
    yes_text = ("<img src=\'/appAsp/images/CheckedBox.gif\'>Yes&nbsp;&nbsp;&nbsp;" +
                "<img src=\'/appAsp/images/CheckBox.gif\'>No")
    yesna_text = ("<img src=\'/appAsp/images/CheckedBox.gif\'>Yes&nbsp;&nbsp;&nbsp;" +
                  "<img src=\'/appAsp/images/CheckBox.gif\'>N/A")
    na_text = ("<img src=\'/appAsp/images/CheckBox.gif\'>Yes&nbsp;&nbsp;&nbsp;" +
               "<img src=\'/appAsp/images/CheckedBox.gif\'>N/A")
    
    bsl1_text = ("<img src=\'/appAsp/images/CheckedBox.gif\'>BSL1<br>" +
                 "<img src=\'/appAsp/images/CheckBox.gif\'>BSL2" +
                 "<br><img src='/appAsp/images/CheckBox.gif\'>BSL3<br>")
    bsl2_text = ("<img src=\'/appAsp/images/CheckBox.gif\'>BSL1<br>"+
                 "<img src=\'/appAsp/images/CheckedBox.gif\'>BSL2"+
                 "<br><img src='/appAsp/images/CheckBox.gif\'>BSL3<br>")
    bsl3_text = ("<img src=\'/appAsp/images/CheckBox.gif\'>BSL1<br>"+
                 "<img src=\'/appAsp/images/CheckBox.gif\'>BSL2"+
                 "<br><img src='/appAsp/images/CheckedBox.gif\'>BSL3<br>")
    
    data = data.replace(no_text, "False").replace(yes_text,"True")
    data = data.replace(bsl1_text,"BSL1").replace(bsl2_text,"BSL2").replace(bsl3_text,"BSL3")
    data = data.replace(yesna_text,"True").replace(na_text,"False")

    name = str(bua_id)
    fname = 'html/' + name + '.html'

    if not os.path.exists('html'):
        os.mkdir('html')
        
    tree = etree.parse(StringIO(data),etree.HTMLParser())
    with open(fname, 'wb') as f:
        f.write(etree.tostring(tree.getroot(),
                               pretty_print=True,
                               method='html'))
    return BUA(bua_id, data)
