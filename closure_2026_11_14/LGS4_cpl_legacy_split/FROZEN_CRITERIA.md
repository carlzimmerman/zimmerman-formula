# LGS4 — the legacy supernova split in a two-parameter (w0, wa) fit: lost precision, or a signal the legacy set made? (FROZEN, before any supernova fit)

2026-11-14. Owner: "Yes, run it". A re-read of public data with a public fitting form. It adopts nothing, edits no
ledger and grades nothing in the framework.

## Why
Nájera, Banik and Desmond (arXiv:2610.23657, Table 3) fit the Chevallier-Polarski-Linder form w(a) = w0 + wa (1 − a) to
DES-SN5YR Dovekie + DESI DR2 BAO + 15 cosmic chronometers + a compressed CMB summary + a BBN prior, and report
- DES + legacy (1,820 supernovae): w0 = −0.802 ± 0.056, wa = −0.770 ± 0.220, 3.36σ from constant dark energy;
- DES only (1,623): w0 = −0.845 ± 0.098, wa = −0.639 ± 0.315, 2.13σ;
- DES + legacy with a free magnitude offset on the legacy rows: 2.21σ, offset 0.013 ± 0.021 mag.
They read this as the preference for evolving dark energy resting on the 197 legacy low-redshift supernovae.
LGS1 to LGS3 found the same direction in this repo's own lanes, for the Dovekie sample only.

Two readings fit a drop from 3.4σ to 2.1σ:
- **A, less data:** the fit sits in the same place and only the error bars grow, because the legacy set is nearly the
  whole anchor below z 0.07.
- **B, legacy-made:** the legacy set is offset from the DES sample and pulled the fit away from constant dark energy.
The paper's numbers were not tested for which one they show. This lane asks that, with an independent implementation.

## Inherited ingredients, listed up front
None of these is the framework's. They are the paper's inputs, taken so that its fit can be reproduced:
- the CPL form and its comparison point w = −1 (a fitting form, not this repo's dark energy; no a0 enters);
- standard pre-recombination physics for the sound horizon r_d and the acoustic angle θ*;
- the compressed CMB summary (100θ*, ω_b, ω_bc) with its covariance and the fits for the decoupling and drag
  temperatures, copied from the paper's Eq. 18–21 (built by its authors from SPT-3G + ACT DR6 + Planck chains);
- the BBN prior ω_b = 0.021915 ± 0.000215; neutrino masses (50, 10, 0) meV, N_eff = 3.044; a flat universe.
So no result of this lane is a statement about the framework, and none may be used as one.

## Data and samples
- Supernovae: the Dovekie Hubble diagram and STAT+SYS inverse covariance on disk (as CFG684 and LGS1), absolute
  magnitude profiled. Samples as LGS1: `full` (1,820), `des_only` (IDSURVEY 10; 1,623), `rand197` (legacy kept, 197
  random DES supernovae dropped, LGS1's seed 20261113). A dropped supernova leaves the covariance as in LGS1.
- DESI DR2 BAO: the 13 numbers of arXiv:2503.14738 as copied in CFG681, now with r_d computed, not profiled.
- Cosmic chronometers: the 15 points and covariance of CFG684.
- Compressed CMB and BBN as above.

## Method
`lgs4_like.py` is an independent implementation: the sound horizon and the distance to decoupling are integrated
numerically with exact Fermi-Dirac neutrinos (the paper uses a closed form). Parameters (h, Ω_bc, ω_b, w0, wa), flat
priors of the paper's Table 1. `lgs4_run.py` finds the best fit (three starts per shape, Nelder-Mead and Powell), the
Laplace covariance, and runs four Metropolis chains of 60,000 steps (5,000 dropped each). Models: `cpl`; `lcdm`
(w0 = −1, wa = 0, written "constant dark energy" below); `cpl_dm` and `lcdm_dm` (the same with one free magnitude
offset on the legacy rows, prior ±1 mag). Eight runs: full × four models, des_only × (cpl, lcdm), rand197 × (cpl, lcdm).
`lgs4_collect.py` applies the rules below. All four scripts are committed with this file.

## Checks made before freezing (no supernova sample fitted; `lgs4_prefreeze_checks.out`)
- CMB summary alone, constant dark energy: H0 = 67.222 ± 0.383 km/s/Mpc; the paper quotes 67.19 ± 0.38 for the chains
  the summary was built from.
- BAO + BBN, constant dark energy: Ω_m = 0.2971 ± 0.0085; DESI DR2 gives 0.2975 ± 0.0086.
- Against CAMB at one point, at CAMB's own redshifts: r* and r_drag agree to 1.4e-5, θ* to 8e-5 (0.36 of the summary's
  σ). The paper's decoupling redshift follows CLASS's definition, 1.1 below CAMB's; the summary is defined with it.
- Supernova bookkeeping: 1,820 / 1,623 / 1,623 rows; the χ² of the full sample at one fixed, arbitrary point equals the
  official likelihood's formula to 1e-8. No minimisation over any supernova sample has been run.

## Gates
- **G0:** every run at the frozen step count, max Gelman-Rubin R − 1 < 0.01, Laplace covariance positive definite.
- **H1 (harness):** the `full` CPL posterior must reproduce the paper's "DES + legacy" row: each of Ω_m 0.314 ± 0.005,
  w0, wa, H0 67.37 ± 0.55 within 0.5 of the paper's sd in the mean and within 0.75–1.33 in the sd. The tolerance is for
  an independent code on the same data: Monte Carlo noise is a few hundredths of a sd, the paper prints three
  decimals, and the early-universe treatment differs at the 0.1σ level (first check above).
- If G0 or H1 fails, every label below is NOT EVALUABLE AS FROZEN and the numbers are reported without weight.

## Rules
- **P1, does the centre move?** d = (w0, wa)_des_only − (w0, wa)_full from the chain means. The samples are nested, so
  the covariance of d is C_des_only − C_full (the 2 × 2 blocks), not the sum. T = dᵀ (C_des_only − C_full)⁻¹ d,
  p = exp(−T/2). CONSISTENT if p ≥ 0.05; SHIFTED if p < 0.05. The same with best fits and Laplace covariances; if the
  two disagree the label is UNSTABLE; if either difference matrix is not positive definite, NOT EVALUABLE.
- **P2, distance from constant dark energy.** Δχ² = χ²_min(lcdm) − χ²_min(cpl) per sample, as a two-sided Gaussian σ
  for two parameters (the paper's convention). Label for des_only: BELOW 2 SIGMA / 2 TO 3 SIGMA / ABOVE 3 SIGMA.
  Context, no label: the Δχ² expected for des_only under each reading. Under A, a non-central χ² (2 dof) with the
  full-sample non-centrality (Δχ²_full − 2) scaled by the share of information des_only keeps along the full-sample
  offset; under B, a central χ² (2 dof). Both tail probabilities are printed.
- **P3, offset or w(z)?** On the full sample, G = χ²_min(lcdm_dm) − χ²_min(cpl): constant dark energy with a legacy
  offset (reading B) against CPL with none (reading A). CPL has one more parameter, which costs 2 (AIC) to
  ln N = 7.5 (BIC, N = 1,852 data points). W(Z) FITS BETTER THAN AN OFFSET if G ≥ ln N + 4 (wins under both by 4);
  AN OFFSET FITS BETTER THAN W(Z) if G ≤ −2 (wins under both by 4); otherwise CANNOT TELL. Laplace evidence ratios
  with the paper's priors are printed as context and compared with the paper's ln B; they carry no label, because
  they move with the prior widths.
- **P4, size control.** CONTROL QUIET if `rand197` keeps the P2 significance of `full` to within 0.5σ (not lower by
  more); else CONTROL ALSO DROPS.
- **P5, how much offset each model wants.** σ = sqrt of the χ² gained by freeing the offset, in constant dark energy
  and in CPL: OFFSET DETECTED (≥ 3) / OFFSET HINTED (2 to 3) / NO OFFSET (< 2). The offset and its sd are reported.

## Reading (one line, fixed now)
- NOT EVALUABLE AS FROZEN if a gate fails.
- NOT TIED TO THE LEGACY SET if P4 is CONTROL ALSO DROPS.
- READS AS A SIGNAL SEEN WITH LESS DATA if P1 is CONSISTENT and P3 is W(Z) FITS BETTER THAN AN OFFSET.
- READS AS LEGACY-MADE if P3 is AN OFFSET FITS BETTER THAN W(Z) and P2 (des_only) is BELOW 2 SIGMA.
- THE SPLIT CANNOT TELL otherwise.

## Guess, written before the run
From the paper's printed rows alone: P1 CONSISTENT (about 0.5σ per axis); P2 des_only 2 TO 3 SIGMA; P3 CANNOT TELL
(G near 6 to 7, between the two penalties); P4 CONTROL QUIET; P5 constant dark energy OFFSET HINTED, CPL NO OFFSET;
reading THE SPLIT CANNOT TELL. The paper's rows are public, so this lane is not blind to its likely outcome; what it
adds is the two-dimensional shift statistic, the offset-against-w(z) comparison and the size control, none of which
the paper prints.

## What the result may and may not say
A re-read. It can say whether, in this fit and this sample, dropping the legacy supernovae changes where the fit sits
or only how well it is pinned, and whether a magnitude offset or w(z) describes the full sample better. It cannot say
which supernova sample is right, whether dark energy evolves, or anything about the framework. LGS3 found no such
effect in Pantheon+ or Union3; nothing here extends to them.

kappa = 1/2 FITTED; not theory closed.
