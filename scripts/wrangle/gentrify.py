GENTRIFY_VARS = {
    'income': lambda x: 0.30 * x['2016']['income_per_capita'] / 200000,
    'bachelors': lambda x: 0.20 * x['2016']['bachelors_pct'] / 100,
    'median_home_value': lambda x: 0.25 * int(x['2016']['median_home_value']) / 500000,
    'owner_occupied': lambda x: 0.15 * x['2016']['owner_occupied_pct'] / 100,
    'white_pct':  lambda x: 0.1 * (x['2016']['white_pct'] - 0.62)
}

def calculate_gentrification(record):
    g = {}
    total = 0
    for k, foo in GENTRIFY_VARS.items():
        try:
            g[k] = round(foo(record), 3)
        except TypeError as err:
            g[k] = 0
        total += g[k]
    g['index'] = total
    return g
