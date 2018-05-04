from pathlib import Path
from census import Census
import csv

KEY_PATH = Path('config', 'key.txt')
META_PATH = Path('config', 'census_meta.csv')

def get_key():
    return KEY_PATH.read_text().strip()

def get_census_client(key=get_key()):
    return Census(key=key)

def get_census_meta():
    txt = META_PATH.read_text()
    rawdata = csv.DictReader(txt.splitlines())
    data = []
    for row in rawdata:
        if row['for_app'] == 'TRUE':
            d = {}
            d['readable_name'] = row['readable_name']
            d['api_value'] = row['api_value']
            data.append(d)
    return data


def get_census_fields():
    fields = [c['api_value'] for c in get_census_meta()]
    return ['NAME', 'GEO_ID'] + fields

