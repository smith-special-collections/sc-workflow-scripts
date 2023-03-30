from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

ID_ZERO_PADDING = 4



DATE = datetime.date.today()
DATE = DATE.__str__()


def make_event(row, accession_uri):
    event_dict = {'event_type':'accession',
                 'jsonmodel_type':'event',
                 'linked_agents': [{'role': 'implementer',
                                  'ref': '/agents/people/43031'}],
                 'linked_records': [{'role': 'source',
                                  'ref': accession_uri}],
                 'date': {'jsonmodel_type':'date',
                 'date_type':'single',
                 'label': 'creation',
                 'era': 'ce',
                 'calendar': 'gregorian',
                 'begin': row['acc_date']}
                 }

    return event_dict

def create_event_records(aspace, csvreader):
    """Takes a csvreader object. Iterates through it and creates the events listed."""
    events = []
    for row in csvreader:
        record = make_event(row)
        try:
            post = aspace.post('/repositories/4/events', record)
            logging.info('Event record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
        except Exception as e:
            logging.warning('Failure to create event record for {}: {}'.format(row['full_name'], e))


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
        events = create_event_records(aspace, csvreader)
    from pprint import pprint
    pprint(events)
