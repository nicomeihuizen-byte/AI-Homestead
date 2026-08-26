"""Smoke test — proves the package imports and the scaffold is wired up."""

import oneacre
from oneacre.config import SITE


def test_version():
    assert oneacre.__version__


def test_site_defaults():
    assert 50 < SITE.lat < 54, "Netherlands-ish"
    assert SITE.knmi_station == 260, "De Bilt"
