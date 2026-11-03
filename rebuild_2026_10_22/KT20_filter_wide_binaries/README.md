# KT20_filter_wide_binaries: PREDICTION, nothing graded. KT17's filter suppresses the wide-binary boost below about 5-8 kAU and matches plain QUMOND above about 15 kAU. At 3 kAU the excess is 15-27 percent of plain's; at 10 kAU 70-91 percent

Criteria: `FROZEN_CRITERIA.md` (94562be676, with KT18 and KT19's), alone first, confirmed landed. `kt20.py`, `kt20.out`, `kt20.json`, `kt20_MUTATE.out`, `kt20_MUTATE.json`. No download; no Gaia data used; the DR4 pre-registration is untouched. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Register K831.

Binary of total mass M as a point mass smoothed over xi = 0.55 sqrt(G M / a0), simple nu, 1D external-field form, spherical average. gamma = g / g_N.

Excess (gamma - 1) of the filter as a fraction of plain QUMOND's, external field 1.9e-10 m/s^2:

| s, kAU | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| canonical, 1.0 Msun (xi 4378 AU) | 0.07 | 0.14 | 0.22 | 0.38 | 0.59 | 0.85 | 0.99 | 1.00 | 1.00 |
| canonical, 1.5 Msun (xi 5362 AU) | 0.06 | 0.12 | 0.18 | 0.30 | 0.45 | 0.71 | 0.95 | 1.00 | 1.00 |
| alt, 1.0 Msun (xi 3983 AU) | 0.09 | 0.18 | 0.27 | 0.46 | 0.67 | 0.91 | 1.00 | 1.00 | 1.00 |
| alt, 1.5 Msun (xi 4878 AU) | 0.08 | 0.15 | 0.22 | 0.37 | 0.53 | 0.78 | 0.98 | 1.00 | 1.00 |

Half-suppression separation s_half: 5.4-7.8 kAU across mass, footing and external field (2.32e-10 gives about 3 percent larger). Plain gamma at 30 kAU: 1.31-1.42 in this 1D form.

## The prediction, in plain words
- **Plain QUMOND:** the boost turns on around 2-5 kAU and is near its full value by 7-10 kAU.
- **The filter:** almost Newtonian below about 3 kAU (gamma under 1.04), rising through 5-10 kAU, and the same as plain QUMOND from about 15 kAU out. **The turn-on moves outward by about a factor of two, and heavier pairs turn on later** (s_half grows as sqrt(M)).
- A Gaia test separates them by comparing the excess at 2-5 kAU with that at 10-20 kAU: plain predicts roughly 0.2-0.3 at 3-5 kAU (gamma 1.12-1.29), the filter 0.02-0.13. At 10-20 kAU both give about 0.3-0.4.
- **What this doesn't test:** the published claims disagree on whether any boost is seen at all. A fully Newtonian result at 10-20 kAU would rule out both, filter included.

## Limits
1D external-field form, spherical average; the real external-field effect is anisotropic and the projection onto observed velocities isn't done. These shift gamma's level but not the filter-to-plain ratio's turn-on separation much. Nothing here grades the model against data.

## Checks
C1: plain form against the direct formula, at most 1.7e-16. C2: excess ratio at 30 kAU 1.000 in every case (0.95 frozen). MUTATE (nu = 1): gamma = 1 exactly, exit 1.
