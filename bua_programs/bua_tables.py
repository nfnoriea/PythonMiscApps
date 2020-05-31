import pprint as pp
import pandas as pd

def get_table2(bua):
    if not bua.tables:
        return
    
    t2 = bua.tables[2].copy()
    dict = {}
    dict['Principal Investigator'] = [t2.iloc[0,1].replace(';','.')] # PI
    dict['Department'] = [t2.iloc[1,1].replace(';','.')] # Dept
    dict['Email'] = [t2.iloc[0,4].replace(';','.')] # Email
    dict['Phone'] = [t2.iloc[1,4].replace(';','.')] # Phone
    dates = t2.iloc[2,1].split('-') # start-end dates
    dict['Date Start'] = [dates[0].replace(';','.')]
    dict['Date End'] = [dates[1].replace(';','.')]

    # after start/end date, the remaining columns are variable depending
    # on the number of rows added
    # get length of table
    #tbllen = len(t2.columns)

    dict['Fax'] = [t2.iloc[2,4].replace(';','.')] # Fax
    dict['Project Title'] = [t2.iloc[4,0].replace(';','.')] # Project Title
    dict['Funding'] = [t2.iloc[6,0].replace(';','.')] # Funding
    # if there is data entry for funding html will add a row for it
    i = 8
    if t2.iloc[6,0] == '':
        i = 7
    dict['Alt Contact'] = [t2.iloc[i,4].replace(';','.')] # Additional Contact
    t2 = pd.DataFrame(dict)
    t2.index = [bua.name]
    t2['id'] = [bua.name]
    return t2

def get_table4(bua):
    if not bua.tables:
        return

    t4 = bua.tables[4].copy()
    
    t4 = t4.drop(t4.index[6])
    t4 = t4.drop(t4.index[7])
    t4.iloc[1,0] = "Approved BUA"
    t4.iloc[2,0] = "Human or Animal Subjects or Conflict of Interest"
    t4.iloc[3,0] = "Other UCR Review Boards"
    t4.iloc[6,0] = "Exotic Plant or Animal Pathogens"
    t4.iloc[9,0] = "Release of Transgenic Organisms"
    t4.iloc[10,0] = "Application for Release"
    t4.iloc[11,0] = "Select Agents"
    t4 = format_bua_table(t4)
    del t4[0]
    t4.index = [bua.name]
    t4['CDFA'][0] = t4['CDFA'][0].replace(';','.')
    t4['APHIS'][0] = t4['APHIS'][0].replace(';','.')               
    t4['IRB (human subjects)'][0] = t4['IRB (human subjects)'][0].replace(';','.')       
    t4['IRB (human subjects)'][0] = t4['IRB (human subjects)'][0].replace('\t','')       
    t4['IACUC (animal subjects)'][0] = t4['IACUC (animal subjects)'][0].replace(';','.')       
    return t4

def get_table5(bua):

    if not bua.tables:
        return
    
    t5 = bua.tables[5].copy()
    t5 = t5.T
    del t5[1]
    t5.index = [bua.name]
    t5.columns = ['Project Description', 'Project Objectives']
    t5['Project Description'][0] = t5['Project Description'][0].replace(';','.')
    t5['Project Objectives'][0] = t5['Project Objectives'][0].replace(';','.')
    t5['Project Description'][0] = t5['Project Description'][0].replace('\t','')
    t5['Project Objectives'][0] = t5['Project Objectives'][0].replace('\t','')
    return t5

def get_table6(bua):

    if not bua.tables:
        return

    t6 = bua.tables[6].copy()

    # plant labels
    for i in range(6,10):
        t6.iloc[i,0] = "Plant " + t6.iloc[i,0]
    # rDNA Labels
    t6.iloc[11,0] = "rDNA"
    t6.iloc[12,0] = "rDNA Release"
    t6.iloc[13,0] = "rDNA Other"
    # write transgenic labels
    t6.iloc[14,0] = "Transgenic Plants lbl"
    for i in range(15,20):
        t6.iloc[i,0] = "Transgenic " + t6.iloc[i,0]
    # write animal labels
    t6.iloc[21,0] = "Zoonotic Reservoirs"
    t6.iloc[22,0] = "Agents in Animals"
    t6.iloc[23,0] = "Cells in Animals"
    t6.iloc[25,0] = "Animal " + t6.iloc[25,0]
    # invert labels
    t6.iloc[29,0] = "Invertebrate Release"
    t6.iloc[31,0] = "Invertebrate Other"
    # Stem cell label to seperate id label from data label
    t6.iloc[32,0] += " lbl"
    
    t6 = format_bua_table(t6)
    del t6['Human or Animal Infectious Agents']
    del t6['Plant Infectious Agents']
    del t6['Recombinant DNA']
    del t6['Transgenic Plants lbl']
    del t6['Human Stem Cells lbl']
    del t6['Invertebrates']
    t6.index = [bua.name]
    return t6

    
def get_controls_ack(bua, index):
    # returns both acknowledgement and controls table in right format
    ctrls = bua.tables[index].copy()
    ctrls = ctrls.T
    ctrls.columns = ['Special Equipment','Special Equipment Desc', 'Medical Surveillance', 'BSL']
    ctrls = ctrls[1:]
    ctrls.index = [bua.name]
    for i in range(len(ctrls.columns)):
        ctrls[ctrls.columns[i]][0] = ctrls[ctrls.columns[i]][0].replace(';','.')

    ack = bua.tables[index+1].copy()               
    ack = ack.T
    odds = [1,3,5,7,9,11]
    for od in odds: 
        del ack[od]
    ack.columns = ["Bleach_Decon_Ack", "Bio_Label_Ack", "BBP_Ack", "Injury_Report_Ack", "Shipment_Ack", "BioWaste_Ack", "FOIA_Ack", "Suspension_Ack", "Final_Ack"]
    ack = ack[1:]
    ack.index = [bua.name]

    df = ctrls.join(ack)
    bua.data['basic'] = bua.data['basic'].join(df)


    # risks are human, plants, rDNA, inverts, animals, stem cells, transgenic plants
def get_risk_qs(bua, risk_name, index):
    df = bua.tables[index].copy()

    if risk_name == 'stem cells':
        df.index = [bua.name]
        return df
    else:
        # add the risk name to the column label
        df = format_bua_table(df)
        del df[0]
        df.index = [bua.name]
        if risk_name == 'plants':
            return label_plant_qs(df)
        elif risk_name == 'animals':
            return label_animal_qs(df)
        else:
            return df


def get_risk_list(bua, index):
    df = bua.tables[index].copy()
    df['id'] = bua.name
    return df


def format_bua_table(table):
    # Transpose so indexes are now columns, reset indexes, and then make
    # the first column is the header
    table = table.T
    table = table.reset_index()
    header = table.iloc[0]
    table.columns = header
    table = table[1:]
    return table

def label_plant_qs(df):
    df.columns = ['Exotic Infectious Agents',
                  'Exotic Infectious Agents Precautions',
                  'Tg Exotic Organisms',
                  'Tg Exotic Organisms Precautions',
                  'Tg Serious Detrimental Impact',
                  'Tg Serious Detrimental Impact Precautions',
                  'Tg Animals or Arthropods',
                  'Tg Animals or Arthropods Description',
                  'Tg Microbes in Arthropods',
                  'Tg Microbes in Arthropods Descriptione',
                  'Tg Microbes in Arthropods Negative Impact',
                  'Tg Microbes in Arthropods Negative Impact Precutions']
    return df

def label_animal_qs(df):
    df.columns = ['Human NHP Cells in Animals',
                  'Infectious Agents in Animals',
                  'Infectious Agents in Animals Precautions',
                  'Shedding Infectious Agents',
                  'Shedding Time Length',
                  'Wild Caught Animals',
                  'Potential Zoonotic Disease',
                  'Potential Zoonotic Disease Precautions']
    return df

