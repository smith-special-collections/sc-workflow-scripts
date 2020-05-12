from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv




DATE = datetime.date.today()
DATE = DATE.__str__()

#translates the status of the person into the appropriate classification link
AFFILIATION_DICT = {
    'faculty': '/repositories/4/classification_terms/186',
    'staff': '/repositories/4/classifications/10',
    'student class of 2020': '/repositories/4/classification_terms/401',
    'student class of 2021': '/repositories/4/classification_terms/402',
    'student class of 2022': '/repositories/4/classification_terms/403',
    'student class of 2023': '/repositories/4/classification_terms/404'
    }

provenance_string1 = 'Received from'
provenance_string2 = 'as part of the Covid-19 Chronicles project.'
title_string = 'Covid-19 digital materials'

def make_accession(accession, agent_uri, accession_id):

    dateformat = datetime.datetime.strptime(str(accession['timestampB']), '%m/%d/%y  %H:%M')
    full_name = accession['full_name']
    gen_note_aff = accession['affiliation']
    gen_note_living = accession['where_living']
    acc_dict = {'jsonmodel_type':'accession',
                 'publish': False,
                 'provenance': f"{provenance_string1} {full_name} {provenance_string2}",
                 'title': f"{full_name} {title_string}",
                 'general_note': f"{gen_note_aff}; {gen_note_living}.",
                 'id_0': str(accession_id['id_0']),
                 'id_1': str(accession_id['id_1']),
                 'id_2': str(accession_id['id_2']),
                 'acquisition_type': 'gift',
                 'resource_type': 'papers',
                 'accession_date': str(dateformat.date()),
                 'subjects':[{'ref':'/subjects/6201'}],
                 'related_resources':[{'ref':'/repositories/4/resources/1630'}] #Adds the subject "electronic records"
                 }

    for key in AFFILIATION_DICT.keys():
        if key == accession['affiliation'].lower().strip():
            affiliation = AFFILIATION_DICT[key]

    acc_dict['classifications'] = []
    classification = {}
    classification['ref'] = affiliation

    try:
         acc_dict['classifications'].append(classification)
    except KeyError:
         logging.error ('issue with affiliation', KeyError)


    # Content Description
    if accession['content_description'] != None:
        acc_dict['content_description'] = accession['content_description']
      


    #Use restrictions
    if accession['copyright'] == 'Public Domain':
        acc_dict['use_restrictions'] = False
        acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to the public domain. Rights will be marked by a Creative Commons CC0 license.'
    elif accession['copyright'] == 'Smith Copyright':
        acc_dict['use_restrictions'] = False
        acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to Smith College.'
    elif accession['copyright'] == 'Donor with cc 4.0':
        acc_dict['use_restrictions'] = True
        acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College, but the donor grants Smith a nonexclusive right to authorize all uses of these materials for research, scholarly or other purposes pursuant to a Creative Commons Attribution 4.0 International License.'
    else:
        acc_dict['use_restrictions'] = True
        acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College.'

    # Access restrictions
    if accession['access'] == 'The materials I contribute can be made available to the public immediately':
        acc_dict['access_restrictions'] = False
        acc_dict['access_restrictions_note'] = accession['access']
    else:
        acc_dict['access_restrictions'] = True
        acc_dict['access_restrictions_note'] = accession['access']


    # Restrictions apply checkbox
    if acc_dict['access_restrictions'] == True:
        acc_dict['restrictions_apply'] = True
    elif acc_dict['use_restrictions'] == True:
        acc_dict['restrictions_apply'] = True
    else:
        acc_dict['restrictions_apply'] = False

    # Add donor agent as source
    acc_dict['linked_agents'] = []
    linked_agent = {}
    linked_agent['role'] = 'source'
    linked_agent['ref'] = agent_uri
    try:
         acc_dict['linked_agents'].append(linked_agent)
    except KeyError:
         logging.error ('issue with linked agent', KeyError) 

    # Add donor agent as creator only if they say "yes" they created it
    role = str(accession['created'])
    yes = 'Yes'
    if yes in role:
        linked_agent_creator = {}
        linked_agent_creator['role'] = 'creator'
        linked_agent_creator['ref'] = agent_uri
        try:
             acc_dict['linked_agents'].append(linked_agent_creator)
        except KeyError:
             logging.error ('issue with creator linked agent', KeyError)

    return acc_dict

def create_accession_records(aspace, csvreader):
    accessions = []
    for row in csvreader:
        if row['nanci_checkB1'].lower() == 'true' and row['nanci_checkB2'].lower() == 'true' and row['nanci_checkA'].lower() == 'true':
            accession_record = make_accession(row)
            try:
                post = aspace.post('/repositories/4/accessions', accession_record)
                logging.info('Accession record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
            except Exception as e:
                logging.warning('Failure to create accession record for {}: {}'.format(row['full_name'], e))


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
