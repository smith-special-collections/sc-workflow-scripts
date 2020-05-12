from archivesspace import archivesspace
import logging
import re
from datetime import datetime

# Remove these after dev
import pdb
import pickle 
from pprint import pprint


CONFIGFILE = "archivesspace.cfg"

ID_ZERO_PADDING = 4

def DEBUG_print_accessions(accessionS):
    for accession in accessionS:
        try:
            content_description = accession['content_description']
        except KeyError:
            content_description = ''
        try:
            accession_date = accession['accession_date']
        except KeyError:
            accession_date = ''
        print(accession['uri'] + "|" + accession_date + "|" + content_description)

def get_accession_ids(accessionS):
    """Return a list of accession IDs from a list of accession records.
    Does sanity checking on the elements of the IDs to ensure that they follow
    the basic rules of IDs: [Year], [Repo Letter Code], [Incrimenting Number].
    """
    accession_idS = [] # Start an empty list
    for accession in accessionS:
        # Is this a valid ID? Does it follow the rules?
        # If not, just throw it out, assuming that it's irrelevant
        try:
            assert type(int(accession['id_0'])) is int
            assert type(re.match(r"[A-Z]", accession['id_1'])) is re.Match
            assert type(int(accession['id_2'])) is int

            myid = {
                "id_0": accession['id_0'],
                "id_1": accession['id_1'],
                "id_2": accession['id_2'],
            }
            accession_idS.append(myid)
        except Exception as e:
            pass
            # logging.debug(f"Skipping ID for {accession} invalid: {e}")

    return accession_idS

def filter_ids_by_year(accession_idS, year):
    """Takes a list of IDs, and returns a list of only those IDs for a given year.
    """
    ids_for_the_year = [] # Start an empty list
    for accession_id in accession_idS:
        try:
            if int(accession_id['id_0']) == year:
                ids_for_the_year.append(accession_id)
        except ValueError as e:
            logging.error(f"Couldn't get year for {accession_id} invalid: {e}")
    return ids_for_the_year

def get_id_numbers(accession_idS):
    """Return a list of just the number component of a list of accession IDs.
    I.e. only the 'id_2' components. Returns values as *integers*.
    E.g. an input of:
      [{'id_0': '1999', 'id_1': 'A', 'id_2': '0149'},
      {'id_0': '1999', 'id_1': 'A', 'id_2': '0150'},
      {'id_0': '1999', 'id_1': 'A', 'id_2': '0151'}]
    returns:
      ['149', '150', '151']
    """
    
    accession_id_numberS = [] # Start an empty list
    for accession_id in accession_idS:
        accession_id_numberS.append(int(accession_id['id_2']))
    return accession_id_numberS

def get_unique_accession_id(aspace, repository_number, repository_letter_code, all_accessions_data):
    """Contacts the ArchivesSpace API and gets a list of IDs from a given repo.
    Finds the latest ID and returns it in the form of a dictionary.
    e.g. {'id_0': 2020, 'id_1': 'A', 'id_2': '0012'}
    Thise function does not reserve the ID! Nor does it make put requests to AS.
    """
    # What year is it?
    current_year = datetime.now().year
    logging.info(f"Making new ID for {current_year}")
    accessionS = all_accessions_data
#    accessionS = aspace.getPaged(f"/repositories/{repository_number}/accessions")
#    accessionS = pickle.load(open('accessions1109.pickle', 'rb')) # DEBUG trick
    accession_idS = get_accession_ids(accessionS)
    ids_for_this_year = filter_ids_by_year(accession_idS, current_year)
    just_numbers = get_id_numbers(ids_for_this_year)
    just_numbers.sort() # very important
    last_id_number = just_numbers[-1]
    new_id_number = last_id_number + 1
    new_id_number_string = str(new_id_number).zfill(ID_ZERO_PADDING)

    # Now make a new ID
    fresh_id = {
        "id_0": current_year,
        "id_1": repository_letter_code,
        "id_2": new_id_number_string,
    }
    
    return fresh_id
    

if __name__ == "__main__":

    # Example usage:
    aspace = archivesspace.ArchivesSpace()
    aspace.setServerCfg('archivesspace.cfg', section='local')
    aspace.connect()

    fresh_id = get_unique_accession_id(aspace, 4, 'A')
    print(fresh_id)
