# Data sources

Two plots in two countries, so two reference networks. Everything here is free and
public. What is *not* symmetric between the plots is called out explicitly, because
that asymmetry propagates into every model downstream.

## Prora: DWD Climate Data Center, no API key

- Base: `https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate`
- Daily climate: `daily/kl/historical/` and `daily/kl/recent/`. Station **00183, Arkona**,
  33.5 km north of the plot on the same island. **Daily series from 1947-01-01.**
- Daily radiation: `daily/solar/`. A separate, far sparser network, roughly **64 stations
  nationally** against thousands for `kl`. Arkona is in it. That is luck, and it is the single
  most useful fact in this document for a project whose binding constraint is the power budget.
- Licence: CC BY 4.0. Attribute it.

**Traps:**

- Missing value is **`9990.0`**. Not blank, not negative, not NaN. A naive mean sails straight
  past it and returns something absurd. Filter before you aggregate.
- **`daily/kl` contains no global radiation at all.** Sunshine duration only. Radiation is a
  separate product. Code written with the KNMI habit of one-file-has-everything will produce an
  empty radiation column and never complain.
- Semicolon-separated CSV inside a zip, fields space-padded, every row terminated by a literal
  `eor`. Strip before you cast.
- `historical` stops some months back; `recent` covers the tail; they overlap. Deduplicate on
  (station, date).

## Castelo Branco: IPMA, and the honest gap

There is **no DWD or KNMI equivalent for Portugal.**

- `https://api.ipma.pt/open-data/` serves **current** observations and forecasts, not deep history.
  Fine as a live sanity check, useless for a thirty-year backfill.
- Long climate series (roughly 50 mainland stations) are published as **downloadable tables** at
  `https://www.ipma.pt/en/oclima/series.longas/`, not as a queryable endpoint. Fetch by hand once,
  commit the parser, move on.
- PT02 is a gridded daily precipitation dataset. Rainfall only.

**Consequence, and it is structural rather than a detail:**

| | Prora | Castelo Branco |
|---|---|---|
| Primary history | DWD station 00183 | ERA5-Land reanalysis |
| Cross-check | ERA5-Land | IPMA long series |
| Station radiation | yes | no |

So the two plots carry different evidence weights. Any statement that compares them has to say
which side is station-grade and which is reanalysis-grade, and **no analysis may pool them silently.**

## Both plots: Open-Meteo

This is the half of the pipeline that did not care about the move from one Dutch plot to two
European ones.

| Product | What for | Endpoint |
|---|---|---|
| **Archive (ERA5-Land)** | 0.1 deg (~11 km), **1950 to present**, 5-day latency. Soil moisture and temperature at depth, reference ET, VPD: the things a weather station cannot measure. | `archive-api.open-meteo.com/v1/archive?...&models=era5_land` |
| **Forecast** | **Per site, and not the same resolution.** `icon_d2` at 2 km for Prora; `icon_eu` at 7 km for Castelo Branco. | `api.open-meteo.com/v1/forecast?...&models=icon_d2` |
| **Satellite** | Satellite-*observed* irradiance (SARAH3, 5 km, 1983 to present). Computes plane-of-array irradiance from `tilt`+`azimuth`, removing a transposition step from the PV model. | `satellite-api.open-meteo.com/v1/archive?...&tilt=70&azimuth=0` |

Licence: CC-BY-4.0. Attribute it. Limits: <10k calls/day, 5k/hour, 600/min.

**Traps:**

- **Nothing at 2 km resolution reaches Portugal.** ICON-D2 covers Germany, Switzerland and Austria.
  Prora therefore gets a materially sharper forecast than Castelo Branco, and reporting forecast
  skill across the plots without stating this compares a 2 km model against a 7 km one.
- **Archive and forecast use different soil depth bins.** Archive (ERA5-Land) 0-7 / 7-28 / 28-100 cm;
  ICON forecast 0 / 6 / 18 / 54 cm. You cannot concatenate them without an explicit mapping step,
  and the exact forecast bins depend on which ICON model you asked for, so pin the model in metadata.
- **Reference evapotranspiration is not one quantity.** Different services compute it by different
  formulas. Never mix two providers' ET in one series.

## Both plots: PVGIS (EU JRC)

One-off system sizing and optimum tilt for the exact coordinates, at each plot separately. A design
tool, not a forecasting tool. `re.jrc.ec.europa.eu/api/v5_3/PVcalc?...&optimalangles=1`

The panel tilts in `config.py` are currently a latitude+15 heuristic, **not** PVGIS output. Replacing
them is milestone M14 and the numbers should change.

## Applies to every station series

Station records are **unsuitable for trend analysis** (relocations, instrument changes). Fine
operationally, wrong for climate trending. This is true of DWD and IPMA alike.
