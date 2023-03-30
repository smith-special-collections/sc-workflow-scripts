from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv




DATE = datetime.date.today()
DATE = DATE.__str__()


def make_accession(accession, donor_uri, creator_uri):
    
    #Accession number, getting the right number of digits
    if len(accession['acc_id_2']) == 1:
        id_2 = str('000') + str(accession['acc_id_2'])
    elif len(accession['acc_id_2']) == 2:
        id_2 = str('00') + str(accession['acc_id_2'])
    elif len(accession['acc_id_2']) == 3:
        id_2 = str('0') + str(accession['acc_id_2'])

    if len(accession['acc_id_3']) == 1:
        id_3 = str('000') + str(accession['acc_id_3'])
    elif len(accession['acc_id_3']) == 2:
        id_3 = str('00') + str(accession['acc_id_3'])
    elif len(accession['acc_id_3']) == 3:
        id_3 = str('0') + str(accession['acc_id_3'])

    acc_dict = {'jsonmodel_type':'accession',
                 'publish': False,
                 'provenance': accession['acq'],
                 'title': accession['acc_title'],
                 'id_0': str(accession['acc_id_0']),
                 'id_1': str(accession['acc_id_1']),
                 'id_2': id_2,
                 'id_3': id_3,
                 'acquisition_type': accession['acc_type'].lower(),
                 'use_restrictions_note': accession['use'],
                 'related_resources':[{'ref':accession['resource_uri']}]
                 }

    #Accession date
    if len(accession['acc_date']) == 4:
        acc_dict['accession_date'] = accession['acc_date'] + "-01-01"
    elif len(accession['acc_receipt_date']) == 7:
        acc_dict['accession_date'] = accession['acc_date'] + "-01"
    else:
        acc_dict['accession_date'] = accession['acc_date']

    # Access restrictions
    if len(accession['access']) == 0:
        acc_dict['access_restrictions'] = False
    else:
        acc_dict['access_restrictions'] = True
        acc_dict['access_restrictions_note'] = accession['access']

    #Scope and scopecontent
    if len(accession['acc_desc']) > 0:
        acc_dict['content_description'] = accession['acc_desc']

    # Restrictions apply checkbox
    if acc_dict['access_restrictions'] == True:
        acc_dict['restrictions_apply'] = True
    else:
        acc_dict['restrictions_apply'] = False

    # Add donor agent as source
    acc_dict['linked_agents'] = []

    if len(accession['donor_lastname']) > 0 and accession['donor_type'] == 'person':
        linked_agent = {}
        linked_agent['role'] = 'source'
        if accession['acc_type'].lower() == 'gift':
            linked_agent['relator'] = 'dnr'
        linked_agent['ref'] = donor_uri
        try:
            acc_dict['linked_agents'].append(linked_agent)
        except KeyError:
            logging.error ('issue with linked agent', KeyError)
            
    if len(accession['donor_lastname']) > 0 and accession['donor_type'] == 'corporate':
        linked_agent_transfer = {}
        linked_agent_transfer['role'] = 'source'
        if accession['acc_type'].lower() == 'gift':
            linked_agent_transfer['relator'] = 'dnr'
        linked_agent_transfer['ref'] = donor_uri
        try:
            acc_dict['linked_agents'].append(linked_agent_transfer)
        except KeyError:
            logging.error ('issue with creator linked agent', KeyError)
    
    if len(accession['creator_lastname']) > 0:
        linked_agent_creator = {}
        linked_agent_creator['role'] = 'creator'
        linked_agent_creator['ref'] = creator_uri
        try:
            acc_dict['linked_agents'].append(linked_agent_creator)
        except KeyError:
            logging.error ('issue with creator linked agent', KeyError)
#Accounting for cases where the donor is the same as the creator.
    elif len(accession['donor_same_as_creator']) > 0:
        linked_agent_creator = {}
        linked_agent_creator['role'] = 'creator'
        linked_agent_creator['ref'] = donor_uri
        try:
            acc_dict['linked_agents'].append(linked_agent_creator)
        except KeyError:
            logging.error ('issue with creator linked agent', KeyError)

    if len(accession['donation_info']) > 0:
        acc_dict['general_note'] = accession['donation_info']

#adding in the stuff for extent and date
    # Extents
    acc_dict['extents'] = []
    extent_dict = {}
    extent_dict['jsonmodel_type'] = 'extent'
    try:
        extent_dict['extent_type'] = 'linear feet'
    except Exception as e:
        logging.error(e)
    try:
        extent_dict['number'] = str(accession['extent'])
    except Exception as e:
        logging.error(e)
    try:
        extent_dict['portion'] = 'whole'
    except Exception as e:
        logging.error(e)

    # Ensures extents array has all the required fields, otherwise an error will be raised when trying to post
    if len(extent_dict) > 3:
        acc_dict['extents'].append(extent_dict)

    # Date field
    acc_dict['dates'] = []
    create_date_dict = {}

    if len(accession['cr_date_end']) > 0 and len(accession['cr_date_begin']) > 0:
        create_date_dict['end'] = accession['cr_date_end']
        create_date_dict['begin'] = accession['cr_date_begin']
        create_date_dict['date_type'] = 'inclusive'
        create_date_dict['calendar'] = 'gregorian'
        create_date_dict['era'] = 'ce'
        create_date_dict['label'] = 'creation'
        if accession['cr_date_certainty'] != None:
            create_date_dict['certainty'] = accession['cr_date_certainty']
        create_date_dict['jsonmodel_type'] = 'date'
        acc_dict['dates'].append(create_date_dict)
    elif len(accession['cr_date_end']) == 0 and len(accession['cr_date_begin']) > 0:
        create_date_dict['begin'] = accession['cr_date_begin']
        create_date_dict['date_type'] = 'single'
        create_date_dict['calendar'] = 'gregorian'
        create_date_dict['era'] = 'ce'
        create_date_dict['label'] = 'creation'
        if accession['cr_date_certainty'] != None:
            create_date_dict['certainty'] = accession['cr_date_certainty']
        create_date_dict['jsonmodel_type'] = 'date'
        acc_dict['dates'].append(create_date_dict)
#End adding in for extent and date

    #Receipt date
    if len(accession['acc_receipt_date']) >= 4:
        recept_date_dict = {}
        if len(accession['acc_receipt_date']) == 4:
            recept_date_dict['begin'] = accession['acc_receipt_date'] + "-01-01"
        elif len(accession['acc_receipt_date']) == 7:
            recept_date_dict['begin'] = accession['acc_receipt_date'] + "-01"
        else:
            recept_date_dict['begin'] = accession['acc_receipt_date']
            recept_date_dict['date_type'] = 'single'
            recept_date_dict['calendar'] = 'gregorian'
            recept_date_dict['era'] = 'ce'
            recept_date_dict['label'] = 'receipt'
            recept_date_dict['jsonmodel_type'] = 'date'
            acc_dict['dates'].append(recept_date_dict)

    return acc_dict

def create_accession_records(aspace, csvreader):
    accessions = []
    for row in csvreader:
        accession_record = make_accession(row)
        try:
            post = aspace.post('/repositories/4/accessions', accession_record)
            logging.info('Accession record created for {}'.format(row['donor_lastname'] + " New URI: " + post['uri']))
            #Attempting to get accession URI
            accession_uri = post['uri']
        except Exception as e:
            logging.warning('Failure to create accession record for {}: {}'.format(row['donor_lastname'], e))
 #2022-12-20 Trying to get the accession uris to link
    return accessions, accession_uri
    row.append(accessions)


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
        accessions = create_accession_records(aspace, csvreader)
    from pprint import pprint
    pprint(accessions)
