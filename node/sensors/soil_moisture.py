"""Capacitive soil moisture, on the RP2040's own ADC.

This is a RELATIVE index, not %VWC. Honest limitations:
  - <400 raw counts across the whole dry->saturated span. The ADC is not the limit; the
    analog front end is. A 16-bit external ADC would not help.
  - Strong temperature cross-sensitivity - always log the co-located DS18B20 and regress it out.
  - The onboard 662k regulator goes out of spec below ~3.4 V, which is where LiFePO4 lives.
  - The ink mask fails within a year unless epoxy-potted. Buy spares.
  - As soil dries it shrinks away from the probe, giving false-dry readings.

Raw counts only here. The calibration curve lives on the laptop (Phase 4) so it can be
improved and history reprocessed without a field trip.
"""


def read() -> dict:
    """TODO Phase 1. Return soil_vwc_raw_a, soil_vwc_raw_b."""
    raise NotImplementedError
