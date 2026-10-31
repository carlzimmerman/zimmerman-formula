# SI2_spec_isolated_colour: with the same red stellar-mass scale for both models, the lensing tension is gone on clean lenses. Conditional on that scale

Criteria: `FROZEN_CRITERIA.md` (9f87d6aef2), committed alone before any number from this split. Script `si2_grade.py <kids_source_cache> <work_dir>` execs SI1's text. Outputs `si2.out`, `si2_results.json`, `si2_MUTATE.*`. Reported afterwards: `si2_sens.py`, `si2_sens.out`, `si2_sens.json`.

## Frozen combined reading (canonical, all lenses at R2): **LENSING TENSION GONE ON CLEAN LENSES**
R2 is S2's ladder: red lenses and red neighbours (u − r > 2.0) +0.295 dex in M★ (+0.123 CFG667, +0.172 CFG926's IMF relation), blue unchanged. It moves both models. Red fraction: S1 0.853, S3 0.910.

| footing, sample, line | χ² law (p) | χ² route E (p) | Δχ² | D | class |
|---|---|---|---|---|---|
| **canonical S3, all R2** | 19.3 (0.199) | 8.7 (0.893) | −10.6 | 2.77 | NOT POWERED |
| **canonical S1, all R2** | 22.7 (0.091) | 22.3 (0.099) | −0.3 | 4.63 | NEITHER |
| canonical S1, blue R0 | 16.7 (0.335) | 20.8 (0.143) | +4.1 | 2.09 | NOT POWERED |
| canonical S1, red R0 | 32.5 (0.006) | 48.6 (0.000) | +16.1 | 4.79 | LAW PREFERRED |
| canonical S1, red R2 | 34.2 (0.003) | 32.2 (0.006) | −2.0 | 5.27 | NEITHER, both poor |
| canonical S3, blue R0 | 17.1 (0.314) | 13.7 (0.549) | −3.4 | 0.87 | NOT POWERED |
| canonical S3, red R2 | 19.8 (0.179) | 9.8 (0.831) | −10.0 | 2.78 | NOT POWERED |
| alt S3, all R2 | 21.3 (0.128) | 8.7 (0.893) | −12.6 | 3.16 | ROUTE E PREFERRED |
| alt S1, all R2 | 29.0 (0.016) | 22.4 (0.097) | −6.6 | 5.26 | NEITHER |

## What the amplitudes say (A = data/model, canonical, all R2)
| | A_in | A_O1 (0.4–1.1 Mpc) | A_O2 (1.1–2.6 Mpc), law |
|---|---|---|---|
| S1 route E | **0.99 ± 0.14** | **1.89 ± 0.39** | |
| S1 law | **1.00 ± 0.12** | **0.72 ± 0.16** | 0.16 ± 0.19 |
| S3 route E | 1.37 ± 0.23 | 1.29 ± 0.77 | |
| S3 law | 1.41 ± 0.23 | 0.47 ± 0.31 | −0.13 ± 0.35 |

Three readings:
- **Inside 0.31 Mpc the two models agree with each other, and R2 is what brings S1 to 1.** At R0 they sit at 1.39 and 1.29.
- **At 0.4–1.1 Mpc the data lie between them on S1:** route E is 2.3σ short, the law 1.8σ over.
- **Beyond 1.1 Mpc the law overshoots on both samples,** at every rung, and route E does not.

## How it moves with the shift (reported; canonical)
| red shift, dex | S3 Δχ² (χ² H) | S1 Δχ² (χ² H, χ² L) | S1 class | S1 A_in H / L |
|---|---|---|---|---|
| 0 | −5.1 (12.6) | +8.7 (24.4, 15.8) | LAW PREFERRED | 1.39 / 1.29 |
| 0.123 | −7.2 (10.9) | +4.9 (21.9, 17.0) | LAW PREFERRED | 1.21 / 1.17 |
| 0.2 | −8.6 (9.8) | +2.5 (21.3, 18.8) | LAW PREFERRED | 1.11 / 1.09 |
| **0.295** | **−10.6 (8.7)** | **−0.3 (22.3, 22.7)** | **NEITHER** | **0.99 / 1.00** |
| 0.4 | −13.1 (7.8) | −3.1 (26.9, 30.1) | NEITHER | 0.88 / 0.91 |

**The frozen class depends on the rung.** At R0 and R1 the combined reading would be MIXED: LAW PREFERRED on S1, but with route E's p above 0.05, so TENSION REMAINS never triggers. χ²(H) on S1 is lowest around +0.2 and worsens by +0.4; the law's rises throughout. S1's A_in = 1 at about +0.3 for both models, which is an internal hint at R2's size; it is not independent, because EM1's M200 moves with M★.

## Limits on R2
- **The rungs are not of equal standing.** +0.123 is a measured estimator difference (old minus young lenses, Taylor vs LePhare, CFG667). It is not shown which estimator is right.
- **+0.172 is ATLAS3D's early-type M/L, applied here to every u − r > 2 lens.** That colour cut takes 85–91 % of these lenses, and it surely includes discs. CFG926's own reading is that the split rests on a declared asymmetry (discs not bottom-heavy) and reads PARTIAL under the record's SLUGGS ceiling.
- **Route E's M200 moves with the IMF rung through EM1's relation.** A bottom-heavy IMF adds stellar mass without any obvious reason to add halo mass. EM1 was calibrated on discs at Υ near 0.5. This choice was frozen and it helps route E more than the law.
- Cold and hot gas stay tied to catalogue M★, as in S2.

## Checks
K1 (colour for all 124,428 LePhare matches), K2 (R0, no split reproduces SI1, 0.0), K3 (blue + red = all, 2.1e-15), MUTATE (labels swapped: red R2 χ²(H) 32.20 → 17.71): all PASS.

**Disclosures.** Shifted neighbours' halos are read through the catalogue-ratio inversion in `g_halo`. The hole term is the sample's full iso-random stack, not colour-matched; the raw L − R variant is its size check (canonical S1 at R2: law 51.1, route E 33.7, Δχ² −17.4, D 4.19, ROUTE E PREFERRED with p(H) 0.004; S3: −13.9, D 2.83, NOT POWERED). Blue lenses are few (S1 1,563; S3 202).

## What this does not show
- It does not measure KiDS leakage. N is small. A neighbouring photo-z sample with this hole term is the next test.
- Route E still has the 2.3σ deficit at 0.4–1.1 Mpc on S1 at R2, and p(H) 0.099 is not a clean fit. Neighbours fainter than r 19.8 are not modelled and could supply part of it; not computed.
- It does not say the data favour route E: S3 is NOT POWERED and S1 is NEITHER at R2.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
