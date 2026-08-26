# Site survey

Fill this in during Phase 0. Everything downstream depends on it, and ADR-0004 cannot be closed
without the distance measurement.

## Plots

| | Summer plot | Winter plot |
|---|---|---|
| Latitude (5 dp) | | |
| Longitude (5 dp) | | |
| Area | | |
| Aspect (compass bearing of slope) | | |
| Slope | | |
| Soil type (and lab result once available) | | |
| Previous crop / history | | |
| Shading: what, which hours, which months | | |

## Node siting

- Stake position relative to plot:
- **Sensor mounting height:** _____ m. WMO convention is 1.25–2 m for comparability with KNMI
  station data; lower measures plant microclimate instead. Whichever you choose, it goes in the
  metadata; otherwise the data is not comparable with anything.
- Soil probe depths: 10 cm and 30 cm (confirm)
- Panel: azimuth _____ (target: due south), tilt _____ ° (target: 60–75° for winter capture)
- **Horizon obstructions from the panel position**: bearing and elevation of anything that blocks
  low winter sun. Trees, the house, a hedge. This matters far more in December than in June.

## Link

- **Straight-line distance, node to laptop: _____ m**  ← ADR-0004 depends on this
- Obstructions in the path: walls, hedges, glazing (note if low-E coated, common in NL and worth
  10–20 dB at 2.4 GHz)
- Transport decision: ______________ (record in ADR-0004)

## Reference station

De Bilt, **KNMI station 260**, ~6 km NE of Utrecht centre. Daily series from 1901-01-01.
Cabauw (348, ~22 km SW) is the CESAR/BSRN radiation supersite, a good independent check on `Q`.
