# What each channel is actually worth

**Fill this in per plot.** The same sensor is not worth the same at both: Prora is checked against
DWD station 00183, which has measured radiation 33.5 km away, while Castelo Branco is checked
against ERA5-Land with IPMA as a weaker cross-reference. Where a channel's realistic accuracy
differs between the plots, say so rather than averaging them.

Fill in during Phase 4. No number goes in a brief or a chart without a line here.

| Channel | Instrument | Stated accuracy | Realistic accuracy | Known bias | Calibrated against |
|---|---|---|---|---|---|
| `air_temp_c` | BME280 in ASA shield | +/-1.0 C | | self-heating if not forced mode; shield error up to ~3 C in sun and low wind | reference station, 14 d |
| `air_rh_pct` | BME280 | +/-3% | | | |
| `air_pressure_hpa` | BME280 | +/-1 hPa | | | |
| `soil_temp_*_c` | DS18B20 | +/-0.5 C | | none worth arguing about | ice water |
| `soil_vwc_*` | capacitive | n/a | | strong temperature cross-sensitivity; ink mask degrades within a year; false-dry as soil shrinks away | oven-dried jars, per probe |
| `rain_mm` | tipping bucket | 0.2794 mm/tip | | reed bounce inflates totals 10-30% if undebounced; under-reads if not level | reference-station monthly totals |
| `wind_kmh` | 3-cup reed | 2.4 km/h per Hz | | stalls below ~1-1.5 m/s: calm reads exactly 0 | |
| `wind_dir` | 8-reed vane | 22.5 deg | | | |
| `lux` | BH1750 | n/a | | photopic-weighted. **NOT PAR**: deriving PPFD is +/-15% at best vs +/-5% for a quantum sensor, and the coefficient is only valid for the spectrum you calibrated under | |
| `batt_v`, `panel_v` | divider + ADC | | | | bench PSU |

## Not measured, and why

- **pH**: continuous in-soil pH is not achievable at this budget. Readings shift ~1.5 pH units
  dry-to-field-capacity and go unreliable below ~11% moisture. Lab sample, 1:5 CaCl2, twice a year.
- **N, P, K**: the cheap RS485 probes derive all three from one bulk EC measurement times three
  fixed constants; the vendor says so in their own literature. Lab sample once or twice a year.
- **EC**: real and useful, if the RS485 probe is fitted. Salinity, fertigation events,
  irrigation fronts. Confounded by moisture, temperature and texture, so trend it, don't level it.
- **PAR**: would need an Apogee quantum sensor at EUR 250-450. Out of scope; `lux` is a
  daylight/cloudiness index and is named accordingly.
