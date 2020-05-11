from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

# This script will create agent records in bulk in ArchivesSpace based on a csv file, and will publish them. The csv file must contain columns labeled last_name, first_name, full_name, legal_name, email, bioghist, and complete. 
#The following fields may be left blank: legal_name, email, bioghist.
# The field "complete" must have a value of TRUE for that row to be included in the data import.

def make_agent_record(agent):

	agent_dict = {'jsonmodel_type':'agent_person',
				 'publish': True,
				 'notes':[]
				 }

	# Contact information
	agent_dict['agent_contacts'] = []
	contacts = {}
	contacts['name'] = agent['full_name']
	contacts['jsonmodel_type'] = 'agent_contact'
	contacts['email'] = agent['email'] #does not cause issue if blank
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
	agent_names['primary_name'] = agent['last_name']
	agent_names['name_order'] = 'inverted'
	agent_names['rest_of_name'] = agent['first_name']
	agent_names['related_agents'] = []
	agent_names['agent_type'] = 'agent_person'
	# Make their legal name
	legal_name = agent['legal_name']
	agent_legal_name = {}
	agent_legal_name['jsonmodel_type'] = 'name_person'
	agent_legal_name['use_dates'] = []
	agent_legal_name['authorized'] = False
	agent_legal_name['is_display_name'] = False
	agent_legal_name['sort_name_auto_generate'] = True
	agent_legal_name['rules'] = 'local'
	agent_legal_name['source'] = 'local'
	agent_legal_name['primary_name'] = agent['legal_name']
	agent_legal_name['name_order'] = 'direct'
	agent_legal_name['related_agents'] = []
	agent_legal_name['agent_type'] = 'agent_person'
	#Accounting for cases where they may not have a legal name different from their preferred name
	if len(legal_name) != 0:
		try:
			agent_dict['names'].append(agent_names)
			agent_dict['names'].append(agent_legal_name)
		except KeyError:
			logging.error ('issue with legal names', KeyError)
	else:
		try:
			agent_dict['names'].append(agent_names)
		except:
			logging.error ('issue with preferred names', KeyError)


	# Bioghist note on agent
	bioghist = agent['bioghist']
	if len(bioghist) != 0:
		agent_dict['notes'] = []
		agent_notes = {}
		agent_notes['jsonmodel_type'] = 'note_bioghist'
		agent_notes['publish'] = True
		agent_notes['subnotes'] = []
		agent_subnotes = {}
		agent_subnotes['jsonmodel_type'] = "note_text"
		agent_subnotes['content'] = agent['bioghist']
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

def create_agent_records(aspace, csvreader):
	"""Takes a csvreader object. Iterated through it and creates the agents listed.
	Returns a list of URIs for the respective records.
	"""

	agents = []
	for row in csvreader:
		if row['nanci_checkB1'] == 'TRUE' and row['nanci_checkB2'] == 'TRUE' and row['nanci_checkA'] == 'TRUE' and len(row['agent_id']) == 0:
			record = make_agent_record(row)
			try:
				post = aspace.post('/agents/people', record)
				logging.info('Agent record created for {}'.format(row['full_name'] + ' URI: ' + post['uri']))
				agents.append( {
					'name': row['full_name'],
					'uri': post['uri'],
				})
			except Exception as e:
				logging.warning('Failure to create agent record for {}: {}'.format(row['full_name'], e))
	return agents

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