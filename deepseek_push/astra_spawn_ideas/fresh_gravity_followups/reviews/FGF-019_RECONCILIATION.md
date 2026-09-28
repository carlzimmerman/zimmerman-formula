# FGF-019: finite pressure non-identification accepted in scope

Worker result SHA256:
`21598c9e1d95398588efb3e01b07b4d0abb6bae1176d8ecd4fc954a07a73dfb4`.
Required result fields, every input/output hash and the numeric_001 manifest
were checked. Coordinator read DERIVATION.md and project.py, reconstructed
the radial-segment projection primitives, and independently checked the
returned matrix using a full QR null basis and a slope computed directly
from pressure nodes. That bounded check is recorded in
`campaign_fresh_gravity_astra/stage_06/finite_operator_audit/run_001/`.

The returned 12x16 matrix has twelve independent measured rows. Its gradient
target has relative null-space component 0.009480543014609584. Positive,
strictly decreasing synthetic pressure profiles produce equal model bins to
relative 1.13e-16 but gradients -3.696567230865879e-6 and
-3.673290373386075e-6 in the declared normalized coordinates. The 0.631677%
exhibited width establishes non-uniqueness in that finite admissible family.
It is not a sharp width or evidence of a discrepancy-sized pressure repair.
Fixing outer amplitudes and the map offset restores a square invertible
model; applying its estimator to the full model fails the independent control.

The source code's full-annulus reductions report zero mask coverage for A644
and full coverage for ZW1215 through five target radii, in this actual patch
and coordinate convention. This extends the earlier center-only inventory.
The coordinator inspected that code, but did not independently reread and
reproject the full FITS map; do not label this an independent data reduction.

The operator uses a stated fiducial angular distance, spherical piecewise-linear
pressure, twelve-bin compression, finite outer support, tangent-plane FFT
beam approximation and declared harmonic cutoff. No convergence test of
those choices, real-data pressure fit, authenticated complete response or
joint ACT/Planck/X-COP covariance was supplied. The constant nuisance is a
map offset after convolution, not a finite-patch physical constant pressure.
The reported pair does not establish a null direction of every original
map pixel or of a simultaneous thermal/X-ray model.

No force was evaluated; no Q/R/M law or a0 history was silently substituted.
All later discrepancy tests must use the specified density/composition and
the actual MOND branch. Finite identifiability is not a physical metric or
photon-coupling derivation. The independently audited PF1 continuum theorem
is distinct and requires its own hypotheses before application to this map.

Release one changed-premise child: sharp pressure-gradient extrema under the
finite positivity/monotonicity constraints, with verified primal/dual bounds.
Begin with the saved synthetic vector; real-map residual requirements must
remain deterministic until independent response/covariance is authenticated.
