GENTRIFY_VARS = {
    'income': lambda x: 0.20 * x['2016']['income_per_capita'] / 200000,
    'bachelors': lambda x: 0.20 * x['2016']['bachelors_pct'] / 100,
    'median_home_value': lambda x: 0.2 * int(x['2016']['median_home_value']) / 500000,
    'owner_occupied': lambda x: 0.15 * x['2016']['owner_occupied_pct'] / 100,
    'white_pct':  lambda x: 0.08 * (x['2016']['white_pct'] - 0.62)
}

def calculate_gentrification(record):
    g = {}
    total = 0
    for k, foo in GENTRIFY_VARS.items():
        g[k] = foo(record)
        total += g[k]
    g['index'] = total
    return g
