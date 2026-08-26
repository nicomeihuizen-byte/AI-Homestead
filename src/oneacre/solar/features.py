"""Feature assembly for the PV forecast.

Inputs: Harmonie AROME forecast irradiance and cloud cover; satellite plane-of-array irradiance
at your actual tilt/azimuth (Open-Meteo computes GTI for you — that removes an entire
transposition step); day-of-year; measured panel voltage; measured battery voltage and its
recent trajectory; air temperature (PV efficiency); soil temperature (thermal mass proxy).

TODO Phase 7.
"""
