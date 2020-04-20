from archivesspace import archivesspace
import argparse
import logging
import pprint
import csv

#This script was updated from one written by Claire Marshall. It has been updated from removing all "Existence and Location of Copies" notes in a repository to instead only remove it from the archival objects specified in an input csv file.

#This script requires the ArchivesSpace module written by Tristan Chambers to run.

def remove_note_by_type(note_type, notes):
	c = 0
	for note in notes:
		if 'type' in note.keys():
			if note['type'] == note_type:
				c += 1
				notes.remove(note)
	if c > 0:
		return notes
	else:
		return None


if __name__ == '__main__':
	
	CONFIGFILE = "archivesspace.cfg"

	argparser = argparse.ArgumentParser()
	argparser.add_argument("SERVERCFG", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'testing'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
	argparser.add_argument("CSVFILE", default="DEFAULT", help="Path to CSV file for parsing.")
	cliArguments = argparser.parse_args()

	aspace = archivesspace.ArchivesSpace()
	aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
	aspace.connect()

	logging.basicConfig(level=logging.INFO)

#	repos = cliArguments.REPO_NUMS

#Open the csv file and get the values from the column labeled "archivalobject_uri"
	with open(cliArguments.CSVFILE, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			record = aspace.get(row['archivalobject_uri'])
			try:
				stripped_notes = remove_note_by_type('altformavail', record['notes']) #You can change 'altformavail' to other note types to delete different types of notes.
				if stripped_notes != None:
					record['notes'] = stripped_notes
					post = aspace.post(record['uri'], record)
					logging.info(post['status'])
			except Exception as e:
				logging.error(e)

#The commented out portion below can be used to delete every note of the type specified in a specific repository.
#	for repo in repos:
#		resources = aspace.get(f'/repositories/{repo}/resources?all_ids=true')
#		for resource in resources:
#			try:
#				rec = aspace.get(f'repositories/{repo}/resources/{resource}')
#				try:
#					stripped_notes = remove_note_by_type('altformavail', rec['notes'])
#					if stripped_notes != None:
#						rec['notes'] = stripped_notes
#						post = aspace.post(rec['uri'], rec)
#						logging.info(post['status'])
#				except Exception as e:
#					logging.error(e)
#			except Exception as e:
#				logging.error(e)




