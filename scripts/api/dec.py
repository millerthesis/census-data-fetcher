import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# https://www.census.gov/data/developers/data-sets/decennial-census.html
# api.census.gov/data/2010/sf1?get=NAME,P0010001&for=state:*&key=[user key]

from api.generic import api_url as generic_api_url
from meta.geo import get_state_fips
import re


VALID_YEARS = ['2000', '2010']
BASE_ENDPOINT = 'https://api.census.gov/data/{year}/{sumfile}'
TABLENAME_RX = re.compile(r'x')

def __filter_api_variables(variables):
   return variables

def api_url(year, sumfile, variables, geo, state_fips=None, api_key=None):
    endpoint = BASE_ENDPOINT.format(year=year, sumfile=sumfile)
    cleanedcodes = __filter_api_variables(variables)
    url = generic_api_url('cen', endpoint, cleanedcodes, geo, state_fips, api_key)
    return url

def batch_urls(year, sumfile, variables, geo, state_fips=None, api_key=None):
    if geo is 'tract':
        fips = get_state_fips()
        urls = [api_url(
                        year, sumfile, variables, geo,
                        state_fips=c, api_key=api_key
                ) for c in fips
        ]
    else:
        urls = [api_url(
                        year, sumfile, variables,  geo,
                        state_fips=state_fips,
                        api_key=api_key)
        ]
    return urls


# def batch(year, sumfile, api_key=None):
#     variables = get_acs_variable_names(year=year)
#     urls = []
#     for g in ['tract', 'county', 'state']:
#         urls.extend(batch_urls(year, variables, 'tract', api_key=api_key))
#     return urls



if __name__ == '__main__':
    from meta.config import read_default_api_key
    key = read_default_api_key()
    variables = ['P0010001', 'P0030001']

    # print("tract urls:")
    # urls = batch_urls('2016', variables, 'tract', api_key=key)
    # for u in urls:
    #     print(u)
    # print("\n")

    for g in ['tract', 'county', 'state',]:
        urls = batch_urls('2010', 'sf1', variables, g, api_key=key)
        print("\n")
        print(g)
        for u in urls:
            print(u)

