"""Site constants.

Two plots, worked in alternation, 2256 km apart. Everything downstream takes a
site; nothing assumes there is only one. The numbers here come from the Phase 0
survey in docs/SITE.md, and anything still marked TODO has not been measured yet.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    slug: str
    name: str
    season: str                    # which season this plot is cultivated through
    lat: float
    lon: float
    timezone: str

    # Reference observations. The provider decides which ingest module reads it.
    reference_provider: str        # 'dwd' | 'ipma'
    reference_station: str         # the provider's own station id, as a string
    reference_from: str            # first date the daily series covers, '' if unconfirmed
    has_station_radiation: bool    # measured global radiation AT the reference station

    # Open-Meteo forecast model. Deliberately per site: these are not the same
    # resolution, and any skill comparison between the plots has to say so.
    forecast_model: str
    forecast_resolution_km: float

    panel_tilt_deg: float
    panel_azimuth_deg: float = 0.0  # 0 = due south (Open-Meteo/PVGIS convention)
    sensor_height_m: float = 1.5    # WMO comparability is 1.25 to 2 m; record what you chose


PRORA = Site(
    slug="prora",
    name="Prora, Ruegen",
    season="summer",
    lat=54.38970,
    lon=13.57440,
    timezone="Europe/Berlin",
    reference_provider="dwd",
    reference_station="00183",      # Arkona, 33.5 km N, same island
    reference_from="1947-01-01",
    has_station_radiation=True,     # Arkona is in DWD's ~64-station daily solar network
    forecast_model="icon_d2",       # 2 km, DWD, covers Germany
    forecast_resolution_km=2.0,
    panel_tilt_deg=70.0,            # TODO: latitude+15 heuristic. Confirm with PVGIS (M14).
)

CASTELO_BRANCO = Site(
    slug="castelo_branco",
    name="Castelo Branco",
    season="winter",
    lat=39.82220,
    lon=-7.49310,
    timezone="Europe/Lisbon",
    reference_provider="ipma",
    reference_station="castelo_branco",  # IPMA long series; there is no open historical API
    reference_from="",                   # TODO Phase 5: confirm from the published table
    has_station_radiation=False,
    forecast_model="icon_eu",            # 7 km. Nothing at 2 km reaches Portugal.
    forecast_resolution_km=7.0,
    panel_tilt_deg=55.0,                 # TODO: latitude+15 heuristic. Confirm with PVGIS (M14).
)

SITES = {s.slug: s for s in (PRORA, CASTELO_BRANCO)}


def get(slug: str) -> Site:
    """Look up a plot by slug. Raises rather than guessing which one you meant."""
    try:
        return SITES[slug]
    except KeyError:
        raise KeyError(f"unknown site {slug!r}; known: {sorted(SITES)}") from None
