from copy import copy
from pathlib import Path, PosixPath
import csv

KEY_PATH = Path('metadata', 'key.txt')
META_PATH = Path('metadata', 'census_meta.csv')
STATECODES_PATH = Path('metadata', 'statecodes.csv')


VALID_GEOGRAPHIES = {
    'us': {'for': 'us:*'},
    'state': {'for': 'state:*'},
    'county': {'for': 'county:*'},
    'tract': {'for': 'tract:*', 'in': 'state:{state_fips}'},
}

def get_geo_params(geo, state_fips=None):
    params = copy(VALID_GEOGRAPHIES.get(geo))
    if type(params) is not dict:
        errmsg = "geo value of '{}' is not in: {}".format(geo, VALID_GEOGRAPHIES.keys())
        raise ValueError(errmsg)

    if geo is 'tract':
        if state_fips is not None:
            params['in'] = params['in'].format(state_fips=state_fips)
        else:
            raise ValueError("For geo of 'tract', must supply a state_fips argument")

    return params


def get_state_codes():
    with open(STATECODES_PATH) as w:
        return list(csv.DictReader(w))

def get_state_fips():
    return [c['fips'] for c in get_state_codes()]


def get_census_api_key(keypath=KEY_PATH):
    if type(keypath) is PosixPath and keypath.exists():
        return keypath.read_text().strip()
    else:
        return ""

def get_tablenames():
    txt = META_PATH.read_text()
    rawdata = csv.DictReader(txt.splitlines())
    data = []
    for row in rawdata:
        if row['for_app'] == 'TRUE':
            d = {}
            d['readable_name'] = row['readable_name']
            d['api_value'] = row['api_value']
            d['dataset'] = row['dataset']
            d['subset'] = row['subset']
            data.append(d)
    return data


def get_acs_tablenames():
    tnames = get_tablenames()
    tnames = [t for t in tnames if 'ACS' in t['dataset']]
    return tnames
# def get_census_fields():
#     fields = [c['api_value'] for c in get_census_meta()]
#     return ['NAME', 'GEO_ID'] + fields



