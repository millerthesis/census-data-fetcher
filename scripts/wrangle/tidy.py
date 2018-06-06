import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from pathlib import Path
import json
from meta.vars import get_variables

DATA_PATH = Path('data')
GEO_NAMES = ['us', 'state', 'county', 'tract']

def read_acs_file(year=2016, geo='us'):
    dpath = DATA_PATH.joinpath('acs', str(year), geo +'.csv')
    records = json.loads(dpath.read_text())
    return records
    # records = csv.DictReader(dpath.read_text().readlines())


def read_acs_headers(year=2016, geo='us'):
    return get_variables('acs', year=2016)



def convert_acs_to_dicts(year=2016, geo='us'):
    # first row is headers
    records = read_acs_file(year, geo)
    headers = records[0]
    rows = records[1:]
    dicts = []
    for row in rows:
        d = {}
        for i, h in enumerate(headers):
            if h in ['NAME', 'GEO_ID']:
                d[h.lower()] = row[i]
            else:
                d[h] = row[i]
        d['year'] = year
        d['geo'] = geo
        dicts.append(d)
    return dicts



def translate_variable_names(records):
    for r  in records:
        r['']





