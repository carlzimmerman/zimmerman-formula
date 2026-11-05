# Clock repair and solved-background bound: contract

Base a6c19b3845fa8b48387e9a17dc3bacd9ef4f6df7; parent derivation d02e943eef.
Owner: this chat. Work stays in this directory and the AZ40 live README.
User explicitly requests clock-caustic repair and testing the gradient bound.
Kappa=1/2 FITTED. No new action adopted, no observational result inherited.

G: Regenerate all24 AC1 radial models with their unchanged equations, domains,
BC, two mesh/tolerance settings and continuation order. Test the corrected
force-subtracted B_J, including the canonical rescaling epsilon=2*length^2.
Compute sampled extrema on3001/6001 geometric points and a conservative global
spline envelope: bound y and |d'| by extrema of each cubic interpolant, use
monotonic sinh derivatives and J(s)>=0. Report the envelope for the numerical
interpolant, not as a rigorous enclosure of the unknown exact BVP solution.
Require original profile agreement<1e-4; relative envelope agreement<1e-3
(normalize by1+absolute fine value). At epsilon=0 B_J=0 is the known limit;
for the16 nonzero-epsilon models report positive/negative/inconclusive bounds
without tuning a threshold. Check physical domain, switch and BC/residuals.
Preserve fine spline knots/coefficients. Compare regenerated summaries with
the committed AC1 results. Missing or failed solutions remain in the count.
Independent algebra check: recover the original local Schur curvature from
B_J+Delta|A_psi|/|A_psi|. A mutation omitting J_background must fail that
identity. A sampled bound is not an all-space certificate for an exact PDE.

C: Pursue three different clock repairs: a canonical kinetic clock, an expansion
penalty, and a hard foliation restriction/identification. Read nearest prior
failures first (X14, CT6, AC2). Derive rather than assume their effect on the
geodesic zero-current branch. For any surviving candidate check kinetic sign,
characteristic/constraint changes and timelike-gradient preservation in an
explicit solvable regime. Distinguish removal of one known counterexample
from global regularity and from preserving the old action/observables.
No inherited new-scale, no-extra-field or observational pass is assumed.

First canonical discriminator: in1+1 Minkowski, evolve the same smooth unit
clock initial data under the canonical wave equation; derive null derivative
bounds and compare with the geodesic characteristic crossing. Then test whether
that result survives cosmological dilution and the P.A coupling. An isolated
wave equation result is not a proof for the coupled action.
Expansion discriminator: derive the actual covariant variation of an expansion
penalty and its constrained quadratic spectrum; do not infer nonlinear no-fold
from a positive linear sound speed. Hard restriction: check whether it merely
selects initial data, changes constraints, or reproduces an existing obstruction.

Computation: one BLAS thread; bounded runs, at most120seconds for the24 BVPs,
60seconds for symbolic checks. Record failed runs, hashes, actual versions and
source mappings. No large simulation or heavy queue submission is authorized
by this contract. Novel analytic work may continue after an unsuccessful test;
new numerical regimes need their own pre-execution specification.
