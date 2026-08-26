"""BLE central using `bleak`. Node = peripheral (NUS), laptop = central.

`bleak` is a GATT client only: it cannot act as a peripheral, so this topology is forced.
Linux needs BlueZ >= 5.55.

TODO Phase 2:
  - scan for the node by name/service UUID
  - subscribe to the NUS TX characteristic
  - unpack packets, ack sequence numbers, write into `readings`
  - reconnect cleanly after walking out of range, and drain the node's backfill
"""
