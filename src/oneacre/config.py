"""Site constants. Fill from docs/SITE.md in Phase 0."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    lat: float = 52.09   # TODO: your actual plot, 5 decimal places
    lon: float = 5.12
    timezone: str = "Europe/Amsterdam"
    knmi_station: int = 260          # De Bilt, ~6 km NE of Utrecht, daily series from 1901
    panel_tilt_deg: float = 65.0     # steep, for winter capture; confirm with PVGIS
    panel_azimuth_deg: float = 0.0   # 0 = due south (Open-Meteo/PVGIS convention)
    sensor_height_m: float = 1.5     # WMO comparability is 1.25–2 m; record whatever you chose


SITE = Site()
