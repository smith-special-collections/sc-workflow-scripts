from asnake.aspace import ASpace
import argparse
import logging
import csv
import pprint
import json

#This script was edited from one Claire Marshall wrote to edit Archival Objects. It has been edited to instead edit digital objects. It can be used to either add a new digital object to an existing archival object or add file versions to an existing digital object.

#Requires as input a csv file with the following columns: repo_id, ao_uri, do_uri, do_publish, do_new_title, do_id, do_type, pres_fileuri, access_fileuri, public_fileuri, public_caption, thumb_fileuri

#Allowable DO types include cartographic, mixed_materials, moving_image, notated_music, software_multimedia, sound_recording, sound_recording_musical, sound_recording_nonmusical, still_image, and text

#This script requires ArchivesSnake to run.

#Defining the JSON for adding a preservation file version.
def add_pres_fv(pres_fileuri):
    pres_fv_dict =  {'file_uri': pres_fileuri,
    'publish': False,
    'jsonmodel_type': 'file_version',
    'caption':'preservation file'
    }

    return pres_fv_dict

#Defining the JSON for adding an access file version.
def add_access_fv(access_fileuri):
    access_fv_dict =  {'file_uri': access_fileuri,
    'publish': False,
    'jsonmodel_type': 'file_version',
    'caption':'access file'
    }

    return access_fv_dict

#Defining the JSON for adding a public file version.
def add_public_fv(public_fileuri):
    public_fv_dict =  {'file_uri': public_fileuri,
    'publish': True,
    'caption': row['public_caption'],
    'jsonmodel_type': 'file_version',
    'xlink_actuate_attribute':'onRequest',
    'xlink_show_attribute':'new'
    }

    return public_fv_dict

#Defining the JSON for adding a thumbnail file version.
def add_thumb_fv(thumb_fileuri):
    thumb_fv_dict =  {'file_uri': thumb_fileuri,
    'publish': True,
    'jsonmodel_type': 'file_version',
    'xlink_actuate_attribute': 'onLoad',
    'xlink_show_attribute': 'embed',
    'use_statement': 'image-thumbnail',
    }

    return thumb_fv_dict

# def make_new_do():
#     {'title':display_string,
#     'digital_object_id':new_do_id,
#     'publish':do_publish}

#authentication stuff
if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Take CSV of locations uris and attach to corresponding top container")
    argparser.add_argument("CSV_FILE", help="CSV file of location data")
    cliargs = argparser.parse_args()

    aspace = ASpace()

    logging.basicConfig(level=logging.INFO)

#opening the csv file, getting the existing digital object, adding the file version
    with open(cliargs.CSV_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print (row.keys())

            if len(str(row['ao_uri'])) != 0:
                #archival_object_json = aspace.client.get(row['ao_uri']).json()
                record = aspace.client.get(row['ao_uri']).json()
                print("Found AO: " + row['ao_uri'] + ", making new digital object.")
                #print(record)
                if len(str(row['do_new_title'])) != 0:
                    display_string = row['do_new_title']
                else:
                    display_string = record['display_string']
                if row['do_publish'].lower() == 'false':
                    publish = False
                else:
                    publish = True
                new_digital_object = {'title':display_string,
                    'digital_object_id':row['do_id'],
                    'publish':publish,
                    'file_versions': []}
                if len(str(row['pres_fileuri'])) != 0:
                    pres_file_version = add_pres_fv(row['pres_fileuri'])
                    new_digital_object['file_versions'].append(pres_file_version)
                if len(str(row['access_fileuri'])) != 0:
                    access_file_version = add_access_fv(row['access_fileuri'])
                    new_digital_object['file_versions'].append(access_file_version)
                if len(str(row['public_fileuri'])) != 0:
                    public_file_version = add_public_fv(row['public_fileuri'])
                    new_digital_object['file_versions'].append(public_file_version)
                if len(str(row['thumb_fileuri'])) != 0:
                    thumb_file_version = add_thumb_fv(row['thumb_fileuri'])
                    new_digital_object['file_versions'].append(thumb_file_version)
                new_digital_object['digital_object_type'] = row['do_type']
                print(" New digital object created for AO, identifier " + row['do_id'])
                #print(new_digital_object)
                try:
                    dig_obj_post = aspace.client.post('/repositories/'+row['repo_id']+'/digital_objects',json=new_digital_object).json()
                    print(dig_obj_post)
                    print('Successful addition of digital object {}'.format(dig_obj_post['uri']))
                    # Build a new instance to add to the archival object, linking to the digital object
                except:
                    print('Failed update at the digital object stage for {}'.format(row['ao_uri']))
                if dig_obj_post['uri']:
                    dig_obj_instance = {'instance_type':'digital_object','jsonmodel_type':'instance','digital_object':{'ref':dig_obj_post['uri']}}
                    print("  This is the digital object instance: ")
                    print(dig_obj_instance)
                    # Append the new instance to the existing archival object record's instances
                    record['instances'].append(dig_obj_instance)
                    print("  This is the record: ")
                    print(record)
                    archival_object_data = record
                    # Repost the archival object
                    try:
                        archival_object_update = aspace.client.post(row['ao_uri'],json=archival_object_data).json()
                        print(archival_object_update)
                        print ('New DO added as instance of new AO: ', archival_object_update['status'])
                    except:
                        print('Failed update at the archival object stage for {}'.format(row['ao_uri']))
                


            else:
                record = aspace.client.get(row['do_uri']).json()
                print("Found DO: " + row['do_uri'] + ", adding file versions.")
                print(record)
                if len(str(row['pres_fileuri'])) != 0:
                    print(" Preservation file version being added.")
                    pres_file_version = add_pres_fv(row['pres_fileuri'])
                    record['file_versions'].append(pres_file_version)
                if len(str(row['access_fileuri'])) != 0:
                    print(" Access file version being added.")
                    access_file_version = add_access_fv(row['access_fileuri'])
                    record['file_versions'].append(access_file_version)
                if len(str(row['public_fileuri'])) != 0:
                    print(" Public file version being added.")
                    public_file_version = add_public_fv(row['public_fileuri'])
                    record['file_versions'].append(public_file_version)
                if len(str(row['thumb_fileuri'])) != 0:
                    print(" Thumbnail file version being added.")
                    thumb_file_version = add_thumb_fv(row['thumb_fileuri'])
                    record['file_versions'].append(thumb_file_version)
                record['digital_object_type'] = row['do_type']
                print(" Done adding file versions")
                print(record)

#repost the digital object that you just updated
                try:
                    post = aspace.client.post(record['uri'], json="record").json()
                    print(post)
                    print('Successful update for {}'.format(post['uri']))
                except:
                    print('Failed update for {}'.format(row['do_uri']))
