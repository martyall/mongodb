#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint
import re

CITIES = 'cities.csv'


def fix_area(area):
    num_list_re = re.compile(r'([0-9]+\.?.*)\|([0-9]+\.?[^}]*)')
    float_re = re.compile(r'[0-9]+\..*')
    
    if area == "NULL" or area == "":
        return None
    
    elif num_list_re.search(area):
        n1_digs, n2_digs = None, None
        sig_digs_re = re.compile(r'(\.)([0-9]+)') 
        n1 = num_list_re.search(area).group(1)
        if sig_digs_re.search(n1):
            n1_digs = sig_digs_re.search(n1).group(2)
        n2 = num_list_re.search(area).group(2)
        if sig_digs_re.search(n2):
            n2_digs = sig_digs_re.search(n2).group(2)
        #print n1, n1_digs
        #print n2, n2_digs
        if not n1_digs:
            if not n2_digs: #then they are both ints, return the first one:
                return int(n1)
            else: #n2 has digs, but not n1:
                return float(n2)
        else: # n1 has digs
            if not n2_digs: 
                return float(n1)
            else: # they both have digs
                if len(n1_digs) >= len(n2_digs): #n1 hass more sig digs
                    return float(n1)
                else:
                    return float(n2) #n2 has more sig digs
    
    elif float_re.search(area):
        return float(area)
    
    else:
        return int(area)
            



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None        
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0    


if __name__ == "__main__":
    test()
