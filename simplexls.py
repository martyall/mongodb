#This script reads in a particular xls data sheet containing
#information about coastal something relative to time. 
#the xlrd module docs are kind of shit, so let this be an example. 


import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


from datetime import datetime

def open_zip(datafile):
    with Zipfile('{0}.zip'.format(datatfile), 'r') as myzip:
        myzip.extractall()

def find_date_by_val(l, val):
    l1 = filter(lambda x: val in x.values(), l) 
    return l1[0]['Hour_End']

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile) #opens excel file for load
    sheet = workbook.sheet_by_index(0) #returns an object of the sheet class 
    #representing sheet number 0
    sheet_data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    keys = sheet_data[0]
    sheet_data.pop(0)
    for i in range(0,len(sheet_data)):
        for j in range(len(sheet_data[i])):
            if j == 0:
                sheet_data[i][j] = datetime(*xlrd.xldate_as_tuple(sheet_data[i][j],1))
            else:
                sheet_data[i][j] = float(sheet_data[i][j])
        sheet_data[i] = dict(zip(keys, sheet_data[i]))
    values = [x[u'COAST'] for x in sheet_data]
    dates = map(lambda x: x.get('Hour_End'), sheet_data)
    maxvalue = max(values)
    print maxvalue
    minvalue = min(values)
    
    data = {
        'maxtime': find_date_by_val(sheet_data,maxvalue),
        'maxvalue': maxvalue,
        'mintime': find_date_by_val(sheet_data, minvalue),
        'minvalue': min(values),
        'avgcoast': 1.0/len(values)*sum(values)
    }
    return data

        
        
    
    
