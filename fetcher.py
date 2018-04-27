from meta import get_census_client, get_census_fields
from pathlib import Path
import csv

THE_GEOGRAPHIES = [
    'us', 'state', 'county'
]


def fetch(geo):
    cclient = get_census_client()
    fields = get_census_fields()
    forwhat = '{g}:*'.format(g=geo)
    params = {'for': forwhat}
    data = cclient.acs5.get(fields, params)
    for row in data:
        row

    return data


def savecsv(destname, data):
    f = open(destname, 'w')
    c = csv.DictWriter(f, fieldnames=get_census_fields(), extrasaction='ignore')
    c.writeheader()
    c.writerows(data)
    f.close()



def fetch_and_save_all():
    for geo in THE_GEOGRAPHIES:        
        print("Fetching:", geo)
        data = fetch(geo)
        print("     Fetched", len(data), 'records...')
        # now write to file
        destname = Path('data', geo + '.csv')
        savecsv(destname, data)
        print("     Saved to", destname)
        






