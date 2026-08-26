"""Flash ring buffer + acknowledged backfill.

This is the difference between a logger and a toy. On connect, drain everything since the last
acknowledged sequence number.

Acceptance test for Phase 2: turn off the laptop's Bluetooth for 20 minutes, turn it back on,
and every reading from the gap must be in the database with correct measured_at values.

TODO Phase 2.
"""
