# AZ2 AMENDMENT A2 (2026-11-12, post hoc, committed alone before the A2 run; corrects A1)

**A1's diagnosis was wrong (sign misread).** The KA3 gap is chi^2_free - chi^2_profile_min = -0.357 / -0.373: the FREE fit is
the LOWER one. The free fit is fine; the profile minimum sits above it because the 2.33-node grid is coarse (step 0.5 outside
the flat band) and the free best X5 = 1.74 falls between grid points 1.5 and 2.0 (profile 0.36 and 0.39 above the free
minimum). A1's change (restart the free fit from the lowest profile point) is therefore inert: the stopped A1 canonical run
(`az2_canonical_A1_partial_stopped.out`, five cells) reproduces the frozen numbers digit for digit. A1's code stays in the
script, inert; the remaining A1 runs were stopped and are not used.

**Every Delta chi^2 in the frozen runs is measured from the free minimum** (min(free, profile) = free), so D_band, D_rival and
the labels are not affected by the gap. What failed is KA3 as a check of the profile optimizer.

**Seen before writing this:** everything listed in A1, plus the frozen MUTATE runs for both footings (headline cell T2 Om 0.30:
sqrt X 1.32 -> 1.79, D_band 1.76 -> 22.2; mutated headline FLAT FAILS) and the five A1 canonical cells.

**Change (only this).** The profile grid in each cell is augmented with the free-fit X5 and with X5_best +- 0.05, 0.10, ...,
0.50. KA3 is then checked as frozen (profile minimum within 0.1 of the free fit) and now tests what it was meant to test: that
the profile re-minimisation reaches the free fit at the free fit's own X5. Band, rival, labels, headline cell, KA1/KA2, MUTATE
and its bite rule are unchanged. Run with `AZ2_A2=1`; outputs `az2_<mode>[_MUTATE]_A2.json/.out`. RESULT.md reports the frozen
reading (headline cell NO VERDICT on KA3 as frozen) and the A2 reading.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
