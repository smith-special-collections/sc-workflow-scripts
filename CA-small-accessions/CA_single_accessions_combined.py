import CA_single_accessions_makeagents
import CA_single_post_accessions
import CA_single_post_archival_objects
#import mint_accession_id.mint_accession_id as mint_accession_id
#from nonotuck_file_manipulation import map_file_data, reorganize_files, make_drive_id_index_file, parse_drive_id_index

from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

# for debugging, remove
from pprint import pprint
import pickle
import pdb

#from nonotuck_config import Config
#config = Config()


ASPACE_REPO_CODE = 'A'
ASPACE_REPO_NUMBER = 4

logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# def make_transfer_office(row, aspace):
#     if len(row['transfer_office_uri']) == 0:
#         record = CA_single_accessions_makeagents.make_transfer_office_record(row)
#         try:
#             post = aspace.post('/agents/corproate_entities', record)
#             logging.info('Agent record created for {}'.format(row['transfer_office'] + ' URI: ' + post['uri']))
#             transfer_office_uri = post['uri']
#         except Exception as e:
#             logging.warning('Failure to create agent record for {}: {}'.format(row['transfer_office'], e))
#             transfer_office_uri = None
#     else:
#         transfer_office_uri = row['transfer_office_uri']

def make_donor_agent(row, aspace):
    # If there is not an agent_id make an agent
    if len(row['donor_uri']) == 0 and row['donor_type'] == 'person':
        # Create person donor agent
        print('No donor URI')
        record = CA_single_accessions_makeagents.make_person_agent_record(row)
        try:
            post = aspace.post('/agents/people', record)
            logging.info('Agent record created for {}'.format(row['donor_lastname'] + ' URI: ' + post['uri']))
            donor_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create agent record for {}: {}'.format(row['donor_lastname'], e))
            donor_uri = None
    elif len(row['donor_uri']) == 0 and row['donor_type'] == 'corporate':
        record = CA_single_accessions_makeagents.make_corporate_agent_record(row)
        try:
            post = aspace.post('/agents/corporate_entities', record)
            logging.info('Agent record created for {}'.format(row['donor_lastname'] + ' URI: ' + post['uri']))
            donor_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create agent record for {}: {}'.format(row['donor_lastname'], e))
            donor_uri = None
    # Otherwise just get it from the spreadsheet
    else:
        donor_uri = row['donor_uri']

    return donor_uri

def make_creator_agent(row, aspace):
    # If there is not an agent_id make an agent
    if len(row['creator_uri']) == 0 and row['creator_type'] == 'person':
        # Create person donor agent
        record = CA_single_accessions_makeagents.make_person_creator_record(row)
        try:
            post = aspace.post('/agents/people', record)
            logging.info('Agent record created for {}'.format(row['creator_lastname'] + ' URI: ' + post['uri']))
            creator_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create agent record for {}: {}'.format(row['creator_lastname'], e))
            creator_uri = None
    elif len(row['creator_uri']) == 0 and row['creator_type'] == 'corporate':
        try:
            post = aspace.post('/agents/corproate_entities', record)
            logging.info('Agent record created for {}'.format(row['creator_lastname'] + ' URI: ' + post['uri']))
            creator_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create agent record for {}: {}'.format(row['creator_lastname'], e))
            creator_uri = None
    # Otherwise just get it from the spreadsheet
    else:
        creator_uri = row['creator_uri']

    return creator_uri

def make_accession(row, donor_uri, creator_uri):
    record = CA_single_post_accessions.make_accession(row, donor_uri, creator_uri)
    try:
        post = aspace.post('/repositories/4/accessions', record)
        logging.info('Accession record created for {}'.format(row['donor_lastname'] + " New URI: " + post['uri']))
        return record
    except Exception as e:
        logging.warning('Failure to create accession record for {}: {}'.format(row['donor_lastname'], e))
        return None

def make_archival_object(row, donor_uri, creator_uri, aspace):
    archival_object_record = CA_single_post_archival_objects.make_archival_object(row, donor_uri, creator_uri)
    try:
        post = aspace.post('/repositories/4/archival_objects', archival_object_record)
        logging.info('Archival object record created for {}'.format(row['donor_lastname'] + " New URI: " + post['uri']))
    except Exception as e:
        logging.warning('Failure to create archival object record for {}: {}'.format(row['donor_lastname'], e))


if __name__ == "__main__":
    CONFIGFILE = "archivesspace.cfg"

    argparser = argparse.ArgumentParser()
    argparser.add_argument("SERVERCFG", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'testing'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
    argparser.add_argument("CSVname", default="DEFAULT", help="Name of the CSV spreadsheet, e.g, 'duplaix.csv. Note: It must be in the same directory as this code file.")
    cliArguments = argparser.parse_args()

    aspace = archivesspace.ArchivesSpace()
    aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
    aspace.connect()

    logging.basicConfig(level=logging.INFO)

    csv_filename = cliArguments.CSVname


    # Reads CSV file
    with open(csv_filename, encoding="utf8", errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)

        report = {}
        for row in csvreader:
                donor_uri = make_donor_agent(row, aspace)
                if donor_uri is None:
                    logging.error(f"No agent created or found, skipping this record! {row['donor_lastname']}")
                    continue # Go back to the top of the loop
                creator_uri = make_creator_agent(row, aspace)
#                if row['transfer_office'] != None:
#                    transfer_office_uri = make_transfer_office(row, aspace)
#                else:
#                    transfer_office_uri = None
                record = make_accession(row, donor_uri, creator_uri)
                archival_object_record = make_archival_object(row, donor_uri, creator_uri, aspace)
#                if record is not None:
                    # Keep a local mirror of the state of accession records on the AS
                    # side, so that get_unique_accession_id() is working with
                    # up to date information, without having to query the server
                    # which is slooooow.
                    #all_accessions_data.append(record)
                    # ### Do file manipulation
                    # # Map google drive URLs to filenames and paths in the synced
                    # # drive folder
                    # submission_file_data = map_file_data(row, drive_id_index, accession_id)
                    # # Now copy the files into a desired human friendly structure
                    # # in the working directory
                    # reorganize_files(submission_file_data, config.working_dir)

        pprint(report)
