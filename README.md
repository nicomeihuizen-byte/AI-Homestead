# One Acre, Zero Dependency

Off-grid, AI-driven farming on two seasonal plots near Utrecht (NL). A solar-powered field node
measures soil and weather; a laptop-side Python stack merges that with 125 years of public Dutch
weather data, forecasts its own solar budget, computes the Thun biodynamic day-type from first
principles, and asks a **local** LLM to turn all of it into a daily plan.

**Project write-up:** https://www.meihuizen.ai/projects/off-grid-ai-homestead.html
**Full build plan:** [`docs/BUILD_PLAN.md`](docs/BUILD_PLAN.md) — start there.

## The question

> How much of a small farm's daily decision-making can genuinely off-grid AI handle end to end,
> from sensor to scheduler?

## Three commitments

1. **Off-grid means off-grid.** No cloud LLM in the daily loop. Public data is pulled during setup,
   never depended on at decision time.
2. **Every number carries its provenance and its error bar.** A €30 probe that claims ±0.3 pH does
   not get to state pH to one decimal. See `docs/BUILD_PLAN.md` §2.
3. **The biodynamic calendar is a hypothesis under test, not a scheduling rule.** The evidence does
   not support the trigon effect; this project logs it as a covariate and tests it honestly,
   pre-registered. A null result is a valid output. See §5.

## Layout

| Path | What |
|---|---|
| `node/` | MicroPython for the Pico W field node |
| `src/oneacre/` | Laptop package: ingest, store, biodynamic, solar, scheduler |
| `docs/` | Build plan, ADRs, site survey, method notes, model cards |
| `hardware/` | Wiring, enclosure, panel siting |
| `data/` | Gitignored. Raw stays raw; calibration applies on read. |

## Status

Phase 0. Nothing is built yet — the plan is.

## Conventions

- **Units in every name**: `air_temp_c`, `soil_vwc_frac`, `rain_mm`, `irradiance_wm2`.
- **Raw stays raw.** Calibration applies on read, never destructively.
- Say **"Thun calendar"**, not "Steiner calendar" — Steiner never published one.

## Licence

MIT (code). Data from KNMI (CC0 / CC-BY) and Open-Meteo (CC-BY-4.0) — attribute per
`docs/DATA_SOURCES.md`. No copyrighted calendar data is redistributed here.
