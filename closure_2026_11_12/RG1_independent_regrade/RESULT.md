# RG1 RESULT: independent regrade of NMB1, PLT1, MWJ1, MWG1, MWI1

2026-11-12. Criteria: `FROZEN_CRITERIA.md` (stamp in `FREEZE_STAMP.txt`), written before any script.
Regrade lane. Adopts nothing. Relabels nothing.

## Labels

| lane | label |
|---|---|
| NMB1 | **REPRODUCED** |
| PLT1 | **REPRODUCED** |
| MWJ1 | **REPRODUCED** |
| MWG1 | **REPRODUCED** |
| MWI1 | **REPRODUCED** (geometry block not re-implemented) |

Every target number is inside its frozen tolerance, and every graded label I computed matches the
lane's. Blindness: my numbers were saved (`rg1.out`, `rg1_results.json`) before any lane script,
output or RESULT was opened. The only shared inputs are the figure-data file, the McMillan 2017
component parameters and constants re-typed from DW1, and the angle-average formula of G239.
Integration, the covariance build, interpolation and the window search are my own code.

## Numbers (mine against the lane's)

NMB1 (N = 24 mocks, k_30 = 1.000, k_80 = 1.392 in both):
- theta_30 = 11.4059 +- 0.0270, theta_80 = 11.8047 +- 0.0567, corr +0.183; target identical.
- Q: E1 can 4.883, E1 alt 2.896, E0 can 2.402, E0 alt 0.046; targets 4.89, 2.91, 2.40, 0.05.
- KA4: 11.4193 +- 0.0259 (30 kpc), 11.7883 +- 0.0248 (80 kpc); the lane printed the same.
- KA3 biases -6.50, -7.54, +5.92, -1.18 per cent; the lane printed the same.

PLT1 (8 H rows, 10 S rows at r >= 100 kpc):
- E1 canonical: H -0.674, S -1.554 (targets -0.68, -1.56). E0 canonical: H +1.016, S +0.284
  (targets +1.01, +0.28). E1 alt -0.659 / -1.534; E0 alt +1.337 / +0.610 (lane -0.66 / -1.54,
  +1.34 / +0.61).
- S median at r >= 150 under E1 canonical: -2.715 (target -2.72); alt -2.714.

MWJ1: field range at A = 1 passing G1, G2, G2p: 0 to 0.0075 on both footings (target the same);
first failure past it at 0.008 is G2p. Amplitude ranges at e_N = 0: 0.91-1.50 / 0.79-1.31; at 0.008:
1.02-1.51 / 1.02-1.32 (same as the lane). Labels: CLOSES WITH CENSUS BARYONS, WEAKER FIELD,
ROTATION CURVE INSIDE, both footings (same).

MWG1 (MB15): field range 0 to 0.0195 canonical, 0.0005 to 0.0195 alt (lane the same); satellite
plateau median at 0.01273: -1.34 both footings (target -1.34); Q there 2.53 / 0.96 (same). Other
models: S15 0-0.0120 both; F20 0-0.0200 / 0.0010-0.0205; F17 0.0045-0.0225 / 0.0045-0.0235. Part 1
fractions match (MB15 0.153e10 inside 27 kpc). Mutation M1 bites on both footings.

MWI1: required stellar mass 7.050-7.411 (canonical), 6.356-6.730 (alt) x 10^10; z canonical +0.85,
+2.84, +4.68, +4.14, +12.24; alt +0.24, +1.62, +3.06, +0.84, +10.33. All equal to the targets.

Instrument: census 6.6814e10; M_sph/M_b 0.9777 (30 kpc), 0.9976 (80 kpc); E0(80) 5.692 / 6.220,
E1(80) 4.978 / 5.111 x 10^11; E1(2000) equals the closed form [nu(e) + e nu'(e)/3] M_b.

## Differences (all inside tolerance), with cause

1. **M_sph at large radius.** My spherical enclosed mass integrates the discs out to R = r; DW1's
   port (used by all five lanes) stops the disc integral at R = 60 kpc. At 80 kpc that is 0.9976 vs
   0.9972 of M_b (within the 0.0005 KA tolerance), and it shifts the line by about +0.04 per cent at
   80 to 300 kpc. Effect: Q 4.883 vs 4.89, medians by 0.002, and one window edge: MWG1 F17 canonical
   upper edge 0.0225 (mine) vs 0.0220 (lane). At e_N = 0.0225 my Q is 6.170; with the 60 kpc cut
   placed in a scratch copy of my script it is 6.1801, just over 6.180, and the edge returns to 0.0220
   and Q to 4.892. Confirmed as the cause. F17 is not primary; no label moves.
2. **NMB1 variants.** My lambda = 1 and lambda = 0 (Hartlap) variants keep the graded k_r (Q for E1
   canonical 8.43 and 2.73); the lane's graded variants recompute k_r with their own lambda (6.90 and
   3.59), and it prints the other choice too (8.43, 2.74), matching mine. E1 canonical stays FRAGILE
   either way (k_r = 1: mine 7.86, lane 7.88; both over 6.180).
3. **MWI1 hot gas.** The criteria fix 0.15e10; MB15 at 27 kpc is 0.1526e10. Using the latter moves
   the need by -0.003 and z by at most 0.01. No class changes.

## Ambiguities in the frozen criteria (findings)

- NMB1: whether the lambda variants recompute the error calibration k_r is not fixed (the lane
  states this itself). Whether RRL and BHB mocks are paired by (halo, view) for the cross-tracer
  covariance is implied but not stated; both implementations paired them.
- PLT1 / MWJ1 / MWG1: "the baryon model as ported in DW1" leaves the 60 kpc disc cut implicit; its
  KA tolerance (0.0005) admits both integrals, and the difference can move a knife-edge grid point
  (item 1 above).
- MWG1: M_hot = M_ref (r/r_ref)^p is applied beyond r_ref with no cap (for MB15 this touches only
  the Fritz20 row at 273 kpc, beyond 250 kpc). With a cap (constant beyond
  r_ref) MB15's window is 0 to 0.0180 on both footings and the plateau median at 0.01273 is -1.43
  instead of -1.34; the record's field still passes, so the label is unchanged.

## Not done

MWI1's geometry block (scale-length force ratios) and KA2 (in-plane force); NMB1 KA5 (synthetic
draws), the reported-not-graded items (A*, NFW through the gate, published bands); PLT1's other
FRAGILE variants (symmetric errors, 10 and 30 per cent floors, single-row drops) and its post hoc
reports. These were not targets.

## Files

- `FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`
- `rg1.py` (run: `python3 -I rg1.py <figdata_dir>`; data kept outside the repository, md5 verified)
- `rg1.out`, `rg1_results.json`

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
