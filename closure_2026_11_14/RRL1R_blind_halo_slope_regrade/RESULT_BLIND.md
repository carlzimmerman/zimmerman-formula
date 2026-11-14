# RRL1R RESULT (BLIND): the stellar halo's density slope from PS1 RR Lyrae, and RAW1's test redone with it

2026-11-14. TEST lane, blind re-grade of RRL1. Adopts nothing, relabels nothing (RAW1, MWT1, MWT2 keep their labels).
Criteria: `FROZEN_CRITERIA.md` (adopts RRL1's sections 0 to 8 as handed to this lane; commit 36f607a3c4, committed
alone with `WHAT_I_SAW_AT_START.md` before any script or RR Lyrae number). Scripts and outputs: commit e59cab4a63.
Graded run: `rrl1r.py` -> `rrl1r.out`, `rrl1r_results.json`, `rrl1r_MUTATE.out`, mock checkpoints `mocks_*.jsonl`.
Written without having opened any RRL1 output; nothing here is compared with RRL1.

## 1. Frozen reading

### Labels (four framework cases, per footing; H and N reported)

| case | footing | label (frozen) | fragility (bracket -> head word) |
|---|---|---|---|
| framework line, census baryons | canonical | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** (20-30 still HOT) | **FRAGILE**: score > 0.9 -> NO POWER; distances x1.05 -> NO POWER; Sgr band none -> FAIL SURVIVES [20-30 COLD]; other model (single) -> FAIL SURVIVES [30-40 HOT] |
| framework line, census baryons | alt | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** | **FRAGILE**: other model (single) -> FAIL REMOVED BY THE MEASURED SLOPE |
| framework line, rotation-curve stellar mass | canonical | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** | **FRAGILE**: other model (single) -> FAIL REMOVED BY THE MEASURED SLOPE |
| framework line, rotation-curve stellar mass | alt | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** | robust: every bracket gives the same head word (bin lists vary) |
| H (DESI NFW), reported | - | MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD] | fragile: other model -> FAIL REMOVED |
| N (Newton, baryons), reported | - | FAIL SURVIVES THE MEASURED SLOPE [all four bins HOT] | robust |

In words: with the measured RR Lyrae profile, RAW1's hot 30-40 kpc bin passes for every framework case (and H), but
the 40-55 kpc bin, which RAW1 graded PASS, now reads COLD for every smooth model, the framework on both footings and
DESI's NFW alike. The census-canonical case also keeps RAW1's 20-30 HOT. No fraction of profile draws reads HOT at
30-40 between 0.16 and 0.84 in the nominal run (rule 1 does not fire). None of this is a pass of the theory.

### The slope measurement (PS1, nominal: S3ab > 0.8, |b| > 20, Sgr band 15, q = 1, 20 <= r < 80 kpc)

- Footprint 5,143 of 16,200 cells (covered 12,071; |b| > 20: 8,180; reddening: 7,836; Sgr band: 5,184; Magellanic
  masks: no change; clump cells: 5,143). Clump rule: 3,077 clump stars, 435 covered cells masked; largest groups at
  (RA, Dec, DM) (282.34, -27.48, 17.13; 1,696 stars, Sgr core / M54), (257.55, -22.92, 14.76; 642), (260.09, 57.91,
  19.36; 189, Draco), (153.28, -1.65, 19.56; 94), (205.54, 28.37, 15.10; 61), (227.19, 67.26, 19.15; 50, Ursa Minor),
  and a chain of small groups at DM about 18.4 to 18.7 near RA 206-243, Dec -13 to +7 (full list in `rrl1r.out`).
- N = 5,421 RRab in range.
- Single law: a = 4.769 +/- 0.039 (Hessian; profile interval 4.730 to 4.808).
- Broken law: a_in = 5.291 +/- 0.076, a_out = 3.934 +/- 0.115, rb = 39.03 +/- 1.14 kpc (Hessian, positive definite).
  The break is INVERTED relative to the usual halo picture: steeper inside, shallower outside.
- 2 Delta ln L = 77.78; T = 7.977 (99th percentile of 100 null mocks from a = 4.769; mock median 2.19, max 9.71).
  **Break detected.** The Jeans step uses the broken law.
- Normalisation check K0n: binned Z equals the full node sum to |Delta ln Z| 1.6e-7.

### Per-bin f and sigma_f, nominal profile (broken 5.291 / 3.934 / 39.03)

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in 200 draws |
|---|---|---|---|---|---|
| FW census canonical | 1.058 +/- 0.027 HOT | 1.052 +/- 0.048 PASS | 0.857 +/- 0.044 COLD | 0.887 +/- 0.111 PASS | 0.000 |
| FW census alt | 1.016 +/- 0.026 PASS | 1.008 +/- 0.046 PASS | 0.820 +/- 0.042 COLD | 0.849 +/- 0.106 PASS | 0.000 |
| FW rc canonical | 0.993 +/- 0.025 PASS | 0.991 +/- 0.045 PASS | 0.809 +/- 0.041 COLD | 0.839 +/- 0.105 PASS | 0.000 |
| FW rc alt | 0.978 +/- 0.025 PASS | 0.973 +/- 0.044 PASS | 0.792 +/- 0.041 COLD | 0.820 +/- 0.103 PASS | 0.000 |
| H | 1.032 +/- 0.026 PASS | 1.002 +/- 0.045 PASS | 0.821 +/- 0.041 COLD | 0.868 +/- 0.101 PASS | 0.000 |
| N | 2.026 +/- 0.051 HOT | 2.410 +/- 0.108 HOT | 2.272 +/- 0.111 HOT | 2.699 +/- 0.277 HOT | 1.000 |

Error parts (s_stat, s_slope, s_beta) for FW census canonical: 20-30 (0.025, 0.007, 0.005); 30-40 (0.046, 0.012,
0.006); 40-55 (0.039, 0.018, 0.005); 55-80 (0.058, 0.019, 0.093). The other cases are alike (`rrl1r.out`). The slope
term is small because the PS1 profile is tight; s_stat dominates.

RAW1's words used as the reference (read from `raw1_results.json`): census canonical HOT, HOT, PASS, PASS; census alt,
rc canonical, rc alt and H PASS, HOT, PASS, PASS; N HOT in all four.

### BHB-versus-RR Lyrae slope check (section 5; reported, does not gate)

PS1 single fit on the 1,033 kept cells (of 1,073) that hold RAW1's 1,495 stars, 20-45 kpc, N = 996:
a = 5.138 +/- 0.146 against RAW1's 5.289 +/- 0.169; difference -0.151, limit 0.446: **CONSISTENT**. As frozen, this
is necessary, not sufficient (different likelihoods), and it only covers the radii where the inner slope rules.

### DES cross-check (reported, not graded)

DES footprint 1,253 cells, N = 1,045 (20-100 kpc, ACc and Sys removed; 2,402 Sys stars and 11 ACc dropped; clump
rule: 8 stars, one group at DM 22.1). Single a = 4.900 +/- 0.082. Broken: a_in 5.043 +/- 0.094, a_out 1.17 +/- 1.62,
rb 76.8 +/- 4.8 kpc; 2 Delta ln L 11.38 against T_DES 8.64: break "detected", but it sits near the top of the range
with an unconstrained outer slope. The Jeans integral with a_out about 1 then barely converges, and f collapses
(FW census canonical 0.914 +/- 0.354, 0.753 +/- 0.416, 0.441 +/- 0.340, 0.278 +/- 0.397; others in `rrl1r.out`).
The DES cross-check is uninformative about the 40-80 kpc slope. Its single slope 4.90 +/- 0.08 is 1.4 sigma from PS1's
single 4.77; neither DES law reproduces PS1's break at 39 kpc. DES words (not graded): census canonical, census alt,
rc canonical, H: FAIL REMOVED; rc alt: MAKES A PASSING BIN FAIL [55-80 COLD]; N: FAIL SURVIVES.

### Known answers, twins, mutations

- K3a (my Jeans, analytic flat-curve answers, single and broken): max relative difference 3.6e-6 / 3.1e-6. PASS.
- K4 (SI): g(30 kpc) = 3.6111e-11 m/s^2 (FW census canonical), M = g r^2 / G = 2.3311e11 Msun, same as
  `raw1_model.M_of_g` to 1e-9; V = 182.8 km/s. PASS.
- K3 (RAW1's six cases with my Jeans at alpha 5.2886 +/- 0.1691): every f and sigma_f within 2.5e-5 (FW cases within
  7.2e-6) of `raw1_results.json`. PASS.
- K0n (normalisation compression): PASS (1.6e-7).
- K1 (single 4.5 mock): a = 4.483 +/- 0.038; 2 Delta ln L 2.94 < T. PASS.
- K2 (3.0 / 5.0 / 35 mock): 2 Delta ln L 200.2 > T; a_in 2.950 +/- 0.116, a_out 4.978 +/- 0.098, rb 35.11 +/- 0.98.
  PASS.
- T1: 1 of 50 further null mocks exceeds T (allowed 3). PASS.
- **T2 FAILED**: with DM shuffled among the 13,299 stars of the kept cells (sky positions kept), N 5,439, broken
  5.012 / 3.951 / 46.4, 2 Delta ln L 31.34 > T. As the specification wrote before any number, at 20-80 kpc r is
  close to d, so a break that lives in the distance distribution survives the shuffle; the failure says the break is
  a property of the DM distribution as a whole, not of particular sky directions. It is not by itself evidence that
  the break is spurious, and not evidence that it is real.
- **M1 FAILED as frozen** (`rrl1r_MUTATE.out`): keeping 60 per cent of the stars beyond 40 kpc (N 4,915) gives a
  detected break (2 Delta ln L 32.9 > T) and a steeper outer slope (4.079 against 3.934), but rb = 48.8 kpc, outside
  my frozen "near 40" window [32.5, 47.5]. The injected step at 40 kpc lands on a profile that already breaks at 39
  with a shallow outer slope, and the broken law moves its break outward to absorb the step. The mutation partly
  bites (2 of 3 conditions); the rb condition, which I set, does not.
- M2 (n = r^-3.5 in the Jeans step): f falls in every bin of all six cases (e.g. FW census canonical 1.058 -> 0.819,
  1.052 -> 0.900, 0.857 -> 0.784, 0.887 -> 0.812). PASS.
- Byte identity: a second run from scratch into a copy folder gives byte-identical `rrl1r_results.json`,
  `rrl1r_MUTATE.out` and all three mock files; `rrl1r.out` differs only in its last-but-one line, which names the
  output folder (`rrl1r_identity.out`).

### Brackets (section 7), all labels and per-bin f

Head-word changes are listed in the label table above. Notable brackets:
- completeness steeper (x0 20.07) and score > 0.6 make the outer slope shallower (3.36), push 40-55 to about 0.70-0.76
  and add 55-80 COLD for most cases; same head word.
- Sgr band none (N 10,118) changes the profile shape entirely: 4.11 inside, 4.75 outside, rb 47.6 (2 Delta ln L 22.5).
  Then 20-30 reads COLD for every smooth model and 40-55 passes for census cases.
- q = 0.7: the broken fit runs to the rb bound (75 kpc) with a_out 0.56 +/- 0.36 (Hessian fell back to the grid
  profile for rb). The Jeans integral with that outer slope gives f = 0.08 to 0.45 for every framework case. Same head
  word as nominal, but the numbers are an artefact of a degenerate outer slope (the same failure RAW1 recorded for
  its two-slope variant). The q = 0.7 single law is 4.632 +/- 0.037.
- other model (single 4.769): census canonical FAIL SURVIVES [30-40 HOT, f 1.125 +/- 0.050]; census alt and rc
  canonical FAIL REMOVED; rc alt MAKES A PASSING BIN FAIL [20-30 COLD, 40-55 COLD].

Full per-bin tables for every bracket follow (generated from `rrl1r_results.json`).

**completeness none: N 5421; single 4.792 +/- 0.039; broken 5.282 / 4.033 / 38.83 kpc; 2 Delta ln L 66.92; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.060 +/- 0.027 HOT | 1.063 +/- 0.048 PASS | 0.873 +/- 0.044 COLD | 0.904 +/- 0.110 PASS | 0.005 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 1.018 +/- 0.026 PASS | 1.018 +/- 0.046 PASS | 0.835 +/- 0.042 COLD | 0.864 +/- 0.106 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 0.995 +/- 0.025 PASS | 1.001 +/- 0.045 PASS | 0.824 +/- 0.042 COLD | 0.854 +/- 0.104 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.980 +/- 0.025 PASS | 0.983 +/- 0.045 PASS | 0.807 +/- 0.041 COLD | 0.835 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| H | 1.034 +/- 0.026 PASS | 1.011 +/- 0.046 PASS | 0.834 +/- 0.042 COLD | 0.882 +/- 0.101 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 2.027 +/- 0.051 HOT | 2.426 +/- 0.108 HOT | 2.303 +/- 0.112 HOT | 2.735 +/- 0.276 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**completeness steeper x0 20.07: N 5421; single 4.658 +/- 0.040; broken 5.300 / 3.359 / 40.85 kpc; 2 Delta ln L 142.40; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.042 +/- 0.027 PASS | 0.995 +/- 0.046 PASS | 0.759 +/- 0.043 COLD | 0.785 +/- 0.119 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 1.001 +/- 0.026 PASS | 0.953 +/- 0.044 PASS | 0.727 +/- 0.041 COLD | 0.751 +/- 0.114 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| FW_rc/canonical | 0.978 +/- 0.025 PASS | 0.938 +/- 0.044 PASS | 0.717 +/- 0.041 COLD | 0.742 +/- 0.113 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| FW_rc/alt | 0.964 +/- 0.025 PASS | 0.920 +/- 0.043 PASS | 0.702 +/- 0.040 COLD | 0.726 +/- 0.110 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| H | 1.018 +/- 0.026 PASS | 0.953 +/- 0.044 PASS | 0.735 +/- 0.040 COLD | 0.779 +/- 0.106 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| N | 2.015 +/- 0.051 HOT | 2.339 +/- 0.105 HOT | 2.084 +/- 0.107 HOT | 2.475 +/- 0.285 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**score > 0.6: N 5995; single 4.520 +/- 0.036; broken 5.251 / 3.356 / 39.92 kpc; 2 Delta ln L 175.24; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.031 +/- 0.026 PASS | 0.977 +/- 0.045 PASS | 0.758 +/- 0.042 COLD | 0.785 +/- 0.119 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 0.990 +/- 0.025 PASS | 0.936 +/- 0.044 PASS | 0.726 +/- 0.040 COLD | 0.750 +/- 0.114 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| FW_rc/canonical | 0.968 +/- 0.025 PASS | 0.921 +/- 0.043 PASS | 0.716 +/- 0.039 COLD | 0.742 +/- 0.112 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| FW_rc/alt | 0.953 +/- 0.024 PASS | 0.903 +/- 0.042 COLD | 0.701 +/- 0.038 COLD | 0.725 +/- 0.110 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| H | 1.007 +/- 0.026 PASS | 0.935 +/- 0.043 PASS | 0.734 +/- 0.039 COLD | 0.779 +/- 0.106 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| N | 1.999 +/- 0.050 HOT | 2.301 +/- 0.104 HOT | 2.082 +/- 0.105 HOT | 2.474 +/- 0.283 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**score > 0.9: N 4920; single 4.887 +/- 0.042; broken 5.302 / 4.199 / 38.90 kpc; 2 Delta ln L 45.10; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.068 +/- 0.027 HOT | 1.086 +/- 0.049 PASS | 0.899 +/- 0.046 COLD | 0.931 +/- 0.109 PASS | 0.195 | NO POWER  |
| FW_census/alt | 1.026 +/- 0.026 PASS | 1.041 +/- 0.047 PASS | 0.860 +/- 0.044 COLD | 0.890 +/- 0.105 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 1.003 +/- 0.026 PASS | 1.023 +/- 0.046 PASS | 0.848 +/- 0.043 COLD | 0.879 +/- 0.103 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.988 +/- 0.025 PASS | 1.004 +/- 0.046 PASS | 0.831 +/- 0.042 COLD | 0.860 +/- 0.101 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| H | 1.042 +/- 0.027 PASS | 1.032 +/- 0.047 PASS | 0.858 +/- 0.043 COLD | 0.906 +/- 0.100 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 2.037 +/- 0.051 HOT | 2.464 +/- 0.110 HOT | 2.354 +/- 0.115 HOT | 2.796 +/- 0.275 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**|b| > 30: N 3706; single 4.669 +/- 0.047; broken 5.334 / 3.617 / 39.33 kpc; 2 Delta ln L 86.85; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.051 +/- 0.027 PASS | 1.013 +/- 0.048 PASS | 0.805 +/- 0.045 COLD | 0.833 +/- 0.116 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 1.010 +/- 0.026 PASS | 0.971 +/- 0.046 PASS | 0.770 +/- 0.043 COLD | 0.796 +/- 0.111 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 0.987 +/- 0.025 PASS | 0.955 +/- 0.045 PASS | 0.760 +/- 0.042 COLD | 0.787 +/- 0.109 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.972 +/- 0.025 PASS | 0.937 +/- 0.044 PASS | 0.744 +/- 0.041 COLD | 0.770 +/- 0.107 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| H | 1.026 +/- 0.027 PASS | 0.967 +/- 0.045 PASS | 0.774 +/- 0.042 COLD | 0.820 +/- 0.104 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 2.023 +/- 0.051 HOT | 2.353 +/- 0.107 HOT | 2.170 +/- 0.111 HOT | 2.578 +/- 0.282 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**Sgr band none: N 10118; single 4.251 +/- 0.027; broken 4.111 / 4.750 / 47.60 kpc; 2 Delta ln L 22.51; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 0.935 +/- 0.023 COLD | 1.055 +/- 0.047 PASS | 0.966 +/- 0.047 PASS | 1.014 +/- 0.106 PASS | 0.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 COLD |
| FW_census/alt | 0.898 +/- 0.022 COLD | 1.011 +/- 0.045 PASS | 0.925 +/- 0.045 PASS | 0.970 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD |
| FW_rc/canonical | 0.878 +/- 0.022 COLD | 0.994 +/- 0.044 PASS | 0.912 +/- 0.044 COLD | 0.958 +/- 0.101 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD |
| FW_rc/alt | 0.865 +/- 0.022 COLD | 0.975 +/- 0.043 PASS | 0.893 +/- 0.043 COLD | 0.937 +/- 0.098 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD |
| H | 0.907 +/- 0.023 COLD | 1.001 +/- 0.044 PASS | 0.918 +/- 0.044 PASS | 0.981 +/- 0.099 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD |
| N | 1.811 +/- 0.045 HOT | 2.380 +/- 0.105 HOT | 2.486 +/- 0.118 HOT | 2.988 +/- 0.275 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**Sgr band 10: N 6557; single 4.596 +/- 0.035; broken 5.069 / 3.964 / 37.85 kpc; 2 Delta ln L 67.11; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.029 +/- 0.026 PASS | 1.033 +/- 0.047 PASS | 0.862 +/- 0.043 COLD | 0.892 +/- 0.110 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 0.988 +/- 0.025 PASS | 0.991 +/- 0.045 PASS | 0.825 +/- 0.041 COLD | 0.854 +/- 0.106 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 0.966 +/- 0.024 PASS | 0.974 +/- 0.044 PASS | 0.814 +/- 0.040 COLD | 0.843 +/- 0.104 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.951 +/- 0.024 COLD | 0.956 +/- 0.043 PASS | 0.797 +/- 0.040 COLD | 0.825 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD |
| H | 1.002 +/- 0.026 PASS | 0.984 +/- 0.044 PASS | 0.825 +/- 0.041 COLD | 0.872 +/- 0.101 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 1.978 +/- 0.050 HOT | 2.370 +/- 0.105 HOT | 2.282 +/- 0.110 HOT | 2.710 +/- 0.275 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**Sgr band 20: N 4539; single 4.872 +/- 0.043; broken 5.323 / 4.017 / 40.27 kpc; 2 Delta ln L 55.86; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.069 +/- 0.027 HOT | 1.079 +/- 0.049 PASS | 0.870 +/- 0.046 COLD | 0.901 +/- 0.111 PASS | 0.080 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 1.027 +/- 0.026 PASS | 1.034 +/- 0.047 PASS | 0.833 +/- 0.044 COLD | 0.862 +/- 0.107 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 1.003 +/- 0.026 PASS | 1.016 +/- 0.046 PASS | 0.821 +/- 0.043 COLD | 0.851 +/- 0.105 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.988 +/- 0.025 PASS | 0.997 +/- 0.046 PASS | 0.804 +/- 0.042 COLD | 0.833 +/- 0.103 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| H | 1.043 +/- 0.027 PASS | 1.027 +/- 0.047 PASS | 0.832 +/- 0.043 COLD | 0.880 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 2.040 +/- 0.051 HOT | 2.460 +/- 0.110 HOT | 2.298 +/- 0.115 HOT | 2.729 +/- 0.278 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**distances x0.95: N 5056; single 4.747 +/- 0.040; broken 5.468 / 3.845 / 36.91 kpc; 2 Delta ln L 109.28; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.065 +/- 0.027 HOT | 1.021 +/- 0.047 PASS | 0.843 +/- 0.043 COLD | 0.872 +/- 0.112 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_census/alt | 1.023 +/- 0.026 PASS | 0.979 +/- 0.045 PASS | 0.807 +/- 0.041 COLD | 0.834 +/- 0.107 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 1.000 +/- 0.025 PASS | 0.962 +/- 0.044 PASS | 0.796 +/- 0.040 COLD | 0.824 +/- 0.105 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.985 +/- 0.025 PASS | 0.944 +/- 0.043 PASS | 0.779 +/- 0.040 COLD | 0.806 +/- 0.103 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| H | 1.040 +/- 0.027 PASS | 0.973 +/- 0.044 PASS | 0.808 +/- 0.040 COLD | 0.855 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 2.043 +/- 0.051 HOT | 2.352 +/- 0.105 HOT | 2.244 +/- 0.109 HOT | 2.665 +/- 0.277 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**distances x1.05: N 5709; single 4.764 +/- 0.038; broken 5.050 / 4.152 / 41.68 kpc; 2 Delta ln L 32.07; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.042 +/- 0.026 PASS | 1.087 +/- 0.049 PASS | 0.892 +/- 0.046 COLD | 0.923 +/- 0.110 PASS | 0.180 | NO POWER  |
| FW_census/alt | 1.001 +/- 0.025 PASS | 1.042 +/- 0.047 PASS | 0.854 +/- 0.044 COLD | 0.883 +/- 0.105 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/canonical | 0.979 +/- 0.025 PASS | 1.024 +/- 0.046 PASS | 0.842 +/- 0.043 COLD | 0.872 +/- 0.104 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| FW_rc/alt | 0.964 +/- 0.024 PASS | 1.005 +/- 0.045 PASS | 0.825 +/- 0.042 COLD | 0.853 +/- 0.102 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| H | 1.016 +/- 0.026 PASS | 1.034 +/- 0.046 PASS | 0.852 +/- 0.043 COLD | 0.900 +/- 0.101 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD |
| N | 1.993 +/- 0.050 HOT | 2.470 +/- 0.110 HOT | 2.342 +/- 0.115 HOT | 2.779 +/- 0.276 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |

**q = 0.7: N 5421; single 4.632 +/- 0.037; broken 4.837 / 0.563 / 75.00 kpc; 2 Delta ln L 107.18; model used broken**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 0.447 +/- 0.236 COLD | 0.266 +/- 0.202 COLD | 0.137 +/- 0.124 COLD | 0.084 +/- 0.204 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| FW_census/alt | 0.427 +/- 0.226 COLD | 0.254 +/- 0.193 COLD | 0.131 +/- 0.118 COLD | 0.080 +/- 0.193 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD 55-80 COLD |
| FW_rc/canonical | 0.423 +/- 0.222 COLD | 0.252 +/- 0.191 COLD | 0.130 +/- 0.117 COLD | 0.079 +/- 0.191 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD 55-80 COLD |
| FW_rc/alt | 0.413 +/- 0.218 COLD | 0.246 +/- 0.187 COLD | 0.127 +/- 0.114 COLD | 0.077 +/- 0.186 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD 55-80 COLD |
| H | 0.803 +/- 0.153 PASS | 0.615 +/- 0.197 PASS | 0.353 +/- 0.150 COLD | 0.226 +/- 0.245 COLD | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 40-55 COLD 55-80 COLD |
| N | 1.891 +/- 0.091 HOT | 2.141 +/- 0.288 HOT | 1.597 +/- 0.373 PASS | 1.174 +/- 0.756 PASS | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT |

**other model: N 5421; single 4.769 +/- 0.039; broken 5.291 / 3.934 / 39.03 kpc; 2 Delta ln L 77.78; model used single**

| case | 20-30 | 30-40 | 40-55 | 55-80 | HOT at 30-40 in draws | label |
|---|---|---|---|---|---|---|
| FW_census/canonical | 1.023 +/- 0.026 PASS | 1.125 +/- 0.050 HOT | 0.982 +/- 0.046 PASS | 1.017 +/- 0.105 PASS | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 30-40 HOT |
| FW_census/alt | 0.982 +/- 0.025 PASS | 1.078 +/- 0.048 PASS | 0.940 +/- 0.044 PASS | 0.973 +/- 0.101 PASS | 0.000 | FAIL REMOVED BY THE MEASURED SLOPE  |
| FW_rc/canonical | 0.960 +/- 0.024 PASS | 1.060 +/- 0.047 PASS | 0.926 +/- 0.043 PASS | 0.961 +/- 0.099 PASS | 0.000 | FAIL REMOVED BY THE MEASURED SLOPE  |
| FW_rc/alt | 0.946 +/- 0.024 COLD | 1.040 +/- 0.046 PASS | 0.908 +/- 0.042 COLD | 0.940 +/- 0.097 PASS | 0.000 | MEASURED SLOPE MAKES A PASSING BIN FAIL 20-30 COLD 40-55 COLD |
| H | 0.995 +/- 0.025 PASS | 1.067 +/- 0.047 PASS | 0.933 +/- 0.043 PASS | 0.984 +/- 0.098 PASS | 0.000 | FAIL REMOVED BY THE MEASURED SLOPE  |
| N | 1.952 +/- 0.048 HOT | 2.519 +/- 0.111 HOT | 2.521 +/- 0.117 HOT | 2.994 +/- 0.272 HOT | 1.000 | FAIL SURVIVES THE MEASURED SLOPE 20-30 HOT 30-40 HOT 40-55 HOT 55-80 HOT |


## 2. What is mine and what is reused

- Mine (`rrl1r.py`): the table reader and sha256 checks; the equal-area sky grid, coverage, latitude, reddening, Sgr,
  Magellanic and clustering masks with friends-of-friends clump reporting; the completeness function; the
  normalisation (per-direction ln d nodes, 4,000-bin compression verified by K0n); the unbinned likelihood; the single
  and broken fits, profile interval and Hessian errors (with a declared fallback); the mock generator, threshold T,
  K1, K2, T1, T2, M1; the profile draws; the Jeans integral for a general (single or broken) tracer profile, proved by
  K3a and K3; s_slope, the per-draw NO POWER rule, the label rules and FRAGILE.
- RAW1's, executed read-only (raw1.py parsed and only its imports, constants and function definitions executed, as
  MWT1 did; raw1_model.py imported): `load`, `build`, `measure` (sample, bins, beta 0.6586 +/- 0.0175, per-bin beta
  ranges, RAW1's alpha for K3), `fit_f` (f and s_stat), `frame_affine`, `sgr_lat_lon`, `g_model`, `M_of_g`;
  `raw1_results.json` for K3 and RAW1's reference words.
- MWT1's: only the AST-execution pattern. MWT1's `tracer`/`sr2_grid`/`predP` were not copied; my Jeans integral was
  written independently and matched RAW1's at the single slope (K3, 7e-6).

## 3. What I saw before writing

`WHAT_I_SAW_AT_START.md`: one truncated memory-index line naming RRL1 and the "hot Milky Way b..." bin, with no label,
slope, break or pass/fail. Before freezing I saw only the MANIFEST files, table headers and two (PS1) / three (DES)
data rows. I opened no RRL1 file, no CJ1 or MWT2 file, no paper, handoff or scorecard, and did not use the web.

## 4. What I could not do, and limits

- PS1 purity as a function of distance is not modelled (the specification brackets it by the score cut only). The
  score brackets move the outer slope from 3.36 (score 0.6) to 4.20 (score 0.9): contamination plausibly flattens the
  outer profile, so the reading of the 40-55 COLD rests on how pure and how complete PS1 is at 40-80 kpc.
- The completeness function uses r_F = DM + 0.6 (memory, PROVISIONAL); the steeper bracket moves a_out by -0.58.
- The q = 0.7 bracket and the DES cross-check both produce degenerate outer slopes; their f values are not
  informative about 40-80 kpc.
- M1 failed my own rb window; T2 failed as the specification anticipated.
- The NO POWER rule uses the nominal s_beta for every draw (declared in my criteria).
- The Jeans step assumes BHB and RR Lyrae share one profile; checked only inside 45 kpc (consistent).

## 5. My hand estimate against the result (written before; compared after)

I expected a single slope about 4.3 (got 4.77) and a break with a shallow INNER slope (literature-like); the data give
a break at 39 kpc with a steeper inner and a shallower outer slope. I expected FAIL REMOVED for the census cases and
MAKES A PASSING BIN FAIL [40-55 COLD] for rc alt; the result is MAKES A PASSING BIN FAIL [40-55 COLD] for all four.
NO POWER: none in the nominal run, as expected. FRAGILE: three of four, as expected, mostly through the other model.

## 6. Post hoc (2026-11-14, written after seeing the numbers; not part of any label)

- The whole frozen reading hangs on one feature: the outer slope a_out = 3.93 beyond 39 kpc. Every smooth model,
  DESI's NFW included, reads COLD at 40-55 with it, so the COLD is a statement about the tracer profile, not about the
  framework in particular (the same pattern RAW1 found for the hot 30-40 bin, inverted).
- An outer profile that gets SHALLOWER beyond about 40 kpc is the opposite of the break most halo studies report
  (DES's own fit, read from the paper per the specification: 2.54 inside, 5.42 outside 32 kpc). Two data-side causes
  would produce it: contamination by non-RR Lyrae at faint magnitudes, and a PS1 completeness that falls faster than
  the adopted logistic. The brackets point that way: score > 0.9 steepens a_out to 4.20, and a steeper completeness
  flattens it to 3.36. Neither is graded here.
- With the single law (the other-model bracket) the 40-55 bin passes for three of four cases; with the broken law it
  fails cold for all. That makes the model choice the deciding lever, and the model choice was made by a 2 Delta ln L
  of 78 that also survives the DM shuffle (T2), i.e. it lives in the overall distance distribution of the stars.
- Nothing here favours or disfavours the framework over DESI's NFW: they move together in every bracket.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
