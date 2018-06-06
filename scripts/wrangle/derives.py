from copy import copy
from meta.vars import NAME_FIELDS

DERIVATIVES = {
    'nonwhite_pct': lambda x: (x['total_population'] - x['white']) / x['total_population'] * 100,
    'white_pct': lambda x:  x['white'] / x['total_population'] * 100,
    'black_pct': lambda x:  x['black'] / x['total_population'] * 100,
    'asian_pct': lambda x:  x['asian'] / x['total_population'] * 100,
    'hispanic_latino_pct': lambda x:  x['hispanic_latino'] / x['total_population'] * 100,
    'renter_occupied_pct': lambda x: x['renter_occupied'] / x['total_households'] * 100,
    'owner_occupied_pct': lambda x: x['owner_occupied'] / x['total_households'] * 100,
    'homes_over_1m': lambda x: (x['homes_between_15m_19m'] + x['homes_between_1m_15m'] + x['homes_over_2m']),
    'homes_over_1m_pct': lambda x: 100 * x['homes_over_1m'] / x['owner_occupied'],
    'rented_less_than_year_ago_pct': lambda x: 100 * x['moved_in_less_than_year_ago'] / x['total_renters'],
    'rented_past_5_years_ago_pct': lambda x: 100 * (x['moved_in_1_to_5_years_ago'] + x['moved_in_less_than_year_ago']) / x['total_renters'],
    'bachelors_pct': lambda x: x['have_bachelors'] / x['population_25_to_64_years'] * 100,
    'poverty_pct': lambda x: x['below_poverty'] / x['poverty_population'] * 100,
    'income_200k_pct': lambda x: x['income_over_200k'] / x['total_households'] * 100,
    'born_in_state_pct': lambda x: x['born_in_state'] / x['total_population'] * 100,
    'born_other_state_pct': lambda x: x['born_other_state'] / x['total_population'] * 100,
    'foreign_born_pct': lambda x: x['foreign_born'] / x['total_population'] * 100,
    'english_only_pct': lambda x: x['english_only'] / x['adults'] * 100,
}


def calculate_derivatives(year_record):
    rec = copy(year_record)
    foo = lambda x: x['total_population']
    for key, foo in DERIVATIVES.items():
        if key not in rec:
            try:
                val = foo(rec)
            except ValueError as err:
                raise err
            except ZeroDivisionError as err:
                rec[key] = None
            except TypeError as err:
                # print('key:', key)
                # print('foo:', foo)
                # print('err:', err)
                raise err

            else:
                if '_pct' in key:
                    val = round(val, 2)
                rec[key] = val
    return rec


def calculate_deltas(record, a_year, b_year):

    deltas = {}
    rec_a = record[a_year]
    rec_b = record[b_year]

    for key in rec_a.keys():
        if key not in NAME_FIELDS:
            aval = rec_a.get(key)
            bval = rec_b.get(key)
            try:
                deltas[key] = round(100 * (bval - aval) / aval, 2)
            except ZeroDivisionError as err:
                deltas[key] = None
            except TypeError as err:
                # print('key:', key)
                # print('aval:', aval)
                # print('bval:', bval)
                deltas[key] = None
    return deltas
