# Field node — Raspberry Pi Pico 2 W, MicroPython

Copy these onto the Pico with `mpremote` or Thonny. `main.py` runs on boot.

    mpremote connect auto fs cp -r sensors link power main.py :

## Order of work (Phase 1)

Get one sensor fully working before adding the next. In this order — easiest and least ambiguous
first, so that when something misbehaves you know which thing changed:

1. `sensors/ds18b20.py` — ice-water test must read 0.0–0.5 °C
2. `sensors/bme280.py` — **forced mode, 1× oversampling** from the very first line of code.
   Continuous mode with high oversampling self-heats the die by +1 to +2 °C and you will not notice.
3. `sensors/bh1750.py` — palm test: lux must drop
4. `sensors/soil_moisture.py` — RP2040 ADC, no external ADC needed. Raw counts only.
5. `sensors/rain_wind.py` — tip the bucket ten times by hand. **Must read exactly 10.**
   11–13 means reed bounce and your debounce is wrong. Fix it now, not in November.

## Contract

Every sensor module exposes `read() -> dict` with **units in the key names**
(`air_temp_c`, `soil_vwc_raw`, `rain_tips`). Raw counts stay raw here — calibration happens on the
laptop, where it can be redone and history reprocessed without a field trip.
