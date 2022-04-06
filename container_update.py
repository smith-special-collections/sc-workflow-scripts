from archivesspace import archivesspace
import argparse
import logging
import csv
import pprint


if __name__ == "__main__":

    CONFIGFILE = "archivesspace.cfg"

    argparser = argparse.ArgumentParser()
    argparser.add_argument("SERVERCFG", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'recording'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
    argparser.add_argument("CSVFILE", default="DEFAULT", help="Path to CSV file for parsing.")
    cliArguments = argparser.parse_args()

    aspace = archivesspace.ArchivesSpace()
    aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
    aspace.connect()


    with open(cliArguments.CSVFILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = aspace.get(row['container_uri'])
            record['indicator'] = row['indicator']
            try:
                post = aspace.post(record['uri'], record)
                print('Successful update for {}'.format(post['uri']))
            except:
                print('Failed update for {}'.format(row['container_uri']))
