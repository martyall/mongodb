"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import time
import re


INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'


def get_year(t):
    try:
        time_obj = time.strptime(t, "%Y-%m-%dT%H:%M:%S+02:00")
    except ValueError:
        return None
    year = time_obj.tm_year 
    return year 


def process_file(input_file, output_good, output_bad):
    re_db = re.compile(r'dbpedia.org')
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        with open(output_good, "w") as good:
            good_writer = csv.DictWriter(good, header)
            good_writer.writeheader()
            with open(output_bad, "w") as bad:
                bad_writer = csv.DictWriter(bad, header)
                bad_writer.writeheader()
                for row in reader:
                    if re_db.search(row["URI"]):
                        year = get_year(row["productionStartYear"])
                        #print year
                        if year <= 2014 and year >= 1886:
                            good_writer.writerow(row)
                            #print "good"
                        else:
                            bad_writer.writerow(row)
                            #print "bad"
                          

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)

    with open(OUTPUT_GOOD) as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = get_year(row["productionStartYear"])
            print year <= 2014 and year >= 1886

if __name__ == "__main__":
    test()
