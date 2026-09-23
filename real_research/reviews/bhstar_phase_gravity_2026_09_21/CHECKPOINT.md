# JWST / BH* missed-law search

Checkpoint: BHSTAR-PHASE-GRAVITY-2026-09-21-A.
Base commit: 44f1694720574d9f5a2d46ce6b5e1d215d142627.
The worktree already contains unrelated modifications and untracked research.
Write scope: this directory only. No previous result is silently overwritten.

User target: inspect the recent JWST research for a missed, Kepler-grade result.
Interpretation: a simple, independently falsifiable relation, with a derivation,
explicit physical premises, a repository-overlap check and a primary-source check.
A numerical coincidence or an algebraic round trip does not qualify as detection.

Routes actually investigated:

1. Wind quarter-power scaling. Read Waves R/T/U. Its normalization and population
   exponent depend on the wind factor and on the luminosity-to-mass ratio. This
   is already in the repo and supplies no new independent law. Retired.
2. Exterior absorption geometry. Eliminating the central mass gives a density
   ceiling for a transition outside a spherical photosphere. Survives as a
   conditional consistency test; cannot be called a measured exclusion without
   establishing which continuum/line region is covered and true versus net gravity.
3. Time-dependent photospheric momentum balance. The net-gravity caveat in the
   primary paper is the missing term in Wave U. Derive a constant-mass law,
   an absolute-radius/mass inversion from relative photometry, and an integral
   implementation that avoids differentiating noisy measurements. This is the
   leading result. Stellar photometric-hydrodynamic precedent is explicitly credited.

The earlier external-field global-existence investigation was redirected by the
user before a proof package was completed. It is not claimed as a result here.

Required evidence: derive the atmosphere-model mapping; test recovery, frame
conventions, identifiability and deliberate violations; distinguish forecasts
from observations; preserve source and scope limitations. No new fundamental
force law or observational confirmation is promised.

Completed checkpoint A: the conditional phase-gravity relation, finite-window
integral inversion, cycle/harmonic tests, sinusoidal amplitude bound and exterior
density ceiling are in PROOF.md. The certified run passed 153 checks, with 18
inverse problems at three resolutions and explicit counterexamples. Its manifest
validated against the current input and result hashes. REVIEW.md is self-review.

Research standing: substantive new-to-this-campaign test and inference method,
with established stellar-method precedent. A Kepler-grade empirical discovery
has not been established. The unresolved physical gate is a material photosphere
with a valid dynamic-to-static atmosphere mapping; the unresolved observational
gate is a joint time sequence of flux, temperature and fitted gravity. No process
is left running. No commit or publication was made.
