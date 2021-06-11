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

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

SAMPLE_OUTPUT_PER_KABUPATEN = 'sample_extracted_data_per_kabupaten.json'

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
        'aaa_kabupaten': kabupaten_id,
        'aaa_tahun': data_kabupaten['periode']['tahun'],
        'aaa_bulan': data_kabupaten['periode']['bln'],
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
    data_kabupaten['aaa_kabupaten_name'] = "fake kabupaten name"

    with open(SAMPLE_OUTPUT_PER_KABUPATEN, 'w') as f:
        json.dump(data_kabupaten, f, indent=4, sort_keys=True)


def get_headers_from_dummy():
    with open(SAMPLE_OUTPUT_PER_KABUPATEN) as f:
        data_kabupaten = json.load(f)
    return data_kabupaten.keys()


def main(starting_period, months):
    # Retrieve the list of all kabupatens across propinsis
    with open('daftar_kabupaten.json') as f:
        daftar_kabupaten = json.load(f)

    prepare_dummy_for_knowing_headers()

    with open('aggregate_%d.csv' % starting_period, 'wb') as csvfile:
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
                    data_kabupaten['aaa_kabupaten_name'] = kabupaten_name
                    aggregate_propinsi.append(data_kabupaten)
                out_csv.writerows(aggregate_propinsi)
                print


if __name__ == '__main__':
    starting_period = int(sys.argv[1])
    months = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(datetime.now())
    print('Downloading data per kabupubaten starting from period %d.\nNumber of months: %d' % (starting_period, months))
    main(starting_period, months)
