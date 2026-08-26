# Power budget

## Measure first

Published Pico W dormant figures disagree by ~30x: 16 mA under MicroPython's `deepsleep` (which
does not actually enter DORMANT and does not power down the CYW43), ~0.2-0.5 mA for a proper
C-SDK dormant, 180 uA for the bare RP2040 die. **Put a multimeter in series and find out.**

| | Measured | Date | Notes |
|---|---|---|---|
| Dormant current | | | |
| Active current (reading) | | | |
| Active current (BLE advertising) | | | |
| Duty cycle | | | |
| **Average draw** | | | |
| **Daily Wh** | | | |

## Sizing

`Panel_W = Daily_Wh / (PSH_Dec x derate)` with PSH_Dec ~= 0.55 and derate ~= 0.55,
i.e. **divide daily Wh by ~0.30**.

De Bilt: June 24 h mean ~200 W/m2, December ~20 W/m2, a factor of ten. And that is a MONTHLY
MEAN: NL routinely delivers runs of 5-10 consecutive days at 0.05-0.15 PSH, near-zero harvest.
**Size the panel for the mean and the battery for the dark run.**

| | Computed | Chosen | Why |
|---|---|---|---|
| Panel W | | | |
| Battery Wh | | | |
| Days of autonomy | | | |
| Tilt / azimuth | | | 60-75 deg due south: winter-biased, sheds snow and grime |

## The trap

A charge controller's own quiescent current can exceed the node's entire consumption. Waveshare
Solar Power Manager (D): <30 mA quiescent = 3.6 Wh/day = 15-45x a Pico node's whole budget.
CN3791 + LiFePO4 direct to VSYS (1.8-5.5 V) avoids every boost stage and every mA-class part.

## Freezer test: before deployment

Charging LiFePO4 below 0 C plates lithium: 1-5% permanent capacity loss per event, irreversible.
Many cheap 1S BMS boards omit low-temperature charge cutoff.

- [ ] BMS datasheet states low-temp charge cutoff
- [ ] Verified in a freezer: cell refuses charge below 0 C
- [ ] Cell insulated or buried (soil at 30 cm barely drops below 3-4 C in NL)
