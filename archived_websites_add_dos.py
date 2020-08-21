import requests
import json
import csv
import os
import getpass
import uuid

#This script has been modified from the duke_create_do_from_ao_uri.py script written by Noah Huffman at Duke. It has been updated to work in python3 and has had the method of publishing the digital object altered.

# Starting with an input CSV, this script will use the ArchivesSpace API to batch create digital object records and link them as instances of specified archival objects.

# This script assumes you have the Archival Object URIs already.

# The script will write out a CSV containing the same information as the starting CSV plus
# the refIDs and URIs for the archival objects and the the URIs for the created digital objects.

# The 5 column input csv should include a header row and be formatted with the columns identified on line 66:
# Input CSV can be modified to supply additional input metadata for forming the digital objects

#AUTHENTICATION STUFF:

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

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository

auth = requests.post(baseURL + '/users/' + user + '/login?password='
                     + password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}

#FILE INPUT / OUTPUT STUFF:
#prompt for input file path
archival_object_csv = input("Path to input CSV: ")

#prompt for output path
updated_archival_object_csv = input("Path to output CSV: ")


#Open Input CSV and iterate over rows
with open(archival_object_csv,'r') as csvfile, open(updated_archival_object_csv,'w') as csvout:
    csvin = csv.reader(csvfile)
    next(csvin, None) #ignore header row
    csvout = csv.writer(csvout)
    for row in csvin:

#INPUT CSV STUFF. This assumes you have URIs for the already created archival objects. The URI should be formatted like: /repositories/2/archival_objects/407720

        ao_uri = row[0]
        new_do_url = row[1]
        new_do_caption = row[2]
        new_do_id = row[3]
        new_do_title = row[4]
        publish_true_false = row[5]
        repo_id = row[6]

        print ('Found AO: ' + ao_uri)

        # Submit a get request for the archival object and store the JSON
        archival_object_json = requests.get(baseURL+ao_uri,headers=headers).json()

        # Add the archival object uri to the row from the csv to write it out at the end
        row.append(ao_uri)
        #Publish the digital object or not.
        if publish_true_false.lower() == 'false':
            publish = False
        else:
            publish = True

        # If you want to reuse the display string from the archival object as the digital object title, uncomment line 87 and replace
        # 'title':new_do_title in line 91 with 'title':display_string
        # Note: this also does not copy over any notes from the archival object

        display_string = archival_object_json['display_string']

        # Form the digital object JSON using the display string from the archival object and the identifier and the file_uri from the csv

        new_digital_object_json = {'title':display_string,'digital_object_id':new_do_id,'publish':publish,'file_versions':[{'file_uri':new_do_url,'xlink_actuate_attribute':'onRequest','xlink_show_attribute':'new','caption':new_do_caption,'publish':publish}]}
        dig_obj_data = json.dumps(new_digital_object_json)

        # Post the digital object
        dig_obj_post = requests.post(baseURL+'/repositories/'+repo_id+'/digital_objects',headers=headers,data=dig_obj_data).json()

        print ('New DO: ', dig_obj_post)

        # Grab the digital object uri
        dig_obj_uri = dig_obj_post['uri']

        print ('New DO URI: ' + dig_obj_uri)


        # Add the digital object uri to the row from the csv to write it out at the end
        row.append(dig_obj_uri)

        # Build a new instance to add to the archival object, linking to the digital object
        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}
        # Append the new instance to the existing archival object record's instances
        archival_object_json['instances'].append(dig_obj_instance)
        archival_object_data = json.dumps(archival_object_json)
        # Repost the archival object
        archival_object_update = requests.post(baseURL+ao_uri,headers=headers,data=archival_object_data).json()

        print ('New DO added as instance of new AO: ', archival_object_update['status'])

        # Write a new csv with all the info from the initial csv + the ArchivesSpace uris for the archival and digital objects
        with open(updated_archival_object_csv,'a') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)

        #print a new line for readability in console
        print ('\n')
