# OA1 -- M-RISE exclusion design card (O02 K2 honest-FAIL door)

FEASIBILITY/DESIGN CARD ONLY (W03 precedent). Generated 2026-09-27 02:41.

## Recompute gates (K1, from O02_results.json loaded verbatim)
- M-RISE arm prediction: 0.023831 dex (stored +0.0238) -- PASS
- Primary estimator z: 3.131 (stored 3.13) -- PASS

## n-scaling card
- current: n=55 in-overlap, Delta=+0.0620 dex, SE=0.0198 (z=3.13 vs framework, 1.93 vs M-RISE)
- 3-leg discrimination (0 vs +0.0238 vs selection): SE <= 0.00397 dex
- n_needed = n0*(SE/SE_target)^2 = 1370 M-overlap clusters (caustic or sigma_p masses)

## Registered kill conditions (O02 K2 verbatim)
M-RISE excluded only if |Delta| < 2 SE from 0.000 AND > 3 SE from the M-RISE prediction scaled to the arm median z

## Honest note
K2's two legs (< 2 SE from 0 AND > 3 SE from M-RISE) are achievable only if the TRUE low-z Delta ~ 0: the current +0.0620 (3.1 SE) reading, if real, is a K1 kill-track (z-invariance violated), not an M-RISE exclusion. C08's mass-dependent structure flags LX selection; the WG high-z leg (X-ray/SZ masses + temperatures) adjudicates.

## Provenance
all numbers recomputed from O02_results.json (loaded, never transcribed): n=55 clusters, SE_jackknife=0.0198 (C04), M-RISE formula (pre_registration.mrise), arm medians z_lo=0.1333 z_hi=0.21705
