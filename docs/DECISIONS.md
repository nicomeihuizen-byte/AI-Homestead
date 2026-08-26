# Architecture Decision Records

One short record per irreversible-ish choice. Format: context → decision → consequences.
Add a new ADR rather than editing an old one; supersede explicitly.

---

## ADR-0001: The field node is a Pico W, not a Raspberry Pi

**Status:** accepted (2026-08-26)

**Context.** The project brief said "Raspberry Pi". A Pi Zero 2 W idles at 0.4–0.6 W; even halted it
draws ~50 mA. De Bilt's 24-hour mean irradiance is ~200 W/m² in June and ~20 W/m² in December, a
factor of ten. An always-on Zero 2 W therefore needs roughly a 60 W panel and 100 Wh of battery.

**Decision.** Pico 2 W in the field box. Its VSYS accepts 1.8–5.5 V, so a single LiFePO4 cell feeds
it directly, no boost stage and therefore no boost-converter quiescent current.

**Consequences.** ~60× smaller power budget (0.08–0.24 Wh/day vs 14.4). No Linux in the field: no
on-device Python ecosystem, no local filesystem logging beyond a flash ring buffer. A Pi may still
be used indoors. Node firmware is MicroPython, not CPython; some libraries will not be available.

**Open:** true dormant current. Published figures disagree by ~30×. Measure before final sizing
(milestone #9). This changes panel sizing, not this decision.

---

## ADR-0002: LLM runs locally

**Status:** accepted (2026-08-26)

**Context.** The project's stated question is whether *genuinely off-grid* AI can close the loop.
A cloud API in the daily decision path would answer a different, less interesting question.

**Decision.** Ollama with a Qwen/Llama-class instruct model on the laptop. Public data APIs are used
for setup and periodic refresh, never as a runtime dependency of a decision.

**Consequences.** Weaker model than a frontier API; the prompt and context design have to carry more
weight. Zero marginal cost per call. The off-grid claim survives scrutiny.

---

## ADR-0003: The LLM never computes

**Status:** accepted (2026-08-26)

**Context.** Language models produce confident, plausible, wrong arithmetic on sensor data.

**Decision.** Every number (degree-days, soil moisture deficit, frost risk, PV budget, day-type) is
computed in tested Python and passed in as a structured context block. The model selects,
prioritises and explains. Output is schema-validated JSON. A deterministic constraint layer runs
*after* the model and can veto or defer.

**Consequences.** More Python, less prompt. Recommendations are auditable via `inputs_used`. The
scheduler degrades to "context block + rules" if the model is unavailable, which is a fine fallback.

---

## ADR-0004: Field-to-house transport, TBD in Phase 0

**Status:** pending, decide after measuring the distance

**Context.** BLE's limit here is not throughput (payload is ~10 bits/s against a 235 kbps floor) but
failure mode: a dropped connection fails silently with no retry, losing data during exactly the
weather events worth observing. Practical guidance: ≤20 m clear LOS → BLE fine; 20–50 m → marginal,
works in July, drops out in a wet November; ≥50 m → LoRa SX1262 point-to-point.

**Decision.** _Pending._ Record the measured distance and obstructions in `docs/SITE.md`, then write
the decision here.

**Consequences either way.** `ingest/` is the seam: swapping BLE for LoRa touches one module. Keep
BLE as the walk-up service/debug interface regardless; that role it does excellently and it is
nearly free.

---

## ADR-0005: Skyfield, not Swiss Ephemeris

**Status:** accepted (2026-08-26)

**Context.** The reference open-source biodynamic implementation (`iouomo/bdc`) builds on Swiss
Ephemeris, which is dual-licensed AGPL/commercial.

**Decision.** Skyfield (MIT) with JPL `de440s.bsp` (public domain, 32 MB, 1849–2150). Pinned
locally, not downloaded at runtime.

**Consequences.** Public repo stays MIT-clean. `bdc` can still be used as a cross-check.
DE440 is *more* accurate than DE441 for lunar work; it includes the Moon's liquid core.

---

## ADR-0006: Two plots, one codebase, `site` on every row

**Status:** accepted (2026-08-26)

**Context.** The Phase 0 site survey resolved the plots to **Prora** on Ruegen (54.39 N, summer)
and **Castelo Branco** in central Portugal (39.82 N, winter): 2256 km and 14.57 degrees of latitude
apart. Until now the code assumed a single site, with Utrecht as a placeholder in `config.py`
(it was labelled `TODO: your actual plot`, so this supersedes a placeholder, not a decision).

Two plots is not a bigger version of one plot. They have different reference networks, different
forecast resolutions, different climates and different timezones. The failure mode is not a crash,
it is a quiet average across two populations that should never have been pooled.

**Decision.** One codebase, one database, and `site` on every table that holds measured or
modelled data, matching a slug in `config.SITES`. `SITES` replaces the `SITE` singleton. Every CLI
command that touches data takes `--site`, and there is **no default**: defaulting silently is
exactly how the pooling error happens.

`daytypes` is deliberately the exception. The Moon's constellation, its declination cycle and the
node/eclipse/perigee moments are geocentric, so they are the same sky at both plots.

**Consequences.** Cross-plot comparison becomes a SQL filter rather than a merge of two databases,
which is what the calendar test and the forecast-skill comparison both need. `ADR-0004` now has to
be answered **per plot** and may resolve differently at each; that is fine, `ingest/` is the seam.
Two plots in different climates is a better test bed for the calendar than one: the same day type
lands on two very different growing environments, which is the confound the historical trials could
not separate. It only works if `site` is always recorded and always used as a stratum.

One trap this creates: Europe/Berlin and Europe/Lisbon are an hour apart, so a day-type transition
just after local midnight at Prora is still the previous day at Castelo Branco. Storing only a date
bakes in one timezone. Flagged in `store/schema.sql`, to resolve in Phase 6.

---

## ADR-0007: DWD and IPMA replace KNMI as reference data

**Status:** accepted (2026-08-26). Supersedes the KNMI assumption in ADR-0001's context.

**Context.** ADR-0001 and the original plan leaned on KNMI, which publishes De Bilt daily from 1901
with global radiation and reference ET in one keyless file. Neither plot is in the Netherlands, so
that source is simply gone. `ingest/knmi.py` is deleted rather than kept: dead code with
authoritative-looking constants is a trap.

**Decision.** `ingest/dwd.py` for Prora, `ingest/ipma.py` for Castelo Branco. ERA5-Land, SARAH3
satellite irradiance and PVGIS are unchanged, being continental or global.

**Consequences, and they are asymmetric.** At Prora the DWD record is strong: station **Arkona
00183** sits 33.5 km north on the same island, daily from 1947, and is one of roughly **64 stations
in DWD's daily solar network**, so measured global radiation is available at the reference station.
At Castelo Branco there is no equivalent: IPMA's open API serves current observations, not deep
history, and the long series are downloadable tables. **ERA5-Land is therefore primary at Castelo
Branco and the station is the check, the reverse of Prora.** The forecast is asymmetric too:
ICON-D2 at 2 km covers Ruegen, nothing at that resolution reaches Portugal, so Castelo Branco gets
ICON-EU at 7 km.

The two plots do not carry equal evidence weight and every cross-plot claim has to say so. Also
inherited: DWD's missing-value code is `9990.0`, and its daily climate product carries no radiation
at all. Both are silent-wrong-answer traps rather than errors. See `docs/DATA_SOURCES.md`.

**Note on ADR-0001.** Its conclusion is unchanged and in fact strengthened. Prora is 2.3 degrees
further north than the Utrecht placeholder: 7.0 hours of daylight on the solstice against 7.5, and
a noon sun at 12.2 degrees against 14.5. The Pico argument got stronger, not weaker.
