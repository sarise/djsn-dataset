import json
import os

import requests
import uncurl
from urlparse import (
    parse_qsl,
    urlparse,
    urlsplit,
    urljoin,
)

OUTPUT_DIR = 'output'

DOWNLOAD_CURL = \
'''
curl 'http://180.250.242.162/server_djsn/store/kabupatenDataStore.php?propinsi=2&callback=receivekabupatendatastore&_=1623324442265' 
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0' 
-H 'Accept: */*' 
-H 'Accept-Language: en-US,en;q=0.5' 
--compressed 
-H 'Connection: keep-alive' 
-H 'Referer: http://sismonev.djsn.go.id/' 
-H 'Cookie: PHPSESSID=q2hkeork4c0qh17ahfi21eofb0'
'''

DATA_PAGE = 'http://180.250.242.162/server_djsn/store/kabupatenDataStore.php'


def curl_to_url_params_headers_cookies(curl_string):
    context = uncurl.parse_context(curl_string)
    url = urljoin(context.url, urlparse(context.url).path)
    params = parse_qsl(urlsplit(context.url).query)
    return url, params, context.headers, context.cookies


def download_kabupatens(propinsi):
    query_params = {
        'propinsi': propinsi,
        'callback': 'receivekabupatendatastore',
        '_': '1623324442265',
    }
    _, _, headers, cookies = curl_to_url_params_headers_cookies(DOWNLOAD_CURL)

    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)

    r = session.get(DATA_PAGE, allow_redirects=True, params=query_params)
    raw_data = r.content[len('receivekabupatendatastore('):-1]
    kabupatens = json.loads(raw_data)['topics']

    result = {}
    for entry in kabupatens:
        result[entry['id']] = entry['name']

    return result


def main():
    all_propinsi = {}
    for propinsi_id in range(1, 35):
        all_propinsi[propinsi_id] = download_kabupatens(propinsi=propinsi_id)

    try:
        os.makedirs(OUTPUT_DIR)
    except OSError:
        if not os.path.isdir(OUTPUT_DIR):
            raise

    output_file = os.path.join(OUTPUT_DIR, 'daftar_kabupaten.json')

    print('Writing the list of kabupatens in %s' % output_file)
    with open(output_file, 'w') as f:
        json.dump(all_propinsi, f, indent=4, sort_keys=True)
    print('Done')


if __name__ == '__main__':
    main()
