"""Thun element/organ mapping over the twelve zodiacal constellations.

SIDEREAL, not tropical. The calendar tracks the Moon against the ACTUAL star constellations.
Tropical astrological signs are currently offset by ~24-25 degrees — roughly a whole sign — so a
tropical implementation is systematically wrong by about two days, every day. This is the most
common bug in hobby implementations of this calendar.

Real IAU (Delporte) boundaries, so the constellations are UNEQUAL in length: Libra spans as
little as ~18 deg, Virgo ~46 deg. Consequence: the day types are structurally unbalanced,
roughly 9 root days against 5-6 flower days per sidereal month. Any statistical test MUST
account for this unequal exposure, or "root days are more numerous" gets mistaken for
"root days work better".
"""

ELEMENT_OF = {
    "Tau": "earth", "Vir": "earth", "Cap": "earth",
    "Cnc": "water", "Sco": "water", "Psc": "water",
    "Gem": "air",   "Lib": "air",   "Aqr": "air",
    "Ari": "fire",  "Leo": "fire",  "Sgr": "fire",
}

ORGAN_OF_ELEMENT = {
    "earth": "root",
    "water": "leaf",
    "air": "flower",
    "fire": "fruit",
}

# The IAU boundaries put a slice of the ecliptic in Ophiuchus, and the Moon spends roughly a
# day per sidereal month there. Thun's zodiac is 12-fold with no Ophiuchus; the printed
# calendars extend the Scorpio/water region across it.
#
# A naive load_constellation_map() implementation WILL disagree with the printed calendar on
# those days. Fold it into water — but always flag it in the output, and verify against a
# printed edition. Thun's exact handling is not documented anywhere findable.
OPHIUCHUS_FOLD = "Sco"

# The Moon's orbit is inclined ~5.1 deg, so it occasionally strays into Orion, Cetus, Auriga,
# Sextans and others. Return None with a log line — never crash, never silently default.
# These cases are a useful sanity check that you are using real boundaries and not equal
# 30-degree divisions.


def organ_for(abbrev: str) -> tuple[str | None, bool]:
    """Map an IAU constellation abbreviation to a Thun organ.

    Returns (organ_or_None, folded_from_ophiuchus).

    TODO Phase 6.
    """
    raise NotImplementedError
