"""KNMI script service: De Bilt station 260, daily series from 1901-01-01. No API key.

    https://www.daggegevens.knmi.nl/klimatologie/daggegevens
        ?stns=260&vars=ALL&start=YYYYMMDD&end=YYYYMMDD&fmt=json

TRAPS (each one silently produces wrong numbers):
  - Integer-scaled: temps in 0.1 C, rain in 0.1 mm, Q in J/cm2 (x2.778 -> Wh/m2).
  - `-1` in RH/SQ means "<0.05", NOT minus one.
  - EV24 is MAKKINK reference ET. Open-Meteo's et0_fao_evapotranspiration is Penman-Monteith.
    They will not agree. Never mix them in one series.
  - KNMI states these series are unsuitable for trend analysis (relocations, instrument changes).

Cache aggressively; these are historical facts and do not change.

TODO Phase 5: fetch(), parse(), to_long_format(), backfill() with a gap report.
"""

DAILY_URL = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"
HOURLY_URL = "https://www.daggegevens.knmi.nl/klimatologie/uurgegevens"
DE_BILT = 260
