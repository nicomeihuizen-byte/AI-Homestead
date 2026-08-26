"""BLE peripheral: Nordic UART Service, via `aioble`.

NUS because every phone BLE app already speaks it, which makes field debugging trivial: walk up
to the box with your phone and read live values.

Topology is forced by the laptop side: `bleak` is a GATT *client* only and cannot act as a
peripheral. So laptop = central, node = peripheral. That is the right direction anyway.

TODO Phase 2: advertise, accept a connection, stream buffered readings, handle acks.
"""
