# RAW1 AMENDMENT A2 (2026-11-12, written before run 3; FROZEN_CRITERIA.md is not edited)

## What happened

Run 2 (under A1; partial output kept as `raw1_run2_beta_profile_bug.out`, stopped by hand during the
fragility variants) passed every known-answer check and printed the nominal numbers and labels. Reading them,
the per-bin beta intervals were implausibly narrow (40-55 kpc: 0.396 [0.379, 0.403] from 231 stars with
60 km/s tangential errors). A grid scan of the profile likelihood (scratch diagnostic, not part of the lane)
showed the cause: the inner Nelder-Mead started vphi_bar at exactly 0, where scipy's default simplex step
is 0.00025, so vphi_bar was often not re-maximised and the profile jumped by several units of lnL between
neighbouring beta values. The frozen estimator (section 4.3: "sr and vphi_bar re-maximised") was not
implemented as written. The same start-at-zero defect sat in the direct-mass dispersion law (mu started
at 0). K1 did not catch it because the synthetic halo has no rotation (true vphi_bar = 0).

## Change (implementation only; no criterion, threshold, sample or label rule changes)

A2.1 beta fit: for fixed (sr, beta) the likelihood is Gaussian with a mean linear in vphi_bar, so vphi_bar
     is re-maximised exactly (closed form); sr is re-maximised by a bounded 1-D search over [20, 600] km/s.
A2.2 direct-mass dispersion law: the mean mu is re-maximised exactly for each (s0, gamma_s); (s0, gamma_s)
     by Nelder-Mead with an explicit initial simplex (steps 0.3 in ln s0 and 0.3 in gamma_s).
A grid scan after the fix gives smooth profiles; per-bin betas (20-30, 30-40, 40-55): 0.671 +/- 0.020,
0.685 +/- 0.037, 0.441 +/- 0.087 (55-80 not usable by the frozen rule). These were seen before run 3.

Known limitation recorded: K1 has no rotating component, so it cannot test the vphi_bar re-maximisation.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
