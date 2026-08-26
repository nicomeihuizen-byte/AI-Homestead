"""Open-Meteo: archive, forecast, satellite radiation. No key for non-commercial. CC-BY-4.0.

Limits: <10k calls/day, 5k/hour, 600/min.

This is the part of the pipeline that survived the move from one Dutch plot to
two European ones unchanged: ERA5-Land and the SARAH3 satellite record are
continental or global and behave identically at both sites.

TRAP: archive and forecast use DIFFERENT soil depth bins.
  archive  (ERA5-Land): 0-7 / 7-28 / 28-100 / 100-255 cm
  forecast (ICON):      0 / 6 / 18 / 54 cm
You cannot concatenate them without an explicit, documented mapping step. The
exact forecast bins depend on which ICON model you asked for, so pin the model
in the metadata alongside the values.

TRAP: the forecast model is PER SITE and the two are not the same resolution.
See config.Site.forecast_model. Reporting forecast skill across the two plots
without stating this is comparing a 2 km model against a 7 km one.

TODO Phase 5: archive(), forecast(), satellite() -> long format with `source`
and `site` columns.
"""

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HIST_FORECAST_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
SATELLITE_URL = "https://satellite-api.open-meteo.com/v1/archive"

ARCHIVE_MODEL = "era5_land"          # 0.1 deg, 1950 -> present, 5-day latency
SATELLITE_MODEL = "eumetsat_sarah3"  # observed irradiance, 5 km, 1983 ->

# Forecast model is a property of the site, not of this module:
#   prora           icon_d2  2 km   DWD's high-resolution model, covers Germany
#   castelo_branco  icon_eu  7 km   nothing at 2 km reaches Portugal
