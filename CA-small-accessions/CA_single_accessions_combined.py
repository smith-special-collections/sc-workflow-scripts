import CA_single_accessions_makeagents
import CA_single_post_accessions
import CA_single_post_archival_objects
import CA_single_post_events

from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

# for debugging, remove
from pprint import pprint
import pickle
import pdb

ASPACE_REPO_CODE = 'A'
ASPACE_REPO_NUMBER = 4

logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def make_donor_agent(row, aspace):
    # If there is not an agent_id make an agent
    if len(row['donor_uri']) == 0 and row['donor_type'] == 'person':
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
        record = CA_single_accessions_makeagents.make_corporate_creator_record(row)
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
        accession_uri = post['uri']
    except Exception as e:
        logging.warning('Failure to create accession record for {}: {}'.format(row['donor_lastname'], e))
        return None

def make_archival_object(row, donor_uri, creator_uri, accession_uri, aspace):
    archival_object_record = CA_single_post_archival_objects.make_archival_object(row, donor_uri, creator_uri, accession_uri)
    try:
        post = aspace.post('/repositories/4/archival_objects', archival_object_record)
        logging.info('Archival object record created for {}'.format(row['donor_lastname'] + " New URI: " + post['uri']))
    except Exception as e:
        logging.warning('Failure to create archival object record for {}: {}'.format(row['donor_lastname'], e))

def make_event(row, accession_uri, aspace):
    event_record = CA_single_post_events.make_event(row, accession_uri)
    try:
        post = aspace.post('/repositories/4/events', event_record)
        logging.info('Event record created for {}'.format(row['donor_lastname'] + " New URI: " + post['uri']))
    except Exception as e:
        logging.warning('Failure to create event record for {}: {}'.format(row['donor_lastname'], e))       

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
                if len(row['donor_same_as_creator']) > 0:
                    creator_uri = donor_uri
                else:
                    creator_uri = make_creator_agent(row, aspace)
                record = make_accession(row, donor_uri, creator_uri)
                record_json = record[0]
                accession_uri = record[1]
                archival_object_record = make_archival_object(row, donor_uri, creator_uri, accession_uri, aspace)
                event_record = make_event(row, accession_uri, aspace)


        pprint(report)
