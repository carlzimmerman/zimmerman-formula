# RRL2 FROZEN CRITERIA: row 28 (halo stars with the RR Lyrae slope) under ONE consistent convention

2026-11-14. TEST lane. Adopts nothing, relabels nothing (RAW1, MWT1, MWT2, RRL1, RRL1R keep their labels; the
scorecard is not edited by this lane), registers nothing. Written and committed alone, before any script of this
lane and before any number of this lane was computed.

## 0. What is known beforehand (disclosed)

Read in full before writing: RRL1 (FROZEN_CRITERIA, RESULT, rrl1.py), MWT1 (FROZEN_CRITERIA, RESULT, mwt1.py, the
`combination.flags` and `diag.B` entries of mwt1_results.json), MWT2 RESULT (first 80 lines), RRL1R RESULT_BLIND
(first 140 lines), the scorecard's rows 27 and 28, RAW1's `grade`. So these numbers are known:
- RRL1 / RRL1R (full-sky PS1 slope, 5,143 cells, 13,100 deg^2): broken 5.29 inside 39.0 kpc, 3.93 beyond; with it
  and RAW1's constant beta 0.6586: FW census 40-55 kpc 0.857 +/- 0.044 (canonical) / 0.820 +/- 0.042 (alt) COLD;
  DESI's NFW (H) 0.820 COLD; 30-40 passes everywhere.
- RRL1's same-profile check on the PS1 cells holding RAW1's BHB stars (1,033 cells), 20-45 kpc only, N = 996:
  single 5.139 [4.994, 5.285]; broken in that window inner 3.76, outer 5.75, break 25.6 kpc, 2 dlnL 9.8, no
  threshold computed. Nothing is known about those cells over 20-80 kpc.
- MWT1: detected corrections C = S2 (31-star overdensity mask, 24 of them in 40-55) + L (logg > 3.75) + B
  (per-bin beta 0.671 / 0.685 / 0.441, p 0.0003) + X-err (error scale 1.3086) + F (equal north / south weight);
  E, S1, D not detected. Under C with RAW1's slope 5.289: FW census canonical 1.090 / 1.225 / 1.164 / 1.143,
  sigma 0.040 / 0.070 / 0.080 / 0.116; H 1.064 / 1.161 / 1.102 / 1.097.
- RRL1 flagged an RR Lyrae chain at RA 219-233, Dec -4 to -13, 49-56 kpc; MWT2 found a cold lump at 30-40 kpc.

Hand estimate (written now): if the own-cells profile over 20-80 kpc keeps the shape RRL1 saw at 20-45 (steep,
about 5.5-5.8, beyond about 26 kpc), the Jeans prediction at 30-55 kpc falls back toward RAW1's single 5.29 and
below, so f rises to RAW1-like or higher; with C on top (beta 0.44 and the S2 mask both heat 40-55) I expect 30-40
HOT again (about 1.2) and 40-55 PASS or HOT, for the framework and H alike: "STILL FAILS", now hot, and
separating nothing. If instead the own cells show RRL1's full-sky shape (shallow beyond 39), C lifts 40-55 by about
+0.11 to about 0.97 / 0.93: the row could pass. My guess: STILL FAILS (30-40 HOT), framework and NFW together.

## 1. Inputs (untracked, never added to git; read with `python3 -I -B`, paths as arguments; sha256 checked)

PS1 RRab table (Sesar+17, sha256 ab4b837f...f813), DES table (6,971 rows, sha256 94e3eb68...8303; loaded only
because RRL1's footprint code expects it, not used for any graded number), DESI DR1 BHB catalogue `MWS_BHB.fits`
(sha256 5669c821...5246). MWT1's detected S2 star list (31 catalogue indices) and X-err scale are read from
`closure_2026_11_13/MWT1_hot_bin_assumptions/mwt1_results.json` (`combination.flags`), read-only; reusing MWT1's
detection, not re-detecting (its shuffles are heavy and the machine is loaded).

## 2. Code reuse (other lanes' files never edited)

`rrl1.py` is copied into this folder as the base of `rrl2.py` (density fit, footprint, completeness, likelihood,
mocks, RAW1 functions by AST). MWT1's `make_opt`, `est_bin`, `fit_scale`, `beta_of`, `tracer`, `sr2_grid`, `predP`
(variable-beta Jeans, hemisphere-weighted estimator, masks, error scale) are copied with citation. RAW1's files are
read-only.

## 3. The one convention (primary case P)

- **Density slope on the kinematic tracers' own sky cells ("own cells"):** PS1 nominal footprint exactly as RRL1
  (score > 0.8, |b| > 20, reddening, Sgr band |B| >= 15, Magellanic masks, clump rule, paper completeness, q = 1),
  INTERSECTED with the cells (RRL1's 2.546 deg^2 equal-area grid) that hold at least one of RAW1's 1,495 sample
  stars at 20-80 kpc (cells defined from RAW1's sample before any C mask; RRL1's definition, 1,033 cells expected).
  Fit range 20 <= r < 80 kpc (the full Jeans range). Single law and broken law; break radius free in
  [22.5, 75] kpc (lower bound 22.5, not RRL1's 25, chosen knowing that RRL1's 20-45 own-cell fit put the break at
  25.6; disclosed). Break DETECTED if 2 dlnL > T_own = 99th percentile of 100 null mocks from the best single law
  on the own-cells footprint, completeness and N (floor 6.63). Profile used: broken if detected, else single.
- **Kinematics: MWT1's C exactly** (L 3.75, S2 31-star mask, X-err 1.3086, B per-bin beta 0.671 / 0.685 / 0.441 with
  beta(>= 55) = 0.441, F equal-hemisphere weight), RAW1's sample, bins, and statistic otherwise.
- sigma_f = sqrt(s_stat^2 + s_slope^2 + s_beta^2): s_stat from MWT1's estimator under C; s_beta as MWT1's B-data
  (all measured betas shifted by +/- their own sigma together for 20-55; beta(>= 55) at 0.2 / 0.8 for 55-80);
  s_slope = std of f over 200 draws of the own-cells profile from its Hessian covariance (RRL1's rule; rb clipped
  to its range, slopes >= 0). RAW1's s_alpha is replaced by s_slope.
- Line: the framework's no-field line (RAW1's raw1_model.py). The owner's actual-field reading puts the Milky Way's
  external field at e_N = 0.000160 (canonical) / 0.000110 (alt) inside the kernel, which inside 300 kpc is the
  no-field line; a reported diagnostic gives nu(sqrt(y^2 + e_N^2)) / nu(y) at 20, 55 and 80 kpc for FW census.
  **Graded footings use the standing a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2** (multipliers on
  RAW1's 9.36e-11 / 1.13e-10, as MWT1's a0m row); the RAW1-rounded values are reported for the known answers and
  as a reported row. Canonical and alt are side by side, never pooled.
- Models: FW census and FW rc on both footings (the four framework cases), DESI's NFW (H), Newton (N). H is graded
  with the same rule and reported beside the framework in every table. N is reported.

## 4. Brackets (each a full re-run of the Jeans step; the density fit redone where it changes)

- B1 full-sky slope + C: RRL1's full-sky nominal profile (its model choice, broken 5.29 / 3.93 / 39.0) with C.
- B2 own-cells slope WITHOUT C: RAW1's constant beta 0.6586 (RAW1's beta ranges for s_beta), no masks, no error
  scale, plain estimator.
- B3 own-cells slope + C WITHOUT the S2 cold-group mask (C minus S2). Reported in its own table beside P, because
  the mask removes cold stars (24 of 31 in 40-55).
- B4 own-cells, the other model (single if broken was chosen, broken if single) + C.
Reported, not brackets: B1 without S2; full-sky slope without C (= RRL1, the known answer); P at RAW1-rounded a0.

## 5. Words (per case; per footing; never pooled)

In this order:
1. **NO VERDICT** if (a) the profile used has an outer slope <= 2 x 0.441 + 0.5 = 1.382 (Jeans integral not
   convergent with beta(>= 55) = 0.441; MWT1's rule), or (b) over the 200 profile draws, with sigma =
   sqrt(s_stat^2 + s_beta^2), the fraction of draws in which all four bins PASS lies between 0.16 and 0.84 (the
   slope's 68 per cent interval spans pass and fail; RRL1's NO POWER rule widened from one bin to the row).
2. **ROW 28 PASSES UNDER ONE CONVENTION** if every bin (20-30, 30-40, 40-55, 55-80) is PASS (|f - 1| <= 2 sigma_f).
3. **STILL FAILS [bins, words]** otherwise.
**FRAGILE** appended if any bracket B1-B4 gives a different word (of the three) for that case.
RRL1's gate lines are unchanged: bins, |f - 1| <= 2 sigma_f, HOT above, COLD below.

Headline: the four framework cases per footing, and H beside them. If the framework cases and H get the same word,
the result is stated as separating nothing between them. A PASS for the framework is a HIT, not a pass of the
theory, and awaits an independent re-grade.

## 6. Known answers (the script stops before any word if one fails)

- KA1 RRL1 reproduced: full-sky PS1 broken fit 5.293 / 3.934 / 39.0 (each within 0.005, rb within 0.1), and with
  RAW1's constant beta, no C, RAW1-rounded a0: FW census 40-55 f = 0.857 (canonical) and 0.820 (alt), and every f
  of the six cases within 5e-4 and sigma_f within 2e-3 of `rrl1_results.json` (`second_step`).
- KA2 MWT1 reproduced: RAW1's slope 5.289 (RAW1's s_alpha) + C, RAW1-rounded a0: FW census canonical 40-55
  f = 1.164 (1.1645), and every f and sigma_f of the four FW cases and H within 5e-4 of `mwt1_results.json`
  (`combination.C`).
- KA3 RRL1's same-profile check reproduced: own cells, 20-45 kpc, rb in [25, 40]: N 996 and single 5.139 within 0.005.
- KA4 SI: g(30 kpc) FW census canonical, M = g r^2 / G equals raw1_model's M_of_g to 1e-9.
- KA5 the own-cell count is between 1,000 and 1,100 (RRL1R reports 1,033 kept of 1,073).

## 7. Twins and mutations (reported; a failed twin is stated, it does not stop the run)

- TW1 null twin, must NOT bite: replace every star's v_gsr (under C's sample) by mean + N(0, P_i + (1.3086 e_i)^2)
  with P_i the primary FW census canonical prediction (true f = 1 in every bin), 20 seeds: the row word must be
  ROW 28 PASSES in at least 12 of 20 seeds (four bins at 95 per cent each give about 16).
- MU1 mutation, must bite: as TW1 but true f = 0.80 in 40-55 only: 40-55 COLD in at least 15 of 20 seeds.
- MU2 mutation, must bite: as TW1 but true f = 1.25 in 30-40 only: 30-40 HOT in at least 15 of 20 seeds.
- MD density mutation: 5 mocks drawn on the own-cells footprint and completeness at the own-cells N from RRL1's
  full-sky law (5.29 / 3.93 / 39.0): report the fraction in which the break is detected at T_own and the outer
  slope is recovered within 2 sigma. It says whether the own cells could see the full-sky shape if it were there;
  a low fraction is stated as a limit on how far the own-cell slope differs from the full-sky one.
- Diagnostic (reported): sky positions and radii of the S2-flagged stars in 40-55 kpc, and how many lie within
  10 deg of RA 226, Dec -8.5 and within 45-60 kpc (RRL1's RR Lyrae chain).

## 8. What this lane cannot settle (stated now)

It keeps RRL1's PS1 cuts, completeness and Sgr band, so it inherits their softness (the outer slope moved 3.35 to
4.20 with them full-sky). The own cells hold about a fifth of the area, so the own-cell slope is noisier. It reuses
MWT1's detections rather than redoing them. The same-profile assumption (BHB and RR Lyrae share one radial profile)
stays an assumption. Spherical Jeans, no flattened model.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
