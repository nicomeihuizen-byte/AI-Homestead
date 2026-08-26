# Site survey

Answered 2026-08-26 for location, timezone and reference data. **The physical survey of each
plot is still open**, and ADR-0004 cannot be closed until the link distance is measured on site.

Two plots, worked in alternation: **2256 km and 14.57 degrees of latitude apart**. That is the
point of the project rather than an inconvenience. You follow the growing season instead of
fighting it.

## Plots

| | Summer plot | Winter plot |
|---|---|---|
| Name | **Prora**, Ruegen, Germany | **Castelo Branco**, Portugal |
| Slug (`config.SITES`) | `prora` | `castelo_branco` |
| Latitude (5 dp) | **54.38970** | **39.82220** |
| Longitude (5 dp) | **13.57440** | **-7.49310** |
| Timezone | Europe/Berlin | Europe/Lisbon |
| Setting | Baltic coast, maritime | inland central Portugal |
| Cultivated through | summer | winter |
| Area | TODO | TODO |
| Aspect (compass bearing of slope) | TODO | TODO |
| Slope | TODO | TODO |
| Soil type (and lab result once available) | TODO: send a sample, Phase 4 | TODO |
| Previous crop / history | TODO | TODO |
| Shading: what, which hours, which months | TODO | TODO |

Coordinates are plot-centre placeholders good to a few hundred metres, adequate for choosing a
reanalysis grid cell and a reference station. **Re-measure to 5 dp at the stake position before
Phase 3**, because panel siting and horizon obstructions are decided from that point, not this one.

## Winter sun, by geometry

Exact for these latitudes; no data source needed, and the reason the hardware is sized the way it is.

| | Prora | Castelo Branco |
|---|---|---|
| Solstice daylight | 7.0 h | 9.2 h |
| Solstice noon sun elevation | 12.2 deg | 26.7 deg |
| Panel tilt (latitude + 15 heuristic) | 70 deg **TODO: confirm with PVGIS** | 55 deg **TODO: confirm with PVGIS** |

**The node is one design, built once and driven between the plots, so it is sized for Prora.**
Every decision in the power path is a Prora decision.

## Node siting

Per plot, and neither is filled in yet.

- Stake position relative to plot: TODO x2
- **Sensor mounting height:** _____ m. WMO convention is 1.25 to 2 m for comparability with the
  reference station; lower measures plant microclimate instead. Whichever you choose, it goes in the
  metadata; otherwise the data is not comparable with anything. **Use the same height at both plots**
  or you have added a confound to the one comparison this project exists to make.
- Soil probe depths: 10 cm and 30 cm (confirm)
- Panel: azimuth _____ (target: due south at both), tilt _____ deg (see the table above)
- **Horizon obstructions from the panel position**: bearing and elevation of anything that blocks
  low winter sun. Trees, the house, a hedge. At Prora, where the sun peaks at 12.2 degrees, an
  obstruction 15 degrees up to the south costs you the entire winter. Survey this one properly.

## Link

Measured per plot. ADR-0004 may resolve differently at each, and that is allowed.

- **Straight-line distance, node to laptop: _____ m at Prora, _____ m at Castelo Branco**
- Obstructions in the path: walls, hedges, glazing (note if low-E coated, worth 10 to 20 dB at 2.4 GHz)
- Transport decision: ______________ (record in ADR-0004)

## Reference stations

| | Prora | Castelo Branco |
|---|---|---|
| Provider | **DWD** Climate Data Center | **IPMA** |
| Station | **Arkona, 00183**, 33.5 km N, same island | Castelo Branco, long-series table |
| Daily series from | **1947-01-01** | TODO: confirm from the published table |
| Measured global radiation | **yes**, one of ~64 in DWD's daily solar network | no |
| Open historical API | yes, plain HTTP, no key, CC BY 4.0 | **no** |
| Deep history therefore comes from | the station, checked against ERA5-Land | ERA5-Land, checked against IPMA |
| Best free forecast | ICON-D2, 2 km | ICON-EU, 7 km |

**The two plots are not equally well observed, and no analysis may quietly pretend otherwise.**
See ADR-0007 and `docs/DATA_SOURCES.md`.
