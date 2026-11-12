# NIM2 RESULT: NMB1's gate at three radii (30, 50, 80 kpc). The third radius adds amplitude, not shape power

2026-11-12. Criteria `FROZEN_CRITERIA.md`, frozen 2026-11-12T20:26:51Z (sha256 c8e668d1...df9b in
`FREEZE_STAMP.txt`), written before the script and before any 50 kpc value was read. One run; no
amendment. TEST lane. Adopts nothing. Relabels no other lane.

## Labels

Gate Q <= 8.02 on 3 dof. z = (line - data)/sigma at 30 / 50 / 80 kpc; negative = line below data.

| case | line 30 / 50 / 80 [10^11] | Q | z30 / z50 / z80 | z_slope | z_curv | label |
|---|---|---|---|---|---|---|
| E1 canonical census | 2.326 / 3.613 / 4.977 | 8.70 | -1.65 / -2.46 / -1.88 | -1.10 | +0.50 | **FAILS LOW (2 to 3 sigma), FRAGILE** |
| E1 alt census | 2.517 / 3.900 / 5.109 | 3.68 | -0.33 / -1.61 / -1.68 | -1.50 | +0.23 | **PASSES** |
| E0 canonical census | 2.331 / 3.684 / 5.691 | 7.59 | -1.61 / -2.24 / -0.85 | -0.11 | +1.07 | **PASSES, FRAGILE** |
| E0 alt census | 2.526 / 4.013 / 6.219 | 2.01 | -0.27 / -1.29 / -0.17 | -0.04 | +1.06 | **PASSES** |
| E1 canonical MB15 | 2.363 / 3.735 / 5.423 | 6.05 | -1.39 / -2.09 / -1.22 | -0.57 | +0.72 | **PASSES, FRAGILE** |
| E1 alt MB15 | 2.557 / 4.034 / 5.633 | 1.68 | -0.07 / -1.23 / -0.93 | -0.88 | +0.50 | **PASSES** |
| E0 canonical MB15 | 2.368 / 3.800 / 6.035 | 5.87 | -1.35 / -1.90 / -0.40 | +0.22 | +1.15 | **PASSES, FRAGILE** |
| E0 alt MB15 | 2.565 / 4.138 / 6.593 | 1.59 | -0.02 / -0.95 / +0.28 | +0.28 | +1.14 | **PASSES** |
| paper's NFW (comparator) | 2.485 / 4.174 / 6.205 | 1.10 | -0.54 / -0.85 / -0.19 | +0.06 | +0.53 | PASSES |

Separation labels:

| footing | E0 vs E1, census | E0 vs E1, MB15 | framework vs NFW |
|---|---|---|---|
| canonical | **SEPARATES** (formally; see below) | **DOES NOT SEPARATE** | **PARTLY SEPARATES** (E1 census only) |
| alt | **DOES NOT SEPARATE** | **DOES NOT SEPARATE** | **DOES NOT SEPARATE** |

**Read plainly: no gain in shape power.** The canonical "SEPARATES" is a threshold accident, not
a resolved difference: E1 sits at Q = 8.70 and E0 at 7.59, either side of 8.02, both FRAGILE (E1
returns inside the gate under four of six pre-named variants; E0 leaves it under two). The two
readings differ from each other by a noncentrality of only 1.18 (about 1.1 sigma). Every move
relative to NMB1 comes from the amplitude at 50 kpc, where the canonical lines sit 2.1 to 2.5
sigma low; none comes from slope or curvature.

## The 50 kpc data and the combined estimate

| curve | 50 kpc [10^11] (16th, 84th) |
|---|---|
| NIMBLE-A RRL | 5.401 (5.085, 5.734) |
| NIMBLE-A BHB | 4.391 (3.949, 4.752) |
| NIMBLE-B RRL | 4.408 (4.098, 4.753) |
| NIMBLE-B BHB | 4.256 (3.938, 4.585) |

NIMBLE-A RRL (the curve the authors distrust) is 0.09 dex above the other three at 50 kpc.

Combined (N = 24 mocks, shrinkage 0.5, k_30 = 1.000, k_50 = 1.305, k_80 = 1.392):
log10 M = 11.4095 +/- 0.0261 (30), 11.6537 +/- 0.0390 (50), 11.8032 +/- 0.0565 (80).
Correlations 30-50 +0.05, 30-80 +0.19, 50-80 +0.47. Slope 30-80 = 0.924 +/- 0.135; 30-50 = 1.10;
50-80 = 0.73; curvature c = -0.37 +/- 0.37. Internal chi-square 3.55 on 9 dof (p = 0.94). The
NIMBLE-only 50 kpc value (4.505 x 10^11) equals Table 4's joint (11.654); my disclosed hand
expectation (about 4 per cent below the joint) was wrong, which is why the canonical lines move
toward the gate.

## How much changed relative to NMB1

- **Errors:** 30 kpc 0.0270 -> 0.0261 dex; 80 kpc 0.0567 -> 0.0565; slope 30-80 0.137 -> 0.135.
  Essentially unchanged. The new 50 kpc point carries 0.039 dex.
- **Curvature has no power:** its error (0.37) is larger than the full spread of model curvatures
  (-0.28 to +0.06; NFW -0.17). Every |z_c| is <= 1.15.
- **Power to separate E0 from E1** (noncentrality lambda; power = P(Q > gate)): canonical census
  1.08 -> 1.18, power 0.13 -> 0.12; alt census 2.32 -> 2.54, power 0.24 -> 0.22; MB15 0.68 -> 0.74
  and 1.48 -> 1.60, power down likewise. **No gain** (the extra degree of freedom costs more than
  the added lambda).
- **Power to separate the framework from the NFW:** small gains for the canonical cases (E0
  canonical census 1.29 -> 2.97, power 0.15 -> 0.26; E1 canonical census 3.45 -> 4.43, 0.35 ->
  0.38), none for alt (E1 alt census 0.26 -> 0.22; E0 alt 0.05 -> 0.06). All powers stay below 0.4.
- **Q values moved by amplitude at 50 kpc:** E1 canonical 4.89 -> 8.70, E0 canonical 2.40 -> 7.59,
  E1 alt 2.91 -> 3.68, E0 alt 0.05 -> 2.01. MB15 hot gas brings the canonical cases back inside
  (6.05, 5.87), as MWG1 found at the outer radii.

## Checks

All pass before any graded number (`nim2.out`):
KA1 md5 equal. KA2 fig10 joint vs Table 4, worst 0.0049 x 10^11. KA3 Figure 8 biases to 0.01 point.
KA4 machinery on all curves per radius: 11.4193 (30, Table 4 11.423 +/- 0.022), 11.6541 (50, 8
curves, Table 4 11.654 +/- 0.0255), 11.7883 (80, 11.804 +/- 0.0345). KA5 NMB1 reproduced with the
50 kpc rows dropped: 11.4059 +/- 0.0270, 11.8047 +/- 0.0567; Q 4.89, 2.91, 2.40, 0.05. KA6 closed form
to 3e-16; synthetic mean Q 3.009, rejection 0.0473. KA7 line at 80 kpc to 0.01 per cent; M_sph
fractions 0.9781 / 0.9977 vs DW1's 0.9777 / 0.9972; f_50 = 0.9952; MB15 3.846e9 inside 50 kpc.
Mutations bite (`nim2_mut.out`): M1 A = 2 fails HIGH, Q 30.7 / 49.2; M2 point mass fails, Q 263,
z_slope -6.83 (z_curv only +0.99: curvature alone would not catch it).
Independent recomputation from `nim2_results.json` with an adaptive-quadrature line: Q 8.700,
7.586, 3.676, 2.007 for E1 can, E0 can, E1 alt, E0 alt census; curvature -0.368 +/- 0.371.

## Limits

- The three radii share stars; 50 kpc is 0.47 correlated with 80 kpc, so it adds amplitude
  information but almost no independent shape information.
- The covariance is from six LambdaCDM haloes with no LMC; the paper's per-method floor is replaced
  by the per-radius calibration k_r, now with k_50 = 1.305.
- The canonical E0/E1 split rests on Q values within 0.7 of the gate on either side and is not
  stable under the pre-named variants; it should not be read as evidence for or against the field.
- Census baryons are McMillan 2017 at A = 1; MB15 is one hot-gas model (MWG1, PROVISIONAL masses).

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `nim2.py` (takes the path of the Zenodo zip; the zip is
not stored in the repository; md5 5b0cc3aa9947286eb9348e947d01182d), `nim2.out`,
`nim2_results.json`, `nim2_mut.out`, `RESULT.md`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
