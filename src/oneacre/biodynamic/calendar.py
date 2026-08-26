"""Thun day-type engine.

Say "Thun calendar", not "Steiner calendar". Steiner's Agriculture Course (GA 327, June 1924)
contains no root/leaf/flower/fruit scheme and no constellation-to-organ mapping. The lineage is
Steiner 1924 -> Franz Rulni 1948-79 -> Maria Thun, first published 1963.

Output per day: constellation, organ, whether folded from Ophiuchus, ascending/descending,
blanking (node / eclipse / perigee) and the engine version that produced it.

THIS IS A LOGGED COVARIATE, NEVER A HARD CONSTRAINT. The scheduler may surface "today is a
leaf day" as context. The evidence does not support the trigon effect — Spiess (1990), working
inside the biodynamic tradition, failed to verify it across a decade of trials. See
docs/BUILD_PLAN.md section 5 and docs/PREREGISTRATION.md.

TODO Phase 6: day_type(date) -> DayType, and a range generator that writes into `daytypes`.
"""

ENGINE_VERSION = "0.1.0-dev"
