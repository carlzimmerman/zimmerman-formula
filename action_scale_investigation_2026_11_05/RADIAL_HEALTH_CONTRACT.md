# Radial short-wave test on the finite-shell branch

Continuation after evidence/shell converged on all four preselected cases.
No change to its boundaries or parameters. Freeze before graded calculation.
Scope: spherical perturbations in unitary phi=q t gauge, areal radial gauge,
about a static V=constant exterior solution, no matter perturbations. This is
not a full angular, finite-frequency, causal or nonlinear health theorem.

Metric ADM form: ds^2=-N^2dt^2+B^2(dr+beta dt)^2+r^2dOmega^2.
The clock and polarization sectors have no shift dependence after spatial
projection; only GR supplies the shift terms. Derive the two extrinsic
curvature eigenvalues and integrate the beta beta' term by parts. Eliminate
the shift to obtain the radial metric perturbation kinetic coefficient;
do not assume its sign before evaluating the actual background equations.

Derive the lapse-lapse Hessian of the radial potential NB r^2(X-V-W),
retaining a0(N). Determine the principal frozen radial spatial operator
from the exact Lr in STATIC_RESULT.md: y=(delta B,delta N,delta p),
H(k)=L_yy+i k(L_y,yprime-L_yprime,y)+k^2 L_yprime,yprime.
Eliminate delta p and then delta N at large k. The omitted derivatives of
background coefficients must be checked for whether they alter the leading
effective lapse coefficient; if they do, no physical speed claim is allowed.

Obtain the leading coordinate omega^2/k^2 and convert to the local radial
speed squared with B^2/N^2. Independently derive the same high-k coefficient
from a generic Hermitian three-field matrix retaining all finite lower-order
entries as symbols. This is an asymptotic characteristic calculation, not
an approximation for modes comparable to a background scale or EFT cutoff.

Evaluate signs of the kinetic coefficient, effective lapse coefficient and
local radial speed on the four saved fine profiles, 201 points each. Record
min/max and any nonpositive or superluminal values; no values tuned. Sign
claims require >=1e-12 margins for positive dimensionless denominator and
0<speed^2<=1; near-zero or uncertain entries get NO VERDICT. No accuracy or
physical scope upgrade beyond the underlying float64 shell solve.

Mutation drops the a0(N) derivative in the lapse Hessian; its symbolic
comparison with differentiation of the actual action must fail. No mutation
of physical data. Separate output, nonzero exit.

Non-claims: no selected b, no ghost/gradient theorem for arbitrary angular
modes, no finite-frequency spectrum, no strong-coupling scale, no global
causality, no actual galaxy, no proof that all backgrounds have this sign.
