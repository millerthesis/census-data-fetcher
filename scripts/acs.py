from pathlib import Path
from scripts.meta import get_census_api_key, get_acs_tablenames
from scripts.meta import get_geo_params

import requests
import csv
from urllib.parse import urlencode

# https://api.census.gov/data/2016/acs/acs5?get=NAME,GEO_ID,B01001_001E,B01001_001M&for=state:06

BASE_ENDPOINT = 'https://api.census.gov/data/{year}/acs/acs5'
# ?get=NAME,GEO_ID,B01001_001E,B01001_001M&for=state:06'



def build_request_params(tablenames, geo, state_fips=None):
    """
    tablenames:
        list of strings (with 'E' and 'M' suffix removed)
        ['B01001_001', 'B01001_002']

    geo:
        a string, like 'county', 'tract', 'state', 'nation'

    optional:
        state_fips: string representing state code, e.g. '06'
    returns:
        dict
    """

    params = {}
    if any(t[-1] in ['E', 'M'] for t in tablenames):
        raise ValueError('Tablenames should not have the E or M suffix, e.g. use B01001_001 not B01001_001E')
    else:
        tpairs = [x for tup in [(f+'E', f+'M') for f in tablenames] for x in tup] # gets E and M of each tablename
        params['get'] = ','.join(['NAME', 'GEO_ID'] + tpairs)

    params.update(get_geo_params(geo, state_fips=state_fips))
    return params


def url_for_api_call(year, tablenames, geo, state_fips=None, api_key=None):
    base_url = BASE_ENDPOINT.format(year=year)
    _params = build_request_params(tablenames, geo, state_fips)
    if api_key:
        _params['key'] = api_key
    query_string = urlencode(_params, safe=':*,')
    url = base_url + '?' + query_string
    return url


"""
from scripts.acs import url_for_api_call
url_for_api_call('2016', ['B01001_001'], 'state')
"""
