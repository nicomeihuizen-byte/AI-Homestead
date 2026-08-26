"""PVGIS (EU JRC): one-off system sizing. Free, no registration.

Use `optimalangles=1` to get the optimum tilt/azimuth for the actual site, then compare against
the 60-75 deg winter-biased tilt in docs/BUILD_PLAN.md §4 and decide deliberately which you want.

Design tool, not a forecasting tool. Do not put this in the daily loop.
Limits: 30 req/s/IP. Server-side calls only.

TODO Phase 5.
"""

BASE = "https://re.jrc.ec.europa.eu/api/v5_3"
