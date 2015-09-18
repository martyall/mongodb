#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'
import re

m = re.compile(r'xml[\s]version')

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()

def get_new_lines(filename):
    new_lines = []
    with open(filename) as f:
        i = 0
        for line in f: 
            if m.search(line):
                new_lines.append(i)
            else:
                pass
            i += 1
    new_lines.append(i)
    return new_lines


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
    new_lines = get_new_lines(filename)
    print new_lines
    with open(filename) as f:
        for n in range(len(new_lines)-1):
            new_file_name = "{}-{}".format(filename, n)
            print new_file_name
            with open(new_file_name, 'w+') as g:
                i = new_lines[n]
                while i < new_lines[n+1]:
                    line = f.readline()
                    g.write(line)
                    i += 1

def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()
