from meta.geo import paramaterize_geo
from meta.geo import get_state_fips
from meta.tables import get_acs_tablecodes
from urllib.parse import urlencode
import re

BASE_ENDPOINT = 'https://api.census.gov/data/{year}/acs/acs5'

TABLENAME_RX = re.compile(r'^([A-Z]\d{5}_\d{3})[ME]?$') # e.g.'B01001_001E'

def generate_tablecodes_for_api(tablecodes):
    """
        tablecodes is list of strings:
            ['B01001_001E']

        returns list of strings
            ['NAME', 'GEO_ID', 'B01001_001E', B01001_001M]
    """
    codes = ['NAME', 'GEO_ID']
    for t in tablecodes:
        _mx = TABLENAME_RX.match(t)
        if not _mx:
            raise ValueError('Tablename "{}" seems invalid'.format(tname))
        t = _mx.groups()[0]
        codes.append(t + 'E')
        codes.append(t + 'M')
    return codes

def paramterize_tablecodes(tablecodes):
    """
    tablecodes is list of strings, e.g. ['B01001_001E']

    returns simple dict:
        {'get': 'NAME,GEO_ID,B01001_001E,B01001_001M'}
    """
    codes = generate_tablecodes_for_api(tablecodes)
    codestr = ','.join(codes)
    return {'get': codestr}




def build_request_params(tablecodes, geo, state_fips=None):
    """
    tablecodes:
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
    params.update(paramaterize_geo(geo, state_fips=state_fips))
    params.update(paramterize_tablecodes(tablecodes))
    return params


def url_for_api_call(year, tablecodes, geo, state_fips=None, api_key=None):
    base_url = BASE_ENDPOINT.format(year=year)
    _params = build_request_params(tablecodes, geo, state_fips)
    if api_key:
        _params['key'] = api_key
    query_string = urlencode(_params, safe=':*,')
    url = base_url + '?' + query_string
    return url



def batch_acs_urls(year, tablecodes, geo, state_fips=None, api_key=None):
    if geo is 'tract':
        fips = get_state_fips()
        urls = [url_for_api_call(
                        year, tablecodes, geo,
                        state_fips=c, api_key=api_key
                ) for c in fips
        ]
    else:
        urls = [url_for_api_call(
                        year, tablecodes,  geo,
                        state_fips=state_fips,
                        api_key=api_key)
        ]
    return urls



if __name__ == '__main__':
    from meta.config import read_default_api_key
    key = read_default_api_key()
    tablecodes = get_acs_tablecodes()

    print("tract urls:")
    urls = batch_acs_urls('2016', tablecodes, 'tract', api_key=key)
    for u in urls:
        print(u)
    print("\n")

    for g in ['county', 'state', 'us']:
        urls = batch_acs_urls('2016', tablecodes, g, api_key=key)
        print("\n")
        print(urls[0])


