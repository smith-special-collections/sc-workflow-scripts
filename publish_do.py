import requests
import json
import csv
import os
import getpass

#This script was updated from one written by Noah Huffman at Duke. It has been updated to work with python3, has been changed from using the find_by_id endpoint to finding a digital object using a uri instead, and has had the authentication method altered.

#Script currently takes a CSV as input (with DO uri in first column) and publishes or unpublishes the DO--as specified in script on line 58.

#Script also requires as input a secrets.py file with the authentication information. See line 26 for the information the secrets file should contain.

#Authenticate and get a session token
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

#Prompt for the input and output csv files
input_csv = input('Path to input CSV: ')
output_csv = input('Path to output CSV: ')

#Open the input CSV file and iterate through each row
with open(input_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(csvfile, None) #ignore header row
    for row in reader:

#Get info from CSV
        digital_object_uri = row[0]

        print ('Looking up Digital Object: ' + digital_object_uri)

        try:

            # Submit a get request for the digital object and store the JSON
            digital_object_json = requests.get(baseURL+digital_object_uri,headers=headers).json()

            #CHANGE AS APPROPRIATE (True=publish or False=unpublish)
            digital_object_json['publish'] = True

            digital_object_data = json.dumps(digital_object_json)
            do_update = requests.post(baseURL+digital_object_uri,headers=headers,data=digital_object_data).json()

            print ('Status: ' + do_update['status'])
            #print confirmation that digital object was updated. Response should contain any warnings. Response will not indicate if digital object was already set to the status you wanted to change it to.
            row.append(do_update['status'])
        except:
            print ('OBJECT NOT FOUND: ' + digital_object_uri)
            row.append('ERROR: OBJECT NOT FOUND')

        with open(output_csv,'a') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)
        #print a new line to the console, helps with readability
        print ('\n')
print ("All done")
