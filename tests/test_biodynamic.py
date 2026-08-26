"""Thun day-type engine tests. Write these BEFORE the implementation (Phase 6).

They encode the three things most likely to be wrong.
"""

import pytest

pytestmark = pytest.mark.skip(reason="Phase 6: implement src/oneacre/biodynamic first")


def test_uses_sidereal_not_tropical():
    """A tropical implementation is offset ~24-25 deg and wrong by ~2 days, every day.

    Pick a date where the sidereal and tropical answers differ and assert the sidereal one.
    """


def test_ophiuchus_is_flagged_not_hidden():
    """Moon in Oph must fold to water/leaf AND set folded_from_oph=True."""


def test_out_of_zodiac_returns_none():
    """Moon strays into Ori/Cet/Aur/Sex. Return None and log; never crash, never default."""


def test_ascending_is_declination_not_phase():
    """Ascending/descending is the ~27.3 d declination cycle, not the 29.53 d synodic one.

    Assert on a date where the two disagree.
    """


def test_day_type_frequencies_are_unequal():
    """Over a year: roughly 9 root days per sidereal month against 5-6 flower days.

    If your counts come out near-equal you are using equal 30-degree divisions, not real
    IAU boundaries.
    """
