# Finite-interval MOND predictions: analysis contract

Approved by the user on 2026-09-04. Written before this study's empirical
outputs. This is a frozen exploratory analysis, not a preregistered test on
previously unseen data: SPARC has been extensively used in this repository.

## Scope and two predictions

For the algebraic, isolated rotation-law branch, write baryonic acceleration
as b and physical dynamical acceleration as g. The primary law is
b = g[1-exp(-g/a0)], with a0=9.36e-11 m/s^2 fixed, not fitted here. The
a0-Lambda identification remains an input, not an action derivation.

1. Finite response: for b_hi>b_lo, sqrt(b_hi/b_lo)<g_hi/g_lo<b_hi/b_lo.
   Also test the exact predicted log ratio, not just the inequality.
2. Finite curvature: for b0<b1<b2, define
   t=ln(b1/b0)/ln(b2/b0) and
   J=log10(g1)-(1-t)log10(g0)-t log10(g2). Predict J<0 and test its exact value.

These predictions require the slope and convexity properties derived in
DERIVATION.md. They are NOT universal consequences of the MOND endpoints.
RAR and simple-mu rivals share them; exact amplitudes can differ. Newtonian
and pure deep-MOND power laws predict J=0. These are formal consequences,
not automatically new physical laws. No relativistic closure is claimed.
An algebraic mapping applied to disk radial forces is an approximation, not
an exact non-spherical AQUAL/QUMOND solution.

## Input and selection, fixed before outcomes

- Existing original SPARC master table and individual eight-column rotmod
  files. Preserve negative signed gas contributions when computing b.
- Primary: catalog Q<=2, inclination>=30 degrees, finite positive measured
  radius and velocity, nonnegative velocity errors, R_disk>0, R>=R_disk,
  positive b, at least six eligible points.
- One broad triple per galaxy, selected using baryonic acceleration only:
  min/max log b, and the remaining point nearest their logarithmic midpoint.
  Require endpoint span >=0.5 dex and midpoint fraction 0.25<=t<=0.75.
- No selection on residuals, observed curvature, or agreement with a kernel.
- Primary mass-to-light ratios: disk .5, bulge .7. Sensitivity variants are
  fixed in advance: disk .3/.8 (bulge=1.4 disk), Q=1 and inclination>=45,
  R>=.5 R_disk, R>=2 R_disk, gas fraction>=.8 at all three selected points,
  and the alternative a0=1.13e-10. List all, without choosing the winner.
- The same three physical points provide the paired observables. Their
  covariance is calculated from the common velocity measurements. No
  pseudo-independent adjacent pairs or bins.

## Statistical contract

- Fixed predictions: mu_exp, nu_rar, simple mu, Newtonian, pure deep MOND.
- Equal-galaxy means, RMS residuals, and paired residual-squared differences.
- Deterministic whole-galaxy bootstrap, 1999 draws, seed 2026090401;
  percentile intervals are descriptive resampling intervals, not Gaussian
  significances or full theory rejection probabilities.
- Conditional measurement-error diagnostics use catalog velocity errors,
  with the log transform explicitly described. Missing inter-ring and
  baryonic covariance prevent a complete likelihood certificate.
- Noise-only synthetic recovery, coherent distance/inclination rescaling,
  additive common-mode covariance cancellation, reversal/curvature mutants,
  and velocity-permutation controls must be run. A control cannot be relabeled
  as empirical support.
- A deterministic per-galaxy label split supplies a replication diagnostic;
  neither part is described as blind or independent of prior SPARC use.

## Reproducibility and outcomes

Python float64/SymPy exact algebra; no network needed to rerun data analysis.
Record starting/ending commits, dirty state, input hashes, software versions,
seed, full sample exclusions, all selected rows and predictions, commands,
exit statuses and runtime in machine-readable output and a Mathbox manifest.
Resource cap: each analysis subprocess 180 seconds; timeouts mean uncomputed,
not refuted. All created executable scripts are run, and relevant existing
kernel regression tests are run afterward.

Code tests passing means implementation checks passed. Scientific outcomes
may be compatible, tension, underpowered, or inconclusive. A new law requires
independent observational support and a much broader novelty check. If that
threshold is not reached, say so and retain the negative results.
