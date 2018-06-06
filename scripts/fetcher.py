# from api.dec import batch_urls as dec_batch_urls
from api.acs import batch as acs_batch
from meta.config import read_default_api_key
from pathlib import Path
import requests
import csv
import json

DATA_PATH = Path('data')


def fetch_acs(years=[2011], key=read_default_api_key()):
    for year in years:
        print(year)
        destdir = DATA_PATH.joinpath('acs', str(year))
        for geo, _urls in acs_batch(year).items():
            if geo == 'tract':
                destdir = destdir.joinpath('tract')
            destdir.mkdir(exist_ok=True, parents=True)

            for meta, url in _urls:
                print("\t", geo, meta['state_fips'])
                resp = requests.get(url)
                if resp.status_code == 200:
                    if geo == 'tract':
                        dest = destdir.joinpath(meta['state_fips'] + '.csv')
                    else:
                        dest = destdir.joinpath(geo + '.csv')
                    with open(dest, 'w') as w:
                        data = json.loads(resp.text)
                        c = csv.writer(w)
                        c.writerows(data)

                else:
                    meta['error'] = 'Status code: {}; {}'.format(resp.status_code, resp.text)
                    meta['url'] = url
                    raise ValueError(meta)

if __name__ == '__main__':
    fetch_acs()
