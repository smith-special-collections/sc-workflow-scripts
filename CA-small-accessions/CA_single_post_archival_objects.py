from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

ID_ZERO_PADDING = 4



DATE = datetime.date.today()
DATE = DATE.__str__()


def make_archival_object(row, donor_uri, creator_uri, accession_uri):
    ao_dict = {'jsonmodel_type':'archival_object',
                 'publish': True,
                 'title': row['acc_title'],
                 'level': 'file',
                 'resource': {'ref':row['resource_uri']},
                 'accession_links': [{'ref': accession_uri}]
                 }

    # Adding the collection as its parent object
    ao_dict['ancestors'] = []
    ancestors = {}
    ancestors['ref'] = row['resource_uri']
    ancestors['level'] = 'collection'
    try:
        ao_dict['ancestors'].append(ancestors)
    except KeyError:
        logging.error ('issue with ancestors', KeyError)

    ao_dict['dates'] = []
    date_dict = {}
    if len(row['cr_date_end']) > 0 and len(row['cr_date_begin']) > 0:
        date_dict['end'] = row['cr_date_end']
        date_dict['begin'] = row['cr_date_begin']
        date_dict['date_type'] = 'inclusive'
        date_dict['calendar'] = 'gregorian'
        date_dict['era'] = 'ce'
        date_dict['label'] = 'creation'
        if row['cr_date_certainty'] != None:
            date_dict['certainty'] = row['cr_date_certainty']
        date_dict['jsonmodel_type'] = 'date'
        ao_dict['dates'].append(date_dict)
    elif len(row['cr_date_end']) == 0 and len(row['cr_date_begin']) > 0:
        date_dict['begin'] = row['cr_date_begin']
        date_dict['date_type'] = 'single'
        date_dict['calendar'] = 'gregorian'
        date_dict['era'] = 'ce'
        date_dict['label'] = 'creation'
        if row['cr_date_certainty'] != None:
            date_dict['certainty'] = row['cr_date_certainty']
        date_dict['jsonmodel_type'] = 'date'
        ao_dict['dates'].append(date_dict)


    # Notes
    ao_dict['notes'] = []
    if len(row['acc_desc']) > 0:
        sc_note = {}
        sc_note['jsonmodel_type'] = 'note_multipart'
        sc_note['publish'] = True
        sc_note['type'] = 'scopecontent'
        sc_note['subnotes'] = []
        sc_subnote = {}
        sc_subnote['jsonmodel_type'] = 'note_text'
        sc_subnote['content'] = row['acc_desc']
        sc_subnote['publish'] = True
        try:
            sc_note['subnotes'].append(sc_subnote)
        except KeyError:
            logging.error ('issue with sc subnote', KeyError)
        try:
            ao_dict['notes'].append(sc_note)
        except KeyError:
            logging.error ('issue with sc note', KeyError)

    if len(row['use']) > 0:
        userestrict_note = {}
        userestrict_note['jsonmodel_type'] = 'note_multipart'
        userestrict_note['publish'] = True
        userestrict_note['rights_restriction'] = {}
        userestrict_note['local_access_restriction_type'] = []
        userestrict_note['type'] = 'userestrict'
        userestrict_note['subnotes'] = []
        userestrict_subnote = {}
        userestrict_subnote['jsonmodel_type'] = 'note_text'
        userestrict_subnote['publish'] = True
        userestrict_subnote['content'] = row['use']
        # Use Restrictions Note
        try:
            userestrict_note['subnotes'].append(userestrict_subnote)
        except KeyError:
            logging.error ('issue with userestrict subnote', KeyError)
        try:
            ao_dict['notes'].append(userestrict_note)
        except KeyError:
            logging.error ('issue with userestrict note', KeyError)

#Adding immediate source of acquisition
    if len(row['acq']) > 0:
        acq_note = {}
        acq_note['jsonmodel_type'] = 'note_multipart'
        acq_note['publish'] = True
        acq_note['type'] = 'acqinfo'
        acq_note['subnotes'] = []
        acq_subnote = {}
        acq_subnote['jsonmodel_type'] = 'note_text'
        acq_subnote['publish'] = True
        acq_subnote['content'] = row['acq']
        try:
            acq_note['subnotes'].append(acq_subnote)
        except KeyError:
            logging.error ('issue with userestrict subnote', KeyError)
        try:
            ao_dict['notes'].append(acq_note)
        except KeyError:
            logging.error ('issue with acq note', KeyError)

    # Access restrictions note
    if len(row['access']) > 0:
        new_restriction = {'jsonmodel_type': 'note_multipart',
            'publish': True,
            'rights_restriction': {},
            'subnotes': [{'content': row['access'],
                          'jsonmodel_type': 'note_text',
                          'publish': True}],
            'type': 'accessrestrict'}
        try:
            ao_dict['notes'].append(new_restriction)
        except KeyError:
            logging.error ('issue with accessrestrict note', KeyError)

    if len(row['creator_lastname']) > 0 or len(row['donor_lastname']) > 0:
        ao_dict['linked_agents'] = []

        if len(row['creator_lastname']) > 0:
            linked_agent_creator = {}
            linked_agent_creator['role'] = 'creator'
            linked_agent_creator['ref'] = creator_uri
            try:
                ao_dict['linked_agents'].append(linked_agent_creator)
            except KeyError:
                logging.error ('issue with creator linked agent creator', KeyError)

        if len(row['donor_lastname']) > 0:
            linked_agent_source = {}
            linked_agent_source['role'] = 'source'
            linked_agent_source['ref'] = donor_uri
            if row['acc_type'].lower() == 'gift':
                linked_agent_source['relator'] = 'dnr'
            try:
                ao_dict['linked_agents'].append(linked_agent_source)
            except KeyError:
                logging.error ('issue with creator linked agent source', KeyError)


    if len(row['top_container_uri']) > 0:
        ao_dict['instances'] = []
        instance = {}
        instance['instance_type'] = 'mixed_materials'
        instance['jsonmodel_type'] = 'instance'
        instance['is_representative'] = False
        instance['sub_container'] = {'jsonmodel_type': 'sub_container',
        'top_container': {'ref': row['top_container_uri']}}
        try:
            ao_dict['instances'].append(instance)
        except KeyError:
            logging.error ('issue with instance', KeyError)


    return ao_dict

def create_archival_object_records(aspace, csvreader):
    """Takes a csvreader object. Iterates through it and creates the archival objects listed."""
    archival_objects = []
    for row in csvreader:
        record = make_archival_object(row)
        try:
            post = aspace.post('/repositories/4/archival_objects', record)
            logging.info('Archival object record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
        except Exception as e:
            logging.warning('Failure to create archival object record for {}: {}'.format(row['full_name'], e))

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
        archival_objects = create_archival_object_records(aspace, csvreader)
    from pprint import pprint
    pprint(archival_objects)
