# RRL3R FROZEN CRITERIA: Milky Way halo stars with the measured RR Lyrae star-count profile and the measured anisotropy (blind)

2026-11-14. TEST lane, blind re-grade. Adopts nothing, relabels nothing, registers nothing. Written and committed
alone (with `WHAT_I_SAW_AT_START.md`), before any script of this lane exists and before any number of this lane was
computed.

## 0. What I had seen before freezing

- The three brief files (house rules, this lane's specification, the RR Lyrae star-count specification with RRL1's
  frozen sections 0 to 8).
- The files the specification allows: `closure_2026_11_13/MWT1_hot_bin_assumptions/FROZEN_CRITERIA.md` and `mwt1.py`;
  `closure_2026_11_12/RAW1_halo_stars_direct/RESULT.md`, `raw1.py`, `raw1_model.py`;
  `closure_2026_11_14/RRL1R_blind_halo_slope_regrade/rrl1r.py`. All are code or RAW1's own result; none holds a number
  under this lane's convention (PS1 RR Lyrae profile with C). RAW1's RESULT gives its f table (single slope 5.289,
  constant beta 0.6586) and the per-bin betas 0.671, 0.685, 0.441, and DESI NFW f = 1.142 +/- 0.055 at 30-40 kpc.
- The starting-context lines quoted in `WHAT_I_SAW_AT_START.md`.
- The script will read `raw1_results.json` (RAW1's own stored f and sigma_f, the same numbers as RAW1's RESULT to more
  decimals) only for KA-1, as MWT1 and RRL1R did; it is not on the forbidden list. Not opened by hand.
- No RR Lyrae table, BHB velocity, or density-fit number has been read by me.

## 1. The question

Per bin (20-30, 30-40, 40-55, 55-80 kpc, Galactocentric spherical r), f scales the spherical Jeans prediction of the
line-of-sight velocity dispersion of RAW1's DESI DR1 BHB stars to the measured one. Word per bin: PASS if
|f - 1| <= 2 sigma_f, HOT if f > 1 + 2 sigma_f, COLD if f < 1 - 2 sigma_f. One frozen convention: the star-count
profile n(r) measured on the full sky from PS1 RR Lyrae (section 2) and the kinematic convention C (section 3).

## 2. Star-count profile (RRL1 sections 1 to 4, as written in the star-count specification)

Inputs (never committed; command-line arguments; sha256 checked): PS1 `table5_subset.tsv` (ab4b837f...f813), DES
`table1.tsv` (94e3eb68...8303), `MWS_BHB.fits` (5669c821...5246).
Sky grid 180 x 90 equal-area cells; per-cell masks: PS1 coverage (dec > -30 and a row of the full table in the cell),
|b| > 20, median E(B-V) <= 0.25, |B_Sgr| >= 15, Magellanic Clouds / Fornax / Sculptor circles, clump cells (>= 4 other
RRab with S3ab > 0.8 within 0.5 deg and |Delta DM| < 0.25, cells within 1.5 deg masked). RRab S3ab > 0.8. Fit range
20 <= r < 80 kpc. Completeness C(d) = 1 / (1 + exp(4.1 (DM + 0.6 - 20.57))). q = 1. Unbinned likelihood
ln L = sum ln n(r_i) - N ln Z, normalisation on 2 x 2 sub-directions per cell and 120 ln d nodes. Single law
n = (r/40)^-a (a in [0, 10]); broken law, rb in [25, 75], grid 2.5 kpc then 3-parameter Nelder-Mead; errors from the
numerical Hessian. Break detected if 2 Delta ln L > T, T = 99th percentile of 100 null mocks from the best single law
(floor 6.63). Profile used: broken if detected, else single, extrapolated with its outer slope to 2e4 kpc.
Implementation: the footprint, completeness, normalisation, likelihood, fit, mock and draw functions are COPIED from
`closure_2026_11_14/RRL1R_blind_halo_slope_regrade/rrl1r.py` with a citation in the script (allowed by the
specification). Seeds (mine): null mocks 331101 (mock i uses `default_rng([331101, i])`), KA-5 single mock 331102,
KA-5 broken mock 331103. DES is fitted as a cross-check with its own 100 null mocks (seed 331108, rb in [25, 95],
20-100 kpc, flat completeness) and its census canonical f under C is reported, not graded.

## 3. The kinematic convention C (MWT1's C exactly; my own code for the Jeans step, the anisotropy and the estimator)

Sample: RAW1's (RAW1's `load` and `build` executed read-only from `raw1.py` by AST, as MWT1 and RRL1R did; nominal
config: Sgr band 15 deg, |v_gsr| <= 400, R0 8.122 kpc, z_sun 20.8 pc, v_sun (12.9, 245.6, 7.78)); RAW1's bins.
- L: drop stars with LOGG > 3.75 and LOGG_ERR < 0.25 (LOGG finite), from the RVTAB extension at the star's row.
- S2: drop the 31 stars whose RAW1 row index (`S["i"]`, the row of the catalogue's RVTAB / FIBERMAP / GAIA tables, as in
  `mwt1.py`) is in the brief's list.
- X: every velocity error multiplied by 1.3085676978624774 in the estimator.
- B: beta profile piecewise constant: beta_1 for r < 30, beta_2 for 30 <= r < 40, beta_3 for 40 <= r < 55, and beta_3
  held for r >= 55 (55-80 is not measured: RAW1's usable rule, PM error larger than the dispersion). Measured by me
  (section 4) on RAW1's full per-bin sample (no L, no S2 mask, unscaled errors), as MWT1 measured it.
- F: per bin, f = (f_north + f_south) / 2 by Galactic latitude (b > 0 / b <= 0), each fitted alone, if both halves
  hold >= 15 stars; stat error 0.5 sqrt(s_N^2 + s_S^2); else the plain f.
- Estimator (mine): v_i ~ N(mu, f^2 P_i + e_i^2), mu maximised exactly for each f (weighted mean), f the maximum of the
  profile likelihood on [0.05, 5]; s_stat = half the width of the Delta ln L = 0.5 interval (root-found each side).
- P_i = sigma_r^2(r_i) (1 - beta(r_i) sin^2 eta_i), eta_i the angle between the line of sight and the Galactocentric
  radius (RAW1's `sin2`).
- Jeans (mine): sigma_r^2(r) = [1 / (n(r) I(r))] Integral_r^inf n I g ds, I(s) = exp(Integral 2 beta(s')/s' ds'),
  for piecewise-constant beta I(s) is the exact product of power laws, continuous at 30, 40, 55. Integral on a log grid
  1 to 2e4 kpc (8,000 nodes, plus the nodes 30, 40, 55 and rb), with the exponential (log-linear) rule per segment,
  exact for power-law integrands; the star's own partial segment is integrated with the same rule. g from RAW1's
  `raw1_model.g_model` (imported read-only).
- a0: graded footings use a0_mult = 9.3603/9.36 (canonical) and 1.1312/1.13 (alt) on RAW1's model; rounded values
  (a0_mult = 1) for KA-1 and KA-2 only.
- sigma_f = sqrt(s_stat^2 + s_slope^2 + s_beta^2).
  - s_beta (20-30, 30-40, 40-55): half |f(beta + sigma) - f(beta - sigma)|, where all three measured betas move by
    their own sigma together and the held beyond-55 value moves with beta_3. s_beta (55-80): half
    |f(beta(>=55) = 0.8) - f(beta(>=55) = 0.2)|, the 20-55 betas kept.
  - s_slope: standard deviation of f over 200 draws of the profile from the Gaussian of the fit's inverse Hessian
    (single: a ~ N(a, sigma_a), a >= 0; broken: (a_in, a_out, rb) multivariate normal, rb clipped to [25, 75], slopes
    >= 0). Seed 331107. Each draw uses the full estimator of C.

## 4. My anisotropy measurement

Per bin, the stars of RAW1's sample in the bin with RAW1's proper-motion quality cut (Gaia source id > 0 and equal to
REF_ID, finite PM and errors, RUWE < 1.4). Observed rest-frame velocity w_i = (v_gsr, 4.74047 d mu_a* + e_a . v_sun,
4.74047 d mu_d + e_d . v_sun) in the (n, e_a, e_d) basis. Model: Galactocentric velocity Gaussian with mean v_phi
along phi-hat, dispersions sigma_r along r-hat and sigma_t = sqrt(1 - beta) sigma_r along theta-hat and phi-hat; the
3 x 3 covariance projected on the star's basis plus errors: v_los error^2; PM errors times 4.74 d with their
correlation; plus (0.10 x tangential velocity)^2 for the distance error on each tangential component (RAW1's model,
which KA-3 needs). v_phi maximised exactly (linear), ln sigma_r maximised numerically, beta profiled on [-3, 0.99];
beta = the maximum, sigma_beta = half the Delta ln L = 0.5 interval. Usable if >= 30 stars, median tangential error
below the bin's line-of-sight dispersion, and sigma_beta <= 0.3 (RAW1's rule). The code is my own; `mwt1.py` and
RAW1's `measure` are run only as cross-checks and printed as such.

## 5. Models and cases

Framework no-field line (`raw1_model.py`): census stellar mass and rotation-curve stellar mass, canonical and alt
(four graded cases). DESI NFW (H): graded by the same rules, shown beside the framework everywhere. Newton (N):
reported.

## 6. Known answers (the script stops before any word if one fails)

- KA-1: RAW1 reproduced with my Jeans and estimator at RAW1's slope 5.289 +/- s_alpha, constant beta 0.6586 and RAW1's
  beta ranges, rounded a0: counts 865 / 264 / 241 / 125 and every f and sigma_f of RAW1's six cases within 5e-4 of
  `raw1_results.json`.
- KA-2: single slope 5.289, C, rounded a0, FW census canonical: stars exactly 727 / 227 / 186 / 115; f within 0.01 of
  1.0901, 1.2248, 1.1645, 1.1432.
- KA-3: my betas for 20-30, 30-40, 40-55 within 0.02 of 0.671, 0.685, 0.441, and 55-80 not usable.
- KA-4: my variable-beta Jeans with one constant beta equals the closed form to 1e-6 (relative): flat curve
  V = 200 km/s, single laws (a, beta) = (4.5, 0.5), (3.5, 0), (5.289, 0.6586), and the broken law (3, 5, 35) with
  beta 0.6586 (exact piecewise formula), at r = 20, 25, 30, 40, 55, 60, 80 kpc. Also reported: agreement with RAW1's
  `sr2_profile` for the real models (trapezoid, so about 1e-4 expected; not gated).
- KA-5: RRL1's K1 (single 4.5 mock recovered within 2 sigma, no break) and K2 (broken 3 / 5 / 35 mock: break detected,
  a_in and a_out within 2 sigma, rb within 2 sigma or 5 kpc), with the nominal footprint, completeness and N. Also
  K0n (binned normalisation equals the node sum to 1e-5).
- KA-6: at 30 kpc, M = g r^2 / G (G = 6.674e-11, Msun 1.989e30, kpc 3.0857e19) from FW census canonical g equals
  `raw1_model.M_of_g` to 1e-9.
- Also printed (not gated): data hashes; the beta cross-check against RAW1's `measure`.

## 7. Twins and mutations (gate the word, per footing, FW census case, primary convention, 20 seeds each)

Stars: the sample under C (after L and S2). Per mock and bin, v_i = mu_bin + N(0, t^2 P_i + (1.3085676978624774
e_i)^2), with P_i the footing's own prediction under the primary profile and measured beta profile, mu_bin the bin's
weighted mean of the real velocities, and t the true f. Each mock is graded with the full C machinery: F estimator,
s_stat, s_beta and s_slope recomputed on the mock velocities (s_slope from the same 200 draws).
- TW1 (t = 1 in every bin): must NOT bite: all four bins PASS in >= 12 of 20. Seeds 331300 + k.
- MU1 (t = 0.80 in 40-55 only): 40-55 must read COLD in >= 15 of 20. Seeds 331400 + k.
- MU2 (t = 1.25 in 30-40 only): 30-40 must read HOT in >= 15 of 20. Seeds 331500 + k.
Written to `rrl3r_MUTATE.out` (and the json).

## 8. Words (per case and footing; this order)

1. NO VERDICT (KNOWN ANSWER) if a known answer fails (the script stops; every case gets it).
2. NO VERDICT (NO POWER) if on that footing TW1 bites, or MU1 or MU2 does not bite. H (no footing) gets NO POWER if
   the gate fails on either footing (my choice; conservative). N likewise; N is reported only.
3. NO VERDICT (SLOPE) if the profile used has an outer slope <= 1.382, or if over the 200 draws, with
   sigma = sqrt(s_stat(draw)^2 + s_beta^2) per bin, the fraction of draws in which all four bins PASS lies in
   [0.16, 0.84].
4. ROW PASSES UNDER THE MEASURED CONVENTION if every bin is PASS.
5. ROW FAILS [bins and their words] otherwise.
FRAGILE appended if any bracket gives a different one of the five words (rules 3 to 5 recomputed on the bracket; rules
1 and 2 carried from the primary). Brackets:
- Ba: C without the S2 mask.
- Bb: the other density model (single if broken used, broken if single), same fit.
- Bc: one constant beta 0.6586 in place of the measured profile, the rest of C kept; s_beta then from RAW1's ranges
  (0.6586 +/- 0.018 for 20-55, 0.2 / 0.8 for 55-80) (my choice where the specification is silent).
- Bd: RR Lyrae score cut S3ab > 0.9 and > 0.6 in place of 0.8; the PS1 fit redone; the nominal model choice (single or
  broken) kept; T kept; new draws (seeds 331601, 331602).
Reported, not a bracket: no C at all (constant beta 0.6586 with RAW1's ranges, no masks, no error scale, plain
estimator), same profile and draws.
Per footing it is stated whether the four framework cases and H get the same word; if so, the gate separates nothing
between them under this convention. A PASS for the framework is a hit that awaits a further independent re-grade.

## 9. Hand estimate (before any number)

Physics: for a flat curve sigma_r^2 = V^2 / (a - 2 beta). KA-2 at a = 5.289 under C gives f = 1.09, 1.22, 1.16, 1.14
(census canonical). A shallower measured profile raises the prediction and lowers f; PS1 RR Lyrae halo fits from
memory (PROVISIONAL) give a single slope near 4.4, and DES finds a broken law (2.5 inside about 32 kpc, 5.4 outside,
with q = 0.7). With a single slope about 4.4: f falls by about 10 to 13 per cent (census canonical about 0.98, 1.09,
1.04, 1.02; 30-40 near the 2 sigma line). With a detected break (shallow inside, about 5 outside): 30-40 stays near
1.15 to 1.2 (HOT) and 20-30 may go COLD.
- Break detected on PS1 (q = 1, 20-80 kpc): 50 per cent.
- FW census canonical: ROW PASSES 30, ROW FAILS (30-40 HOT, perhaps 20-30 COLD) 45, NO VERDICT (SLOPE) 15, NO VERDICT
  (NO POWER) 5, NO VERDICT (KNOWN ANSWER) 5.
- FW census alt: PASSES 40, FAILS 35, SLOPE 15, other NO VERDICT 10.
- FW rc canonical and rc alt: PASSES 45, FAILS 30, SLOPE 15, other NO VERDICT 10.
- H: PASSES 40, FAILS 35, SLOPE 15, other 10.
- Framework and H get the same word on a footing: 60 per cent. FRAGILE on at least one framework case: 60 per cent
  (Bb, the other density model, is the likeliest to flip).
- The gate (TW1 / MU1 / MU2) passes on both footings: 85 per cent (MU1 at f 0.80 in 40-55 with sigma about 0.06 is
  3.3 sigma: about 90 per cent COLD per seed; MU2 at 1.25 in 30-40 with sigma about 0.07: about 3.5 sigma).

## 10. Changes

Never edited after this commit. Departures only as dated AMENDMENT_A#.md files committed alone before the numbers they
govern are read; the as-frozen reading is reported first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
