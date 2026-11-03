# HX1_hot_ladder: result

Criteria 495b3dae23, committed alone before any script. Code, AMENDMENT A1 and checks K1-K2: 9291c1344e, before any graded number. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 are reported apart, never pooled. No LCDM input. A description: no action, no field equation, no particle, no fluid, no halo. Not route E: nothing is added, the law's own phantom is multiplied. The cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. Not blind.

**Question.** Is there one boost of the law's phantom, g = g_N + B(sigma) (law - g_N), keyed on a hot system's measured velocity dispersion, that lifts each dispersion-supported class by what it needs, ellipticals through groups to clusters?

## Verdict: NO LADDER on both footings. Stage 2 (a fitted B(sigma) through RQ3) doesn't run, as frozen.

The boost each class needs isn't one function of sigma. MaNGA ellipticals at sigma 170-260 km/s need B 3-4, as much as X-COP clusters at 1000 km/s. Groups between them need 1.1-1.5. Inside each cluster, the need also falls with radius, so no single boost per system fits a cluster's profile.

| rung (key sigma, km/s) | canonical: median B_need, y = log B, s | alt |
|---|---|---|
| ATLAS ellipticals (98) | 1.59, +0.20 +- 0.34 | 1.39, +0.14 +- 0.34 |
| MaNGA Q1 (110) | 1.95, +0.29 +- 0.11 | 1.72, +0.24 +- 0.12 |
| Tian groups (144) | 1.18, +0.07 +- 0.08 | 1.08, +0.03 +- 0.08 |
| SLUGGS (152) | 1.64, +0.22 +- 0.15 | 1.45, +0.16 +- 0.15 |
| MaNGA Q2 (170) | 3.15, +0.50 +- 0.10 | 2.79, +0.45 +- 0.10 |
| MaNGA Q3 (210) | 3.55, +0.55 +- 0.08 | 3.15, +0.50 +- 0.08 |
| MaNGA Q4 (256) | 4.22, +0.63 +- 0.08 | 3.73, +0.57 +- 0.08 |
| Lovisari groups, R500 (469) | 1.53, +0.19 +- 0.10 | 1.38, +0.14 +- 0.10 |
| Lovisari groups, R2500 (469) | 2.49, +0.40 +- 0.10 | 2.24, +0.35 +- 0.10 |
| X-COP (1035) | 4.09, +0.61 +- 0.14 | 3.66, +0.56 +- 0.14 |

| test | canonical | alt |
|---|---|---|
| L-ORDER (isotonic in sigma, B >= 1) | chi2 17.2, p 0.005, **NOT ORDERED** | chi2 16.2, p 0.009, **NOT ORDERED** |
| L-NEED (X-COP) | Z +4.42, PASS | Z +4.06, PASS |
| L-FLAT, X-COP (log B_need on log x) | slope -0.335 +- 0.026, Z -12.8, **NOT FLAT** | -0.332 +- 0.026, Z -12.9, **NOT FLAT** |
| L-FLAT, Lovisari (R2500 - R500) | +0.211, Z +1.52, FLAT | +0.210, Z +1.51, FLAT |
| L-KEY (MaNGA, 1195 with B > 0) | sigma +0.90 (Z +17.4), gbar(Re) +0.07 (Z +2.5): BOTH | +0.90 (Z +17.4), +0.06 (Z +2.2): BOTH |
| **Stage 1 class** | **NO LADDER** | **NO LADDER** |

Reported only (no external field in the B1 integral): Local Group dwarfs (8.7 km/s) need B 1.46, Fornax dwarfs (26) 1.50, Virgo dwarfs (32) 1.79 on canonical; 1.32, 1.36, 1.62 on alt. Numbers: `hx1_ladder.out`, `hx1_ladder.json`.

## What it says, plainly
- **Almost every hot class asks for more than the law, but not in step with sigma.** The only rung consistent with B = 1 is the Tian groups. The MaNGA ellipticals' need climbs with sigma (L-KEY, Z +17), up to the clusters' level by 256 km/s. Then it drops back to 1.5 for the Lovisari groups at twice that sigma.
- **Inside the clusters, the need falls with radius as about x^-0.33.** The inner X-COP points need more boost than the outer ones, so a boost that is one number per system can't match B25's shape or the keys, even if the order held. The Lovisari groups lean the same way (R2500 needs more than R500), but there the difference is within the errors.
- **The order break comes from the MaNGA ellipticals.** Post-read and reported only (`hx1_post.out`), without MaNGA the rest line up: p 0.37 / 0.42 (0.23 / 0.26 without ATLAS too). MaNGA's need is measured inside Re, where the law is close to Newton and the stellar IMF moves D_N. A bottom-heavy IMF in high-sigma ellipticals would also give a need that climbs with sigma. So the break can be read as IMF, and HX1 can't separate the two. Even then X-COP's L-FLAT failure stands, and the ladder would read LADDER, NOT FLAT, with B25 and the keys predicted to fail.

## Expectations on record against results
| Expectation (criteria) | Result |
|---|---|
| L-ORDER ORDERED, canonical (35 %) | NOT ORDERED. Right, but not for the reason given: SLUGGS against the Tian groups is a small step (+0.22 against +0.07). The break is MaNGA against Lovisari |
| L-NEED (97 %) | PASS. Right |
| L-FLAT, X-COP (30 %) | NOT FLAT, Z -12.8. Right |
| L-FLAT, Lovisari (25 %) | FLAT, Z +1.5. Wrong; the difference is +0.21, inside a wide error |
| MaNGA ill-conditioned (60 %) | No. Errors 0.075-0.11 dex, set by the +-0.10 dex mass systematic. Wrong |
| NO LADDER on both footings (55 %) | Right |

## Checks
- **K1 PASS.** At B = 1 the machinery gives RQ3's own law rows on both footings: B1 to 1e-17, A26a and B23 exactly, B2 to 4e-4 (`hx1_ladder_checks.out`, before any graded number).
- **K2 PASS.** Linearity at B = 2 to 6e-16 for the B1 integral and X-COP. SLUGGS's closed form is off by 1.6e-6, and the root is used there (A1).
- **K3 PASS.** At the real keys and errors, a planted ladder reads median p 0.45 with NEED Z 3.0. A planted break reads median p 0.000, and the real keys do put ellipticals below the groups' sigma.
- **K4 PASS.** The rerun is byte-identical (`hx1_post_checks.out`, cmp exit 0).
- **MUTATE** (B_need to 1/B_need): NEED fails on both footings, exit 1 by the result.

## Disclosures
1. **X-COP has 35 points, not 60.** The criteria wrote "its 60 points". The rung uses B23's own point set, which keeps a radius only where all three profiles reach it, and K1 reproduces B23 exactly on it.
2. **`hx1_post.py` was written after the read.** It changes no label.
3. **The key sigma for the cluster and the Lovisari rungs comes from kT** with beta_spec = 1, using TX1's emission-weighted kT for X-COP. The cluster temperatures were seen while testing TX1's loader, before the run.

## Limits
These are the criteria's limits. Everything is static and spherical. The Tian rungs are isotropic Hernquist, SLUGGS uses a gamma 3 tracer, and Lovisari and X-COP are hydrostatic (X-COP DISPUTED). Inside Re, B_need carries the IMF. The Lovisari star masses come from h7's relation. The dwarfs have no external field and are reported only. Red KiDS lenses have no sigma per lens and aren't graded.

## Files
`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `hx1_ladder.py` (stage 1), `hx1_acc.py` (loads RQ3's acceptance.py unedited), `hx1_post.py`, `run_hx1.sh`. The harness's byte copies are `old_gates.py`, `tolerances.json` and `row_marks.json`. Outputs: `hx1_ladder{,_checks,_MUTATE}.{out,json}`, `hx1_post.out`, `hx1_post_checks.out`.
