# One Acre, Zero Dependency: Build Plan

**Repo:** `one-acre` · **Owner:** Nico Meihuizen · **Site:** https://www.meihuizen.ai/projects/off-grid-ai-homestead.html
**Plan date:** 2026-08-26 · **Target:** first winter plot instrumented before the 2026/27 season, both plots running through 2027.

---

## 0. What this project actually claims

> How much of a small farm's daily decision-making can genuinely off-grid AI handle end to end, from sensor to scheduler?

That is a research question, not a product spec, and the plan below is built to answer it honestly. Three commitments follow from it:

1. **Off-grid means off-grid.** No cloud LLM in the daily loop. The scheduler runs on the laptop against a local model. Network is used for *pulling public historical data* during setup and for occasional refreshes, never as a runtime dependency of a decision.
2. **Every number carries its provenance and its error bar.** A €30 sensor that claims ±0.3 pH does not get to state pH to one decimal in a report. See §2 for what the hardware can and cannot honestly measure.
3. **The biodynamic calendar is a hypothesis under test, not a scheduling rule.** This is the most interesting part of the project and the easiest to get wrong. See §6.

---

## 1. System architecture

```
   FIELD (birdbox on stake)              HOUSE (laptop, mains)
 ┌──────────────────────────┐        ┌──────────────────────────────────┐
 │ Pico W  (MicroPython)    │        │  oneacre  (Python 3.11+)         │
 │  ├ BME280 air T/RH/P     │        │                                  │
 │  ├ DS18B20 ×2 soil T     │        │  ingest/                         │
 │  ├ capacitive soil VWC×2 │  BLE   │   ├ ble_client  (bleak)          │
 │  ├ BH1750 lux            │ ─────► │   ├ knmi        (De Bilt 260)    │
 │  ├ tipping rain gauge    │  or    │   ├ openmeteo   (ERA5-Land +     │
 │  ├ anemometer + vane     │  LoRa  │   │              Harmonie AROME) │
 │  └ battery V / panel V   │        │   └ pvgis       (PV design)      │
 │                          │        │                                  │
 │ LiFePO4 26650 ─ CN3791   │        │  store/  SQLite + parquet        │
 │ 5–10 W panel @ 65° S     │        │                                  │
 └──────────────────────────┘        │  biodynamic/ skyfield → day-type │
                                     │  solar/      LSTM → PV forecast  │
                                     │  scheduler/  local LLM → advice  │
                                     │  vision/     stock counting      │
                                     └──────────────────────────────────┘
```

**Why the node is a Pico W and not a Raspberry Pi.** A Pi Zero 2 W idles at 0.4–0.6 W. In a Dutch December the 24-hour mean irradiance at De Bilt is ~20 W/m² against ~200 W/m² in June, a **factor of ten**, not a factor of two ([KNMI](https://www.knmi.nl/over-het-knmi/nieuws/zonnestraling-in-december-vergeleken-met-juni)). That puts an always-on Zero 2 W at a ~60 W panel and ~100 Wh of battery: a caravan installation bolted to a birdbox. A duty-cycled Pico W node runs on 0.08–0.24 Wh/day: a 5 W panel and a €3 cell with 60 days of autonomy. **Factor of ~60 in the power budget.** The Pi still has a place in this project; it just isn't in the field box.

**Why not skip BLE and use WiFi/LoRa.** Decide this by measured distance, and decide it in Phase 0 (§3), not later:

| Field-to-house distance | Use |
|---|---|
| ≤ ~20 m, clear line of sight | **BLE**: simplest thing that works, no extra radios |
| ~20–50 m, some vegetation | BLE will work in July and drop out in a wet November. Marginal. |
| ≥ ~50 m | **LoRa point-to-point (SX1262)**: 20–40 dB of margin you never think about again |

BLE's problem at range isn't throughput (your payload is ~10 bits/second against a 235 kbps floor); it's that a dropped connection fails *silently and without retry*, so you lose data during exactly the storm you built the station to observe. Keep BLE as the walk-up service interface regardless of what carries telemetry; that role it does excellently.

**The pluggable boundary.** `ingest/` writes rows into the store. Everything downstream reads the store. Swapping BLE for LoRa touches one module. That is the whole reason for the layering.

---

## 2. What the hardware can honestly measure

Read this before buying anything. Three of the sensors people reflexively buy for this project do not measure what their product page says.

### The NPK channels are fabricated
The cheap 7-in-1 RS485 soil probes report N, P and K in mg/kg. A sensor vendor states plainly in their own product literature that the device measures bulk electrical conductivity and multiplies it by three fixed constants:

> "the soil NPK sensor actually measures the electrical conductivity of the soil… such sensors cannot accurately measure the actual nitrogen, phosphorus and potassium content of the soil on site, but give an empirical, theoretical value." Source: [Niubol](https://www.niubol.com/Product-knowledge/Soil-NPK-Sensors-Principle.html)

So N, P and K are three scaled copies of one number and move together. Add urea and watch phosphorus "rise". **Buy the probe for its moisture, temperature and EC channels (those are real and EC is genuinely useful), and never make a fertiliser decision from the N/P/K registers.** For actual fertility, send soil to a lab (Eurofins Agro, Wageningen) once or twice a year. That costs about what the sensor costs and produces numbers that mean something.

### Continuous in-soil pH is not achievable at this budget
Readings rise by **~1.5 pH units** as the same soil goes from dry to field capacity, the relationship is soil-type dependent (linear in sand, exponential in clay), and below ~11% moisture readings become unreliable ([Vasques et al., *SOIL* 10:321, 2024](https://soil.copernicus.org/articles/10/321/2024/)). A real lab-grade probe is ~€100 with a ~2.5-year life plus a ~€65 high-impedance carrier board, and it needs its glass bulb kept permanently hydrated, which a July soil will not do. **Do pH the boring way:** a sample indoors, 1:5 soil:CaCl₂, calibrated €50 bench meter, twice a year. NL soil pH does not move on a daily timescale, so continuous logging has almost no information value anyway.

### Capacitive soil moisture is a relative index, not %VWC
Expect <400 raw counts across the entire dry→saturated span (the ADC is not the limit, the analog front end is), strong temperature cross-sensitivity, and the ink mask failing inside a year unless epoxy-potted ([Cave Pearl Project](https://thecavepearlproject.org/2020/10/27/hacking-a-capacitive-soil-moisture-sensor-for-frequency-output/)). Also: the onboard 662k regulator goes out of spec below ~3.4 V supply, which is where a LiFePO4 cell lives. **Log soil temperature next to every moisture probe and regress it out.** Getting real %VWC means oven-drying 5–10 jars of your own soil at known water fractions, worth doing once, in Phase 4.

### The two that are unambiguously good
- **DS18B20 waterproof soil temperature**, ±0.5 °C, €4–9. Bury two (10 cm and 30 cm); the phase lag between them is genuinely informative and costs €6. Use a 4.7 kΩ pull-up and **avoid parasite power on long cables**: that is the single most common cause of flaky 1-Wire in a field.
- **SparkFun/Argent weather meters** (rain + anemometer + vane, €72.99 ex VAT). All three are passive reed switches, zero standby current, which is exactly right for solar. Debounce the rain reed in software or you will silently inflate rainfall totals by 10–30%.

### Two configuration traps that produce plausible-looking wrong data
- **BME280 self-heating.** Continuous mode with high oversampling biases its own temperature reading **+1 to +2 °C**. Use forced mode, 1× oversampling, one reading per ≥60 s, sleep between, which is what the power budget wants anyway.
- **No radiation shield = you are not measuring air temperature.** An unshielded sensor in sun errs by up to ~3 °C, and inadequate airflow *compresses the diurnal range*, underestimating maxima and overestimating minima, which looks plausible and is therefore worse than a constant offset. Print a multi-plate Stevenson shield in **ASA or PETG, not PLA** (PLA loses notable strength outdoors within 30 days). Mount the BME280 in the shield on a short I²C tail, away from the electronics' waste heat.

### The condensation trap that will kill the node
A sealed box breathes: warm day, air expands out; cold night, damp air sucked in through every imperfection; over weeks it pumps itself full of water. **A tighter seal makes this worse.** In the Dutch climate this is a certainty, not a risk. Fit a **Gore-type ePTFE pressure-equalisation vent** (~€3, the highest-value three euros in the build), add indicating desiccant, conformal-coat the boards, put every gland and the vent on the *underside*, and drip-loop every cable. Use the wooden birdbox as the decorative rain/sun shell and put a proper IP66 ABS box **inside** it; the air gap between them buffers thermal swings nicely.

### And one destroys hardware rather than data
**Never charge LiFePO4 below 0 °C.** Lithium plates on the anode: 1–5% permanent capacity loss per event, irreversible, dendrite risk. Many cheap 1S BMS boards **do not implement low-temperature charge cutoff**: verify the datasheet or add an NTC + MOSFET yourself. NL frost mornings are also the clear-sky sunny ones, so the correlation works against you. Bury or insulate the cell; soil at 30 cm barely drops below 3–4 °C.

---

## 3. Bill of materials (~€175 ex VAT, ~€100 without the weather meters)

Kiwi Electronics lists **ex 21% VAT**; Tinytronics incl. Prices captured Aug 2026, verify at checkout.

| Item | Source | € ex VAT | Notes |
|---|---|---|---|
| Raspberry Pi Pico 2 W (with header) | Kiwi | 7.19 | VSYS takes 1.8–5.5 V → LiFePO4 direct, no boost |
| BME280 air T/RH/P | Tinytronics | ~6 | forced mode only |
| DS18B20 waterproof ×2 (1 m + 2 m) | Tinytronics | ~12 | 10 cm + 30 cm depth |
| Capacitive soil moisture ×2 | Tinytronics | 8 | epoxy-pot them; buy spares |
| BH1750 lux | Tinytronics | ~5 | call it lux, **not** PAR, in the schema |
| SparkFun Weather Meters SEN-15901 | Kiwi | 72.99 | rain + anemometer + vane, passive reeds |
| LiFePO4 26650 4500 mAh + 1S BMS | NKON (Arnhem) | ~5 | **BMS must have low-temp charge cutoff** |
| CN3791 MPPT charger, LiFePO4 config | AliExpress | ~4 | µA-class quiescent |
| Solar panel 5–10 W ETFE | Kiwi | ~35 | or generic 20 W 12 V glass, €25–45 |
| IP66 ABS box + Gore vent + desiccant + glands | generic | ~15 | inside the birdbox |
| ASA/PETG radiation shield | self-printed | ~3 | [Printables #73421](https://www.printables.com/model/73421-radiation-shields-for-diy-weather-station) |
| **Total** | | **~173** | |

**Optional, considered:** 7-in-1 RS485 probe (~€30) + MAX3485 + 12 V boost; buy only for moisture/temp/**EC**, and power-gate it (0.15 W would otherwise dominate the node). LoRa SX1262 pair (~€20) if Phase 0 measures >50 m.

**The trap when shopping:** a charge controller's own quiescent current can exceed a well-designed node's entire consumption. The Waveshare Solar Power Manager (D) draws **<30 mA quiescent = 3.6 Wh/day**, 15–45× a Pico node's whole budget. **Pick the power path before you pick the MCU.** The CN3791 + direct-to-VSYS route above avoids every boost stage and every mA-class controller.

**Availability note:** Pi Zero 2 W was out of stock at Kiwi with a 14-10-2026 restock at time of writing. Doesn't matter; it isn't in this BOM.

---

## 4. The phases

Each phase has a **goal**, **steps**, and a **done-when** you can actually check. Nothing is "done" because code exists; it is done when it produces a verifiable artefact. Phases 0–3 are sequential. Phase 5 (weather/history) can run in parallel with 1–3 since it needs no hardware; start it on the first rainy evening.

### Phase 0: Repo, decisions, and one measurement (½ day, no hardware)
**Goal:** the repo exists, the site survey is done, and the transport decision is made on evidence.

1. `git init`, first commit of the scaffold, push to GitHub. Public: the project is documentation as much as code.
2. Fill in `docs/DECISIONS.md` ADR-0001 through 0004 (stubs are written; the reasoning is in §1–2 above).
3. **Walk the distance from the plot to where the laptop lives and write the number down.** Then §1's table picks your transport. Do not skip this; it is the one irreversible architectural choice.
4. Record plot geometry: lat/lon of each plot to 5 decimals, aspect, slope, soil type, what was grown there last, panel mounting position and its horizon obstructions. Into `docs/SITE.md`.
5. Set up the Python env: `uv venv && uv pip install -e ".[dev]"` (or venv + pip). Confirm `pytest` runs and finds zero tests without erroring.

**Done when:** repo is on GitHub, ADRs 0001–0004 have a decision line each, `docs/SITE.md` has real coordinates, `pytest` exits 0.

### Phase 1: Bench node (1 weekend)
**Goal:** the node reads every sensor correctly on a desk, powered by USB. No solar, no BLE, no enclosure.

1. MicroPython on the Pico 2 W. Confirm REPL over USB.
2. One sensor at a time, in this order, each fully working before the next: DS18B20 (easiest, unambiguous) → BME280 (**forced mode, 1× oversampling** from the start) → BH1750 → capacitive moisture on the RP2040 ADC → rain reed on an IRQ with debounce → anemometer reed → vane through the ADC divider.
3. `node/sensors/*.py`: one module per sensor, each exposing `read() -> dict` with **units in the key names** (`air_temp_c`, `soil_vwc_raw`, `rain_tips`). Raw counts stay raw at this layer; calibration happens on the laptop where you can redo it without a field trip.
4. `node/link/packet.py`: pack a reading into a compact fixed-schema payload. Include a **schema version byte**. You will change this schema and you will be glad it is versioned.
5. Sanity checks that catch real bugs: breathe on the BME280 (RH must jump), palm the BH1750 (lux must drop), tip the rain bucket ten times by hand (**must read exactly 10**; if it reads 11–13 your debounce is wrong, fix it now not in November), put a DS18B20 in a glass of ice water (must read 0.0–0.5 °C).

**Done when:** a single `main.py` loop prints a complete, plausible reading dict every 60 s for an hour with no exception, and the ten-tip test reads exactly 10.

### Phase 2: The link (1 weekend)
**Goal:** readings arrive on the laptop and land in a database.

1. Node side: BLE peripheral advertising a **Nordic UART Service** (`aioble` on MicroPython). NUS because every phone BLE app already speaks it, which makes field debugging trivial.
2. Laptop side: `src/oneacre/ingest/ble_client.py` using **bleak**. Note bleak is *client-only*: it cannot act as a peripheral, so the topology is forced: laptop = central, node = peripheral. That is the right direction anyway.
3. `store/schema.sql` + `store/db.py`: SQLite, one `readings` table, one row per sensor-timestamp, with `schema_version`, `node_id`, `received_at` **and** `measured_at` (they differ after a dropout, and that difference is data).
4. **Make the node buffer.** Ring buffer of the last N readings in flash; on connect, drain everything since the last acknowledged sequence number. This is the difference between a logger and a toy. Sequence numbers, not timestamps; the Pico has no RTC worth trusting.
5. `oneacre ingest ble --minutes 60` CLI command, and a check that reconnects cleanly after you walk out of range and back.

**Done when:** you unplug the laptop's Bluetooth for 20 minutes, plug it back in, and the database contains **every** reading from that gap with correct `measured_at` values.

*If Phase 0 said LoRa:* same contract, `ingest/lora_client.py` instead, SX1262 point-to-point with a sequence-numbered ack. Everything downstream is unchanged; that is the layering earning its keep.

### Phase 3: Power and deployment (1 weekend + a winter of patience)
**Goal:** the node survives outdoors, unattended, through a Dutch winter.

1. **Measure your own dormant current before sizing anything.** Published Pico W deep-sleep figures disagree by ~30× (16 mA under MicroPython's fake deepsleep, ~0.2–0.5 mA for a proper C-SDK dormant, 180 µA for the bare die). Put a multimeter in series and find out. This changes panel sizing by a factor of several; it does not change the Pico-vs-Pi conclusion.
2. Duty cycle: wake → read → append to buffer → advertise for N seconds → sleep. Budget from your measured number, then **double the panel**: in December the marginal cost of an oversized panel is trivial and it is the only thing harvesting on a dim day.
3. Assemble power: panel → CN3791 (LiFePO4 profile) → cell + BMS **with verified low-temp cutoff** → VSYS directly. No boost stage, no mA-class controller.
4. Enclosure: IP66 box inside the birdbox, Gore vent and all glands on the underside, desiccant in, boards conformal-coated, drip loops on every cable. Radiation shield separate, on a short I²C tail.
5. Panel at **60–75° from horizontal, due south**, much steeper than the annual optimum (~36°). You are deliberately sacrificing summer surplus to catch winter's low sun, and the steep angle sheds snow, leaves and grime.
6. Log **battery voltage and panel voltage as sensor channels.** These are the training data for Phase 7 and the early warning for everything else.
7. Mount height: WMO convention is 1.25–2 m for comparability with KNMI. Lower is fine if you care about microclimate at the plants, but **write which you chose into the metadata**, or your data is not comparable with anything.

**Done when:** 14 consecutive days outdoors with no gaps, no manual intervention, and battery voltage recovering to full on every sunny day. Then a second 14 days spanning a genuinely overcast week.

### Phase 4: Calibration (a weekend, once, properly)
**Goal:** raw counts become numbers with units and error bars.

1. **Soil moisture:** 5–10 jars of your own soil, oven-dried, rewetted to known gravimetric water fractions at consistent bulk density. Fit and store the curve per probe (they differ) in `data/calibration/`. Model the temperature cross-sensitivity from the co-located DS18B20 and subtract it.
2. **Air temperature:** co-locate with De Bilt 260 daily values for a fortnight. A persistent offset is your shield or siting; a *compressed diurnal range* means inadequate ventilation.
3. **Rain:** cross-check monthly totals against De Bilt. Persistent under-reading is usually a not-quite-level gauge.
4. **pH and fertility:** one lab sample per plot. This is your ground truth and it costs about what one bad sensor costs.
5. Every calibration is a versioned file, applied **on read**, never destructively to raw rows. You will improve these curves and want to reprocess history.

**Done when:** `calibration.apply()` turns a raw row into a physical row, and `docs/UNCERTAINTY.md` states a defensible error bar for each channel.

### Phase 5: Public weather and history (can start day one, no hardware)
**Goal:** decades of context around your few months of local readings.

**Sources, in order of value to this project:**

| Source | What for | Access |
|---|---|---|
| **KNMI script service** | De Bilt **station 260**, ~6 km NE of Utrecht, **daily data from 1901-01-01**. Ground truth. Includes `Q` (global radiation) and `EV24` (Makkink reference ET). | `https://www.daggegevens.knmi.nl/klimatologie/daggegevens?stns=260&vars=ALL&start=…&end=…&fmt=json`, **no API key** |
| **Open-Meteo archive** | ERA5-Land 0.1° (~11 km), **1950→present**, 5-day latency. Soil moisture and soil temperature at depth, `et0_fao_evapotranspiration`, VPD: the things a weather station cannot measure. | `archive-api.open-meteo.com/v1/archive?…&models=era5_land`, no key, non-commercial |
| **Open-Meteo forecast** | **KNMI Harmonie AROME at 2 km, hourly updates**, KNMI's own operational high-res model. Best available forecast for a Utrecht plot. | `api.open-meteo.com/v1/forecast?…&models=knmi_harmonie_arome_netherlands` |
| **Open-Meteo satellite radiation** | Satellite-*observed* irradiance (SARAH3, 5 km, 1983→). Computes **plane-of-array irradiance** for you from `tilt`+`azimuth`, which removes an entire transposition step from the PV model. | `satellite-api.open-meteo.com/v1/archive?…&tilt=65&azimuth=0` |
| **PVGIS (EU JRC)** | One-off system sizing and optimum tilt for your exact coordinates. Design tool, not a forecasting tool. | `re.jrc.ec.europa.eu/api/v5_3/PVcalc?…&optimalangles=1`, free, no registration |

**Four traps in this phase, all of which produce silently wrong data:**
- KNMI values are **integer-scaled**: temperatures in 0.1 °C, rain in 0.1 mm, radiation in J/cm² (×2.778 for Wh/m²). `-1` in RH/SQ means "<0.05", not "minus one".
- **KNMI `EV24` is Makkink; Open-Meteo `et0_fao_evapotranspiration` is FAO-56 Penman-Monteith.** They will not agree. Never mix them in one series.
- **Open-Meteo's archive and forecast soil layers use different depth bins** (archive: 0–7/7–28/28–100 cm; forecast: 0/6/18/54 cm). You cannot concatenate them without an explicit mapping step.
- KNMI states its station series are **unsuitable for trend analysis** (relocations, instrument changes). Fine operationally, wrong for climate trending.

**Steps:** one ingester module per source, each writing a tidy long-format table into the store with a `source` column. Cache aggressively; these are historical facts and do not change. Open-Meteo free tier: <10k calls/day, 5k/hour, 600/min, CC-BY-4.0, attribute it.

**Done when:** `oneacre weather backfill --from 1990-01-01` produces a continuous daily series with an explicit gap report, and a plot of your Phase-3 local readings overlaid on De Bilt tracks visibly.

### Phase 6: Biodynamic calendar engine (a weekend, the most interesting week of the project)
Its own section: see §5.

### Phase 7: Solar/battery LSTM (1–2 weeks, after ≥3 months of local data)
**Goal:** predict tomorrow's harvestable energy and the resulting battery state, so power-hungry work gets scheduled into the sun.

1. **Start with a baseline you must beat**: persistence ("tomorrow = today") and a clear-sky-index model. Report skill *relative to these*. An LSTM that cannot beat persistence is a finding, and an honest one.
2. Features: Harmonie AROME forecast irradiance and cloud cover, satellite GTI at your actual panel tilt/azimuth, day-of-year, measured panel voltage, measured battery voltage and its recent trajectory, air temperature (PV efficiency), soil temperature (thermal mass proxy).
3. Targets: next-24h harvested Wh, and battery SoC trajectory.
4. **Walk-forward validation only.** No random train/test splits on a time series; it leaks the future and produces flattering nonsense.
5. **The honest constraint: you will have one winter of data.** An LSTM on ~90 days of a strongly seasonal signal will overfit. Options, in order of preference: pre-train on PVGIS/satellite reconstructed history at your coordinates and fine-tune on local data; or accept that a well-fitted physical model plus a small residual regressor beats a data-hungry network here, and log it as a result. **Do not report a deep model as better than it is because it was more fun to build.**

**Done when:** `oneacre solar forecast` outputs next-24h Wh with a stated interval, and `docs/MODEL_CARD_solar.md` reports skill vs. both baselines on a walk-forward split.

### Phase 8: LLM scheduler (1–2 weeks)
**Goal:** the daily brief. This is where "sensor to scheduler" gets closed.

1. **Local model:** Ollama with a Qwen/Llama-class instruct model sized to your laptop. Keeps the off-grid claim honest and costs nothing per call.
2. **The LLM does not compute.** Every number (degree-days, soil moisture deficit, frost risk, day-type, PV budget) is computed in Python, tested, and passed in as a structured context block. The model's only jobs are *selection*, *prioritisation* and *explanation*. This is the single most important design rule in this phase: an LLM asked to do arithmetic on sensor data will produce confident, plausible, wrong numbers.
3. **Structured output.** The model returns JSON, a list of `{action, crop, plot, window, rationale, confidence, inputs_used}`, validated against a schema. `inputs_used` is what makes the recommendation auditable afterwards.
4. **Constraint layer runs after the model, not inside it.** Hard rules (frost tonight, soil too wet to work, water budget, "this bed is already planted") are Python filters that veto or defer. The LLM proposes; deterministic code disposes.
5. Prompt versioning: prompts in `scheduler/prompts/`, each output row records the prompt hash. When advice changes you need to know whether the world changed or the prompt did.
6. Output: a dated markdown brief to `data/briefs/YYYY-MM-DD.md`. Also the artefact that becomes the public log for the site.

**Done when:** a week of daily briefs, each traceable to its inputs, and at least one where **you disagreed with the recommendation**: write down why, in `docs/DISAGREEMENTS.md`. That file is the actual research output of this project.

### Phase 9: Vision inventory + anomaly detection (spring 2027)
Deliberately last: it needs a full season of data before it means anything.

1. Phone photos of the store shelves → a fine-tuned detector or a local VLM → counts per item per date.
2. Anomaly detection on the compost/fertiliser side: an unsupervised model over the soil temperature, moisture and EC series flagging deviations from the seasonal pattern. **Start with a seasonal decomposition and a threshold**: this is a "boring statistics first" problem, and if the boring version works, that is the result.
3. Every flag is logged with what happened next. Without that, "anomaly detected" is unfalsifiable.

---

## 5. The biodynamic calendar, done honestly

The most interesting and most misrepresented part of this project. Get the history right, compute it correctly, and test it fairly.

### It isn't Steiner's calendar
Steiner's *Agriculture Course* (GA 327, eight lectures at Koberwitz, June 1924) contains the farm-as-organism concept and the numbered preparations. It contains **no root/leaf/flower/fruit scheme and no constellation-to-organ mapping.** The lineage is:

**Steiner 1924** (cosmic-forces doctrine, no calendar) → **Franz Rulni 1948–1979** (hand-distributed constellation seed calendar) → **Maria Thun, first published 1963** (the root/leaf/flower/fruit system everyone actually means; the 2026 edition is the 64th, which confirms the start year).

Thun's radish trials began as an attempt to *test* Rulni's claims. Say "Thun calendar" in the code and the docs, not "Steiner calendar"; the project loses credibility on the first sentence otherwise.

### The mapping
| Element | Organ | Constellations |
|---|---|---|
| Earth | **Root** | Taurus, Virgo, Capricorn |
| Water | **Leaf** | Cancer, Scorpio, Pisces |
| Air/Light | **Flower** | Gemini, Libra, Aquarius |
| Fire/Warmth | **Fruit/Seed** | Aries, Leo, Sagittarius |

### Four things that make this a real computation, not a lookup table

1. **Sidereal, not tropical.** The calendar tracks the Moon against the actual star constellations. Tropical astrological signs are currently offset ~24–25°, roughly a whole sign, so a tropical implementation is **systematically wrong by about two days, every day**. This is the most common bug in hobby implementations.
2. **Real IAU constellation boundaries, unequal in length.** I checked this against the ephemeris rather than trusting the secondhand figures, and the usual quote ("Libra ~18°") is wrong: **Scorpius is the short one**. Measured as the fraction of a sidereal month the Moon actually spends in each constellation: Virgo 3.30 d, Pisces 3.29 d, down to Scorpius **0.68 d**, a 4.8× spread. Consequence: **the day types are structurally unbalanced**: **7.35 root days against 5.63 flower days** per sidereal month, and on a majority-of-day basis over 2027, **107 root days against 67 flower days: 60% more**. (That last figure does vindicate Kollerstrom's critique, *"Root days (Earth) were assigned over 50 per cent more of the month than the Flower days (Air)"*, even though his stated constellation widths do not.) Any statistical test **must** account for this unequal exposure, or you will mistake "root days are more numerous" for "root days work better". Reference figures: `data/fixtures/expected_daytype_frequencies.json`, reproducible with `scripts/thun_reference.py`.
3. **Ascending/descending is declination, not phase.** A ~27.3-day tropical-month cycle of lunar declination, completely independent of the 29.53-day waxing/waning cycle. Ascending = sap-rising, favour above-ground work; descending = the "planting period", favour transplanting and root work. Confusing this with waxing/waning is the second most common bug.
4. **Blanking rules.** Node crossings (both), eclipses, and (in the Thun tradition) perigee are marked unfavourable, with a window of hours either side.

### Implementation: skyfield, MIT-licensed
- `from skyfield.api import load_constellation_map`: 88 IAU/Delporte boundaries from CDS VI/42. **It handles the B1875 precession internally**; you do not.
- Ephemeris: **de440s.bsp (32 MB), 1849–2150.** Covers any historical validation back to 1963. Pin it locally; do not assume a runtime download works off-grid. (For lunar work DE440 is *more* accurate than DE441: it includes the Moon's liquid core.)
- `find_maxima` / `find_minima` are in **`skyfield.searchlib`, not `skyfield.almanac`**; many online examples get this wrong. Use them over apparent lunar declination (`rough_period≈27.3`) for ascending/descending, and over Earth–Moon distance (`rough_period≈27.55`, the *anomalistic* month, a different constant) for perigee/apogee.
- Nodes: `almanac.moon_nodes(eph)` + `find_discrete`. Eclipses: `almanac.lunar_eclipses`. Oppositions/conjunctions: `almanac.oppositions_conjunctions`. **Trines are not provided**: compute from geocentric ecliptic longitude differences ≈120°±orb. The calendar is geocentric.
- **Do not vendor Swiss Ephemeris** (AGPL/commercial dual licence). Skyfield is MIT, JPL kernels are public domain. Much cleaner basis for a public repo.

### Two gotchas that only appear in a correct implementation
- **Ophiuchus.** Real IAU boundaries put a slice of the ecliptic in Ophiuchus, and the Moon spends ~a day per sidereal month there. Thun's zodiac is 12-fold with no Ophiuchus; the printed calendars extend the Scorpio/water region across it. A naive `load_constellation_map` implementation **will disagree with the printed calendar on those days**. Fold `Oph` into water/leaf, but flag it explicitly in the output and verify against a printed edition, because Thun's exact handling is not documented anywhere I could find.
- **Non-zodiacal constellations.** The Moon's orbit is inclined ~5.1°, so it occasionally strays into Orion, Cetus, Auriga, Sextans. Return `None` with a log line rather than crashing or silently defaulting. These are a useful sanity check that you are using real boundaries.

### Validation
There is **no open, licensed dataset of Thun calendar days**: the published calendars are copyrighted compilations and, in the EU, additionally protected by the sui generis database right (Dir. 96/9/EC). The dates themselves are astronomical facts; the compilation is not.

**Protocol:** buy one printed edition (~€10). Hand-key 60–90 days spanning at least two sidereal months into `data/fixtures/thun_validation.json`. **Keep that file out of the public repo**; `.gitignore` already excludes it. Private verification of your own implementation is defensible; republishing a machine-readable Thun calendar is not.

Expect disagreements to cluster on exactly three things: the Ophiuchus fold-in, the node-blanking window width, and transition times of day. **If your mismatches are scattered rather than clustered on those three, you have a real bug**, almost certainly tropical-vs-sidereal.

### The evidence, stated plainly
The specific claim (that the Moon's position against a constellation at sowing measurably changes yield in the corresponding plant organ) is **not supported by the evidence**.

- **Hartmut Spiess (1990)**, working *inside* the biodynamic tradition at the Institute for Biodynamic Research, ran systematic radish seeding trials 1977–1986. He found modest synodic effects but **failed to verify Thun's trigon effect**, precisely the constellation mechanism. Koepf and von Plato's summary: *"No established findings emerged regarding sidereal Moon-trigon positions."*
- **Mayoral et al. (2020)**, *Agronomy* 10(7):955: *"there is no reliable, science-based evidence for any relationship between lunar phases and plant physiology."* The physics is also unkind: lunar tidal force on a 2 m organism is ~1000× smaller than a 1 kg mass at 1 m. Oceans respond to tides through basin-scale resonance over thousands of km; that does not scale down to a plant.
- The one favourable review, **Kollerstrom & Staudenmaier (2001)**, is a contested reanalysis of Spiess's own data by an author who is not a neutral figure. Weigh it accordingly against the primary experimentalist's negative conclusion.
- Separately and honestly: there **is** credible plant science on **moonlight as a weak photoperiodic cue** (circadian entrainment in *Coffea arabica*; phototropin/phytochrome moonlight perception in *Arabidopsis*). That is evidence about photons, not constellations. **Do not let the first launder the second.**

**So what does the calendar do in this system?** It is a **logged covariate**, never a hard constraint. The scheduler may surface "today is a leaf day" as context. Every planting gets its day-type recorded. Then, over seasons, you test it, and you are in an unusually good position to do so, because Phase 5 gives you exactly the weather covariates the historical trials lacked.

**Three design notes if you want the test to mean anything:** sowing date is perfectly confounded with weather and season, so you need many repeated sowings across seasons, randomised and blocked, not one season's comparison. Weight for the unequal day-type frequencies (§5.2). And **pre-register the analysis** in `docs/PREREGISTRATION.md` before the first sowing: with 4 day-types × 4 organ-types × several crops, something will look significant by chance.

A null result, honestly obtained and published, is a genuinely valuable output of this project. Possibly the most valuable one.

---

## 6. Repository layout

_The fully annotated tree, with every stub file and what it is for, is in the [README](../README.md#repository-layout)._

```
one-acre/
├─ docs/            BUILD_PLAN, ARCHITECTURE, BOM, DECISIONS (ADRs), SITE,
│                   DATA_SOURCES, BIODYNAMIC_METHOD, PREREGISTRATION, UNCERTAINTY
├─ node/            MicroPython for the Pico W: sensors/, link/, power/
├─ src/oneacre/     Laptop package
│   ├─ ingest/      ble_client, lora_client, knmi, openmeteo, pvgis
│   ├─ store/       schema.sql, db.py           (SQLite; parquet exports)
│   ├─ biodynamic/  ephemeris, constellations, calendar, validate
│   ├─ solar/       features, baselines, lstm
│   ├─ scheduler/   context, prompts/, llm, constraints, brief
│   ├─ vision/      (Phase 9)
│   └─ cli.py       `oneacre …`
├─ tests/           pytest; biodynamic tests run offline against a pinned kernel
├─ hardware/        wiring diagrams, enclosure STLs, panel siting notes
├─ data/            gitignored except fixtures/README: raw/, processed/,
│                   calibration/, briefs/
├─ notebooks/       exploration only; nothing load-bearing lives here
└─ scripts/         one-off backfills, issue creation
```

**Two conventions worth holding to:**
- **Units in every column and variable name.** `air_temp_c`, `soil_vwc_frac`, `rain_mm`, `irradiance_wm2`. Half the bugs in a project like this are unit bugs, and they are invisible.
- **Raw stays raw.** Calibration and correction apply on read, never destructively. You will improve every curve in this repo and want to reprocess three years of history.

---

## 7. Milestones → GitHub issues

`scripts/create_issues.sh` creates these with `gh` once the repo is pushed. Each is one focused piece of work.

| # | Milestone | Phase | Done when |
|---|---|---|---|
| 1 | Site survey + transport decision (ADR-0004) | 0 | Distance measured, table in §1 applied, ADR written |
| 2 | Python env, CI, pre-commit | 0 | `pytest` and `ruff` green on GitHub Actions |
| 3 | DS18B20 + BME280 reading on the bench | 1 | Ice-water test passes; forced mode confirmed |
| 4 | Soil moisture, lux, rain, wind on the bench | 1 | Ten-tip test reads exactly 10 |
| 5 | Packet format + schema versioning | 1 | Round-trip test in `tests/` |
| 6 | BLE peripheral (NUS) on the node | 2 | Readable from a phone BLE app |
| 7 | `bleak` ingest → SQLite | 2 | 60 min of readings land with correct timestamps |
| 8 | Node-side ring buffer + ack'd backfill | 2 | 20-minute dropout loses zero readings |
| 9 | Measure real dormant current | 3 | A number in `docs/POWER_BUDGET.md` |
| 10 | Power path assembled, low-temp cutoff verified | 3 | Cell will not charge below 0 °C, tested in a freezer |
| 11 | Enclosure, vent, shield, deployment | 3 | 14 days outdoors, zero gaps |
| 12 | KNMI ingester (station 260, 1901→) | 5 | Backfill with gap report |
| 13 | Open-Meteo archive + forecast ingesters | 5 | ERA5-Land soil layers stored; depth-bin mapping documented |
| 14 | Satellite radiation + PVGIS sizing | 5 | Optimum tilt for the actual site, recorded |
| 15 | Skyfield day-type engine | 6 | Ophiuchus and out-of-zodiac cases handled explicitly |
| 16 | Ascending/descending, nodes, perigee, blanking | 6 | Turning points found via `searchlib` |
| 17 | Validation against a purchased printed edition | 6 | Mismatches cluster on the three known causes |
| 18 | Calibration curves + uncertainty doc | 4 | `calibration.apply()` + stated error bars |
| 19 | Solar baselines (persistence, clear-sky) | 7 | Skill scores recorded: the bar the LSTM must clear |
| 20 | LSTM + walk-forward validation + model card | 7 | Honest comparison against #19 |
| 21 | Scheduler context builder (all numbers in Python) | 8 | Context block is fully tested, LLM-free |
| 22 | Local LLM + structured output + constraint layer | 8 | Schema-validated JSON; constraints veto correctly |
| 23 | Daily brief generation + public log | 8 | Seven consecutive dated briefs |
| 24 | Pre-registration of the biodynamic analysis | 6/8 | Written **before** the first sowing |
| 25 | Vision inventory spike | 9 | Counts from shelf photos |

---

## 8. Risks, and what to do about them

| Risk | Likelihood | What it costs | Mitigation |
|---|---|---|---|
| BLE link unreliable at the real distance | **High if >30 m** | Silent data loss in bad weather | Measure in Phase 0; switch to LoRa. The `ingest/` boundary makes this a one-module change. |
| Condensation kills the node | **Near-certain without a vent** | A dead node in February | ePTFE vent + desiccant + conformal coat + underside glands. €5 total. |
| LiFePO4 charged below 0 °C | Moderate | Permanent, irreversible cell damage | Verify BMS low-temp cutoff **in a freezer** before deployment |
| Sensor data plausible but wrong (self-heating, no shield, reed bounce) | **High: this is the default outcome** | Months of confidently wrong analysis | The four bench tests in Phase 1; cross-check against De Bilt in Phase 4 |
| LSTM overfits one winter | High | An impressive-looking model that forecasts nothing | Baselines first (#19), walk-forward only, pre-train on reconstructed history |
| LLM does arithmetic and gets it wrong | **Certain if allowed** | Confident, plausible, wrong advice | All numbers computed in Python; LLM selects and explains only |
| Biodynamic analysis finds a spurious effect | Moderate | The project's credibility | Pre-register (#24); weight for unequal day-type frequency |
| Scope creep into the vision/inventory side | High, it is the fun part | The core loop never closes | Phase 9 is gated behind a full season of data. Hold the line. |

---

## 9. Rough sequencing

| When | Focus |
|---|---|
| **Sep 2026** | Phases 0–1. Order the BOM week one; shipping is the long pole. Phase 5 ingesters on rainy evenings. |
| **Oct 2026** | Phase 2 (link), Phase 6 (biodynamic engine: indoor work, well suited to shortening days). |
| **Nov 2026** | Phase 3. Deploy before the weather turns. The first winter *is* the hard test. |
| **Dec–Feb** | Let it run. Phase 4 calibration, Phase 5 completion, Phase 7 baselines. Fix what breaks, and something will. |
| **Mar–Apr 2027** | Phase 8 scheduler live for the spring sowing. Pre-registration written **before** the first seed goes in. |
| **May–Sep 2027** | Summer plot. Second node if the first survived. Phase 9. First season of biodynamic day-type data. |
| **Oct 2027** | Write up. Including, especially, whatever came back null. |

---

## 10. Immediate next actions

1. **Walk the plot-to-laptop distance and write the number in `docs/SITE.md`.** Everything in Phase 2 depends on it.
2. **Order the BOM.** Kiwi + Tinytronics + NKON covers all of it; the CN3791 is the only AliExpress item and therefore the long pole; order that first.
3. **Push the repo and create the issues** (`scripts/create_issues.sh`).
4. **Start Phase 5 tonight**: it needs no hardware. The KNMI ingester against station 260 is an hour's work and gives you 125 years of De Bilt to look at while you wait for parcels.
5. **Buy one printed Thun calendar** now; you need it in Phase 6 and it ships slowly.

---

## Appendix: sources

**Hardware:** [KNMI Dec vs Jun irradiance](https://www.knmi.nl/over-het-knmi/nieuws/zonnestraling-in-december-vergeleken-met-juni) · [Cave Pearl: capacitive soil sensors](https://thecavepearlproject.org/2020/10/27/hacking-a-capacitive-soil-moisture-sensor-for-frequency-output/) · [Cave Pearl: BH1750 vs PAR](https://thecavepearlproject.org/2024/08/10/using-a-bh1750-lux-sensor-to-measure-par/) · [Niubol: how NPK sensors work](https://www.niubol.com/Product-knowledge/Soil-NPK-Sensors-Principle.html) · [Vasques et al. 2024, in-situ pH](https://soil.copernicus.org/articles/10/321/2024/) · [BME280 self-heating](https://github.com/esphome/issues/issues/402) · [Barani: radiation shield error](https://www.baranidesign.com/faq-articles/2019/5/5/sensor-and-radiation-shield-comparison-calculator-for-temperature-error) · [3D-printed shields, ASA vs PLA](https://hackaday.com/2022/02/04/3d-printed-radiation-shields-get-put-to-the-test/) · [Gore condensation management](https://www.gore.com/solutions-condensation-management) · [LiFePO4 cold charging](https://gridwright.com/blog/lifepo4-cold-charging) · [bleak docs (client-only)](https://bleak.readthedocs.io/) · [BLE throughput](https://novelbits.io/bluetooth-5-speed-maximum-throughput/)

**Data:** [KNMI script service](https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script) · [KNMI Data Platform](https://dataplatform.knmi.nl/) · [De Bilt 260 series from 1901](https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/temp_260.txt) · [Open-Meteo historical](https://open-meteo.com/en/docs/historical-weather-api) · [Open-Meteo forecast](https://open-meteo.com/en/docs) · [Open-Meteo satellite radiation](https://open-meteo.com/en/docs/satellite-radiation-api) · [Open-Meteo terms](https://open-meteo.com/en/terms) · [PVGIS API](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en)

**Biodynamic:** [Steiner GA 327](https://rsarchive.org/Lectures/GA327/) · [Biodynamic Association UK on the calendar](https://www.biodynamic.org.uk/the-biodynamic-sowing-and-planting-calendar/) · [Bross-Burkhardt critical review](https://terrabc.org/cms/uploads/2019/02/Mondkalender_und_Aussaattage_kritisch_betrachtet.pdf) · [Lunarium on unequal constellations](https://www.lunarium.co.uk/articles/lunar-gardening/) · [Mayoral et al. 2020](https://www.mdpi.com/2073-4395/10/7/955) · [Spiess 1990](https://www.tandfonline.com/doi/abs/10.1080/01448765.1990.9754544) · [Kollerstrom & Staudenmaier 2001](https://www.tandfonline.com/doi/abs/10.1080/01448765.2001.9754928) · [Chalker-Scott, WSU](https://s3.wp.wsu.edu/uploads/sites/403/2015/03/biodynamic-agriculture.pdf) · [Skyfield](https://rhodesmill.org/skyfield/) · [Thun-Verlag](https://thun-verlag.com/aussaattage2023/)

**Uncertainties flagged during research, to resolve yourself:** Pico W true dormant current (sources disagree ~30×, measure it); BLE range figures (from an SEO-flavoured source, plan on half); Tinytronics prices (not machine-readable, verify at checkout); how Thun handles Ophiuchus (undocumented, check a printed edition); KNMI Data Platform hourly/daily dataset path identifiers (resolve from the dataset browser); the KNMI script service's long-term future (Dataverkenner is stated to eventually replace it, keep a fallback).
