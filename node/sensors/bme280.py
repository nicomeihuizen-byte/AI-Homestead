"""BME280 air temperature / humidity / pressure.

CRITICAL: forced mode, 1x oversampling, one reading per >=60 s, sleep between.
Continuous mode with high oversampling biases the die's own temperature reading by +1 to +2 C.
It looks completely plausible, which is what makes it dangerous.

Bench test: breathe on it. RH must jump and recover.
"""


def read() -> dict:
    """TODO Phase 1. Return air_temp_c, air_rh_pct, air_pressure_hpa."""
    raise NotImplementedError
