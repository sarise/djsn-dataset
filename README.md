# djsn_scrapper

This is a simple script to automate the data collection from 
the Dewan Jaminan Sosial Nasional (DJSN) offical website 
(http://sismonev.djsn.go.id). The website contains statistical 
data related to the Indonesian social welfare system. 
I focus on the state-owned healthcare insurance 
(Jaminan Kesehatan Nasional a.k.a. JKN) data.

_This code is developed on Python 2.7_

## How to use the script
1. Create a virtualenv and install the python module, including its dependency
```
virtualenv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install .
```
Note: When developing `python setup.py develop`

2. Run the script to retrieve the ID of all kabupatens in Indonesia.
```
retrieve_kabupaten_id
# Writing the list of kabupatens in /Users/sari/repositories/djsn_scrapper/output/daftar_kabupaten.json
# Done
```

3. Run the script to download and aggregate data of all kabupatens for a given period of time
```
extract_data --starting-period 11 --months 1
# Start time: 2021-06-18 14:11:29.041660
# Downloading data per kabupaten starting from period 11.
# Number of months: 1
# Writing extracted data to /Users/sari/repositories/djsn_scrapper/output/aggregate_011.csv
# 11
# 366 367 370 368 369 ...
```

## How to parallelize the job
1. Spawn multiple processes with a different starting period 
```
extract_data --starting-period 1 --months 5
extract_data --starting-period 6 --months 5
extract_data --starting-period 11 --months 5
extract_data --starting-period 16 --months 5
extract_data --starting-period 21 --months 5
extract_data --starting-period 26 --months 5
extract_data --starting-period 31 --months 5
extract_data --starting-period 36 --months 5
extract_data --starting-period 41 --months 5
extract_data --starting-period 46 --months 5
extract_data --starting-period 51 --months 5
extract_data --starting-period 56 --months 5
extract_data --starting-period 61 --months 5
```
2. Combine the output files into one csv file. 
   Note that each output file has headers. The final file should only keep one set of headers.
_Assuming that "\_\_tahun" is the starting string of the header line._
```
grep "^__tahun" output/aggregate_001.csv > aggregate.csv && grep -vh "^__tahun" output/aggregate_*csv >> aggregate.csv
```
