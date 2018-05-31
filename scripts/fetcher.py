from scripts.meta import get_census_api_key
from scripts.meta import get_state_fips
from scripts.acs import url_for_api_call as acs_url


def batch_acs_urls(year, tablenames, geo, state_fips=None, api_key=None):
    if geo is 'tract':
        codes = get_state_fips()
        urls = [acs_url(year, tablenames, geo,
                        state_fips=c, api_key=api_key) for c in codes]
    else:
        urls = [acs_url(year, tablenames,  geo,
                                state_fips=state_fips, api_key=api_key)]
    return urls


    cclient = get_census_client()
    fields = get_census_fields()
    forwhat = '{g}:*'.format(g=geo)
    params = {'for': forwhat}
    data = cclient.acs5.get(fields, params)
    for row in data:
        row

    return data

"""
from scripts.fetcher import batch_acs_urls
batch_acs_urls('2016', ['B01001_001'], 'state')
batch_acs_urls('2016', ['B01001_001'], 'tract')

"""
