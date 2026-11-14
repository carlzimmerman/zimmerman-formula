# RRL3R RESULT (blind): Milky Way halo stars with the measured RR Lyrae star-count profile and the measured anisotropy

2026-11-14. Blind TEST lane. Adopts nothing. Criteria `FROZEN_CRITERIA.md` (commit 33c0932f6c), one amendment
`AMENDMENT_A1.md` (commit 96c6f91588), written after run 1 stopped on a known answer and before any word was computed.

## Words first

**As frozen (run 1): NO VERDICT (KNOWN ANSWER) for every case on both footings.** KA-5's single planted broken mock
(seed 331103) gave an outer slope of 4.745 +/- 0.082 against the true 5.0 (3.1 sigma). Over 40 more seeds the fit is
unbiased (outer-slope pull mean +0.32, sd 0.95, 40 of 40 seeds pass). A1 judges KA-5 over those 40 seeds.

**Under A1 (run 2), primary convention (PS1 RR Lyrae profile + C), graded a0:**

| case | canonical (a0 9.3603e-11) | alt (a0 1.1312e-10) |
|---|---|---|
| framework, census stellar mass | **NO VERDICT (SLOPE)**, FRAGILE | **ROW PASSES UNDER THE MEASURED CONVENTION**, FRAGILE |
| framework, rotation-curve stellar mass | **ROW PASSES UNDER THE MEASURED CONVENTION**, FRAGILE | **NO VERDICT (SLOPE)**, FRAGILE |
| DESI NFW (H), beside them (no footing) | ROW PASSES UNDER THE MEASURED CONVENTION, FRAGILE | same |
| Newton (N), reported | ROW FAILS, HOT in all four bins | same |

The two NO VERDICT (SLOPE) words sit at the edge of the rule. Over the 200 profile draws, all four bins pass in a
fraction 0.825 (census canonical) and 0.840 (rotation-curve alt) of the draws. The NO VERDICT window is 0.16 to 0.84,
boundaries included. In the nominal row every bin of every framework case reads PASS.

Framework against DESI's NFW: the words differ on each footing only because of those two SLOPE no-verdicts. No
framework case passes where the NFW fails, and the NFW passes on both. **The gate does not separate the framework from
DESI's NFW in the framework's favour under this convention.** The two framework passes are hits that await a further
independent re-grade. They are not a pass of the theory. Every case is FRAGILE.

## The star-count profile (PS1, q = 1, 20-80 kpc, N = 5,421 RRab in 5,143 cells)

- Single: a = 4.769 +/- 0.039.
- Broken: a_in 5.291 +/- 0.076, a_out 3.934 +/- 0.115, rb 39.03 +/- 1.14 kpc. 2 Delta ln L = 77.8 against
  T = 10.63 (99th percentile of 100 null mocks; mock single slopes 4.764 +/- 0.039). The break is detected, so the
  broken law is used. Its outer slope (3.93; draws 3.68 to 4.13) is well above the 1.382 limit.
- The break is INVERTED: steeper inside, shallower outside. That is the opposite of the published DES broken law
  (2.5 inside, 5.4 outside). Its outer slope depends strongly on the RR Lyrae score cut: 4.20 at S3ab > 0.9, 3.93 at
  0.8, 3.36 at 0.6. See "Looked wrong" below.
- DES cross-check (1,045 stars, 20-100 kpc, flat completeness): single 4.900 +/- 0.082. 2 Delta ln L 11.38 is below
  T_DES 11.82, so DES detects no break.

## Anisotropy (my own fit, the stars' own proper motions)

beta = 0.6713 [20-30], 0.6854 [30-40] and 0.4412 [40-55] kpc. 55-80 is not usable: the median PM error is larger than
the line-of-sight dispersion. The beyond-55 value is held at 0.4412. These agree with RAW1's own `measure` to the 4 printed
decimals, errors included (cross-check only). My code uses the same physical model as RAW1's, so this is a check of
the code, not an independent measurement.

## Per case, footing and bin (primary): stars, f, sigma_f, word; sigma parts (s_stat, s_slope, s_beta)

Stars per bin under C: 727 / 227 / 186 / 115.

| case | 20-30 | 30-40 | 40-55 | 55-80 | all-PASS in draws |
|---|---|---|---|---|---|
| census canonical | 1.0607 +/- 0.0339 PASS | 1.0880 +/- 0.0618 PASS | 0.9721 +/- 0.0691 PASS | 0.9537 +/- 0.1184 PASS | 0.825 |
| census alt | 1.0189 +/- 0.0326 PASS | 1.0427 +/- 0.0592 PASS | 0.9305 +/- 0.0662 PASS | 0.9120 +/- 0.1133 PASS | 0.990 |
| rc canonical | 0.9958 +/- 0.0318 PASS | 1.0251 +/- 0.0582 PASS | 0.9175 +/- 0.0652 PASS | 0.9011 +/- 0.1118 PASS | 0.975 |
| rc alt | 0.9809 +/- 0.0314 PASS | 1.0058 +/- 0.0571 PASS | 0.8985 +/- 0.0639 PASS | 0.8812 +/- 0.1094 PASS | 0.840 |
| H (DESI NFW) | 1.0347 +/- 0.0332 PASS | 1.0337 +/- 0.0584 PASS | 0.9265 +/- 0.0651 PASS | 0.9261 +/- 0.1087 PASS | 0.990 |
| N | 2.016 HOT | 2.460 HOT | 2.535 HOT | 2.840 HOT | 0.000 |

Parts for census canonical: (0.0318, 0.0065, 0.0100), (0.0562, 0.0115, 0.0228), (0.0612, 0.0184, 0.0262),
(0.0713, 0.0183, 0.0928). The other cases are within 10 per cent of these (`rrl3r.out`).

What makes each SLOPE word:
- Census canonical: 20-30 is close to the HOT line (f 1.061; the line is at 1.067 without s_slope), so some draws
  cross it.
- rc alt: 40-55 is close to the COLD line (f 0.899; the line is at 0.877).

## Known answers (all pass in run 2)

- KA-1: RAW1 reproduced with my Jeans and estimator. All six cases are within 3.3e-5; counts 865 / 264 / 241 / 125.
- KA-2: counts 727 / 227 / 186 / 115 exact. f = 1.0902, 1.2248, 1.1645, 1.1432 against 1.0901, 1.2248, 1.1645,
  1.1432.
- KA-3: 0.6713 / 0.6854 / 0.4412 against 0.671 / 0.685 / 0.441; 55-80 not usable.
- KA-4: the closed forms are matched to 4e-9 (single laws), 1.5e-9 (broken law) and 3.7e-9 (piecewise beta). Against
  RAW1's trapezoid the difference is 2e-5 (not gated).
- KA-5:
  - The single 4.5 mock gives 4.575 +/- 0.038 (pull 1.97, inside 2 sigma) with no break (1.09 against T).
  - The planted break is detected (135.3).
  - As frozen, seed 331103 fails on a_out (above).
  - Under A1, over 40 seeds: pull means +0.15, +0.32 and +0.23 for a_in, a_out and rb; pull sd 0.88, 0.95 and
    0.86; 40 of 40 seeds pass.
  - K0n: 1.2e-7.
- KA-6: at 30 kpc, M = 2.33114e11 Msun = raw1_model to 1e-9; V = 182.83 km/s.

## Twins and mutations (gate; FW census, primary convention, 20 seeds)

| footing | TW1 all four PASS (need >= 12) | MU1 40-55 COLD (need >= 15) | MU2 30-40 HOT (need >= 15) | gate |
|---|---|---|---|---|
| canonical | 20 of 20 | 18 of 20 | 20 of 20 | holds |
| alt | 20 of 20 | 18 of 20 | 20 of 20 | holds |

The recovered mean f is 0.791 for MU1's planted 0.80 and 1.269 for MU2's planted 1.25. The gate could have failed
these rows, and did not. TW1 never gave a non-PASS bin in 80 bin readings. That suggests sigma_f is a little
generous, since it holds s_slope and s_beta on top of s_stat.

## Brackets (word of rules 3 to 5)

| bracket | census can | census alt | rc can | rc alt | H |
|---|---|---|---|---|---|
| primary | SLOPE | PASSES | PASSES | SLOPE | PASSES |
| Ba no S2 mask | PASSES | PASSES | SLOPE | SLOPE (40-55 COLD) | SLOPE |
| Bb single law 4.769 | FAILS (30-40 HOT, f 1.151) | PASSES | PASSES | SLOPE | PASSES |
| Bc constant beta 0.6586 | SLOPE | FAILS (40-55 COLD) | FAILS (40-55 COLD) | FAILS (40-55 COLD) | FAILS (40-55 COLD) |
| Bd score > 0.9 (a_out 4.20) | SLOPE (20-30 HOT) | PASSES | PASSES | PASSES | PASSES |
| Bd score > 0.6 (a_out 3.36) | SLOPE | FAILS (40-55 COLD) | FAILS (40-55 COLD) | FAILS (40-55 COLD) | FAILS (40-55 COLD) |

Every case is FRAGILE.

Reported, no C at all (same profile): 40-55 COLD for every framework case and H (f 0.79 to 0.86), and census
canonical is also HOT at 20-30. Most of what C does lies in B: the measured beta 0.44 at 40-55 lifts that bin by
about 0.07.

DES profile (single 4.90) under C, reported: census canonical FAILS (30-40 HOT, 1.170 +/- 0.064); census alt
SLOPE; H PASSES.

## Hand estimate against result

| item | estimate | result |
|---|---|---|
| break detected | 50 per cent | yes, inverted (steep inside, shallow outside); I expected shallow inside |
| census canonical | PASSES 30, FAILS 45, SLOPE 15 | SLOPE (at the edge) |
| census alt | PASSES 40 | PASSES |
| rc canonical | PASSES 45 | PASSES |
| rc alt | SLOPE 15 | SLOPE (at the edge) |
| H | PASSES 40 | PASSES |
| same word for framework and H on a footing | 60 | no, but only through the SLOPE words |
| a FRAGILE framework case | 60 | all four |
| gate holds on both footings | 85 | yes |

## What the lane does not cover

- It shares RAW1's catalogue, sample cuts and bins.
- It shares the PS1 completeness function: the M_r = +0.6 and the logistic parameters are PROVISIONAL, from memory
  and from a web read.
- It shares the frame, MWT1's S2 cold-group star list and L cut, the X scale, and the assumption that BHB stars and RR
  Lyrae share one density profile. That last assumption is not checked here.
- Spherical Jeans, steady state, no LMC correction, no flattening (q = 1).
- The 55-80 kpc anisotropy is not measured.
- Only one KA-5 seed is frozen; the replacement (A1) was chosen after a diagnostic was seen (disclosed).

## Looked wrong

- The inverted break. The PS1 outer slope moves from 4.20 to 3.36 as the score cut is loosened from 0.9 to 0.6.
  That pattern is what contamination does to the outermost stars: purity is lower near 80 kpc, and contaminants
  flatten the outer slope. It is also what an over-steep completeness drop would do. DES, at higher completeness,
  sees no break and a single slope of 4.90. If the shallow outer slope comes from contamination, the predicted
  dispersion beyond 40 kpc is too high, and f there too low. Bb (single 4.77) and the DES profile put census
  canonical back to 30-40 HOT. The primary pass leans on this outer slope.
- The SLOPE rule's 0.84 boundary decides two words: 0.825 and 0.840 = 168/200, with the boundary inclusive as frozen.
- In run 2 the null mocks were reloaded from run 1's checkpoint (same seed 331101, same sample), so T is identical.

## Files

`FROZEN_CRITERIA.md`, `WHAT_I_SAW_AT_START.md`, `AMENDMENT_A1.md`, `rrl3r.py`, `rrl3r.out` (run 2),
`rrl3r_results.json`, `rrl3r_MUTATE.out`, `rrl3r_run1_ASFROZEN_KA5_FAIL.out`, `rrl3r_ka5_check.py` and its outputs,
`mocks_null.jsonl`, `mocks_des_null.jsonl`.
Run: `python3 -I -B rrl3r.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits>` (about 2 to 3 minutes).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
