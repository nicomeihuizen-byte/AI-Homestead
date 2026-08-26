"""`oneacre` CLI.

Planned commands:
    oneacre ingest ble --minutes 60
    oneacre weather backfill --from 1990-01-01
    oneacre biodynamic day 2026-09-01
    oneacre biodynamic validate
    oneacre solar forecast
    oneacre brief

TODO: wire up as each phase lands.
"""

import typer

app = typer.Typer(help="One Acre, Zero Dependency")


@app.command()
def status() -> None:
    """Show what is wired up so far."""
    typer.echo("Phase 0. See docs/BUILD_PLAN.md")


if __name__ == "__main__":
    app()
