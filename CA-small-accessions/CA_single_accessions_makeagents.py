from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

# This script will create agent records in bulk in ArchivesSpace based on a csv file, and will publish them.

def make_person_agent_record(agent):

    agent_dict = {'jsonmodel_type':'agent_person',
                'publish': True,
                'notes':[]
                }

    # Contact information
    agent_dict['agent_contacts'] = []
    contacts = {}
    contacts['name'] = (agent['donor_firstname'] + " " + agent['donor_lastname'])
    contacts['jsonmodel_type'] = 'agent_contact'
    contacts['email'] = agent['donor_email']
    contacts['address_2'] = agent['donor_address']
    contacts['city'] = agent['donor_city']
    contacts['region'] = agent['donor_state']
    contacts['post_code'] = agent['donor_zip'] #does not cause issue if blank
    try:
        agent_dict['agent_contacts'].append(contacts)
    except KeyError:
        logging.error ('issue with contacts', KeyError)

    # Name information
    # Make their preferred name
    agent_dict['names'] = []
    agent_names = {}
    agent_names['jsonmodel_type'] = 'name_person'
    agent_names['use_dates'] = []
    agent_names['authorized'] = True
    agent_names['is_display_name'] = True
    agent_names['sort_name_auto_generate'] = True
    agent_names['rules'] = 'local'
    agent_names['source'] = 'local'
    agent_names['primary_name'] = agent['donor_lastname']
    agent_names['name_order'] = 'inverted'
    agent_names['rest_of_name'] = agent['donor_firstname']
    agent_names['related_agents'] = []
    agent_names['agent_type'] = 'agent_person'
    #Accounting for cases where they may not have a legal name different from their preferred name

    try:
        agent_dict['names'].append(agent_names)
    except:
        logging.error ('issue with preferred names', KeyError)


# Bioghist note on agent
    bioghist = agent['donor_classyear']
    if len(bioghist) != 0:
        agent_dict['notes'] = []
        agent_notes = {}
        agent_notes['jsonmodel_type'] = 'note_bioghist'
        agent_notes['publish'] = True
        agent_notes['subnotes'] = []
        agent_subnotes = {}
        agent_subnotes['jsonmodel_type'] = "note_text"
        agent_subnotes['content'] = agent['donor_classyear']
        agent_subnotes['publish'] = True
        try:
            agent_notes['subnotes'].append(agent_subnotes)
        except KeyError:
            logging.error ('issue with subnotes', KeyError)
        try:
            agent_dict['notes'].append(agent_notes)
        except KeyError:
            logging.error ('issue with notes', KeyError)


    return agent_dict

def make_person_creator_record(agent):

    agent_dict = {'jsonmodel_type':'agent_person',
                'publish': True,
                'notes':[]
                }

    # Name information
    # Make their preferred name
    agent_dict['names'] = []
    agent_names = {}
    agent_names['jsonmodel_type'] = 'name_person'
    agent_names['use_dates'] = []
    agent_names['authorized'] = True
    agent_names['is_display_name'] = True
    agent_names['sort_name_auto_generate'] = True
    agent_names['rules'] = 'local'
    agent_names['source'] = 'local'
    agent_names['primary_name'] = agent['creator_lastname']
    agent_names['name_order'] = 'inverted'
    agent_names['rest_of_name'] = agent['creator_firstname']
    agent_names['related_agents'] = []
    agent_names['agent_type'] = 'agent_person'
    #Accounting for cases where they may not have a legal name different from their preferred name

    try:
        agent_dict['names'].append(agent_names)
    except:
        logging.error ('issue with preferred names', KeyError)


# Bioghist note on agent
    bioghist = agent['creator_classyear']
    if len(bioghist) != 0:
        agent_dict['notes'] = []
        agent_notes = {}
        agent_notes['jsonmodel_type'] = 'note_bioghist'
        agent_notes['publish'] = True
        agent_notes['subnotes'] = []
        agent_subnotes = {}
        agent_subnotes['jsonmodel_type'] = "note_text"
        agent_subnotes['content'] = agent['creator_classyear']
        agent_subnotes['publish'] = True
        try:
            agent_notes['subnotes'].append(agent_subnotes)
        except KeyError:
            logging.error ('issue with subnotes', KeyError)
        try:
            agent_dict['notes'].append(agent_notes)
        except KeyError:
            logging.error ('issue with notes', KeyError)


    return agent_dict

def make_corporate_agent_record(agent):

    agent_dict = {'jsonmodel_type':'agent_corporate_entity',
                'publish': True,
                'notes':[]
                }

    # Contact information
    agent_dict['agent_contacts'] = []
    contacts = {}
    contacts['name'] = agent['donor_lastname']
    contacts['jsonmodel_type'] = 'agent_contact'
    contacts['email'] = agent['donor_email']
    contacts['address_2'] = agent['donor_address']
    contacts['city'] = agent['donor_city']
    contacts['region'] = agent['donor_state']
    contacts['post_code'] = agent['donor_zip'] #does not cause issue if blank
    try:
        agent_dict['agent_contacts'].append(contacts)
    except KeyError:
        logging.error ('issue with contacts', KeyError)

    # Name information
    # Make their preferred name
    agent_dict['names'] = []
    agent_names = {}
    agent_names['jsonmodel_type'] = 'name_corporate_entity'
    agent_names['use_dates'] = []
    agent_names['authorized'] = True
    agent_names['is_display_name'] = True
    agent_names['sort_name_auto_generate'] = True
    agent_names['rules'] = 'local'
    agent_names['source'] = 'local'
    agent_names['primary_name'] = agent['donor_lastname']
    agent_names['related_agents'] = []
    agent_names['agent_type'] = 'agent_corproate_entity'

    try:
        agent_dict['names'].append(agent_names)
    except:
        logging.error ('issue with preferred names', KeyError)


    return agent_dict

def make_corporate_creator_record(agent):

    agent_dict = {'jsonmodel_type':'agent_corporate_entity',
                'publish': True,
#                'notes':[]
                }
    # Name information
    agent_dict['names'] = []
    agent_names = {}
    agent_names['jsonmodel_type'] = 'name_corporate_entity'
    agent_names['use_dates'] = []
    agent_names['authorized'] = True
    agent_names['is_display_name'] = True
    agent_names['sort_name_auto_generate'] = True
    agent_names['rules'] = 'local'
    agent_names['source'] = 'local'
    agent_names['primary_name'] = agent['creator_lastname']
    agent_names['related_agents'] = []
    agent_names['agent_type'] = 'agent_corproate_entity'

    try:
        agent_dict['names'].append(agent_names)
    except:
        logging.error ('issue with preferred names', KeyError)

    print('making corproate creator agent')
    return agent_dict

# def make_transfer_office_record(agent):
#
#     agent_dict = {'jsonmodel_type':'agent_corporate_entity',
#                 'publish': True,
#                 'notes':[]
#                 }
#     # Name information
#     agent_dict['names'] = []
#     agent_names = {}
#     agent_names['jsonmodel_type'] = 'name_corporate_entity'
#     agent_names['use_dates'] = []
#     agent_names['authorized'] = True
#     agent_names['is_display_name'] = True
#     agent_names['sort_name_auto_generate'] = True
#     agent_names['rules'] = 'local'
#     agent_names['source'] = 'local'
#     agent_names['primary_name'] = agent['transfer_office']
#     agent_names['related_agents'] = []
#     agent_names['agent_type'] = 'agent_corproate_entity'
#
#     try:
#         agent_dict['names'].append(agent_names)
#     except:
#         logging.error ('issue with transfer office name', KeyError)
#
#     return agent_dict

def create_agent_records(aspace, csvreader):
#Takes a csvreader object. Iterated through it and creates the agents listed.
#Returns a list of URIs for the respective records.
    agents = []
    for row in csvreader:
        if len(row['donor_uri']) == 0 and row['donor_type'] == 'person':
            record_1 = make_person_agent_record(row)
            try:
                post = aspace.post('/agents/people', record_1)
                logging.info('Agent record created for {}'.format(row['donor_lastname'] + ' URI: ' + post['uri']))
                agents.append( {
                'name': row['donor_lastname'],
                'uri': post['uri'],
                })
            except Exception as e:
                logging.warning('Failure to create agent record for {}: {}'.format(row['donor_lastname'], e))
        if len(row['donor_uri']) == 0 and row['donor_type'] == 'corporate':
            print("Yes there's an agent here")
            record_2 = make_corporate_agent_record(row)
            try:
                post = aspace.post('/agents/corporate_entities', record_2)
                logging.info('Agent record created for {}'.format(row['donor_lastname'] + ' URI: ' + post['uri']))
                agents.append( {
                'name': row['donor_lastname'],
                'uri': post['uri'],
                })
            except Exception as e:
                logging.warning('Failure to create agent record for {}: {}'.format(row['donor_lastname'], e))
        if len(row['creator_uri']) == 0 and row['creator_type'] == 'person':
            record_3 = make_person_creator_record(row)
            try:
                post = aspace.post('/agents/people', record_3)
                logging.info('Agent record created for {}'.format(row['creator_lastname'] + ' URI: ' + post['uri']))
                agents.append( {
                'name': row['creator_lastname'],
                'uri': post['uri'],
                })
            except Exception as e:
                logging.warning('Failure to create agent record for {}: {}'.format(row['creator_lastname'], e))
        if len(row['creator_uri']) == 0 and row['creator_type'] == 'corporate':
            print("Yes there's an agent here")
            record_4 = make_corporate_creator_record(row)
            try:
                post = aspace.post('/agents/corporate_entities', record_4)
                logging.info('Agent record created for {}'.format(row['creator_lastname'] + ' URI: ' + post['uri']))
                agents.append( {
                'name': row['creator_lastname'],
                'uri': post['uri'],
                })
            except Exception as e:
                logging.warning('Failure to create agent record for {}: {}'.format(row['donor_lastname'], e))

    return agents
    row.append(agents)




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
        create_agent_records(aspace, csvreader)
