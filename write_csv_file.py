# Loops over iterable (list) and writes data to CSV file

import sys
import csv

def write_data(csv_file, content):
    """Write data to a CSV file
       csv_file = CSV file to write data to
       content = iterable content to loop over and write to csv file"""
    try:
        # write content to csv file
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f, dialect='excel', delimiter=',', lineterminator='\n')
            # iterate over data
            for item in content:
                # write content to csv file
                writer.writerow(item)
    except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        # TODO: generate file name through code logic
        print('error at Line {} in "write_csv_file.py"'.format(tbE.tb_lineno))
        # Write the error print( to the log file
        print('error: {}'.format(str(e)))