# Self-audit, 2026-10-24

Verdict: conditional effective-model feasibility established on the declared
toy inputs; the full physical explanation remains incomplete. This is a
self-review, not independent review.

The completed manifests for run_angular64, run_angular128, run_angular256 and
run_diagnostics pass the computation-audit manifest validator; stderr is
empty. Manifest validity certifies the evidence record, not physical truth.

Analytic checks: completing the auxiliary square gives C S² exactly;
qT+qF=1 with both nonnegative; endpoint first variations vanish; enclosed
mass is integrated before calculating the field; the endpoint Hessian
includes the spatial stiffness; a positive Rayleigh metric gives decreasing
energy with positive receiver heating. Uniform F is a global minimum,
which rules out spontaneous formation of T under this fixed-background
dissipation. A uniform path is only an upper bound on an escape barrier.

Numerical checks: finite-difference gradient relative error 1.45e-5 against
the predeclared 2e-5 threshold; Hessian error 5.25e-9; curvature error
2.65e-10; initial enclosed-mass error 4.45e-16. Auxiliary elimination error
2.78e-17 over 2665 points. Boost and coordinate-rotation checks return zero
within the implemented precision. Resolution changes and energy balance
are reported separately from these derivative checks in README.md.

Model selection was exploratory. beta=20 and ell=30 kpc are post-selection
parameters. The nine-point neighborhood is a sensitivity check, not held-out
validation. Mean vorticity is a physical input but its chosen weighting is
an ansatz. No object names select the equations; reporting branches flag
unstable endpoints and do not change their dynamics.

Rejected or superseded evidence: polynomial phase maps could leave their
admissible interval; bounded angular replacement changes the potential and
is explicitly a new model. A midpoint enclosed-mass approximation violated
the field domain and was replaced with exact within-cell fractions. Initial
derivative subtraction suffered cancellation, diagnosed by a step study.
An earlier stiff local-drag run was interrupted; it is not a completed run.
Gradient damping is an extra physical dissipation assumption, not presented
as merely a numerical fix. These records are retained.

Physical gaps are consequential: frozen positions remove live gravitational
rearrangement; the spherical Jeans construction does not establish a 3D
distribution function; the global receiver does not supply a microscopic
heat carrier. No thermal lifetime, cosmological preparation, observational
RAR scatter, lensing fit or excess bound mass follows from these tests.
The rotating cluster endpoint and equal counterrotating streams expose
limits that must survive into future comparisons rather than be relabeled.
