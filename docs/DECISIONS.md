# Architecture Decision Records

One short record per irreversible-ish choice. Format: context → decision → consequences.
Add a new ADR rather than editing an old one; supersede explicitly.

---

## ADR-0001 — The field node is a Pico W, not a Raspberry Pi

**Status:** accepted (2026-08-26)

**Context.** The project brief said "Raspberry Pi". A Pi Zero 2 W idles at 0.4–0.6 W; even halted it
draws ~50 mA. De Bilt's 24-hour mean irradiance is ~200 W/m² in June and ~20 W/m² in December — a
factor of ten. An always-on Zero 2 W therefore needs roughly a 60 W panel and 100 Wh of battery.

**Decision.** Pico 2 W in the field box. Its VSYS accepts 1.8–5.5 V, so a single LiFePO4 cell feeds
it directly — no boost stage and therefore no boost-converter quiescent current.

**Consequences.** ~60× smaller power budget (0.08–0.24 Wh/day vs 14.4). No Linux in the field: no
on-device Python ecosystem, no local filesystem logging beyond a flash ring buffer. A Pi may still
be used indoors. Node firmware is MicroPython, not CPython — some libraries will not be available.

**Open:** true dormant current. Published figures disagree by ~30×. Measure before final sizing
(milestone #9). This changes panel sizing, not this decision.

---

## ADR-0002 — LLM runs locally

**Status:** accepted (2026-08-26)

**Context.** The project's stated question is whether *genuinely off-grid* AI can close the loop.
A cloud API in the daily decision path would answer a different, less interesting question.

**Decision.** Ollama with a Qwen/Llama-class instruct model on the laptop. Public data APIs are used
for setup and periodic refresh, never as a runtime dependency of a decision.

**Consequences.** Weaker model than a frontier API; the prompt and context design have to carry more
weight. Zero marginal cost per call. The off-grid claim survives scrutiny.

---

## ADR-0003 — The LLM never computes

**Status:** accepted (2026-08-26)

**Context.** Language models produce confident, plausible, wrong arithmetic on sensor data.

**Decision.** Every number — degree-days, soil moisture deficit, frost risk, PV budget, day-type — is
computed in tested Python and passed in as a structured context block. The model selects,
prioritises and explains. Output is schema-validated JSON. A deterministic constraint layer runs
*after* the model and can veto or defer.

**Consequences.** More Python, less prompt. Recommendations are auditable via `inputs_used`. The
scheduler degrades to "context block + rules" if the model is unavailable, which is a fine fallback.

---

## ADR-0004 — Field-to-house transport: TBD in Phase 0

**Status:** pending — decide after measuring the distance

**Context.** BLE's limit here is not throughput (payload is ~10 bits/s against a 235 kbps floor) but
failure mode: a dropped connection fails silently with no retry, losing data during exactly the
weather events worth observing. Practical guidance: ≤20 m clear LOS → BLE fine; 20–50 m → marginal,
works in July, drops out in a wet November; ≥50 m → LoRa SX1262 point-to-point.

**Decision.** _Pending._ Record the measured distance and obstructions in `docs/SITE.md`, then write
the decision here.

**Consequences either way.** `ingest/` is the seam: swapping BLE for LoRa touches one module. Keep
BLE as the walk-up service/debug interface regardless — that role it does excellently and it is
nearly free.

---

## ADR-0005 — Skyfield, not Swiss Ephemeris

**Status:** accepted (2026-08-26)

**Context.** The reference open-source biodynamic implementation (`iouomo/bdc`) builds on Swiss
Ephemeris, which is dual-licensed AGPL/commercial.

**Decision.** Skyfield (MIT) with JPL `de440s.bsp` (public domain, 32 MB, 1849–2150). Pinned
locally, not downloaded at runtime.

**Consequences.** Public repo stays MIT-clean. `bdc` can still be used as a cross-check.
DE440 is *more* accurate than DE441 for lunar work — it includes the Moon's liquid core.
