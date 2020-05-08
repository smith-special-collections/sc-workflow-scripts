import csv
from dateutil.parser import parse
from slugify import slugify
import re
import logging

import pdb

form_a_filename = "/Users/tchambers/gdrive/COVID-19 Chronicles collecting form and responses/Covid-19 Chronicles contributor form (Responses)_exports/Covid-19 Chronicles contributor form (Responses).csv"
form_b_filename = "/Users/tchambers/gdrive/COVID-19 Chronicles collecting form and responses/(responses) COVID-19 Chronicles electronic file upload form_exports/(responses) COVID-19 Chronicles electronic file upload form.csv"
drive_id_index_filename = "/Users/tchambers/gdrive/drive_id_index.txt"

def make_drive_id_index(drive_id_index_filename):
    with open(drive_id_index_filename, "r") as drive_id_index_file:
        id_path_index = {}
        for line in drive_id_index_file:
            # Skip the first header line
            if re.match("FileId", line) is not None:
                continue
            line_split = re.split("\" +\"", line)
            id = line_split[0].strip('"')
            path = line_split[1].strip('"')
            id_path_index[id] = path
    return id_path_index

drive_id_index = make_drive_id_index(drive_id_index_filename)

def drive_url_to_local_filepath(drive_id_index, drive_url):
    id = drive_url.split('id=')[1]
    return[drive_id_index[id]]


with open(form_b_filename, "r") as form_b_fp:
    form_b_reader = csv.DictReader(form_b_fp)
    phoney_id_2 = 0
    submissions = []
    for row in form_b_reader:
        if len(row['Timestamp']) > 0:
            timestamp = parse(row['Timestamp'])
            epoch_string = str(int(timestamp.timestamp()))
            sani_email = slugify(row['Email Address'])
            submission_id = epoch_string + "__" + sani_email
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
            submissions.append({
              "submission_id": submission_id,
              "files": files,
            })

pdb.set_trace()
