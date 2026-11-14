# AGB2 amendment 1 (2026-11-14): the weights of the host fit. Committed alone, before any amplitude is read

## What happened
The five known-answer checks were run on the real data after the scripts commit (86df7a46bb).
KG, K1 (Ω_m 0.3316), K2 (raw step +0.0405 ± 0.0105 mag) and K3 (eight twins) pass.
**K4 fails for the per-host template:** under 400 shuffles of host mass the fitted amplitude scatters by 0.143,
against a claimed error of 0.099 (ratio 1.44; allowed 0.8–1.25). The step-run template passes at the edge (1.22).
By the frozen rule H1, H2 and J1–J3 are therefore **NOT EVALUABLE as frozen**. That stands and will be reported.

## Why it failed (diagnosed without reading any amplitude)
The frozen fit weights the supernovae with the inverse of the full STAT+SYS covariance. A scratch diagnosis
(error bars and shuffles only; the real-data amplitude was never printed) shows the estimator then leans on the
off-diagonal terms of that covariance:
- the per-host amplitude's claimed error is 0.097 (reading P), but the diagonal of the covariance alone, through the
  same weights, gives 0.49; the claimed value needs large cancellations from off-diagonal terms, and rows at z < 0.03
  carry 149 % of the claimed variance (the rest is negative cross terms);
- an error estimate from the residuals themselves (a sandwich estimator, clustered by supernova) is 1.6 to 3.5 times
  the claimed error (step run 0.65 against 0.40; per host 0.29 against 0.099 in reading R);
- with **diagonal weights** (each row weighted by its own published total error, off-diagonal terms dropped) the
  three error estimates agree: claimed, sandwich and shuffle scatter are 0.411, 0.405, 0.418 for the step run and
  0.123, 0.123, 0.128 for the per-host template in reading R (ratios 0.94 to 1.04 over both readings).
The off-diagonal terms describe shifts shared by many supernovae (calibration, peculiar-velocity flows, the same
supernova seen by two surveys). A contrast between host groups inside one redshift bin should not gain a factor of
five in precision from them, and the data say it does not. The frozen check K4 was put there to catch this.

## The change (everything else in FROZEN_CRITERIA.md is unchanged)
1. **Weights.** Every fit of Part H, and of K2, K3 and K4, uses diagonal weights 1/C_ii from the published STAT+SYS
   covariance. The error of a parameter is the weighted-least-squares formula. K1 keeps the full covariance (it
   tests the loader against the published Ω_m).
2. **K4, amended (same tolerances).** For both templates, in the primary configuration: |mean Â| ≤ 0.2 σ_A and the
   shuffle scatter within [0.8, 1.25] σ_A; **and** the sandwich error clustered by supernova (CID) within
   [0.8, 1.25] σ_A (this covers rows of the same supernova, which share their intrinsic scatter).
3. **Words.** H1, H2, J1, J2, J3 are judged by the frozen rules on the amended fits and carry the tag "(amendment 1)".
   The power forecast becomes σ_A ≈ 0.41 (step run) and 0.12 (per host).
4. **Both readings are reported.** The fits with the full covariance are still run and printed, labelled NOT
   EVALUABLE (K4), beside the amended ones. Amended outputs are written to separate files (`agb2_<MODE>_diag.json`).

## What had been seen when this was written
K1, K2 (the two constant steps: raw +0.0405 ± 0.0105 mag, published −0.0028 ± 0.0096 mag), K3, K4, and the diagnosis
above. No amplitude A of any real-data fit, in either weighting, in either reading. Mode H and Part J have not been run.

kappa = 1/2 FITTED; not theory closed.
