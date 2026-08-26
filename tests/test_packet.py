"""Wire format round-trip. Phase 1."""

import pytest

pytestmark = pytest.mark.skip(reason="Phase 1 — implement node/link/packet.py first")


def test_pack_unpack_roundtrip():
    ...


def test_schema_version_is_carried():
    """You will change the schema. Make sure the version byte survives the trip."""
