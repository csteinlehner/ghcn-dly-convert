# GHCN DLY to JSON

Converts GHCN DLY Data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ to JSON file 

convert_to_json.py converts all given values structured by Year/Month/Day with initial year filter.
convert_to_json_weekly_single.py converts PRCP given values structured by Year/Week with initial year filter. Weekly PRCP values are added up.


Usage:
> python convert_to_json.py stationname.dly YYYY-YYYY
>
> python convert_to_json_weekly_single.py stationname.dly YYYY-YYYY