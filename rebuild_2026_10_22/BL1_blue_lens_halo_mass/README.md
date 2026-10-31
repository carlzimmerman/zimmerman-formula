# BL1_blue_lens_halo_mass: blue KiDS lenses need no halo-mass shift in amplitude (COLOUR SPLIT), but route E's shape still loses to the law

Criteria: `FROZEN_CRITERIA.md` (c64f9be055), committed alone before any script or number. Script `bl1_blue.py`, S2's forward model read-only. Outputs `bl1.out`, `bl1_results.json`. Reported afterwards: `bl1_posthoc.py`, `bl1_posthoc.out`, `bl1_posthoc.json`.

## Frozen grade (route E at EM1's M200, FC1's core rule, halo continued to r_ta; A = data/model in CFG829's window, 6 points)
| class | canonical A | alt A | Δ log M200 for A = 1, canonical (2σ) | law A, canonical / alt |
|---|---|---|---|---|
| blue | **1.053 ± 0.095 consistent** | 1.046 ± 0.094 consistent | **+0.03 (−0.10, +0.14)** | 0.878 / 0.802 |
| red | 1.649 ± 0.083 short | 1.647 ± 0.083 short | +0.32 (+0.25, +0.38) | 1.313 / 1.200 |
| all | 1.494 ± 0.054 short | 1.490 ± 0.054 short | +0.26 (+0.21, +0.30) | 1.207 / 1.103 |

**Grade: BLUE CONSISTENT. Colour reading: COLOUR SPLIT,** both footings: Δ_blue's 2σ range contains 0 and Δ_red's does not. Profile T (cut at R200) gives the same amplitudes within 0.01.

So X55's 0.4 dex gap is not present in amplitude for blue lenses, the population SPARC actually samples. On "all" it is driven by the red lenses.

## This is not a pass of the shape
Reported after the result. It comes from checking this win as hard as a fail.

| canonical | χ², all 15 bins: route E / law | χ², 6-point window, no amplitude: route E / law |
|---|---|---|
| blue | **109.2 / 27.5** | 25.0 / 9.2 |
| red | 562.4 / 136.7 | 100.9 / 27.3 |
| all | 693.1 / 78.7 | 168.8 / 30.5 |

The amplitude agrees only because a slope miss averages out. Blue data/route E runs 0.63, 0.71, 1.16, 1.53, 2.04, 1.59 across the window from inner to outer, and 3 to 6 beyond it, where the law stays near 1. Route E's ΔΣ falls about as R⁻² past R200, and these data fall about as R⁻¹.

X53's caveat applies directly: the isolation here is photometric and leakage adds a ~1/R excess. BL1 does not separate the two. SI1 tests that on spectroscopic isolation.

## Red masses (reported)
S2's red-mass ladder (M★ +0.123 dex from CFG667; +0.172 more from CFG926's IMF), applied to route E as to the law, canonical:

| red M★ | route E red A | route E all A | law red A | law all A | χ²(15), all: route E / law |
|---|---|---|---|---|---|
| R0 | 1.649 ± 0.083 | 1.494 ± 0.054 | 1.313 | 1.207 | 693 / 79 |
| R1 +0.123 | 1.386 ± 0.070 | 1.325 ± 0.048 | 1.191 | 1.129 | 634 / 53 |
| R2 +0.295 | **1.080 ± 0.054 consistent** | 1.104 ± 0.040 between | 1.023 | 1.012 | 569 / 39 |

Route E's amplitude responds more strongly than the law's, because EM1's M200 rises with M★. At R2 the amplitude gap is nearly gone for both classes. The χ² gap is not. The red-mass choice remains open (CFG667 §3).

## Checks
K1 (S2's L4 reproduced, |d| 0), K2 (M_h(R200) 2e-15), K3 (solve 2e-15), MUTATE (halo × 0.5: blue A 1.053 → 1.871): all PASS. 0 saturated solves. Runs: single thread, under 1 GB.

**Code error, mine, fixed before this write-up.** The first run printed "GAP IN BOTH". The colour test had the two ends of the 2σ range swapped: the bound named "lo" is the upper one. The printed ranges already showed blue containing 0. Only that label line changed, and the rerun's numbers are identical.

## What this does not show
- Blue M★ has its own scale error, not measured here. A 0.2 dex offset moves Δ_blue by about 0.2.
- S2's central colour split is u − r 2.0-based (`typ`). The u − r 2.5 split gives blue A 1.041, but that split leaves very few red lenses (1,432), and its K5 ratios against B21 are far from 1 (1.78, 1.44). Do not rely on it.
- A colour split is a new requirement on the halo rule, not a derivation. Nothing here says why red lenses would be heavier at fixed M★, apart from the mass-scale question above.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
