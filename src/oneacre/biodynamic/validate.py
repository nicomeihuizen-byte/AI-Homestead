"""Validate the engine against a hand-keyed sample from ONE purchased printed edition.

The fixture (data/fixtures/thun_validation.json) is gitignored and stays local. Published
calendars are copyrighted compilations and, in the EU, additionally protected by the sui
generis database right (Dir. 96/9/EC). The dates themselves are astronomical facts and we
compute them ourselves; private verification of your own implementation is defensible,
republishing a machine-readable Thun calendar is not.

Protocol: 60-90 days spanning at least two full sidereal months.

EXPECT disagreements to cluster on exactly three things:
  1. the Ophiuchus fold-in
  2. the node-blanking window width
  3. boundary-crossing times of day

If your mismatches are SCATTERED rather than clustered on those three, you have a real bug,
almost certainly tropical-vs-sidereal.

TODO Phase 6.
"""

FIXTURE = "data/fixtures/thun_validation.json"
