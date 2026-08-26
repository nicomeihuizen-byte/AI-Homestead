"""Skyfield wrapper. MIT-licensed; JPL kernels are public domain.

Kernel: de440s.bsp (32 MB, 1849-2150) — covers any historical validation back to 1963.
PIN IT LOCALLY. Do not assume a runtime download works; this is an off-grid project.
(For lunar work DE440 is MORE accurate than DE441: it includes the Moon's liquid core.)

Two API facts that most online examples get wrong:

  1. find_maxima / find_minima live in skyfield.searchlib, NOT skyfield.almanac.
         from skyfield.searchlib import find_maxima, find_minima

  2. load_constellation_map() handles the B1875 precession internally. You do not.

What to compute where:
  - constellation      : load_constellation_map() over apparent geocentric position
  - ascending/descending: find_maxima/find_minima over apparent lunar DECLINATION,
                          rough_period ~= 27.3 d (tropical month).
                          This is a declination cycle, NOT waxing/waning. Confusing the two
                          is the second most common bug in this calendar.
  - perigee/apogee     : find_minima/find_maxima over Earth-Moon DISTANCE,
                          rough_period ~= 27.55 d (anomalistic month — a DIFFERENT constant).
                          Set step_days well below the period or you will skip extrema.
  - nodes              : almanac.moon_nodes(eph) + find_discrete
  - eclipses           : almanac.lunar_eclipses(...)
  - oppositions/conj.  : almanac.oppositions_conjunctions(eph, target)
  - trines             : NOT provided. Compute from geocentric ecliptic longitude
                         differences ~= 120 deg +/- orb. The calendar is geocentric.

TODO Phase 6.
"""

KERNEL = "de440s.bsp"
