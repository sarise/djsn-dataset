import argparse
import csv
import requests
import sys
import uncurl

from datetime import datetime
from urlparse import (
    parse_qsl,
    urlparse,
    urlsplit,
    urljoin,
)

from scrapper.constants import (
    KABUPATEN_IDS_FILE,
    OUTPUT_AGGREGATE_FILE,
    SAMPLE_EXTRACTED_KABUPATEN_FILE, SAMPLE_RAW_FILE,
)

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

DOWNLOAD_CURL = \
'''
curl 'http://180.250.242.162/server_djsn/kepesertaan/proporsi.php?periode=61&propinsi=1&kabupaten=19&tahun=2021&callback=receiveproporsi&_=1623324442259' 
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0' 
-H 'Accept: */*' 
-H 'Accept-Language: en-US,en;q=0.5' 
--compressed 
-H 'Connection: keep-alive' 
-H 'Referer: http://sismonev.djsn.go.id/' 
-H 'Cookie: PHPSESSID=q2hkeork4c0qh17ahfi21eofb0'
'''

DATA_PAGE = 'http://180.250.242.162/server_djsn/kepesertaan/proporsi.php'
session = requests.Session()


def curl_to_url_params_headers_cookies(curl_string):
    context = uncurl.parse_context(curl_string)
    url = urljoin(context.url, urlparse(context.url).path)
    params = parse_qsl(urlsplit(context.url).query)
    return url, params, context.headers, context.cookies


def download_data_kabupaten(periode, propinsi, kabupaten):
    query_params = {
        'periode': periode,
        'propinsi': propinsi,
        'kabupaten': kabupaten,
        'callback': 'receiveproporsi',
        '_': '1623324442259',
    }
    _, _, headers, cookies = curl_to_url_params_headers_cookies(DOWNLOAD_CURL)

    session.headers.update(headers)
    session.cookies.update(cookies)

    r = session.get(DATA_PAGE, allow_redirects=True, params=query_params)
    raw_data = r.content[len('receiveproporsi('):-1]
    return json.loads(raw_data)


def simplify_data(data_kabupaten, kabupaten_id):
    relevant_data = {
        '_kabupaten': kabupaten_id,
        '__tahun': data_kabupaten['periode']['tahun'],
        '_bulan': data_kabupaten['periode']['bln'],
    }
    for key, values in data_kabupaten.iteritems():
        if values and isinstance(values, list):
            for entry in values:
                keys = entry.keys()
                if 'nama' in keys and 'jumlah' in keys:
                    relevant_data['%s %s' %(key, entry['nama'])] = entry['jumlah']

    return relevant_data


def process_kabupaten(periode, propinsi, kabupaten):
    data_kabupaten = download_data_kabupaten(periode, propinsi, kabupaten)
    return simplify_data(data_kabupaten, kabupaten)


def prepare_dummy_for_knowing_headers():
    data_kabupaten = process_kabupaten(periode=1, propinsi=1, kabupaten=1)
    data_kabupaten['_kabupaten_name'] = "fake kabupaten name"

    with open(SAMPLE_EXTRACTED_KABUPATEN_FILE, 'w') as f:
        json.dump(data_kabupaten, f, indent=4, sort_keys=True)


def get_headers_from_dummy():
    with open(SAMPLE_EXTRACTED_KABUPATEN_FILE) as f:
        data_kabupaten = json.load(f)
    return data_kabupaten.keys()


def process(starting_period, months):
    # Retrieve the list of all kabupatens across propinsis
    with open(KABUPATEN_IDS_FILE) as f:
        daftar_kabupaten = json.load(f)

    prepare_dummy_for_knowing_headers()

    output_file = OUTPUT_AGGREGATE_FILE % starting_period
    print('Writing extracted data to %s' % output_file)
    with open(output_file, 'wb') as csvfile:
        headers = get_headers_from_dummy()
        headers = sorted(headers)
        out_csv = csv.DictWriter(csvfile, headers)
        out_csv.writeheader()
        for periode in range(starting_period, starting_period+months):
            if periode > 64:
                return
            print periode

            for propinsi, kabupatens in daftar_kabupaten.iteritems():
                aggregate_propinsi = []
                for kabupaten_id, kabupaten_name in kabupatens.iteritems():
                    print kabupaten_id,
                    data_kabupaten = process_kabupaten(periode=periode, propinsi=propinsi, kabupaten=kabupaten_id)
                    data_kabupaten['_kabupaten_name'] = kabupaten_name
                    aggregate_propinsi.append(data_kabupaten)
                out_csv.writerows(aggregate_propinsi)
                print


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A script to collect the statistical data from DJSN.')
    parser.add_argument('--starting-period', type=int,
                        help='Note: January 2016 is 1')
    parser.add_argument('--months', type=int,
                        help='The number of months to be collected.')
    parser.add_argument('--raw-sample', action='store_true', default=False,
                        help='Only download and store the raw data for a certain kabupaten.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    print('Start time: %s' % datetime.now())

    if args.raw_sample:
        raw_sample = download_data_kabupaten(periode=61, propinsi=1, kabupaten=6)
        print('Writing raw data sample to %s' % SAMPLE_RAW_FILE)
        with open(SAMPLE_RAW_FILE, 'w') as f:
            json.dump(raw_sample, f, indent=4, sort_keys=True)
    else:
        print('Downloading data per kabupaten starting from period %d.\nNumber of months: %d' % (
            args.starting_period,
            args.months
        ))
        process(args.starting_period, args.months)
    print('Done.')


if __name__ == '__main__':
    main()
