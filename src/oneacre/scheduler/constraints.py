"""Deterministic constraint layer. Runs AFTER the model, not inside it.

Hard rules that veto or defer: frost tonight, soil too wet to work, water budget exhausted,
bed already planted, insufficient PV budget for a power-hungry task.

The LLM proposes; this disposes. If the model is unavailable, context + constraints is still a
usable fallback brief — which is a good property for an off-grid system.

TODO Phase 8.
"""
