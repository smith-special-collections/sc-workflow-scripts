from archivesspace import archivesspace
import argparse
import logging
import datetime
import csv

#translates the status of the person into the appropriate classification link
AFFILIATION_DICT = {
	'faculty': '/repositories/4/classification_terms/186',
	'staff': '/repositories/4/classifications/10',
	'class of 2020': '/repositories/4/classification_terms/401',
	'class of 2021': '/repositories/4/classification_terms/402',
	'class of 2022': '/repositories/4/classification_terms/403',
	'class of 2023': '/repositories/4/classification_terms/404'
}

provenance_string1 = 'Received from'
provenance_string2 = 'as part of the Covid-19 Chronicles project.'
title_string = 'Covid-19 digital materials' 


DATE = datetime.date.today()
DATE = DATE.__str__()


def make_accession(accession):
	full_name = accession['full_name']
	gen_note_aff = accession['affiliation']
	gen_note_living = accession['where_living']
	acc_dict = {'jsonmodel_type':'accession',
				 'publish': False,
				 'provenance': f"{provenance_string1} {full_name} {provenance_string2}",
				 'title': f"{full_name} {title_string}",
				 'content_description': accession['content_description'],
				 'general_note': f"{gen_note_aff}; {gen_note_living}.",
				 
#				 'use_restrictions': True, #Needs to be changed to false if they gave us copyright.
#				 'use_restrictions_note': 'Copyright info.', #Needs to be populated from spreadsheet.
				 'id_0': '2020',
				 'id_1': 'A',
				 'acquisition_type': 'gift',
				 'resource_type': 'papers',
				 'accession_date': DATE,
				 'subjects':[{'ref':'/subjects/6201'}] #Adds the subject "electronic records"
				 }

	for key in AFFILIATION_DICT.keys():
		if key == accession['affiliation'].lower().strip():
			affiliation = AFFILIATION_DICT[key]

	acc_dict['classifications']	= []
	classification = {}
	classification['ref'] = affiliation

	try:
 			acc_dict['classifications'].append(classification)
	except:
 			print ('issue with affiliation')

	
	# Id
	try:
		i2 = str(accession['id_2']).split('.')
		acc_dict['id_2'] = i2[1]
		if len(acc_dict['id_2']) < 4:
			while len(acc_dict['id_2']) < 4:
				acc_dict['id_2'] = acc_dict['id_2'] + '0'
	except:
		print ('issue with id_2')
	
	# Content Description
	if accession['content_description'] != None:
		acc_dict['content_description'] = accession['content_description']
		
		
	#Use restrictions
	if accession['copyright'] == 'public domain':
		acc_dict['use_restrictions'] = False
		acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to the public domain. Rights will be marked by a Creative Commons CC0 license.'
	elif accession['copyright'] == 'college':
		acc_dict['use_restrictions'] = False
		acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to Smith College.'
	elif accession['copyright'] == 'donor but cc 4.0':
		acc_dict['use_restrictions'] = True
		acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College, but the donor grants Smith a nonexclusive right to authorize all uses of these materials for research, scholarly or other purposes pursuant to a Creative Commons Attribution 4.0 International License.'
	else:
		acc_dict['use_restrictions'] = True
		acc_dict['use_restrictions_note'] = 'To the extent that they own copyright, donor has retained copyright in their works donated to Smith College.'
		
	# Access restrictions
	if accession['access_restrictions'] == 'The materials I contribute can be made available to the public immediately':
		acc_dict['access_restrictions'] = False
		acc_dict['access_restrictions_note'] = accession['access_restrictions']
	else:
		acc_dict['access_restrictions'] = True
		acc_dict['access_restrictions_note'] = accession['access_restrictions']
		
		
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
	linked_agent['ref'] = accession['agent_uri']
	try:
 			acc_dict['linked_agents'].append(linked_agent)
	except:
 			print ('issue with linked agent')
 			
	# Add donor agent as creator only if they say "yes" they created it	
	role = str(accession['role'])
	yes = 'Yes'
	if yes in role:
		linked_agent_creator = {}
		linked_agent_creator['role'] = 'creator'
		linked_agent_creator['ref'] = accession['agent_uri']
		try:
 			acc_dict['linked_agents'].append(linked_agent_creator)
		except:
 			print ('issue with creator linked agent')
					 	
	#
	# # Extents
	# acc_dict['extents'] = []
	# extent_dict = {}
	# extent_dict['jsonmodel_type'] = 'extent'
	# try:
	# 	extent_dict['extent_type'] = accession['extent_type'].lower().strip() + 's'
	# except:
	# 	continue
	# try:
	# 	extent_dict['number'] = str(int(accession['extent'])).strip()
	# except:
	# 	continue
	# try:
	# 	extent_dict['portion'] = accession['portion'].lower().strip()
	# except:
	# 	continue
	#
	# # Ensures extents array has all the required fields, otherwise an error will be raised when trying to post
	# if len(extent_dict) > 3:
	# 	acc_dict['extents'].append(extent_dict)
	#
	# Date field
	# acc_dict['dates'] = []
	# date_dict = {}

	# if accession['date_type'] != None and accession['begin_date'] != None:
	# 	if accession['date_type'].lower().strip() == 'inclusive':
	# 		date_dict['end'] = accession['end_date']
	# 	if len(str(accession['begin_date'])) > 4 or len(str(accession['begin_date'])) < 4:
	# 		date_dict['begin'] = '0000'
	# 	else:
	# 		date_dict['begin'] = str(int(accession['begin_date']))
	# 	if accession['certainty'] != None and (accession['certainty'].lower().strip() == 'approximate' or accession['certainty'].lower().strip() == 'inferred' or accession['certainty'].lower().strip() == 'questionable'):
	# 		date_dict['certainty'] = accession['certainty'].strip()
	# 	date_dict['date_type'] = accession['date_type'].lower().strip()
	# 	date_dict['calendar'] = 'gregorian'
	# 	date_dict['era'] = 'ce'
	# 	date_dict['jsonmodel_type'] = 'date'
	# 	date_dict['label'] = 'publication'
	# 	acc_dict['dates'].append(date_dict)
	#
	# # Acquisition Type
	# try:
	# 	acc_dict['acquisition_type'] = accession['\ufeffacquisition_type'].lower().strip()
	# except:
	# 	continue
	#
	# # Linked agents
	# acc_dict['linked_agents'] = []
	#
	# if accession['agent_type1'] != None:
	# 	for key in RELATOR_DICT.keys():
	# 		if key == accession['agent_type1'].lower().strip():
	# 			relator1 = RELATOR_DICT[key]
	# 		else:
	# 			relator1 = ""
	#
	# if accession['agent_type2'] != None:
	# 	for key in RELATOR_DICT.keys():
	# 		if key == accession['agent_type2'].lower().strip():
	# 			relator2 = RELATOR_DICT[key]
	# 		else:
	# 			relator2 = ""
	#
	# agent1 = {}
	# agent1['terms'] = []
	# try:
	# 	if accession['agent_uri1'][0] == '/':
	# 		agent1['ref'] = accession['agent_uri1'].strip()
	# 		if relator1 != "":
	# 			agent1['relator'] = relator1
	# 		if accession['linked_agent_role1'].strip() != None:
	# 			agent1['role'] = accession['linked_agent_role1'].lower().strip()
	#
	# 		acc_dict['linked_agents'].append(agent1)
	# except:
	# 	continue
	#
	# agent2 = {}
	# agent2['terms'] = []
	# try:
	# 	if accession['agent_uri2'][0] == '/':
	# 		agent2['ref'] = accession['agent_uri2'].strip()
	# 		if relator2 != "":
	# 			agent2['relator'] = relator1
	# 		if accession['linked_agent_role2'].strip() != None:
	# 			agent2['role'] = accession['linked_agent_role2'].lower().strip()
	#
	# 		acc_dict['linked_agents'].append(agent2)
	# except:
	# 	continue

	return acc_dict


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
				record = make_accession(row)
				try:
					post = aspace.post('/repositories/4/accessions', record)
					logging.info('Accession record created for {}'.format(row['full_name'] + " New URI: " + post['uri']))
				except Exception as e:
					logging.warning('Failure to create accession record for {}: {}'.format(row['full_name'], e))
