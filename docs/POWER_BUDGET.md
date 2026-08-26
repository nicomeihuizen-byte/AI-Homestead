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

**Size for Prora**, the northern plot: 7.0 h of daylight on the winter solstice with the sun
peaking at 12.2 degrees. Castelo Branco (9.2 h, 26.7 degrees) is the easy site and does not get a
vote, because the node is one design driven between both plots.

TODO Phase 5: **PSH_Dec above is still the old De Bilt figure. Re-derive it for Prora** from DWD
station 00183 (Arkona) daily solar data, which is measured global radiation 33.5 km from the plot.
Expect it to come out lower. Whatever the monthly mean turns out to be, a Baltic winter delivers
runs of consecutive near-zero days, so **size the panel for the mean and the battery for the dark
run.**

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
