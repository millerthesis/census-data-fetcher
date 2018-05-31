import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from copy import copy
from meta.geo import VALID_GEOGRAPHIES
from urllib.parse import urlencode

def paramterize_variables(variables):
    """
    variables is list of strings, e.g. ['B01001_001E']

    returns simple dict:
        {'get': 'NAME,GEO_ID,B01001_001E,B01001_001M'}
    """
    codes = ['NAME'] + variables
    codestr = ','.join(codes)
    return {'get': codestr}


def paramaterize_geo(api, geo, state_fips=None):
    params = copy(VALID_GEOGRAPHIES[api].get(geo))
    if type(params) is not dict:
        errmsg = "geo value of '{}' is not in: {}".format(geo, VALID_GEOGRAPHIES.keys())
        raise ValueError(errmsg)

    if geo is 'tract':
        if state_fips is not None:
            params['in'] = params['in'].format(state_fips=state_fips)
        else:
            raise ValueError("For geo of 'tract', must supply a state_fips argument")

    return params



def parameterize(api, variables, geo, state_fips=None):
    """
    variables:
        list of strings (with 'E' and 'M' suffix removed)
        ['B01001_001', 'B01001_002']

    api:
        string, like 'acs', 'cen'

    geo:
        a string, like 'county', 'tract', 'state', 'nation'

    optional:
        state_fips: string representing state code, e.g. '06'
    returns:
        dict
    """

    params = {}
    params.update(paramterize_variables(variables))
    params.update(paramaterize_geo(api, geo, state_fips=state_fips))
    return params


def api_url(api, endpoint, variables, geo, state_fips=None, api_key=None):
    _params = parameterize(api, variables, geo, state_fips)

    if api_key:
        _params['key'] = api_key
    query_string = urlencode(_params, safe=':*,')
    url = endpoint + '?' + query_string
    return url

