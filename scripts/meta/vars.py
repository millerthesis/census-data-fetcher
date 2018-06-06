from pathlib import Path, PosixPath
import csv
SRC_PATH = Path('metadata', 'canonical_variables.csv')


def get_variables(census_type=None, year=None):
    """
        census_type is string, e.g. "ACS"

        returns list of dicts, or list of strings
    """
    rawtext = SRC_PATH.read_text()
    records = csv.DictReader(rawtext.splitlines())

    # any filters
    if census_type:
        records = [t for t in records if census_type in t['census_type']]

    if year:
        yrstr = str(year)
        records = [t for t in records if yrstr in t['census_year']]


    result_records = []
    for row in records:
        if row['for_app'] == 'TRUE':
            if not facet:
                d = {}
                d['name'] = row['name']
                d['slug'] = row['slug']
                d['variable'] = row['variable']
                d['census_type'] = row['census_type']
                d['census_year'] = year
                d['census_subtype'] = row['census_subtype']
            else:
                d = row[facet]
            result_records.append(d)
    return result_records


def get_acs_variables(year):
    return get_variables(census_type='ACS', year='year')

def get_acs_variable_names(year):
    return [v['variable'] for v in get_acs_variables(year)]


# def get_dec_variable_names(year=year, sumfile):
#     return [v['variable'] for v in get_dec_variables(census_type='DEC', year=year)]

# def get_decs_variables()


def get_acs_variable_keys():
    """
    returns {
        'B00_001': {slug, census_type, census_subtype, etc}
    }
    """
    return {r['variable']: r for r in get_acs_variables() }


if __name__ == '__main__':
    for t in get_variables():
        print(t)

    print("\n")
    print("Just ACS codes:")
    for t in get_acs_variable_names():
        print("\t", t)
