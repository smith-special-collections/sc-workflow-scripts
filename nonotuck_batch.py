import post_agents
import post_accessions_concat
import mint_accession_id.mint_accession_id as mint_accession_id

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

def make_agent(row, aspace):
    # If there is not an agent_id make an agent
    if len(row['agent_id']) == 0:
        # Create agents
        record = post_agents.make_agent_record(row)
        try:
            post = aspace.post('/agents/people', record)
            logging.info('Agent record created for {}'.format(row['full_name'] + ' URI: ' + post['uri']))
            agent_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create agent record for {}: {}'.format(row['full_name'], e))
            agent_uri = None
    # Otherwise just get it from the spreadsheet
    else:
        agent_uri = '/agents/people/' + row['agent_id']

    return agent_uri

def make_accession(row, agent_uri, aspace):
    record = post_accessions_concat.make_accession(row, agent_uri, accession_id)
    try:
        post = aspace.post('/repositories/4/accessions', record)
        logging.info('Accession record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
        return record
    except Exception as e:
        logging.warning('Failure to create accession record for {}: {}'.format(row['full_name'], e))
        return None

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

    # Get a list of all current accessions from ASpace so that we can generate
    # new accession IDs from the list of existing ones.
    # Do this query once at the beginning of this loop for performance
    logging.info("Fetching list of all accessions for making accession IDs")
    all_accessions_data = aspace.getPaged(f"/repositories/{ASPACE_REPO_NUMBER}/accessions")
    # all_accessions_data = pickle.load(open('accessions1109.pickle', 'rb'))

    # Reads CSV file
    with open(csv_filename, encoding="utf8", errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)

        report = {}
        for row in csvreader:
            logging.error(row['full_name'])
            if row['nanci_checkB1'] == 'TRUE' and row['nanci_checkB2'] == 'TRUE' and row['nanci_checkA'] == 'TRUE':
                agent_uri = make_agent(row, aspace)
                if agent_uri is None:
                    logging.error(f"No agent created or found, skipping this record! {row['full_name']}")
                    continue # Go back to the top of the loop
                # First, get ourselves and ID
                accession_id = mint_accession_id.get_unique_accession_id(aspace, ASPACE_REPO_NUMBER, ASPACE_REPO_CODE, all_accessions_data)
                record = make_accession(row, agent_uri, aspace)
                if record is not None:
                    # Keep a local mirror of the state of accession records on the AS
                    # side, so that get_unique_accession_id() is working with
                    # up to date information, without having to query the server
                    # which is slooooow.
                    all_accessions_data.append(record)
                pdb.set_trace()
    pprint(report)
