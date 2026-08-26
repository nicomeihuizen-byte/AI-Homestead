"""Smoke test: proves the package imports and the scaffold is wired up.

Several of these encode asymmetries between the two plots that the docs claim in
prose. If one of them ever fails, the prose is now wrong too. Fix both.
"""

import oneacre
from oneacre.config import CASTELO_BRANCO, PRORA, SITES, get


def test_version():
    assert oneacre.__version__


def test_two_sites():
    assert set(SITES) == {"prora", "castelo_branco"}


def test_lookup_refuses_to_guess():
    assert get("prora") is PRORA
    try:
        get("utrecht")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown site should raise, not fall back to a default")


def test_sites_are_where_we_think_they_are():
    assert 54.0 < PRORA.lat < 54.8, "Ruegen, German Baltic coast"
    assert 13.0 < PRORA.lon < 14.0
    assert 39.5 < CASTELO_BRANCO.lat < 40.2, "central Portugal"
    assert -8.0 < CASTELO_BRANCO.lon < -7.0, "west of Greenwich; sign errors are the classic bug"


def test_the_plots_are_seasonal_opposites():
    assert {PRORA.season, CASTELO_BRANCO.season} == {"summer", "winter"}
    assert PRORA.lat > CASTELO_BRANCO.lat, "the summer plot is the northern one"


def test_forecast_resolution_is_not_symmetric():
    # Prora gets a 2 km model; nothing that sharp reaches Portugal. Any skill
    # comparison across the plots has to account for this before it means anything.
    assert PRORA.forecast_resolution_km < CASTELO_BRANCO.forecast_resolution_km


def test_only_prora_has_station_radiation():
    # Arkona is one of ~64 stations in DWD's daily solar network. IPMA publishes
    # no equivalent open record, so Castelo Branco leans on reanalysis instead.
    assert PRORA.has_station_radiation
    assert not CASTELO_BRANCO.has_station_radiation


def test_panel_is_steeper_at_the_northern_plot():
    assert PRORA.panel_tilt_deg > CASTELO_BRANCO.panel_tilt_deg
