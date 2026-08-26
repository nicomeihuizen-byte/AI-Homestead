"""SQLite access. Raw stays raw; calibration applies on read.

TODO Phase 2: connect(), init_schema(), insert_readings(), query helpers.
Use WAL mode — the ingester and your notebooks will both want the file open.
"""
