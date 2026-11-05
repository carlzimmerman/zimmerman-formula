# Direct force on stars from the illustrative eddy field

User instruction: work out how eddies pull on stars and test rotation curves
and the coefficient without inserting it. Base:a5b87ecec0. This is new
authorized work after the previous blocked goal; no earlier no-progress
count is carried into it. Only this investigation's directory is writable.

Use the explicit canonical complex-field action in FLOW_POSTULATE_TRANSLATION.md,
minimally coupled to baryons. Compute the leading weak gravitational field
from its full stress tensor, not mass density alone. Natural units c=hbar=1.
Subtract the homogeneous vacuum background when computing the local vortex
perturbation. Retain V0 as independent, and identify the local regime below
the cosmological curvature radius. No MOND coupling is appended.

First configuration: straight static global vortex theta=n phi, f=f(r),
U=lambda(f^2-v0^2)^2/4. Derive rho and all principal pressures, active
source rho+sum p_i, radial potential and circular-orbit contribution.
Use the profile equation to obtain a radial virial identity and determine
the large-radius coefficient including its sign. The straight configuration
is a local cylindrical diagnostic, not a finite spherical galaxy.

Numerical check: n=1, x=sqrt(lambda)v0 r, F=f/v0. Solve
F''+F'/x-F/x^2-F(F^2-1)=0 on[1e-4,R], R=20,40,80. Impose the regular
core Robin condition F'=F/x and outer F(R)=1-1/(2R^2).
For each R use400 and800 logarithmically spaced initial nodes, tolerances
1e-8 and1e-9, max20000 nodes. Require successful solves, agreement of
profiles below1e-5 absolute, finite-domain virial relative residual below
1e-6, and the far-field integral plus leading tail within1e-4 of its
analytic limit. Sample0<=F<=1 with tolerance1e-6; do not infer full
nonlinear stability from these profiles. Bound runs to60 seconds,1 thread.

Second configuration, analytic: theta=-omega t+n phi. Compute the active
source relative to the uniform finite-charge background at the same omega.
Do not equate phase velocity with star velocity or omit the limitations of
the stationary/gravitomagnetic approximation. This tests an actual phase
current, unlike the static defect.

Also give the independent Newtonian spherical density benchmark required
for a positive flat rotation curve. It is a comparison condition, not a
derived eddy density profile. No baryonic mass, empirical acceleration,
vacuum density or target numerical coefficient is supplied to the script.

Negative control: replacing the full stress source by energy density alone
must fail the stress identity and pure-gradient cancellation checks.
Record exact symbolic identities and numerical profiles with separate
runner manifests. Interpret both the successful and mutated runs explicitly.
Neither a string calculation nor a chosen r^-2 density profile is a proof
of a complete galaxy model or the Zimmerman coefficient.
