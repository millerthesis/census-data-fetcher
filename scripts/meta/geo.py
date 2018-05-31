from copy import copy
import csv
from pathlib import Path, PosixPath


STATECODES_PATH = Path('metadata', 'statecodes.csv')

VALID_GEOGRAPHIES = {
    'us': {'for': 'us:*'},
    'state': {'for': 'state:*'},
    'county': {'for': 'county:*'},
    'tract': {'for': 'tract:*', 'in': 'state:{state_fips}'},
}

def paramaterize_geo(geo, state_fips=None):
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


def get_state_meta():
    with open(STATECODES_PATH) as w:
        return list(csv.DictReader(w))

def get_state_fips():
    return [c['fips'] for c in get_state_meta()]
