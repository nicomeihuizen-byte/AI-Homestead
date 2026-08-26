"""IPMA, Portugal. Reference record for the CASTELO BRANCO plot, and the weaker
half of this project's data story. That is worth stating plainly rather than
discovering in Phase 7.

There is no DWD or KNMI equivalent here:
  - api.ipma.pt/open-data/ serves CURRENT observations and forecasts, not deep
    history. Good for a live sanity check, useless for a thirty-year backfill.
  - The long climate series (roughly 50 mainland stations) are published as
    downloadable tables, not as a queryable endpoint.
  - PT02 is a gridded daily precipitation dataset. Rainfall only.

CONSEQUENCE, and this is a real asymmetry rather than a footnote:
  At Prora the station record is primary and reanalysis is the cross-check.
  At Castelo Branco it runs the other way round. ERA5-Land is primary and IPMA is
  the cross-check. Every comparison between the two plots has to carry that
  difference, and no analysis may quietly pool them.

TODO Phase 5: hand-fetch the long-series table for Castelo Branco, commit the
parser, and record in docs/UNCERTAINTY.md what the resulting series is worth.
"""

OPEN_DATA = "https://api.ipma.pt/open-data/"
OBSERVATIONS = "https://api.ipma.pt/open-data/observation/meteorology/stations/"
LONG_SERIES = "https://www.ipma.pt/en/oclima/series.longas/"
PT02_GRIDDED = "https://www.ipma.pt/en/produtoseservicos/index.jsp?page=dataset.pt02.xml"
