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


def make_archival_object(archival_object):
	full_name = archival_object['full_name']
	component_id = str(archival_object['id_2']).zfill(ID_ZERO_PADDING)
	ao_dict = {'jsonmodel_type':'archival_object',
				 'publish': True,
				 'component_id': f"2020-A-{component_id}",
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

 	
 	
 	# All the file descriptions. Need to figure out how to include without adding extra commas or semicolons into the resulting archival object. Description is required for each file uploaded but date is not.
	f1 = archival_object['file1_desc']
	f1_date = archival_object['file1_date']
	f2 = archival_object['file2_desc']
	f2_date = archival_object['file2_date']
	f3 = archival_object['file3_desc']
	f3_date = archival_object['file3_date']
	f4 = archival_object['file4_desc']
	f4_date = archival_object['file4_date']
	f5 = archival_object['file5_desc']
	f5_date = archival_object['file5_date']
	f6 = archival_object['file6_desc']
	f6_date = archival_object['file6_date']
	f7 = archival_object['file7_desc']
	f7_date = archival_object['file7_date']
	f8 = archival_object['file8_desc']
	f8_date = archival_object['file8_date']
	f9 = archival_object['file9_desc']
	f9_date = archival_object['file9_date']
	f10 = archival_object['file10_desc']
	f10_date = archival_object['file10_date']	
 			
 	# Notes
	bioghist = archival_object['bioghist']
	content_description = archival_object['content_description']
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
	sc_subnote['content'] = str(f"{content_description} Includes: {f1}, {f1_date}; {f2}, {f2_date}; {f3}, {f3_date}; {f4}, {f4_date}; {f5}, {f5_date}; {f6}, {f6_date}; {f7}, {f7_date}; {f8}, {f8_date}; {f9}, {f9_date}; {f10}, {f10_date}.".strip(',; '))	
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
	if archival_object['copyright'] == 'public domain':
		userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to the public domain. Rights will be marked by a Creative Commons CC0 license.'
	elif archival_object['copyright'] == 'college':
		userestrict_subnote['content'] = 'To the extent that they own copyright, donor has transferred any intellectual rights of their work to Smith College.'
	elif archival_object['copyright'] == 'donor but cc 4.0':
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
 			
	# Add donor agent as creator only if they say "yes" they created it	
	role = str(archival_object['role'])
	yes = 'Yes'
	if yes in role:
		ao_dict['linked_agents'] = []
		linked_agent_creator = {}
		linked_agent_creator['role'] = 'creator'
		linked_agent_creator['ref'] = archival_object['agent_uri']
		try:
 			ao_dict['linked_agents'].append(linked_agent_creator)
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
