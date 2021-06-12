# djsn_scrapper

This is a simple script to automate the data collection from 
the Dewan Jaminan Sosial Nasional (DJSN) offical website 
(http://sismonev.djsn.go.id). The website contains statistical 
data related to the Indonesian social welfare system. 
I focus on the state-owned healthcare insurance 
(Jaminan Kesehatan Nasional a.k.a. JKN) data.

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
extract_data 6 1
# 2021-06-12 11:38:36.139625
# Downloading data per kabupaten starting from period 6.
# Number of months: 1
# Writing extracted data to /Users/sari/repositories/djsn_scrapper/output/aggregate_6.csv
# 6
# 366 367 370 368 369
# ...
```

## How to parallelize the job
1. Spawn multiple processes with a different starting period 
```
extract_data 1 5
extract_data 6 5
extract_data 11 5
extract_data 16 5
extract_data 21 5
extract_data 26 5
extract_data 31 5
extract_data 36 5
extract_data 41 5
extract_data 46 5
extract_data 51 5
extract_data 56 5
extract_data 61 5
```
2. Combine the output files into one csv file.
```

```


