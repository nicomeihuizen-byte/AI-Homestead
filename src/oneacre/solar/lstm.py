"""LSTM for next-24h harvestable Wh and battery SoC trajectory.

WALK-FORWARD VALIDATION ONLY. A random train/test split on a time series leaks the future and
produces flattering nonsense.

THE HONEST CONSTRAINT: you will have one winter of data. An LSTM on ~90 days of a strongly
seasonal signal will overfit. In order of preference:
  1. pre-train on PVGIS/satellite-reconstructed history at your coordinates, fine-tune on local
  2. accept that a physical model plus a small residual regressor beats a data-hungry network
     here, and log that as a result

Do not report a deep model as better than it is because it was more fun to build.

TODO Phase 7.
"""
