# FRZ1R RESULT_BLIND (committed before FRZ1's RESULT or any frz1_* output was opened)

**Label (reading L, gate Delta chi^2 <= 4): canonical FOREST ROW FAILS (Delta chi^2 8142.08); alt FOREST ROW FAILS
(7685.51). Lane: FAILS.** Footings not pooled. A fail of a TEST lane on form B's frozen layout; it relabels nothing.

At the forest's redshifts form B's layout REMOVES small-scale power: R_cold at z 3, k 3 / 5 h/Mpc is 0.863 / 0.696
(canonical) and 0.847 / 0.692 (alt). My hand estimate (READING.md) had the sign wrong (+0.02 to +0.10 expected).

## R_cold(k, z), reading L (frz1r_hm_<foot>.json / .out)

| z | canonical k 1 / 3 / 5 | alt k 1 / 3 / 5 |
|---|---|---|
| 0 (validation) | 1.0059 / 1.0509 / 1.0902 | 1.0101 / 1.0877 / 1.1590 |
| 2.2 | 0.9915 / 0.8776 / 0.7728 | 0.9919 / 0.8805 / 0.7971 |
| 3.0 | 0.9931 / 0.8634 / 0.6963 | 0.9925 / 0.8473 / 0.6924 |
| 4.4 | 0.9967 / 0.9273 / 0.7561 | 0.9965 / 0.9177 / 0.7379 |

## Delta chi^2 per DESI bin (own covariance block) and total (frz1r_forest_<foot>.json / .out)

| bin | 2.2 | 2.4 | 2.6 | 2.8 | 3.0 | 3.2 | 3.4 | 3.6 | 3.8 | 4.0 | 4.2 | 4.4 | **total (full cov)** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| canonical | 295.3 | 482.6 | 575.1 | 764.6 | 1062.2 | 1126.1 | 1047.4 | 682.9 | 259.2 | 328.1 | 153.3 | 82.0 | **8142.08** |
| alt | 241.7 | 417.8 | 519.8 | 734.7 | 997.3 | 1070.4 | 1001.2 | 672.3 | 251.5 | 320.2 | 149.9 | 80.3 | **7685.51** |

Amplitude ratio fed to the gate: 0.568-0.922 (canonical), 0.584-0.929 (alt).

## Reported, never graded
- Reading V (galaxy charge inside the virial radius only): 99.23 / 23.82 (R_cold at z 3, k 3 / 5: 1.003 / 0.991 canonical,
  1.027 / 1.039 alt). Also fails the gate, by much less.
- Ambiguity 1 alternative (unplaced cold mass as a shell at r_ta): 15978.64 / 13618.41.
- Cause, as far as read: at z >= 2.2 the comoving r_M = sqrt(G M_b (1+z)^2 / a0) puts r_t near or beyond r_ta for most galaxy
  haloes; the phantom then spreads the cold dark energy out to r_ta (and, in reading L, the unplaced part in the reference
  shape) instead of NFW's concentrated inner profile, so the 1-halo power at k >= 2 drops. No clusters exist above v_stiff.

## Validation (all pass)
- z = 0 against CO1's printed R_cold at k 1 / 3 / 5: canonical 1.0059 / 1.0509 / 1.0902 vs 1.006 / 1.051 / 1.090; alt
  1.0101 / 1.0877 / 1.1590 vs 1.010 / 1.088 / 1.159 (all within 0.001; line 0.02).
- Gate: R = 1 gives 0 exactly, DESI md5 matches; CO1's stored z = 0 R_cold held at every bin gives 160.74 / 1025.57
  (HLF1's 160.74 / 1025.57); my own z = 0 R_cold held gives 160.75 / 1025.58.
- Every layout holds M_ta inside r_ta and is non-decreasing to 2.2e-16. D(3) (1+3) = 1.263 (EdS limit ~1.27).
- Mutation (bites): a0 unscaled in comoving units at z 3 moves R_cold(k 3) by +0.483 / +0.593 (line 0.005).

## What is shared with FRZ1
- Inputs: CFG556's cosmology and numerical settings (EH no-wiggle shape, sigma8 0.811, Tinker 2008 / 2010, Duffy c(M), Moster
  stars, beta-model gas, turnaround construction, the halo-model spectrum formulas): taken from CFG556's CODE (its text does
  not define them), re-implemented in `frz1r_hm.py`, nothing imported. CO1's layout from CO1's criteria text; PD1's shares and
  v_stiff; FRZ1's z-scalings from its criteria.
- The gate is SHARED MACHINERY: `frz1r_forest.py` copies HLF1's set-up of the record's `ss1_cosmo.forest_eval` (DESI DR1 P1D,
  form B's own CLASS spectrum as the reference). My independence covers R_cold(k, z), not the gate.
- My own choices that FRZ1 may have made differently: ambiguity 1 (READING.md), point-mass condensed baryons, the cluster
  isothermal remainder from r = 0, nearest-bin ZG mapping.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
