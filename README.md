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
# Writing the list of kabupatens in output/daftar_kabupaten.json
# Done
```


