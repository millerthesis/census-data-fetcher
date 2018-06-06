import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from pathlib import Path
from meta.vars import get_acs_variable_keys
from meta.geo import get_state_fips
from meta.vars import NAME_FIELDS
from wrangle.gentrify import calculate_gentrification
from wrangle.derives import calculate_derivatives, calculate_deltas
import re
import csv
import json
CENSUS_NULL_VAL = '-666666666'

DESTDIR = Path('data', 'wrangle')
DESTDIR.mkdir(exist_ok=True)

from copy import copy

DEC_PAT = re.compile(r'\d+\.\d+')


DATA_PATH = Path('data')
GEO_NAMES = ['us', 'state', 'county', 'tract']

def read_acs_file(year=2016, geo='us', state_fips=None):
    dpath = DATA_PATH.joinpath('acs', str(year))
    if geo == 'tract':
        records = []
        for fip in get_state_fips():
            _path = dpath.joinpath(geo, '{}.csv'.format(fip))
            data = list(csv.DictReader(_path.read_text().splitlines()))
            records.extend(data)

    else:
        _path = dpath.joinpath('{}.csv'.format(geo))
        records = list(csv.DictReader(_path.read_text().splitlines()))
    return records

def collect_acs_files(years=[2011, 2016], geonames=GEO_NAMES):
    """
        {'2016': {'01': {}}, '2011': {'01': {}}}

    """
    results = {}
    for y in years:
        yr = str(y)
        results[yr] = resyr = {}
        varmap = get_acs_variable_keys(yr)
        for geo in geonames:
            data = read_acs_file(yr, geo, state_fips=None)
            for d in data:
                # create a wrangled version of d
                entry = {}
                entry['name'] = d['NAME']
                entry['geo'] = geo # e.g. 'county'
                entry['id'] =  entry['geo_id'] = d['GEO_ID']
                for k, v in d.items():
                    vm = varmap.get(k.strip('E'))
                    if vm:
                        slug = vm['slug']
                        if v == CENSUS_NULL_VAL:
                            v = None
                        elif v.isnumeric():
                            val = int(v)
                        elif DEC_PAT.search(v):
                            val = float(v)
                        else:
                            val = v
                        entry[slug] = val
                resyr[entry['id']] = entry
    return results



def collate(data, a_year=2011, b_year=2016):
    results = []
    a_year = str(a_year)
    b_year = str(b_year)
    xdata = data[a_year]
    ydata = data[b_year]

    for id, xrow in xdata.items():
        yrow = ydata.get(id)
        if yrow:
            d = {}
            for n in NAME_FIELDS:
                d[n] = xrow[n]
            d[a_year] = xrow
            d[b_year] = yrow
            results.append(d)

    return results


def wrangle(data=None, a_year='2011', b_year='2016'):
    if data is None:
        data = collate(collect_acs_files(), a_year, b_year)
    results = {}
    for d in data:
        idkey = d['id']
        results[idkey] = wrangle_record(d)
    return results


def wrangle_record(record, a_year='2011', b_year='2016'):
    rec = copy(record)
    a_year = str(a_year)
    b_year = str(b_year)

    for yr in [a_year, b_year]:
        rec[yr] = copy(record[yr])

        _dvs = calculate_derivatives(rec[yr])
        rec[yr].update(_dvs)


    rec['delta'] = calculate_deltas(rec, a_year, b_year)
    rec['gentrification'] = calculate_gentrification(rec)


    return rec




def flatten(data, xyear='2011', yyear='2016'):
    prefixes = ['gentrification', 'delta', xyear, yyear]
    results = []
    for id, d in data.items():
        r = {}
        for n in NAME_FIELDS:
            r[n] = d[n]  # name fields
        for p in prefixes:
            e = d[p]
            for k in e.keys():
                fkey = p + '_' + k
                try:
                    r[fkey] = e[k]
                except KeyError:
                    pass
                    # print(p, k, fkey)
        results.append(r)
    return results







if __name__ == '__main__':
    print("Wrangling data...")
    data = wrangle()
    #write JSON
    datavals = data.values()
    for geo in GEO_NAMES:
        jpath = DESTDIR.joinpath(geo + '.json')
        gdata = [d for d in datavals if d['geo'] == geo]
        print(geo, 'data has', len(gdata), 'objects')
        print("Saving JSON to", jpath)
        with open(jpath, 'w') as f:
            f.write(json.dumps(gdata))

    # write CSV
    destpath = DESTDIR.joinpath('records.csv')

    print("Flattening data to save at", destpath)
    flatdata = flatten(data)
    headers = flatdata[0].keys()
    with open(destpath, 'w') as f:
        o = csv.DictWriter(f, fieldnames=headers)
        o.writeheader()
        o.writerows(flatdata)

