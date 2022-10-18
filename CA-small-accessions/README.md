Code to create CA Accessions. This tool is for accessioning archivists to bulk add accession records to ArchivesSpace, instead of manually creating individual accession records. It requires Tristan Chambers' [ArchivesSpace module](https://github.com/SmithCollegeLibraries/archivesspace-python) to run, and a config file titled archivesspace.cfg with your test and production connection info.

Download the list of accessions from AirTable. Once downloaded, run the script [rename_CA_form_columns.py](/blob/master/CA-small-accessions/rename_CA_form_columns.py). You must have pandas installed to run this script.
It takes as an input file a CVS titled "CA small accessions-Grid view.csv" and generates an ouput file titled "CA_small_acc.csv"

To run:
```
python3 rename_CA_form_columns.py
```

Once the spreadsheet is renamed you can run the [CA_single_accessions_combined.py](/blob/master/CA-small-accessions/CA_single_accessions_combined.py) script.
To run:
```
python3 CA_single_accessions_combined.py [server] [csv title]
```
for example:
```
python3 CA_single_accessions_combined.py test CA_small_acc.csv
```

Tested with Python 3.8.9.
