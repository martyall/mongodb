#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import re

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]


def is_number(s):
    try:
        return type(1.1) == type(float(s))
    except ValueError:
        return False

def convert_to_num(s):
    if re.search(r'\.', s):
        return float(s)
    else:
        return int(s)
    
def audit_file(filename, fields):
    fieldtypes = {}
    global FIELDS
    for field in FIELDS:
        fieldtypes[field] = set([])
    # YOUR CODE HERE
    with open(filename) as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for i in range(3):
            reader.next()
        for row in reader:
            for field in FIELDS:
                val = row[field]
                if field == "point":
                 #   x = True
                    print val
                #else:
                 #   x = False
                if val == "" or val == "NULL":
                    fieldtypes[field].add(type(None))
                  #  if x:
                   #     print row[field], type(None)
                    #    print "\n"
                    continue
                elif is_number(val):
                    fieldtypes[field].add(type(convert_to_num(val)))
                    #if x:
                     #   print row[field], type(convert_to_num(val))
                      #  print "\n"
                    continue
                #elif re.search(r'')
                elif val[0] == "{":
                    fieldtypes[field].add(type([1,2,3]))
                    #if x:
                     #   print row[field],  type([1,2,3])
                      #  print "\n"
                    continue
                else:
                    fieldtypes[field].add(type("s"))
                    #if x:
                       # print row[field], type("s")
                        #print "\n"

    #print "fieldtypes:", fieldtypes
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
