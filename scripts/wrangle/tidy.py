import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from collections import defaultdict

from pathlib import Path
from meta.vars import get_acs_variable_keys
from meta.geo import get_state_fips
from wrangle.gentrify import calculate_gentrification
import re
import csv
import json
NAME_FIELDS = ['id', 'geo_id', 'name', 'geo']

DESTDIR = Path('data', 'wrangle')
DESTDIR.mkdir(exist_ok=True)

from copy import copy

DEC_PAT = re.compile(r'\d+\.\d+')


DATA_PATH = Path('data')
GEO_NAMES = ['us', 'state', 'county', 'tract']

def read_acs_file(year=2016, geo='us', state_fips=None):
    dpath = DATA_PATH.joinpath('acs', str(year))
    if geo == 'tract':
        dpath = dpath.joinpath(geo, '{}.csv'.format(state_fips))
    else:
        dpath = dpath.joinpath('{}.csv'.format(geo))
    records = list(csv.DictReader(dpath.read_text().splitlines()))
    return records

def collect_acs_files(years=[2011, 2016], geonames=['us', 'state', 'county']):
    """
        {'2016': {'01': {}}, '2011': {'01': {}}}

    """
    results = {}
    for y in years:
        yr = str(y)
        results[yr] = res = {}
        varmap = get_acs_variable_keys(yr)
        for geo in geonames:
            data = read_acs_file(yr, geo, state_fips=None)
            for d in data:
                # create a wrangled version of d
                x = {}
                for k, v in d.items():
                    vmeta = varmap.get(k.strip('E'))
                    if vmeta:
                        if v.isnumeric():
                            val = int(v)
                        elif DEC_PAT.search(v):
                            val = float(v)
                        else:
                            val = v
                        x[vmeta['slug']] = val
                x['name'] = d['NAME']
                x['id'] =  x['geo_id'] = d['GEO_ID']
                x['geo'] = geo
                res[x['id']] = x
    return results



def collate(data, first_year=2011, last_year=2016):
    results = []
    iyear = str(first_year)
    jyear = str(last_year)
    xdata = data[iyear]
    ydata = data[jyear]

    for id, xrow in xdata.items():
        yrow = ydata.get(id)
        if yrow:
            d = {}
            d[iyear] = xrow
            d[jyear] = yrow
            results.append(d)

    return results


def wrangle(data=None, xyear='2011', yyear='2016'):
    if data is None:
        _x = collect_acs_files()
        data = collate(_x, xyear, yyear)

    results = []
    for d in data:
        results.append(wrangle_record(d))
    return results


def wrangle_record(record, xyear='2011', yyear='2016'):
    rec = {}
    xyear = str(xyear)
    yyear = str(yyear)
    for yr in [xyear, yyear]:
        x = rec[yr] = copy(record[yr])

        # race
        x['nonwhite_pct'] =  (x['total_population'] - x['white']) / x['total_population'] * 100
        x['white_pct'] = x['white'] / x['total_population'] * 100

        # housing
        x['renter_occupied_pct'] = x['renter_occupied'] / x['total_households'] * 100
        x['owner_occupied_pct'] = x['owner_occupied'] / x['total_households'] * 100

        if yr == '2016':
            x['homes_over_1m'] = (x['homes_between_15m_19m'] +
                                                    x['homes_between_1m_15m'] +
                                                    x['homes_over_2m'])

        if x['owner_occupied'] == 0:
            x['homes_over_1m_pct'] = 0
        else:
            x['homes_over_1m_pct'] = 100 * x['homes_over_1m'] / x['owner_occupied']



#        x['moved_in_5_years_ago'] = x['moved_in_1_to_5_years_ago'] + x['moved_in_less_than_year_ago']
        x['moved_in_less_than_year_ago_pct'] = 100 * x['moved_in_less_than_year_ago'] / x['total_population']

        # education
        x['bachelors_pct'] = x['have_bachelors'] / x['population_25_to_64_years'] * 100
        # poverty income
        x['poverty_pct'] = x['below_poverty'] / x['poverty_population'] * 100
        x['income_200k_pct'] =  x['income_over_200k'] / x['total_households'] * 100
        # origins
        x['born_in_state_pct']    = x['born_in_state'] / x['total_population'] * 100
        x['born_other_state_pct'] = x['born_other_state'] / x['total_population'] * 100
        x['foreign_born_pct']    = x['foreign_born'] / x['total_population'] * 100
        x['english_only_pct']  =  x['english_only'] / x['adults'] * 100


    deltas = rec['delta'] = {}

    x = rec[xyear]
    for key in x.keys():
        if key not in NAME_FIELDS:
            denom = rec[xyear][key]

            try:
                if denom == 0:
                    deltas[key] = 0
                else:
                    deltas[key] = round(100 * (rec[yyear][key] - denom) / denom, 2)
            except TypeError as err:
                deltas[key] = None
    for n in NAME_FIELDS:
        rec[n] = x[n]

    rec['gentrification'] = calculate_gentrification(rec)

    ## gentrify

    return rec




def flatten(data, xyear='2011', yyear='2016'):
    prefixes = ['gentrification', 'delta', xyear, yyear]
    results = []
    for d in data:
        r = {}
        for n in NAME_FIELDS:
            r[n] = d[xyear][n]  # name fields
        for p in prefixes:
            e = d[p]
            for k in e.keys():
                fkey = p + '_' + k
                try:
                    r[fkey] = e[k]
                except KeyError:
                    print(p, k, fkey)
        results.append(r)
    return results







if __name__ == '__main__':

    data = wrangle()
    flatdata = flatten(data)

    headers = flatdata[0].keys()
    destpath = DESTDIR.joinpath('records.csv')
    with open(destpath, 'w') as f:
        o = csv.DictWriter(f, fieldnames=headers)
        o.writeheader()
        o.writerows(flatdata)



# def wrangle(data, first_year=2011, last_year=2016):
#     results = []
#     iyear = str(first_year)
#     jyear = str(last_year)
#     xdata = data[iyear]
#     ydata = data[jyear]









# def map_acs_files(years=[2011, 2016], geos=GEO_NAMES):
#     results = {}
# #    state_fips_codes = get_state_fips()
#     for geo in GEO_NAMES:
#         data = read_acs_file(yr, geo, state_fips)

#         for d in data:
#             x = {}
#             for k, v in d.items():
#                 vmeta = varmap.get(k.strip('E'))
#                 if vmeta:
#                     x[vmeta['slug']] = v
#             x['name'] = d['NAME']
#             x['id'] =  x['geo_id'] = d['GEO_ID']
#             x['geo'] = geo
#             res.append(x)


#     for y in years:
#         yr = str(y)
#         varmap = get_acs_variable_keys(yr)
#         res = results[yr] = {}
#             return results



# # def map_acs_file(years=[2011,2016], geo='us', state_fips=None):
# #     results = {}
# #     for y in years:
# #         yr = str(y)
# #         for geo in ['us']:
# #         data = read_acs_file(yr, geo, state_fips)

# #         res = results[yr]


# #     varmap = get_acs_variable_keys(year)
# #     for d in data:
# #         x = {}
# #         for k, v in d.items():
# #             vmeta = varmap.get(k.strip('E'))
# #             if vmeta:
# #                 x[vmeta['slug']] = v

# #         x['name'] = d['NAME']
# #         x['id'] =  x['geo_id'] = d['GEO_ID']
# #         results.append(x)
# #     return results






# def convert_acs_to_dicts(year=2016, geo='us'):
#     # first row is headers
#     records = read_acs_file(year, geo)
#     headers = records[0]
#     rows = records[1:]


