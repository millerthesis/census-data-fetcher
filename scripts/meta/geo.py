import csv
from pathlib import Path, PosixPath


STATECODES_PATH = Path('metadata', 'statecodes.csv')

VALID_GEOGRAPHIES = {
    'acs': {
        'us': {'for': 'us:*'},
        'state': {'for': 'state:*'},
        'county': {'for': 'county:*'},
        'tract': {'for': 'tract:*', 'in': 'state:{state_fips}'},
    },

    # https://api.census.gov/data/2010/sf1/geography.html
    'cen': {
        'state': {'for':'state:*'},
        'county': {'for':'county:*'},
        'tract': {'for': 'tract:*', 'in': 'state:{state_fips}'},
    }
}




def get_state_meta():
    with open(STATECODES_PATH) as w:
        return list(csv.DictReader(w))

def get_state_fips():
    return [c['fips'] for c in get_state_meta()]
