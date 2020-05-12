import csv
from dateutil.parser import parse
from slugify import slugify
import re
import logging
import os
import shutil

from pprint import pprint
import pdb

from nonotuck_config import Config

logging.basicConfig(level=logging.DEBUG)

def make_drive_id_index_file(drive_command_path, drive_sync_dir, output_file):
    logging.debug("Fetching Google Drive file ID index")
    os.system(f'{drive_command_path} id -depth 10 "{drive_sync_dir}" > {output_file}')

def parse_drive_id_index(drive_id_index_filename):
    """Parse an index file created by the 'drive' utility.
    Example command for generating the file:
    `drive id -depth 5 COVID-19\ Chronicles\ collecting\ form\ and\ responses/ > drive_id_index.txt`
    """
    with open(drive_id_index_filename, "r") as drive_id_index_file:
        id_path_index = {}
        for line in drive_id_index_file:
            # Skip the first header line
            if re.match("FileId", line) is not None:
                continue
            line_split = re.split("\" +\"", line)
            id = line_split[0].strip('"')
            path = line_split[1].strip('\n').strip('"')
            id_path_index[id] = os.getcwd() + path
    return id_path_index

def drive_url_to_local_filepath(drive_id_index, drive_url):
    id = drive_url.split('id=')[1]
    local_file_path = drive_id_index[id]
    return local_file_path

def map_file_data(row, drive_id_index, accession_id):
    """Take a row and return a data structure of:
    - The submission ID
    - The accession ID
    - The files names/paths, their Google Drive URLs/IDs,
    """
    timestamp = parse(row['Timestamp'])
    epoch_string = str(int(timestamp.timestamp()))
    sani_email = slugify(row['Email Address'])
    # Make a provisional ID just for keeping track of things in this
    # in-between state. Won't be used in AS or preservation system.
    submission_id = epoch_string + "_" + sani_email 
    logging.debug(submission_id)
    files = []
    for file_num in range(1, 9):
        file_uri_field = row['File %s: Upload your file or zipped folder of files' % file_num]
        if len(file_uri_field) > 0:
            drive_url = file_uri_field
            files.append({
                "url": file_uri_field,
                "path": drive_url_to_local_filepath(drive_id_index, drive_url),
                })
            logging.debug(f"File {file_num}: " + file_uri_field)
    return {
      "submission_id": submission_id,
      "accession_id": accession_id,
      "files": files,
    }

def reorganize_files(submission_file_data, destination):
    """Copy the files from the gdrive sync folder into a desired human friendly
    structure in the given destination directory.
    """
    destination_dir_name = submission_file_data['submission_id'] + '_' + submission_file_data['accession_id']
    destination_dir_path = destination + '/' + destination_dir_name
    logging.debug(f"Making dir: {destination_dir_path}")
    os.mkdir(destination_dir_path)
    for file_data in submission_file_data['files']:
        file_basename = os.path.basename(file_data['path'])
        logging.debug(f"Copying {file_basename}")
        shutil.copyfile(file_data['path'], destination_dir_path + '/' + file_basename)

if __name__ == "__main__":
    form_a_filename = "/Users/tchambers/gdrive/COVID-19 Chronicles collecting form and responses/Covid-19 Chronicles contributor form (Responses)_exports/Covid-19 Chronicles contributor form (Responses).csv"
    form_b_filename = "/Users/tchambers/gdrive/COVID-19 Chronicles collecting form and responses/(responses) COVID-19 Chronicles electronic file upload form_exports/(responses) COVID-19 Chronicles electronic file upload form.csv"

    config = Config()
    # config.drive_sync_dir = "/Users/tchambers/gdrive/COVID-19 Chronicles collecting form and responses/"
    # config.drive_id_index_filename = "/Users/tchambers/gdrive/drive_id_index.txt"
    # config.drive_command_path = "/Users/tchambers/go/bin/drive"
    # config.working_dir = "/tmp/workingdir"

#    make_drive_id_index_file(config.drive_command_path, config.drive_sync_dir, config.drive_id_index_filename)
    drive_id_index = parse_drive_id_index(config.drive_id_index_filename)

    with open(form_b_filename, "r") as form_b_fp:
        form_b_reader = csv.DictReader(form_b_fp)
        phoney_id_2 = 0

        for row in form_b_reader:
            # Is this row not blank?
            if len(row['Timestamp']) > 0:
                # Testing rig leave this out when we merge into nonotuck_batch.py
                phoney_id_2 = phoney_id_2 + 1
                accession_id = '9999-A-' + str(phoney_id_2)

                ### The heart of the matter
                # Map google drive URLs to filenames and paths in the synced
                # drive folder
                submission_file_data = map_file_data(row, drive_id_index, accession_id)
                # Now copy the files into a desired human friendly structure
                # in the working directory
                reorganize_files(submission_file_data, config.working_dir)
