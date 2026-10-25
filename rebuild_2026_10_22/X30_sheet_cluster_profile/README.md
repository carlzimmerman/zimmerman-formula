# X30_sheet_cluster_profile: does the X26 sheet's hydrostatic cluster profile match the INNER / MID / OUTER shear bands?

Criteria: `FROZEN_CRITERIA.md` (c6be83f91c, committed alone, before any script or number). No amendment. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy is gravitating field mass, never a particle. Nothing fitted: the sheet
points are X26's committed scenario-B allowed set. Not "theory closed". Nothing here says the data favour the framework.
Every number is from `x30_sheet_cluster_profile.out` / `_results.json`.

## Verdict (frozen classes): **PROFILE EXCLUDES THE SHEET (OUTER: G-OUT-all, G-OUT-T1, G-OUT-T2, G-OUT-T3)**, both footings

- **All 19 (canonical) and 16 (alt) sheet points FAIL**, including the two MGAS500 survivors. No point is PASS and none is
  INNER-ONLY.
- **The binding band is OUTER (1.42–3 Mpc).** The OUTER all-KT stack and all three OUTER KT terciles fail at every point,
  in both h cells:
  - all-KT: |Z| 5.4–11.0 (canonical) and 6.0–10.8 (alt);
  - terciles: Z_T1 −2.4 to −4.9, Z_T2 −2.7 to −6.8, Z_T3 −3.6 to −7.2.
- **At the 7 r = 0 points the MGAS500 OUTER grades fail too, with X7's calibrated errors.** OUTER all Z −5.8 to −13.4, and
  every OUTER MGAS500 tercile fails.
- **What passes everywhere:**
  - MID terciles and MID slope. This is X26's own cut, reproduced exactly (K0a).
  - The OUTER KT slope: Z −2.0 to +1.2. The predicted OUTER rise with KT has about the right size; the level is wrong.
  - INNER all-KT: Z −0.1 to +0.5. It is uninformative at σ_IN ≈ 1.4–1.7, as frozen.

**Reading.** The sheet's partial-retention profile puts the cold mass far out:
- its core radius is 2–5 × the gas core;
- 0.03–0.23 % of the retained cold mass lies inside 0.15 Mpc, and 0.7–4.5 % inside 0.5 Mpc;
- the rest lies out to r_ta.

Fixing MID therefore raises OUTER about as much as MID (pred OUTER/MID 0.97–1.12, all-KT stacks). The data have OUTER **below** the
law in the KT sample (0.72 ± 0.14 against MID 1.67 ± 0.19, canonical h 0.672).

This is X2's V1 statement ("any monotone component added to the law that fixes MID overshoots OUTER"), now made quantitative
for the sheet's own profile. The overshoot is 4–11σ, not X2's 1.8–3.6σ lower bound from a point mass.

## Measured bands (step 0; X21 / X7 / X2 conventions; canonical h 0.672, alt h 0.672 in brackets)

| selection | INNER (σ_IN = X2 (e)) | MID | OUTER |
|---|---|---|---|
| KT, 106, all | 1.94 ± 1.67 (1.78 ± 1.53) | 1.67 ± 0.19 (1.53 ± 0.17), reported | 0.72 ± 0.14 (0.66 ± 0.13) |
| KT terciles | 1.16 ± 1.84 / 2.52 ± 0.78 / 2.15 ± 3.08, reported | 1.10 ± 0.38 / 1.65 ± 0.32 / 2.13 ± 0.25 (X21) | 0.39 ± 0.32 / 0.62 ± 0.23 / 1.03 ± 0.22 (0.36 / 0.57 / 0.94) |
| KT slope b | 3.19 ± 2.13, reported | +2.24 ± 0.74 (X21) | +1.50 ± 0.64 (+1.38 ± 0.59) |
| 326, all | 2.28 ± 1.05 (2.09 ± 0.96) | — | 0.93 ± 0.10 (0.85 ± 0.09), X7 CAL |
| 326, MGAS500 terciles | — | 1.10 / 1.85 / 1.84, X7, reported (X26 A3 line) | 0.49 ± 0.30 / 0.76 ± 0.14 / 1.37 ± 0.10 (0.45 / 0.70 / 1.26), X7 CAL |

- The KT-sample INNER and OUTER values are new summaries of X7's committed arrays, made with X21's code and seeds. The other
  values reproduce the record exactly (K0b, K0c).
- σ is σ_STAT = max(bootstrap, jackknife) for KT (X21's convention) and X7 CAL for the 326.
- The INNER cross-shear offset is −1.14 to −1.25 in A units. That is why σ_IN is about 3 × σ_STAT.
- X13's selection correction does not apply: no source split is made here.

## Predicted vs measured per sheet point (h 0.672; the h 0.686 values are in the `.out`; every grade needs both h cells)

KT c_s is the median over the 106 KT clusters. Pred columns are A_pred = Σ d(C\* + cold) / Σ d(C\*). The MGAS500 OUTER Z
appears only at r = 0. * marks an X26 A3 MGAS500 survivor.

**Canonical** (measured OUTER all 0.72 ± 0.14; terciles 0.39 / 0.62 / 1.03)

| log c_*, r, q | KT c_s | INNER pred | MID terciles pred | OUTER all pred (Z) | OUTER terciles pred | MGAS500 OUTER all Z |
|---|---|---|---|---|---|---|
| 2.375, +0.375, −0.125 | 587 | 2.12 | 1.76 / 1.95 / 2.46 | 2.02 (−9.3) | 1.78 / 1.94 / 2.25 | |
| 2.500, +0.250, −0.125 | 632 | 1.82 | 1.41 / 1.60 / 2.26 | 1.79 (−7.6) | 1.50 / 1.66 / 2.10 | |
| 2.500, +0.375, 0 | 586 | 1.62 | 1.66 / 1.74 / 1.96 | 1.87 (−8.2) | 1.75 / 1.83 / 1.99 | |
| 2.625, +0.125, −0.125 | 685 | 1.64 | 1.20 / 1.37 / 2.10 | 1.61 (−6.3) | 1.29 / 1.45 / 1.96 | |
| 2.625, +0.250, 0 | 636 | 1.40 | 1.33 / 1.44 / 1.79 | 1.64 (−6.6) | 1.45 / 1.55 / 1.85 | |
| 2.750, 0, −0.125 | 736 | 1.54 | 1.08 / 1.22 / 1.97 | 1.47 (−5.4) | 1.16 / 1.30 / 1.84 | −5.8 |
| 3.000, 0, +0.250 | 584 | 1.67 | 1.43 / 1.69 / 2.47 | 2.00 (−9.1) | 1.60 / 1.84 / 2.41 | −11.0 |
| 3.125, −0.125, +0.250 | 627 | 1.50 | 1.19 / 1.39 / 2.24 | 1.74 (−7.3) | 1.32 / 1.53 / 2.21 | |
| **3.125, 0, +0.375 \*** | 595 | 1.37 | 1.38 / 1.54 / 1.99 | 1.84 (−7.9) | 1.56 / 1.73 / 2.12 | −9.3 |
| 3.250, −0.250, +0.250 | 674 | 1.40 | 1.08 / 1.21 / 2.07 | 1.57 (−6.0) | 1.17 / 1.33 / 2.04 | |
| 3.250, −0.125, +0.375 | 641 | 1.24 | 1.15 / 1.28 / 1.80 | 1.59 (−6.2) | 1.29 / 1.44 / 1.93 | |
| 3.625, −0.250, +0.750 | 547 | 1.61 | 1.74 / 2.01 / 2.55 | 2.26 (−11.0) | 1.95 / 2.18 / 2.56 | |
| 3.750, −0.500, +0.625 | 629 | 1.44 | 1.12 / 1.29 / 2.51 | 1.79 (−7.6) | 1.25 / 1.46 / 2.44 | |
| 3.750, −0.375, +0.750 | 585 | 1.38 | 1.29 / 1.51 / 2.31 | 1.90 (−8.4) | 1.47 / 1.71 / 2.37 | |
| 3.875, −0.625, +0.625 | 663 | 1.37 | 1.06 / 1.15 / 2.30 | 1.62 (−6.4) | 1.15 / 1.27 / 2.24 | |
| 3.875, −0.500, +0.750 | 638 | 1.27 | 1.13 / 1.25 / 2.09 | 1.66 (−6.7) | 1.26 / 1.41 / 2.16 | |
| 3.875, −0.375, +0.875 | 599 | 1.30 | 1.36 / 1.49 / 1.97 | 1.79 (−7.6) | 1.52 / 1.65 / 2.09 | |
| 4.000, −0.625, +0.750 | 688 | 1.21 | 1.06 / 1.13 / 1.91 | 1.51 (−5.6) | 1.15 / 1.25 / 1.98 | |
| 4.000, −0.500, +0.875 | 645 | 1.19 | 1.15 / 1.26 / 1.79 | 1.56 (−6.0) | 1.28 / 1.39 / 1.90 | |

**Alt** (measured OUTER all 0.66 ± 0.13; terciles 0.36 / 0.57 / 0.94)

| log c_*, r, q | KT c_s | INNER pred | MID terciles pred | OUTER all pred (Z) | OUTER terciles pred | MGAS500 OUTER all Z |
|---|---|---|---|---|---|---|
| 2.625, +0.125, −0.125 | 685 | 1.92 | 1.27 / 1.48 / 2.34 | 1.72 (−8.3) | 1.37 / 1.55 / 2.11 | |
| 2.625, +0.250, 0 | 636 | 1.57 | 1.44 / 1.59 / 2.02 | 1.78 (−8.7) | 1.56 / 1.69 / 2.02 | |
| 2.750, 0, −0.125 | 736 | 1.79 | 1.13 / 1.30 / 2.19 | 1.57 (−7.1) | 1.21 / 1.38 / 1.99 | −8.4 |
| 2.750, +0.125, 0 | 691 | 1.41 | 1.21 / 1.35 / 1.86 | 1.58 (−7.2) | 1.32 / 1.46 / 1.87 | |
| 2.875, 0, 0 (universal) | 750 | 1.32 | 1.09 / 1.20 / 1.74 | 1.44 (−6.1) | 1.18 / 1.30 / 1.75 | −6.8 |
| 3.125, 0, +0.375 | 595 | 1.55 | 1.54 / 1.75 / 2.29 | 2.05 (−10.8) | 1.74 / 1.94 / 2.36 | −13.4 |
| 3.250, −0.250, +0.250 | 674 | 1.58 | 1.11 / 1.30 / 2.34 | 1.69 (−8.0) | 1.22 / 1.43 / 2.23 | |
| 3.250, −0.125, +0.375 | 641 | 1.36 | 1.22 / 1.41 / 2.06 | 1.75 (−8.5) | 1.38 / 1.58 / 2.15 | |
| **3.250, 0, +0.500 \*** | 606 | 1.35 | 1.51 / 1.63 / 1.89 | 1.90 (−9.6) | 1.71 / 1.84 / 2.08 | −11.6 |
| 3.375, −0.250, +0.375 | 692 | 1.27 | 1.10 / 1.21 / 1.88 | 1.55 (−6.9) | 1.21 / 1.35 / 1.96 | |
| 3.375, −0.125, +0.500 | 648 | 1.20 | 1.20 / 1.31 / 1.68 | 1.60 (−7.3) | 1.36 / 1.48 / 1.87 | |
| 3.500, −0.375, +0.375 | 738 | 1.22 | 1.05 / 1.11 / 1.76 | 1.42 (−6.0) | 1.12 / 1.21 / 1.82 | |
| 3.875, −0.500, +0.750 | 638 | 1.39 | 1.18 / 1.37 / 2.40 | 1.82 (−9.0) | 1.33 / 1.55 / 2.40 | |
| 3.875, −0.375, +0.875 | 599 | 1.44 | 1.51 / 1.70 / 2.27 | 1.99 (−10.4) | 1.69 / 1.87 / 2.32 | |
| 4.000, −0.625, +0.750 | 688 | 1.30 | 1.08 / 1.19 / 2.19 | 1.63 (−7.6) | 1.19 / 1.33 / 2.20 | |
| 4.000, −0.500, +0.875 | 645 | 1.28 | 1.22 / 1.36 / 2.04 | 1.71 (−8.2) | 1.36 / 1.52 / 2.12 | |

**The least-failing points** are the hottest ones (KT c_s ≈ 690–750 km/s), which hold the least cold mass:
- canonical 2.750 / 0 / −0.125: OUTER all Z −5.4; terciles −2.4 / −3.0 / −3.7;
- alt 3.500 / −0.375 / +0.375 and alt 2.875 / 0 / 0: OUTER all −6.0 and −6.1.

Even these predict OUTER ≥ 1.42 against a measured 0.66–0.72. Making the component hotter lowers MID T3 below what X26
requires, which is why the sheet ends there.

## Reported only: the predicted cold-mass profile (KT-tercile medians, h 0.672)

| quantity | range over the sheet (both footings) |
|---|---|
| cold-core radius r_c,cold (ρ_c = ρ_c(0)/2) | 0.29–0.63 Mpc, vs gas core 0.15 R500 = 0.12–0.15 Mpc (about 2–5 ×) |
| retained cold mass inside 0.15 Mpc | 0.03–0.23 % (T2 medians) |
| retained cold mass inside 0.5 Mpc | 0.7–4.5 % |
| retained fraction of the fair share | T1 0.31–0.78; T3 0.56–1.00 |
| M_c / M_b inside R500 | T1 0.12–1.75; T3 0.67–3.79 |

The isothermal fluid at c_s ≈ 1.1–1.5 σ_KT is nearly flat inside about 0.3–0.6 Mpc. Most of its mass sits between 1 Mpc and
r_ta: a "core" in the shear sense means an outskirts-heavy component, not a centrally concentrated one.

## Step 0 and checks (8/8 PASS; MUTATE exit 1 as required)

| check | result |
|---|---|
| K0a X26 A2 direct KT-tercile A_pred and b_pred, 35 points × 2 h cells | 8.9e-16 |
| K0b X21 KT MID terciles A, s and slope b, s_b | 0 |
| K0c X7 MGAS500 tercile MID/OUTER A_CAL + s_STAT, X7 all OUTER; X2 C\* INNER A / s_jk / s_tot; C\* vector vs X2 `stack_model` | 4.4e-16 / 0 |
| K0d X23 A1 KT-tercile A_pred at c_s,need × 3, × 4 | 0 |
| K1 band partition | 2.1e-16 |
| K2 hydrostatic solver (point-mass closed form; uniform limit) | 5.9e-6; 8.5e-10 |
| K3 zero-cold limit equals C\* | exact |
| K4 peak RSS | 0.56 GB |

- **MUTATE** (`X30_MUTATE=1`: m1 swaps the INNER and OUTER bins on the measurement side; m2 flips the hydrostatic sign):
  K0a **FAILS** (3.38), K0c **FAILS** (1.66), and K0d and K2 fail as well. The verdict is UNDECIDED (step 0), exit 1.

## What this does not show

- **The model is the record's** (X23/X26): an isothermal hydrostatic fluid in the baryon C\* field; an outer boundary at r_ta
  with the min(cosmic mean, fair share) normalisation; the cold self-gravity omitted from the profile shape, though it sources
  the lensing. It is spherical, and c_s is the z = 0 value, as in X26.
- **The exclusion is of this partial-retention profile at the sheet's c_s.** A component with the same MID amount but a
  truncated or centrally concentrated profile is not tested.
  - The record has no derived alternative profile.
  - R6's requirement that the heat be kinetic (collisionless dispersion, possibly anisotropic) is not modelled. A
    collisionless 600 km/s medium need not take the isothermal fluid's shape.
- **The OUTER errors for the KT sample are σ_STAT (X21's convention).** The 326-cluster MGAS500 grades use X7's full CAL
  errors and fail at every r = 0 point (Z −5.8 to −13.4), so the class does not hinge on the error model.
- **INNER carries no weight.** σ_IN is about 1.4–1.7 (cross-shear offset ≈ −1.2), as X13 found.
- **Only X26's grid points are tested.** The true sheet is thicker than the grid step (X26). But every point fails OUTER by
  ≥ 5σ, and the least-failing points sit at the hot edge, where MID T3 closes.

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X30_sheet_cluster_profile/x30_sheet_cluster_profile.py                # exit 0, ~80 s, 0.56 GB
PYTHONHASHSEED=0 X30_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X30_sheet_cluster_profile/x30_sheet_cluster_profile.py   # exit 1 by design
```

Read-only inputs:
- X2's source (functions exec'd);
- X7's per-cluster npz and JSON;
- the eRASS1 FITS;
- the X2, X21, X22, X23 and X26 JSONs;
- X26's pass-mask npz.
