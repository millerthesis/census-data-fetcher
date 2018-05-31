from pathlib import Path
import requests
import csv

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
    if geo is 'us':
        params['for'] = 'us:*'
    elif geo is 'state':
        params['for'] = 'state:*'
    elif geo is 'county':
        params['for'] = 'county:*'
    elif geo is 'tract' and state_fips is not None:
        params['for'] = 'tract:*'
        params['in'] = 'state:{}'.format(state_fips)
    else:
        raise ValueError('geo must be us, state, county, tract + state_fips')
    return params



def call_api(year, tablenames, geo, state_fips=None):
    myparams = build_request_params(tablenames, geo, state_fips)
    baseurl = BASE_ENDPOINT.format(year=year)
    resp = requests.get(baseurl, params=myparams)
    return resp


