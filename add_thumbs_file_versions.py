from archivesspace import archivesspace
import argparse
import logging
import csv
import pprint

#This script was edited from one Claire Marshall wrote to edit Archival Objects. It has been edited to instead edit digital objects. It adds a new file version to existing digital objects. It assumes you want the new file versions to be published.

#Requires as input a csv file with the following columns: digitalobject_uri and file_uri_csv.

#This script requires the ArchivesSpace module written by Tristan Chambers to run.

#Defining the JSON for the added file version.
def add_file_version(file_uri_csv):
    note_dict =  {'file_uri': file_uri_csv,
    'publish': True, #change to False if you do not want the file version to be published.
    'xlink_actuate_attribute': 'onLoad',
    'xlink_show_attribute': 'embed',
    'use_statement': 'image-thumbnail',
    'jsonmodel_type': 'file_version'
    }

    return note_dict

#authentication stuff
if __name__ == "__main__":

    CONFIGFILE = "archivesspace.cfg"

    argparser = argparse.ArgumentParser()
    argparser.add_argument("SERVERCFG", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'recording'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
    argparser.add_argument("CSVFILE", default="DEFAULT", help="Path to CSV file for parsing.")
    cliArguments = argparser.parse_args()

    aspace = archivesspace.ArchivesSpace()
    aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
    aspace.connect()

#opening the csv file, getting the existing digital object, adding the file version
    with open(cliArguments.CSVFILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print (row.keys())

            record = aspace.get(row['digitalobject_uri'])
            if not len(str(row['file_uri_csv'])) == 0:
                new_file_version = add_file_version(row['file_uri_csv'])
                record['file_versions'].append(new_file_version)

#repost the digital object that you just updated
            try:
                post = aspace.post(record['uri'], record)
                print('Successful update for {}'.format(post['uri']))
            except:
                print('Failed update for {}'.format(row['digitalobject_uri']))
