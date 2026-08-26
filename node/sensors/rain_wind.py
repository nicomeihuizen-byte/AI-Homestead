"""Tipping rain gauge, anemometer, wind vane (SparkFun/Argent SEN-15901).

All three are passive reed switches -> zero standby current, which is exactly right for solar.

- Rain: 0.2794 mm per tip. Count on a GPIO IRQ. DEBOUNCE IT.
  Bench test: tip the bucket ten times by hand. Must read exactly 10. If it reads 11-13,
  your debounce window is too short and every rainfall total you ever record will be
  inflated by 10-30%.
- Anemometer: 1 closure/s = 2.4 km/h. Stalls below ~1-1.5 m/s, so calm reads exactly zero
  rather than "light air" - do not mistake that for a fault.
- Vane: 8 reed switches + resistor divider -> RP2040 ADC. 22.5 deg resolution, no better.
"""

MM_PER_TIP = 0.2794
KMH_PER_HZ = 2.4


def read() -> dict:
    """TODO Phase 1. Return rain_tips (cumulative), wind_rev, vane_raw."""
    raise NotImplementedError
