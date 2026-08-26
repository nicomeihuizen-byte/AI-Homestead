# Pre-registration: the biodynamic day-type analysis

**Write and freeze this BEFORE the first sowing of spring 2027.** With 4 day-types x 4 organ-types
x several crops, something will look significant by chance. That is the whole reason this file
exists.

## Hypothesis under test

Sowing a crop on a day whose Thun day-type matches the crop's harvested organ (root crop on a
root day, etc.) produces a measurably different yield than sowing it on a non-matching day.

## Prior

Against. Spiess (1990), working inside the biodynamic tradition at the Institute for Biodynamic
Research, ran systematic radish trials 1977-1986 and found modest synodic effects but failed to
verify the trigon effect. Mayoral et al. (2020) find no reliable evidence for lunar-phase effects
on plant physiology, and the tidal-force mechanism fails by ~3 orders of magnitude. The one
favourable review (Kollerstrom & Staudenmaier 2001) is a contested reanalysis of Spiess's own
data by a non-neutral author.

**A null result, honestly obtained and published, is a valid and valuable output of this project.
Possibly the most valuable one.**

## Design: fill in before sowing

- Crops and organs:
- Number of sowing dates per crop per season:
- Randomisation and blocking scheme:
- Bed assignment (must be randomised, bed quality is a confound):
- Response variable and how it is measured:
- Weather covariates conditioned on (from Phase 5):

## Analysis plan: fill in before sowing

- Model specification:
- **Weighting for unequal day-type frequency** (roughly 9 root days to 5-6 flower days per
  sidereal month, this is not optional):
- Handling of blanked days:
- Multiple-comparison correction:
- Pre-specified primary test (exactly one):
- What result would change my mind, in either direction:

## Known confound

Sowing date is perfectly confounded with weather and season. One season's comparison proves
nothing. This needs many repeated sowings across multiple seasons, randomised and blocked. The
upside: the Phase 5 weather pipeline gives us exactly the covariates the historical trials
lacked, which is a genuine advantage over Thun's and Spiess's own designs.

## Frozen on

_date, and the git commit hash of this file_
