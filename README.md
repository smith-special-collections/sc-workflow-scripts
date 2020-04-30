Python scripts used to perform various bulk actions via the ArchivesSpace API
## Authenticating to the API

Because these scripts are mostly edited scripts from different sources, they require different authentication methods. Some require a secrets.py file in the same directory that must contain the following text:

	baseURL='[ArchivesSpace API URL]'
	user='[user name]' 
	password='[password]' 
	repository='[repository]'

Some will request login information within the command line after starting running a script, some require the ArchivesSpace module written by Tristan Chambers for authentication, and some require ArchivesSnake.

## Scripts
#### [addfileversions.py](/addfileversions.py)
Python script that adds file versions to existing digital objects using an input CSV. The CSV should include a header row with the columns "digitalobject_uri", "file_uri_csv", and "caption_csv". The script assumes you want the file version to be published, but you can change that to false if necessary. 
Requires the ArchivesSpace module written by Tristan Chambers to run, and an archviesspace.cfg file with your credentials for authentication.

#### [archived_websites.py](/archived_websites.py)
Python script that adds archival objects as children of existing archival objects and/or resources using an input CSV. Necessary columns are listed in the comments in the script. The script is configured specifically for Smith's addition of archived websites, but the JSON could be edited to apply to other cases.
This script requires the ArchivesSnake client and a secrets.py file with your ArchivesSpace credentials for authentication.

#### [archived_websites_add_dos.py](/archived_websites_add_dos.py)
Python script that adds digital objects to existing archival objects using an input CSV. Necessary columns are listed in the comments in the script. The script is configured specifically for Smith's addition of archived websites, but the JSON could be edited to apply to other cases.
This script requires a secrets.py file with your ArchivesSpace credentials for authentication.
	
#### [publish_do.py](/publish_do.py)
Python script that publishes unpublished digital objects using an input CSV. The CSV should include a header row with the digital object uri in the first column.
This script requires a secrets.py file with your ArchivesSpace credentials for authentication.
	
#### [remove_altformavail_notes_from_aos.py](/remove_altformavail_notes_from_aos.py)
Python script that deletes Existence and Location of copies notes from specified archival objects using an input CSV. The CSV should include a header row with the archival object uri in a column called "archivalobject_uri". This script can easily be edited to delete other types of notes.
Requires the ArchivesSpace module written by Tristan Chambers to run, and an archviesspace.cfg file with your credentials for authentication.
