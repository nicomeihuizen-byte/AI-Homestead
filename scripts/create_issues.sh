#!/usr/bin/env bash
# Create the milestone issues on GitHub. Requires `gh auth login` and the repo pushed.
set -euo pipefail

issue() { gh issue create --title "$1" --body "$2" --label "${3:-}"; }

issue "M1 Site survey + transport decision (ADR-0004)" \
  "Measure straight-line node->laptop distance and obstructions. Fill docs/SITE.md. Apply the table in BUILD_PLAN section 1. Write ADR-0004.
Done when: distance recorded, ADR-0004 has a decision line." "phase-0"

issue "M2 Python env, CI, pre-commit" \
  "uv venv; uv pip install -e '.[dev]'; ruff + pytest in GitHub Actions.
Done when: green on a push." "phase-0"

issue "M3 DS18B20 + BME280 on the bench" \
  "One at a time. BME280 in FORCED mode, 1x oversampling, from the first line of code - continuous mode self-heats +1 to +2 C and looks plausible.
Done when: DS18B20 in ice water reads 0.0-0.5 C; breathing on the BME280 moves RH." "phase-1"

issue "M4 Soil moisture, lux, rain, wind on the bench" \
  "Raw counts only; calibration lives on the laptop.
Done when: tipping the rain bucket ten times by hand reads EXACTLY 10. 11-13 means reed bounce - fix the debounce now, not in November." "phase-1"

issue "M5 Packet format + schema versioning" \
  "Fixed schema, version byte, sequence number (the Pico has no trustworthy RTC).
Done when: round-trip test passes in tests/test_packet.py." "phase-1"

issue "M6 BLE peripheral (NUS) on the node" \
  "aioble, Nordic UART Service - every phone BLE app speaks it, which makes field debugging trivial.
Done when: live values readable from a phone." "phase-2"

issue "M7 bleak ingest -> SQLite" \
  "bleak is client-only, so laptop=central and node=peripheral. Store measured_at AND received_at.
Done when: 60 min of readings land with correct timestamps." "phase-2"

issue "M8 Node ring buffer + acknowledged backfill" \
  "The difference between a logger and a toy.
Done when: Bluetooth off for 20 minutes, back on, ZERO readings lost." "phase-2"

issue "M9 Measure real dormant current" \
  "Published figures disagree by ~30x. Multimeter in series.
Done when: a number in docs/POWER_BUDGET.md." "phase-3"

issue "M10 Power path + low-temp cutoff verified" \
  "Panel -> CN3791 (LiFePO4) -> cell+BMS -> VSYS direct. No boost stage.
Done when: freezer test confirms the cell refuses charge below 0 C. Getting this wrong destroys hardware, not just data." "phase-3"

issue "M11 Enclosure, vent, shield, deployment" \
  "IP66 box INSIDE the birdbox. ePTFE vent + desiccant + conformal coat + underside glands + drip loops. ASA/PETG radiation shield on a short I2C tail.
Done when: 14 consecutive days outdoors, zero gaps, battery recovering on sunny days." "phase-3"

issue "M12 KNMI ingester (station 260, 1901->)" \
  "Watch the integer scaling (0.1 C, 0.1 mm, J/cm2) and the -1 = '<0.05' convention.
Done when: backfill completes with a gap report." "phase-5"

issue "M13 Open-Meteo archive + forecast ingesters" \
  "ERA5-Land archive + Harmonie AROME forecast. Archive and forecast use DIFFERENT soil depth bins - document the mapping.
Done when: soil layers stored, mapping written down." "phase-5"

issue "M14 Satellite radiation + PVGIS sizing" \
  "Pass tilt+azimuth for plane-of-array irradiance. PVGIS optimalangles=1 for the real site.
Done when: optimum tilt recorded in docs/SITE.md." "phase-5"

issue "M15 Skyfield day-type engine" \
  "SIDEREAL, real IAU boundaries. load_constellation_map handles B1875 precession for you.
Done when: Ophiuchus folds to water AND is flagged; out-of-zodiac returns None with a log line." "phase-6"

issue "M16 Ascending/descending, nodes, perigee, blanking" \
  "find_maxima/find_minima are in skyfield.searchlib, NOT almanac. Declination rough_period 27.3 d; distance rough_period 27.55 d - different constants.
Done when: turning points and blanking windows computed." "phase-6"

issue "M17 Validate against a purchased printed edition" \
  "60-90 days, fixture stays gitignored.
Done when: mismatches cluster on Ophiuchus / node-window / transition-times. Scattered mismatches = a real bug, almost certainly tropical-vs-sidereal." "phase-6"

issue "M18 Calibration curves + uncertainty doc" \
  "Oven-dried jars per probe; temperature cross-sensitivity regressed out; cross-check air temp and rain against De Bilt.
Done when: calibration.apply() works and docs/UNCERTAINTY.md has defensible error bars." "phase-4"

issue "M19 Solar baselines (persistence, clear-sky)" \
  "Build these BEFORE the LSTM. They are the bar it must clear.
Done when: skill scores recorded." "phase-7"

issue "M20 LSTM + walk-forward validation + model card" \
  "Walk-forward only. One winter of data will overfit - pre-train on reconstructed history or accept a physical model + residual regressor and log that as the result.
Done when: honest comparison against M19 in docs/MODEL_CARD_solar.md." "phase-7"

issue "M21 Scheduler context builder" \
  "EVERY number computed in tested Python. No LLM in this module at all.
Done when: context block fully unit-tested." "phase-8"

issue "M22 Local LLM + structured output + constraint layer" \
  "Ollama, schema-validated JSON, inputs_used for auditability. Constraints run AFTER the model.
Done when: constraints correctly veto a recommendation." "phase-8"

issue "M23 Daily brief generation + public log" \
  "Done when: seven consecutive dated briefs, each traceable to its inputs." "phase-8"

issue "M24 Pre-register the biodynamic analysis" \
  "docs/PREREGISTRATION.md, frozen with a commit hash, BEFORE the first sowing.
Done when: primary test pre-specified and day-type frequency weighting decided." "phase-6"

issue "M25 Vision inventory spike" \
  "Gated behind a full season of data. Boring statistics first on the anomaly side.
Done when: item counts from shelf photos." "phase-9"

echo "Created 25 issues."
