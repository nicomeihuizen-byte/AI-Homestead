"""LoRa SX1262 point-to-point receiver. Only if Phase 0 measured >50 m.

Same contract as ble_client: unpack, ack, write into `readings`. That the swap is one module
is the entire point of this layering.

EU 868 duty cycle applies but is a non-issue at one 60-byte packet per minute — verify which
sub-band your frequency lands in if you ever raise the rate.

TODO — only if ADR-0004 says LoRa.
"""
