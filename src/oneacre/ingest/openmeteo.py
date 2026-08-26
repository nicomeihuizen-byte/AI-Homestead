"""Open-Meteo: archive, forecast, satellite radiation. No key for non-commercial. CC-BY-4.0.

Limits: <10k calls/day, 5k/hour, 600/min.

TRAP: archive and forecast use DIFFERENT soil depth bins.
  archive  (ERA5-Land): 0-7 / 7-28 / 28-100 / 100-255 cm
  forecast (AROME):     0 / 6 / 18 / 54 cm; moisture 0-1 / 1-3 / 3-9 / 9-27 / 27-81 cm
You cannot concatenate them without an explicit, documented mapping step.

TODO Phase 5: archive(), forecast(), satellite() -> long format with a `source` column.
"""

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HIST_FORECAST_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
SATELLITE_URL = "https://satellite-api.open-meteo.com/v1/archive"

ARCHIVE_MODEL = "era5_land"                            # 0.1 deg, 1950 -> present, 5-day latency
FORECAST_MODEL = "knmi_harmonie_arome_netherlands"     # 2 km, hourly updates, KNMI's own
SATELLITE_MODEL = "eumetsat_sarah3"                    # observed irradiance, 5 km, 1983 ->
