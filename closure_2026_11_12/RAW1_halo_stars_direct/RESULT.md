# RAW1 RESULT: the halo stars direct (DESI DR1 BHB, spherical Jeans in velocity space, no calibration)

2026-11-12. TEST lane. Adopts nothing. Criteria `FROZEN_CRITERIA.md` (sha256 6234c608..., `FREEZE_STAMP.txt`),
written before any velocity, distance, magnitude or proper motion was read. Two amendments, both written before
the run they govern: A1 (the frozen magnitude window failed check K6b; window moved to observed r, MWS-targeted
main-survey stars), A2 (bug fix: the nuisance means were not re-maximised in the beta and dispersion-law fits).
The failed and buggy runs are kept (`raw1_run1_K6b_FAIL.out`, `raw1_run2_beta_profile_bug.out`).
Graded run: run 3 (`raw1.out`).

## Labels (frozen rule: PASSES if |f - 1| <= 2 sigma_f in every bin; f = observed / predicted dispersion)

| model | footing | label | failing bins | fragility |
|---|---|---|---|---|
| framework line, census baryons | canonical | **FAILS HOT, FRAGILE** | 20-30, 30-40 | flips only under the two-slope density (to FAILS COLD) |
| framework line, census baryons | alt | **FAILS HOT, FRAGILE** | 30-40 | two-slope: FAILS COLD; two-class window (A1.2): PASSES |
| framework line, stars at rotation-curve mass | canonical | **FAILS HOT, FRAGILE** | 30-40 | two-slope: FAILS COLD; two-class window: PASSES |
| framework line, stars at rotation-curve mass | alt | **FAILS HOT, FRAGILE** | 30-40 | alpha low end: PASSES; two-slope: FAILS COLD; two-class window: FAILS COLD (40-55, at the edge) |

Comparators (reported, not graded): Newtonian census baryons FAILS HOT in every bin (f = 2.1 to 3.2).
DESI's NFW (M200c 1.19e12, c 12) **also FAILS HOT at 30-40** (f = 1.142 +/- 0.055) and passes elsewhere.

Read together: every smooth model fails hot in the same bin, 30-40 kpc, where the stars are hotter
(sigma_los 106.7 km/s) than at 20-30 (97.2) and 40-55 (92.6). That is a feature of the stars, not of the
framework alone. Outside that bin, the census line on canonical is also hot at 20-30 (f = 1.095 +/- 0.035,
2.7 sigma). The rotation-curve stellar mass brings 20-30, 40-55 and 55-80 to f within 1 sigma of 1 on both
footings. The FRAGILE tags are real under the frozen rule, but the two-slope flip is not informative: in the
nominal window the outer slope is unconstrained (0.6 +/- 2.4), and the Jeans integral then diverges, which
gives f = 0.05 to 0.18 for every model (DESI's NFW included).

## Numbers (nominal: Sgr band 15 deg, |v_gsr| <= 400, R0 8.122, solar velocity (12.9, 245.6, 7.78))

Sample: 1,495 stars at 20-80 kpc (865 / 264 / 241 / 125 per bin; no merge needed); 1,444 with usable Gaia PMs.

| bin [kpc] | N | sigma_los [km/s] (68%) | beta (own PMs) | usable for beta |
|---|---|---|---|---|
| 20-30 | 865 | 97.24 [94.95, 99.63] | 0.671 [0.650, 0.691] | yes (median t-error 12 km/s) |
| 30-40 | 264 | 106.74 [102.25, 111.57] | 0.685 [0.646, 0.721] | yes (26) |
| 40-55 | 241 | 92.62 [88.51, 97.04] | 0.441 [0.348, 0.522] | yes (60) |
| 55-80 | 125 | 95.30 [89.43, 101.82] | not fitted | no: PM error 116 km/s > dispersion; bracket 0.2-0.8 |

Global beta (usable bins together) 0.659 +/- 0.018. Density slope alpha (single, 1,021 stars in the window
r_obs 16.2-18.9) 5.289 [5.120, 5.458]; two-slope: inside 40 kpc 5.39 +/- 0.18, outside 0.6 +/- 2.4
(unconstrained; the window reaches about 45 kpc).

f per bin (sigma_f = stat + alpha + beta in quadrature):

| model | 20-30 | 30-40 | 40-55 | 55-80 |
|---|---|---|---|---|
| FW census canonical | 1.095 +/- 0.035 | 1.205 +/- 0.058 | 1.052 +/- 0.053 | 1.090 +/- 0.106 |
| FW census alt | 1.052 +/- 0.034 | 1.155 +/- 0.056 | 1.007 +/- 0.051 | 1.043 +/- 0.102 |
| FW rc canonical | 1.028 +/- 0.033 | 1.135 +/- 0.055 | 0.992 +/- 0.050 | 1.030 +/- 0.100 |
| FW rc alt | 1.012 +/- 0.032 | 1.114 +/- 0.054 | 0.972 +/- 0.049 | 1.007 +/- 0.098 |
| N (Newton, baryons) | 2.064 +/- 0.061 | 2.662 +/- 0.125 | 2.664 +/- 0.131 | 3.164 +/- 0.278 |
| H (DESI NFW) | 1.068 +/- 0.035 | 1.142 +/- 0.055 | 0.997 +/- 0.050 | 1.050 +/- 0.099 |

Two-class window (A1.2, r_obs 16.2-19.9, 1,319 stars, alpha 4.719 +/- 0.092, two-slope 5.27 / 3.12 +/- 0.31):
FW census canonical 1.015, 1.117, 0.975, 1.010; alt 0.975, 1.071, 0.933, 0.966; rc canonical 0.953, 1.052,
0.920, 0.954; rc alt 0.939, 1.033, 0.901, 0.933 (bins in order).

Direct Jeans enclosed mass (no calibration; M = r sr^2 (alpha + gamma_s - 2 beta) / G with sr^2 a power law
fitted to the line-of-sight velocities: sr = 99.2 km/s at 40 kpc, gamma_s = 0.105), 1e11 Msun:

| r | stars (nominal) | stars, two-class window | FW census can / alt | FW rc can / alt | DESI joint |
|---|---|---|---|---|---|
| 30 kpc | 2.89 -0.18 +0.14 | 2.48 | 2.33 / 2.53 | 2.64 / 2.73 | 2.65 -0.13 +0.14 |
| 50 kpc | 4.56 -0.29 +0.19 | 3.92 | 3.68 / 4.01 | 4.14 / 4.31 | 4.51 -0.26 +0.27 |

The errors (300 bootstraps plus beta) do not include the window choice. The window alone moves the masses by
0.4 to 0.6, about 2 to 3 of the quoted sigmas.

## Assumptions that remain, and how far each moves the answer

| assumption | varied how | movement |
|---|---|---|
| steady state (equilibrium) | not testable directly; Sgr band 10 / 20 deg; no Sgr cut | 10 deg: f down 0.01 to 0.05 (rc models PASS both footings); 20 deg: f up 0.00 to 0.03; **no cut: f down 0.06 to 0.30, all four FAIL COLD, M50 3.05**. The 30-40 kpc excess that drives every fail may be unremoved substructure. |
| spherical potential and tracers | not varied | unknown; a limit |
| power-law tracer density | single vs two-slope; window 18.9 vs 19.9 | 1 sigma in alpha: f +/- 0.02; window: f down 0.08, M30 2.89 -> 2.48, M50 4.56 -> 3.92; two-slope in nominal window degenerate (above) |
| constant beta | per-bin 0.67, 0.69, 0.44 +/- 0.09: **not constant** across 40 kpc | beta 0.2: f up 0.08 to 0.12 (all FAIL HOT), M50 5.48; beta 0.8: f down 0.03 to 0.04 (rc models PASS), M50 4.27 |
| catalogue distances (no error column) | x0.95, x1.05 | f +/- 0.01 to 0.04; rc alt PASSES at x1.05; M30 2.93 / 2.74 |
| 10 per cent distance error in the PM fit | 0 and 0.2 | beta 0.61 / 0.71; f +/- 0.01; rc alt PASSES at 0.2 |
| solar position and motion | R0 8.275, (11.1, 251.5, 8.59) | f up 0.005 to 0.013; labels unchanged |
| magnitude completeness (flat in r_obs inside the window; MWS main classes) | faint limit 18.5; two-class 19.9 | 18.5: f up 0.01, labels unchanged; 19.9 as above |
| velocity clip | 350, 500, none | 350 removes no star; 500 / none add 2 stars (30-40 sigma 106.7 -> 109.9); labels unchanged |
| no LMC correction | not modelled | 55-80 bin mean is -21.6 km/s (others 0 to 6), a hint of the LMC-induced motion; not corrected |
| baryon census (McMillan 2017) | census vs rotation-curve stellar mass | f down 0.06 to 0.08; the main lever after the window |
| no external field | dropped per owner note (0.000160 / 0.000110) | none inside 300 kpc |

## Checks

All known-answer checks passed before any label in run 3: K1 synthetic at the real positions (alpha
4.550 +/- 0.164 vs 4.5; beta 0.523 +/- 0.024 vs 0.5; f 1.014, 1.032, 0.983, 1.085, all within 2 sigma);
K2 projection limits and Monte Carlo (0.6243 vs 0.6250); K3 flat-curve Jeans integral to 0.001 per cent;
K4 80 kpc line 5.6905 / 6.2183 (brief: 5.691 / 6.219) and r V^2/G = 4.649e11; K5 Sgr core at
Lambda 0.09, B 1.55; K6a identifiers; K6b' (A1.3, set after the magnitudes were seen, not blind).
**Failed check: frozen K6b** (run 1; 4.85 per cent of stars outside the frozen magnitude window), which
forced A1. Mutations bite: Newtonian baryons FAIL HOT in all bins; a0 x 16 FAILS COLD in all bins, both
footings (`raw1_mut.out`).
Independent SI check (`raw1_verify.py`, own frame transform, scipy quad): sigma_los(20-30) by moments 97.25
vs ML 97.24 km/s; hand-built f for FW census canonical in 20-30 is 1.094 vs 1.095. Direct mass at 30 kpc
re-derived by hand in SI: 2.886e11.

## Limits

- The nominal magnitude window reaches about 45 kpc, so alpha (and through it every prediction) is set
  inside 45 kpc and extrapolated outward. The two-class window reaches further, but it assumes the faint
  BHB class is as complete as the main classes. The lane cannot tell which window is right, and the labels
  differ between them.
- K1 has no rotating component and did not catch the A2 defect. The A2 fix was checked by a grid scan.
- beta is not constant (0.67 inside 40 kpc, 0.44 +/- 0.09 at 40-55). The Jeans model's constant-beta
  assumption is violated at about 2.5 sigma.
- The magnitude limits came from memory of the MWS targeting (PROVISIONAL). A1 reads them from the data's
  own target bits.
- The f-label line in `raw1.out` says "stars in the g window"; the window is in observed r (A1). The wording
  is stale.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt` (criteria, model module and amendment hashes), `AMENDMENT_A1.md`,
`AMENDMENT_A2.md`, `DATA_SOURCE.txt` (URL, size, sha256; the file is not in the repository), `raw1_model.py`,
`raw1.py`, `raw1.out`, `raw1_results.json`, `raw1_mut.out`, `raw1_verify.py`, `raw1_verify.out`,
`raw1_run1_K6b_FAIL.out`, `raw1_run2_beta_profile_bug.out`.
Run: `python3 -I -B raw1.py <MWS_BHB.fits>` (about 10 minutes).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
