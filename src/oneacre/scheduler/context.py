"""Build the structured context block for the LLM.

EVERY NUMBER IS COMPUTED HERE, IN TESTED PYTHON. Degree-days, soil moisture deficit, frost risk,
PV budget, day-type, days-since-last-rain. The model never does arithmetic on sensor data —
it will produce confident, plausible, wrong numbers if allowed to. See ADR-0003.

This module must be fully testable with no LLM involved.

TODO Phase 8.
"""
