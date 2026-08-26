"""Field node main loop.

Phase 1: run this over USB and just print. Phase 2: buffer + advertise. Phase 3: duty-cycle.

Read docs/BUILD_PLAN.md §4 before filling this in.
"""

import time

# TODO Phase 1: import each sensor module as you get it working
# from sensors import ds18b20, bme280, bh1750, soil_moisture, rain_wind

READ_INTERVAL_S = 60
SCHEMA_VERSION = 1


def read_all() -> dict:
    """Collect one full reading. Units in key names. Raw counts stay raw.

    TODO Phase 1: call each sensor's read() and merge. A failing sensor should log and return
    None for its channels, not take down the whole loop — one dead probe must not cost you
    a month of data from the others.
    """
    return {
        "schema_version": SCHEMA_VERSION,
        "uptime_ms": time.ticks_ms(),
        # "air_temp_c": ..., "air_rh_pct": ..., "air_pressure_hpa": ...,
        # "soil_temp_10cm_c": ..., "soil_temp_30cm_c": ...,
        # "soil_vwc_raw_a": ..., "soil_vwc_raw_b": ...,
        # "lux": ..., "rain_tips": ..., "wind_rev": ..., "vane_raw": ...,
        # "batt_v": ..., "panel_v": ...,   # <- Phase 3; these are Phase 7 training data
    }


def main() -> None:
    # TODO Phase 2: replace print with buffer.append() + BLE advertise
    # TODO Phase 3: replace the sleep with a real duty cycle (power/duty_cycle.py)
    while True:
        print(read_all())
        time.sleep(READ_INTERVAL_S)


if __name__ == "__main__":
    main()
