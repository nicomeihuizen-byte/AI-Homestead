"""DWD Climate Data Center. Open data over plain HTTP, no API key, CC BY 4.0.

Reference record for the PRORA plot: Arkona, station 00183, 33.5 km north on the
same island. Daily climate series from 1947-01-01.

    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/
        daily/kl/historical/tageswerte_KL_00183_19470101_YYYYMMDD_hist.zip
        daily/kl/recent/
        daily/solar/tageswerte_ST_00183_row.zip

TRAPS (each one silently produces wrong numbers):
  - Missing value is 9990.0. Not blank, not negative, not NaN. A naive mean sails
    straight past it and comes out absurd. Filter before you aggregate.
  - The daily `kl` product carries NO global radiation at all. Sunshine duration
    only. Radiation lives in `daily/solar/`, a separate and far sparser network:
    ~64 stations nationally against thousands for `kl`. Arkona happens to be in
    both, which is luck rather than planning. Code written with the KNMI habit of
    one-file-has-everything will produce an empty radiation column and not complain.
  - Semicolon-separated CSV inside a zip, fields padded with spaces, every row
    terminated by a literal `eor`. Strip before you cast.
  - `historical` stops some months back and `recent` covers the tail. You need
    both, they overlap, so deduplicate on (station, date).
  - Station series are unsuitable for trend analysis (relocations, instrument
    changes). Fine operationally, wrong for climate trending.

Cache aggressively: these are historical facts and do not change.

TODO Phase 5: fetch(), parse(), to_long_format(), backfill() with a gap report.
"""

BASE = ("https://opendata.dwd.de/climate_environment/CDC"
        "/observations_germany/climate")

DAILY_KL_HISTORICAL = BASE + "/daily/kl/historical/"
DAILY_KL_RECENT = BASE + "/daily/kl/recent/"
DAILY_SOLAR = BASE + "/daily/solar/"

ARKONA = "00183"     # Prora's reference station
MISSING = 9990.0     # not -999, not blank. See the traps above.
