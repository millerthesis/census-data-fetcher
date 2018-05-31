from pathlib import Path, PosixPath
import csv
TABLES_PATH = Path('metadata', 'census_meta.csv')


def get_tables(dataset=None, facet=None):
    """
        dataset is string, e.g. "ACS"

        returns list of dicts, or list of strings
    """
    rawtext = TABLES_PATH.read_text()
    records = csv.DictReader(rawtext.splitlines())

    # any filters
    if dataset:
        records = [t for t in records if 'ACS' in t['dataset']]

    result_records = []
    for row in records:
        if row['for_app'] == 'TRUE':
            if not facet:
                d = {}
                d['readable_name'] = row['readable_name']
                d['api_value'] = row['api_value']
                d['dataset'] = row['dataset']
                d['subset'] = row['subset']
            else:
                d = row[facet]
            result_records.append(d)
    return result_records


def get_acs_tablecodes():
    return get_tables(dataset='ACS', facet='api_value')


if __name__ == '__main__':
    for t in get_tables():
        print(t)

    print("\n")
    print("Just ACS codes:")
    for t in get_acs_tablecodes():
        print("\t", t)
