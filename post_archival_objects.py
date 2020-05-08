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


def make_archival_object(archival_object, accession_id, agent_uri):
    full_name = archival_object['full_name']
    component_id = str(archival_object['id_2']).zfill(ID_ZERO_PADDING)
    ao_dict = {'jsonmodel_type':'archival_object',
                 'publish': True,
                 'component_id': str(accession_id['id_0']) + '-' + str(accession_id['id_1']) + '-' + str(accession_id['id_2']),
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
    except:
            print ('issue with ancestors')

    
    
    # Building the file descriptions. This works but is messy. Jinja template would be better if have time.
    if len(archival_object['file1_desc']) != 0:
        if len(archival_object['file1_date']) != 0:
            file1 = 'Includes: ' + archival_object['file1_desc'] + ', ' + archival_object['file1_date']
        else:
            file1 = 'Includes: ' + archival_object['file1_desc']
    else:
        file1 = None
    if len(archival_object['file2_desc']) != 0:
        if len(archival_object['file2_date']) != 0:
            file2 = '; ' + archival_object['file2_desc'] + ', ' + archival_object['file2_date']
        else:
            file2 = '; ' + archival_object['file2_desc']
    else:
        file2 = None
    if len(archival_object['file3_desc']) != 0:
        if len(archival_object['file3_date']) != 0:
            file3 = '; ' + archival_object['file3_desc'] + ', ' + archival_object['file3_date']
        else:
            file3 = '; ' + archival_object['file3_desc']
    else:
        file3 = None
    if len(archival_object['file4_desc']) != 0:
        if len(archival_object['file4_date']) != 0:
            file4 = '; ' + archival_object['file4_desc'] + ', ' + archival_object['file4_date']
        else:
            file4 = '; ' + archival_object['file4_desc']
    else:
        file4 = None
    if len(archival_object['file5_desc']) != 0:
        if len(archival_object['file5_date']) != 0:
            file5 = '; ' + archival_object['file5_desc'] + ', ' + archival_object['file5_date']
        else:
            file5 = '; ' + archival_object['file5_desc']
    else:
        file5 = None
    if len(archival_object['file6_desc']) != 0:
        if len(archival_object['file6_date']) != 0:
            file6 = '; ' + archival_object['file6_desc'] + ', ' + archival_object['file6_date']
        else:
            file6 = '; ' + archival_object['file6_desc']
    else:
        file6 = None
    if len(archival_object['file7_desc']) != 0:
        if len(archival_object['file7_date']) != 0:
            file7 = '; ' + archival_object['file7_desc'] + ', ' + archival_object['file7_date']
        else:
            file7 = '; ' + archival_object['file7_desc']
    else:
        file7 = None
    if len(archival_object['file8_desc']) != 0:
        if len(archival_object['file8_date']) != 0:
            file8 = '; ' + archival_object['file8_desc'] + ', ' + archival_object['file8_date']
        else:
            file8 = '; ' + archival_object['file8_desc']
    else:
        file8 = None
    if len(archival_object['file9_desc']) != 0:
        if len(archival_object['file9_date']) != 0:
            file9 = '; ' + archival_object['file9_desc'] + ', ' + archival_object['file9_date']
        else:
            file9 = '; ' + archival_object['file9_desc']
    else:
        file9 = None
    if len(archival_object['file10_desc']) != 0:
        if len(archival_object['file10_date']) != 0:
            file10 = '; ' + archival_object['file10_desc'] + ', ' + archival_object['file10_date']
        else:
            file10 = '; ' + archival_object['file10_desc']
    else:
        file10 = None
    
    content_description = archival_object['content_description']
        
    #Now make the combined description
    if file10 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}{file6}{file7}{file8}{file9}{file10}"
    elif file9 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}{file6}{file7}{file8}{file9}" 
    elif file8 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}{file6}{file7}{file8}"
    elif file7 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}{file6}{file7}"
    elif file6 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}{file6}"
    elif file5 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}{file5}"
    elif file4 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}{file4}"    
    elif file3 != None:
        combined_description = f"{content_description} {file1}{file2}{file3}"   
    elif file2 != None:
        combined_description = f"{content_description} {file1}{file2}"  
    elif file1 != None:
        combined_description = f"{content_description} {file1}" 
    else:
        combined_description = f"{content_description}"
        
    # Notes
    bioghist = archival_object['bioghist']
    gen_note_aff = archival_object['affiliation']
    gen_note_living = archival_object['where_living']
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
    sc_subnote['content'] = combined_description
    sc_subnote['publish'] = True
    userestrict_note = {}
    userestrict_note['jsonmodel_type'] = 'note_multipart'
    userestrict_note['publish'] = True
    userestrict_note['type'] = 'userestrict'
    userestrict_note['subnotes'] = []
    userestrict_subnote = {}
    userestrict_subnote['jsonmodel_type'] = 'note_text'
    userestrict_subnote['publish'] = True
    
    if len(bioghist) != 0:
        try:
            bio_note['subnotes'].append(bio_subnote)
        except:
            print ('issue with bio subnote')
        try:
            ao_dict['notes'].append(bio_note)
        except:
            print ('issue with bio note')
    if len(content_description) != 0:
        try:
            sc_note['subnotes'].append(sc_subnote)
        except:
            print ('issue with sc subnote')
        try:
            ao_dict['notes'].append(sc_note)
        except:
            print ('issue with sc note')

    # Use Restrictions Note
    if archival_object['copyright'] == 'Public Domain':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to the public domain. Rights will be marked by a Creative Commons CC0 license.'
    elif archival_object['copyright'] == 'Smith Copyright':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to Smith College.'
    elif archival_object['copyright'] == 'Donor with cc 4.0':
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College, but the donor grants Smith a nonexclusive right to authorize all uses of these materials for research, scholarly or other purposes pursuant to a Creative Commons Attribution 4.0 International License.'
    else:
        userestrict_subnote['content'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College.'
    try:
        userestrict_note['subnotes'].append(userestrict_subnote)
    except:
        print ('issue with userestrict subnote')
    try:
        ao_dict['notes'].append(userestrict_note)
    except:
        print ('issue with userestrict note')
        
        
    # Restrictions apply checkbox
    if archival_object['access_restrictions'] == 'The materials I contribute can be made available to the public immediately':
        ao_dict['restrictions_apply'] = False
    else:
        ao_dict['restrictions_apply'] = True
        accessrestrict_note = {}
        accessrestrict_note['jsonmodel_type'] = 'note_multipart'
        accessrestrict_note['publish'] = True
        accessrestrict_note['type'] = 'accessrestrict'
        accessrestrict_note['subnotes'] = []
        accessrestrict_subnote = {}
        accessrestrict_subnote['jsonmodel_type'] = 'note_text'
        accessrestrict_subnote['publish'] = True
        accessrestrict_subnote['content'] = 'At the direction of the donor, this material is closed until January 1, 2026.'
        try:
            accessrestrict_note['subnotes'].append(accessrestrict_subnote)
        except:
            print ('issue with accessrestrict subnote')
        try:
            ao_dict['notes'].append(accessrestrict_note)
        except:
            print ('issue with accessrestrict note')
            
    # Add donor agent as creator only if they say "yes" they created it 
    role = str(archival_object['role'])
    yes = 'Yes'
    if yes in role:
        ao_dict['linked_agents'] = []
        linked_agent_creator = {}
        linked_agent_creator['role'] = 'creator'
        linked_agent_creator['ref'] = agent_uri
        try:
            ao_dict['linked_agents'].append(linked_agent_creator)
        except:
            print ('issue with creator linked agent')

    return ao_dict


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

    csv_file = cliArguments.CSVname

    # Reads CSV file
    with open(csv_file, encoding="utf8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['complete'] == 'TRUE':
                record = make_archival_object(row)
                try:
                    post = aspace.post('/repositories/4/archival_objects', record)
                    logging.info('Archival object record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
                except Exception as e:
                    logging.warning('Failure to create archival object record for {}: {}'.format(row['full_name'], e))
