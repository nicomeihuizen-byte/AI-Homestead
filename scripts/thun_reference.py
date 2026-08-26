#!/usr/bin/env python3
"""Reproduce data/fixtures/expected_daytype_frequencies.json.

This is a REFERENCE calculation, deliberately kept out of src/oneacre/biodynamic/ --
it exists so your own engine has something to check itself against, not so you can
import it. Write the real one yourself; that is the point of the exercise.

    pip install skyfield
    python3 scripts/thun_reference.py

Needs de421.bsp or de440s.bsp. Pin the kernel locally -- this is an off-grid project
and a runtime download is not a dependency you want.

Two API facts most online examples get wrong:
  - find_maxima / find_minima are in skyfield.searchlib, NOT skyfield.almanac
  - load_constellation_map() precesses to B1875 internally; you do not
"""

import collections
import numpy as np
from skyfield.api import load, load_constellation_map

ELEMENT = {"Tau": "earth", "Vir": "earth", "Cap": "earth",
           "Cnc": "water", "Sco": "water", "Psc": "water",
           "Gem": "air",   "Lib": "air",   "Aqr": "air",
           "Ari": "fire",  "Leo": "fire",  "Sgr": "fire"}
ORGAN = {"earth": "root", "water": "leaf", "air": "flower", "fire": "fruit"}
SIDEREAL_MONTH = 27.321661

eph = load("de421.bsp")
ts = load.timescale()
earth, moon = eph["earth"], eph["moon"]
constellation_at = load_constellation_map()

t0, t1 = ts.utc(2026, 1, 1), ts.utc(2036, 1, 1)
t = ts.tt_jd(np.linspace(t0.tt, t1.tt, int((t1.tt - t0.tt) * 48)))
cons = np.array(constellation_at(earth.at(t).observe(moon).apparent()))

counts = collections.Counter(cons.tolist())
total = len(cons)
for c, k in counts.most_common():
    print(f"{c:4s} {k/total*100:6.2f}%  {k/total*SIDEREAL_MONTH:5.2f} d/sidereal month  "
          f"{ELEMENT.get(c, '-')}")

by_organ = collections.defaultdict(float)
for c, k in counts.items():
    if c in ELEMENT:
        by_organ[ORGAN[ELEMENT[c]]] += k / total
by_organ["leaf"] += counts.get("Oph", 0) / total   # Thun has no Ophiuchus

print()
for organ in ("root", "leaf", "flower", "fruit"):
    print(f"{organ:7s} {by_organ[organ]*SIDEREAL_MONTH:5.2f} d/sidereal month")
print(f"\nroot/flower = {by_organ['root']/by_organ['flower']:.2f}")
