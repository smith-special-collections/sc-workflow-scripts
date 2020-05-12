from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

ID_ZERO_PADDING = 4

provenance_string1 = 'Received from'
provenance_string2 = 'as part of the Covid-19 Chronicles project.'
title_string = 'digital materials'



DATE = datetime.date.today()
DATE = DATE.__str__()


def make_archival_object(row, agent_uri, accession_id):
    full_name = row['full_name']
    ao_dict = {'jsonmodel_type':'archival_object',
                 'publish': True,
                 'component_id': 'Accession ' + str(accession_id['id_0']) + '-' + str(accession_id['id_1']) + '-' + str(accession_id['id_2']),
                 'title': f"{full_name} {title_string}", #Consider changing the title to be name and the content_description field
                 'level': 'file',
                 'resource': {'ref': '/repositories/4/resources/1630'}
                 }

    # Adding the collection as its parent object
    ao_dict['ancestors'] = []
    ancestors = {}
    ancestors['ref'] = '/repositories/4/resources/1630'
    ancestors['level'] = 'collection'
    try:
        ao_dict['ancestors'].append(ancestors)
    except KeyError:
        logging.error ('issue with ancestors', KeyError)



    # Building the file descriptions for the defined list.
    if len(row['file1_desc']) != 0:
        if len(row['file1_date']) != 0:
            file1 = str(row['file1_desc']).strip('. ') + ', ' + row['file1_date']
        else:
            file1 = str(row['file1_desc'])
    else:
        file1 = None
    if len(row['file2_desc']) != 0:
        if len(row['file2_date']) != 0:
            file2 = str(row['file2_desc']).strip('. ') + ', ' + row['file2_date']
        else:
            file2 = str(row['file2_desc'])
    else:
        file2 = None
    if len(row['file3_desc']) != 0:
        if len(row['file3_date']) != 0:
            file3 = str(row['file3_desc']).strip('. ') + ', ' + row['file3_date']
        else:
            file3 = str(row['file3_desc'])
    else:
        file3 = None
    if len(row['file4_desc']) != 0:
        if len(row['file4_date']) != 0:
            file4 = str(row['file4_desc']).strip('. ') + ', ' + row['file4_date']
        else:
            file4 = str(row['file4_desc'])
    else:
        file4 = None
    if len(row['file5_desc']) != 0:
        if len(row['file5_date']) != 0:
            file5 = str(row['file5_desc']).strip('. ') + ', ' + row['file5_date']
        else:
            file5 = str(row['file5_desc'])
    else:
        file5 = None
    if len(row['file6_desc']) != 0:
        if len(row['file6_date']) != 0:
            file6 = str(row['file6_desc']).strip('. ') + ', ' + row['file6_date']
        else:
            file6 = str(row['file6_desc'])
    else:
        file6 = None
    if len(row['file7_desc']) != 0:
        if len(row['file7_date']) != 0:
            file7 = str(row['file7_desc']).strip('. ') + ', ' + row['file7_date']
        else:
            file7 = str(row['file7_desc'])
    else:
        file7 = None
    if len(row['file8_desc']) != 0:
        if len(row['file8_date']) != 0:
            file8 = str(row['file8_desc']).strip('. ') + ', ' + row['file8_date']
        else:
            file8 = str(row['file8_desc'])
    else:
        file8 = None
    if len(row['file9_desc']) != 0:
        if len(row['file9_date']) != 0:
            file9 = '; ' + str(row['file9_desc']).strip('. ') + ', ' + row['file9_date']
        else:
            file9 = str(row['file9_desc'])
    else:
        file9 = None
    if len(row['file10_desc']) != 0:
        if len(row['file10_date']) != 0:
            file10 = str(row['file10_desc']).strip('. ') + ', ' + row['file10_date']
        else:
            file10 = str(row['file10_desc'])
    else:
        file10 = None

    # Notes
    bioghist = row['bioghist']
    gen_note_aff = row['affiliation']
    gen_note_living = row['where_living']
    ao_dict['notes'] = []
    bio_note = {}
    bio_note['jsonmodel_type'] = 'note_multipart'
    bio_note['publish'] = True
    bio_note['type'] = 'bioghist'
    bio_note['subnotes'] = []
    bio_subnote = {}
    bio_subnote['jsonmodel_type'] = 'note_text'
    bio_subnote['content'] = f"{bioghist} {full_name} is a {gen_note_aff} member. {gen_note_living} during the 2020 Covid-19 pandemic."
    bio_subnote['publish'] = True
    sc_note = {}
    sc_note['jsonmodel_type'] = 'note_multipart'
    sc_note['publish'] = True
    sc_note['type'] = 'scopecontent'
    sc_note['subnotes'] = []
    sc_subnote = {}
    sc_subnote['jsonmodel_type'] = 'note_text'
    sc_subnote['content'] = row['content_description']
    sc_subnote['publish'] = True
    userestrict_note = {}
    userestrict_note['jsonmodel_type'] = 'note_multipart'
    userestrict_note['publish'] = True
    userestrict_note['type'] = 'userestrict'
    userestrict_note['subnotes'] = []
    userestrict_subnote = {}
    userestrict_subnote['jsonmodel_type'] = 'note_text'
    userestrict_subnote['publish'] = True

    try:
        bio_note['subnotes'].append(bio_subnote)
    except KeyError:
        logging.error ('issue with bio subnote', KeyError)
    try:
        ao_dict['notes'].append(bio_note)
    except KeyError:
        logging.error ('issue with bio note', KeyError)
        
    try:
        sc_note['subnotes'].append(sc_subnote)
    except KeyError:
        logging.error ('issue with sc subnote', KeyError)
    try:
        ao_dict['notes'].append(sc_note)
    except KeyError:
        logging.error ('issue with sc note', KeyError)

    # Use Restrictions Note
    if row['copyright'] == 'Public Domain':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to the public domain. Rights will be marked by a Creative Commons CC0 license.'
    elif row['copyright'] == 'Smith Copyright':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to Smith College.'
    elif row['copyright'] == 'Donor with cc 4.0':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College, but the donor grants Smith a nonexclusive right to authorize all uses of these materials for research, scholarly or other purposes pursuant to a Creative Commons Attribution 4.0 International License.'
    else:
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College.'
    try:
        userestrict_note['subnotes'].append(userestrict_subnote)
    except KeyError:
        logging.error ('issue with userestrict subnote', KeyError)
    try:
        ao_dict['notes'].append(userestrict_note)
    except KeyError:
        logging.error ('issue with userestrict note', KeyError)


    # Restrictions apply checkbox and machine actionable note
    if row['access'] == 'The materials I contribute can be made available to the public immediately':
        ao_dict['restrictions_apply'] = False
    else:
        ao_dict['restrictions_apply'] = True
        new_restriction = {'jsonmodel_type': 'note_multipart',
            'publish': True,
            'rights_restriction': {'begin': DATE, 'end': '2026-01-01', 'local_access_restriction_type': ["RestrictedSpecColl"]},
            'subnotes': [{'content': 'At the direction of the donor, this material is closed until January 1, 2026.',
                          'jsonmodel_type': 'note_text',
                          'publish': True}],
            'type': 'accessrestrict'}
        try:
            ao_dict['notes'].append(new_restriction)
        except KeyError:
            logging.error ('issue with accessrestrict note', KeyError)
            
    defined_list = {'jsonmodel_type': 'note_definedlist',
                        'title': 'Included files:',
                        'publish': True,
                        'items': []}
                
    #Create items for the defined list
    item1 = {'label': 'File 1','value': file1}
    item2 = {'label': 'File 2','value': file2}
    item3 = {'label': 'File 3','value': file3}
    item4 = {'label': 'File 4','value': file4}
    item5 = {'label': 'File 5','value': file5}
    item6 = {'label': 'File 6','value': file6}
    item7 = {'label': 'File 7','value': file7}
    item8 = {'label': 'File 8','value': file8}
    item9 = {'label': 'File 9','value': file9}
    item10 = {'label': 'File 10','value': file10}
    
    if file1 != None:
        try:
            defined_list['items'].append(item1)
        except KeyError:
            logging.error ('issue with file1', KeyError)
    if file2 != None:
        try:
            defined_list['items'].append(item2)
        except KeyError:
            logging.error ('issue with file2', KeyError)
    if file3 != None:
        try:
            defined_list['items'].append(item3)
        except KeyError:
            logging.error ('issue with file3', KeyError)
    if file4 != None:
        try:
            defined_list['items'].append(item4)
        except KeyError:
            logging.error ('issue with file4', KeyError)
    if file5 != None:
        try:
            defined_list['items'].append(item5)
        except KeyError:
            logging.error ('issue with file5', KeyError)
    if file6 != None:
        try:
            defined_list['items'].append(item6)
        except KeyError:
            logging.error ('issue with file6', KeyError)
    if file7 != None:
        try:
            defined_list['items'].append(item7)
        except KeyError:
            logging.error ('issue with file7', KeyError)
    if file8 != None:
        try:
            defined_list.append(item8)
        except KeyError:
            logging.error ('issue with file8', KeyError)
    if file9 != None:
        try:
            defined_list['items'].append(item9)
        except KeyError:
            logging.error ('issue with file9', KeyError)
    if file10 != None:
        try:
            defined_list['items'].append(item10)
        except KeyError:
            logging.error ('issue with file10', KeyError)
            
    if file1 != None:
        try:
            sc_note['subnotes'].append(defined_list)
        except KeyError:
            logging.error ('issue with defined list', KeyError)

    # Add donor agent as creator only if they say "yes" they created it
    role = str(row['created'])
    yes = 'Yes'
    if yes in role:
        ao_dict['linked_agents'] = []
        linked_agent_creator = {}
        linked_agent_creator['role'] = 'creator'
        linked_agent_creator['ref'] = agent_uri
        try:
            ao_dict['linked_agents'].append(linked_agent_creator)
        except KeyError:
            logging.error ('issue with creator linked agent', KeyError)

    return ao_dict

def create_archival_object_records(aspace, csvreader):
    """Takes a csvreader object. Iterates through it and creates the archival objects listed."""
    archival_objects = []
    for row in csvreader:
        if row['nanci_checkB1'].lower() == 'true' and row['nanci_checkB2'].lower() == 'true' and row['nanci_checkA'].lower() == 'true':
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
