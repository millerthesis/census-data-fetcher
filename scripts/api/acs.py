import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from api.generic import api_url as generic_api_url
from meta.geo import get_state_fips
from meta.vars import get_acs_variable_names
import re

VALID_YEARS = ['2011', '2016']
BASE_ENDPOINT = 'https://api.census.gov/data/{year}/acs/acs5'
VARNAME_RX = re.compile(r'^([A-Z]\d{5}_\d{3})[ME]?$') # e.g.'B01001_001E'


def api_url(year, variables, geo, state_fips=None, api_key=None):
    endpoint = BASE_ENDPOINT.format(year=year)
    cleanedcodes = __filter_api_variables(variables)
    url = generic_api_url('acs', endpoint, cleanedcodes, geo, state_fips, api_key)
    return url


def batch_urls(year, variables, geo, state_fips=None, api_key=None):
    if geo is 'tract':
        fips = get_state_fips()
        urls = [api_url(
                        year, variables, geo,
                        state_fips=c, api_key=api_key
                ) for c in fips
        ]
    else:
        urls = [api_url(
                        year, variables,  geo,
                        state_fips=state_fips,
                        api_key=api_key)
        ]
    return urls



def __filter_api_variables(variables):
    """
        variables is list of strings:
            ['B01001_001E']

        returns list of strings
            ['GEO_ID', 'B01001_001E', B01001_001M]
    """
    codes = ['GEO_ID']
    for t in variables:
        _mx = VARNAME_RX.match(t)
        if not _mx:
            raise ValueError('Variable name "{}" seems invalid'.format(tname))
        t = _mx.groups()[0]
        codes.append(t + 'E')
        codes.append(t + 'M')
    return codes



if __name__ == '__main__':
    from meta.config import read_default_api_key
    key = read_default_api_key()
    variables = get_acs_variable_names()

    print("tract urls:")
    urls = batch_urls('2016', variables, 'tract', api_key=key)
    for u in urls:
        print(u)
    print("\n")

    for g in ['county', 'state', 'us']:
        urls = batch_urls('2016', variables, g, api_key=key)
        print("\n")
        print(urls[0])


