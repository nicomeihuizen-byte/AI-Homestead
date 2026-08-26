"""Wire format for one reading.

Include the schema version byte. You WILL change this schema and you will be glad it is versioned.
Use a sequence number, not a timestamp; the Pico has no RTC worth trusting. The laptop stamps
`received_at`; the node's sequence number plus its known interval reconstructs `measured_at`.

TODO Phase 1: pack()/unpack() with a round-trip test in tests/test_packet.py.
"""

SCHEMA_VERSION = 1


def pack(reading: dict, seq: int) -> bytes:
    raise NotImplementedError


def unpack(payload: bytes) -> tuple[dict, int]:
    raise NotImplementedError
