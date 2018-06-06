# Census data fetcher




## To do


CSV version of data is in [data/wrangle/records.csv](data/wrangle/records.csv).

To generate it, run:

```py
$ python scripts/wrangle/tidy.py
```

## Adjust gentrification

To tweak gentrification:

[scripts/wrangle/gentrify.py](scripts/wrangle/gentrify.py)

## Quick analysis

Quickie analysis of the records.csv file produced by tidy

```sh
cat data/wrangle/records.csv \
  | csvgrep -c geo -m state \
  | csvcut -c name,gentrification_index,gentrification_income \
  | csvsort -r -c gentrification_index \
  | csvlook \
  | head -n 20
```











## IGnore

Canonical data/schema:
https://docs.google.com/spreadsheets/d/17c0DtNuuI-qd8jNqAo77lql1r9aFnwMrl9n9OzyTLFU/edit

Then edit [config/census_meta.csv](config/census_meta.csv) to contain fields you want.

Make sure config/key.txt exists

Run:

```sh
$  python fetcher.py
```


## APIs


ACS:
https://api.census.gov/data/2016/acs/acs5?get=NAME,GEO_ID,B01001_001E,B01001_001M&for=state:06


https://api.census.gov/data/2010/sf1?get=NAME,GEO_ID,PCT012A015,PCT012A119&for=state:01

