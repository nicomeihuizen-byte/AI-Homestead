"""`oneacre` CLI.

Every command that touches measured or modelled data takes --site. There is no
default: there are two plots, and silently defaulting to one of them is exactly
how you end up pooling them by accident.

Planned commands:
    oneacre sites
    oneacre ingest ble --site prora --minutes 60
    oneacre weather backfill --site prora --from 1990-01-01
    oneacre biodynamic day 2026-09-01        # site-independent, see store/schema.sql
    oneacre biodynamic validate
    oneacre solar forecast --site castelo_branco
    oneacre brief --site prora

TODO: wire up as each phase lands.
"""

import typer

from oneacre.config import SITES

app = typer.Typer(help="One Acre, Zero Dependency")


@app.command()
def status() -> None:
    """Show what is wired up so far."""
    typer.echo("Phase 0. See docs/BUILD_PLAN.md")


@app.command()
def sites() -> None:
    """List the configured plots and where their reference data comes from."""
    for s in SITES.values():
        typer.echo(
            f"{s.slug:<15} {s.name:<18} {s.season:<7} "
            f"{s.lat:>8.4f}, {s.lon:>8.4f}  "
            f"ref={s.reference_provider}:{s.reference_station}  "
            f"forecast={s.forecast_model} ({s.forecast_resolution_km:g} km)"
        )


if __name__ == "__main__":
    app()
