# Data sources

## KNMI script service: no API key
- Daily: `https://www.daggegevens.knmi.nl/klimatologie/daggegevens`
- Hourly: `https://www.daggegevens.knmi.nl/klimatologie/uurgegevens`
- Params: `stns` (260 = De Bilt), `vars` (`ALL` or groups), `start`/`end` (`YYYYMMDD` / `YYYYMMDDHH`), `fmt=json`
- **Daily data from 1901-01-01.** Hourly from 1951. Latency: evening of the following day.
- Key agronomic vars: `Q` global radiation (J/cm², ×2.778 → Wh/m²), `EV24` Makkink reference ET (0.1 mm)
- **Integer-scaled**: temps 0.1 °C, rain 0.1 mm. `-1` in RH/SQ means "<0.05", not minus one.
- KNMI states these series are **unsuitable for trend analysis** (relocations, instrument changes).
- Licence: CC0 for in-situ observation datasets.
- ⚠ KNMI's Dataverkenner is stated to eventually replace this page. Keep the KNMI Data Platform
  (`api.dataplatform.knmi.nl`, free key, NetCDF, EDR API for point queries) as the fallback.

## Open-Meteo: no key for non-commercial, CC-BY-4.0, attribute it
Limits: <10k calls/day, 5k/hour, 600/min.

- **Archive** `archive-api.open-meteo.com/v1/archive`: ERA5 0.25° 1940→, **ERA5-Land 0.1° 1950→**
  (`models=era5_land`), 5-day latency. Soil layers 0–7 / 7–28 / 28–100 / 100–255 cm.
  `et0_fao_evapotranspiration` (FAO-56 Penman-Monteith), VPD, GHI/DNI/DHI.
- **Forecast** `api.open-meteo.com/v1/forecast`: **`models=knmi_harmonie_arome_netherlands`, 2 km,
  hourly updates.** Best available for a Utrecht plot.
  ⚠ **Forecast soil layers use different bins** (0 / 6 / 18 / 54 cm; moisture 0–1 / 1–3 / 3–9 /
  9–27 / 27–81 cm). Cannot be concatenated with archive layers without an explicit mapping.
- **Historical forecast** `historical-forecast-api.open-meteo.com/v1/forecast`: stitched high-res
  model runs, ~2022→, 2 km, no latency. Gap-fills between ERA5-Land and now.
- **Satellite radiation** `satellite-api.open-meteo.com/v1/archive`: SARAH3 5 km 1983→, MTG 2.5 km
  10-min Feb 2026→. Pass `tilt`+`azimuth` for **plane-of-array irradiance**, which removes a whole
  transposition step from the PV model.

⚠ **KNMI `EV24` is Makkink; Open-Meteo `et0_fao_evapotranspiration` is Penman-Monteith.** They will
not agree. Never mix them in one series.

## PVGIS (EU JRC): free, no registration
`https://re.jrc.ec.europa.eu/api/v5_3/{PVcalc|seriescalc|tmy}?...`
Use `PVGIS-SARAH3` for Europe. `optimalangles=1` finds the optimum tilt/azimuth for the site.
Limits: 30 req/s/IP; server-side calls only. Design tool, not for daily forecasting.

## Cross-validation only
- **E-OBS / ECA&D** v33.0e, 0.1°, 1950–2025, includes `QQ` radiation and an ensemble spread field
  (useful for honest error bars). **Non-commercial research/education licence only.**
- **NASA POWER** `power.larc.nasa.gov/api/temporal/daily/point`, community `AG`, 0.5° (~55 km):
  too coarse to add much at a single Dutch site, but the ICASA output format feeds DSSAT/APSIM.

## Not a data source: the Thun calendar
Published editions are copyrighted compilations and, in the EU, additionally protected by the sui
generis database right (Dir. 96/9/EC). The *dates* are astronomical facts and we compute them
ourselves. A hand-keyed validation sample from one purchased edition stays local and gitignored.
