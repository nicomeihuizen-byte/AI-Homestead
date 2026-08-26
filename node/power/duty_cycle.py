"""Wake -> read -> buffer -> advertise for N s -> sleep.

BEFORE sizing anything: put a multimeter in series and measure your own dormant current.
Published Pico W figures disagree by ~30x (16 mA under MicroPython's fake deepsleep, ~0.2-0.5 mA
for a proper C-SDK dormant, 180 uA for the bare die). This changes panel sizing by a factor of
several. Record the number in docs/POWER_BUDGET.md.

TODO Phase 3.
"""
