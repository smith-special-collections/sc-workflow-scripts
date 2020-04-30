import csv
from asnake.client import ASnakeClient
from asnake.aspace import ASpace

#This script has been modified from a script created by Noah Huffman at Duke. It can be used to add archival objects as children to different resources or archival objects.

#The script adds title, level, some date metadata, extent metadata, and a scope and contents note. It is currently configured for a project adding archived websites to ArchivesSpace in bulk. The JSON on line 74 will need editing for other types of materials or for different metadata additions.

#Script currently is pointed toward repository number 2. Edit the number if you need to make updates in a different repository.

#Script takes as input a csv with the columns identified below. See lines 58-71.

import asnake.logging as logging
logging.setup_logging(level='DEBUG', filename="batch_add_aos.log", filemode="a")

secretsVersion = input('To edit production server, enter the name of the \
secrets file: ')

if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print('Editing Production')
    except ImportError:
        secrets = __import__('secrets')
        print('Editing Development')
else:
    print('Editing Development')   

aspace = ASpace(baseurl=secrets.baseURL,
                      username=secrets.user,
                      password=secrets.password)

#Log Into ASpace and set repo
aspace_client = ASnakeClient(baseurl=secrets.baseURL,
                      username=secrets.user,
                      password=secrets.password)
aspace_client.authorize()
#Set target repo
repo = aspace_client.get("repositories/2").json()
print("Logged into: " + repo['name'])

ssc_repo = aspace.repositories(2)

#input is CSV with existing resource URIs (column 1) and AO URIs (or resource URIs repeated, if you want to add the new ao as a direct child of the resource) (column1) and other columns for new AO metadata
input_csv = input("Path to CSV Input: ")

#output will be input CSV plus some extra columns for reporting on actions taken, errors, etc.
output_csv = input("Path to CSV Output: ")


#Open Input CSV and iterate over rows
with open(input_csv,'rt') as csvfile, open(output_csv,'wt') as csvout:
    csvin = csv.reader(csvfile)
    next(csvin, None) #ignore header row
    csvout = csv.writer(csvout)
    for row in csvin:

        resource_uri = row[0]
        archival_object_parent_uri = row[1]

#ARCHIVAL OBJECT STUFF

        # Use metadata from CSV to create archival object children of existing archival object
        new_ao_level = row[2]
        new_ao_title = row[3]
        new_ao_date_begin = row[4]
        new_ao_date_type = row[5]
        new_ao_date_expression = row[6]
        new_ao_extent = row[7]
        new_ao_extent_type = row[8]
        new_ao_scope_contents = row[9]

        #Form the new Archival Object JSON - this will need to be edited if, for example, you don't want to add a scope and contents note.
        new_ao_data = {"children": [{"title":new_ao_title , "level": new_ao_level, "publish": True, "extents":[{"number": new_ao_extent, "portion": "whole", "extent_type": new_ao_extent_type}], "notes": [{"jsonmodel_type": "note_multipart", "type": "scopecontent", "subnotes": [{"jsonmodel_type": "note_text", "content":new_ao_scope_contents, "publish": True }], "publish": True }], "dates": [{"expression":new_ao_date_expression, "begin":new_ao_date_begin, "label": "event", "date_type": "single" }], "resource":{"ref":resource_uri}}]}


        #print (new_ao_data)


        #For later....Make some JSON for the Top Container
        top_container_data = {}

        #post archival object as child of specified parent using /children endpoint
        new_ao_post = aspace_client.post(archival_object_parent_uri + '/children', json=new_ao_data).json()

        print (new_ao_post)

        row.append(new_ao_post)

        print ('Created new AO child of: ', new_ao_post['id'])

            # Write a new csv with all the info from the initial csv + the ArchivesSpace uris for the archival and digital objects
        with open(output_csv,'at') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)

            #print a new line for readability in console
        print ('\n')
