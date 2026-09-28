# FGF-015 finite checkpoint

**Outcome: `supports_scoped_claim`, pending orchestrator review.** A conforming
piecewise-linear variational calculation verifies the positive global
longitudinal spectrum of the actual inhomogeneous Q/R hydrostatic slab with
exactly xi=psi=0 at both walls. The scalar-flux perturbation is not set to zero.
This confirms the finite implementation of FGF-011's exact factorization;
it is not a search that discovered or excluded arbitrary physical instabilities.

The raw derivation was written before code in `DERIVATION.md`. The executable
is `slab_modes.py`. Accepted finite evidence is `numeric_001/results.json`
with its validated version-2 `manifest.json`; the full return contract is
`result.json`.

## Actual backgrounds and spectra

Both selected backgrounds have dimensionless B(0)/a=.01, initial
r=4piG cs² rho/a²=.1, and interval 0<=x a/cs²<=1. The coefficients are
the varying rho and A=b_g of the hydrostatic solution. They were reconstructed
from their ODEs and checked against the pinned samples and an independently
integrated first integral. No locally frozen density or field was substituted.

The twelve parameter cells are Q/R x eta=.01,.04 x N=64,128,256 interior
nodes. At a single fixed cs/c=sqrt(.005), these inertias equal K=2,8.
The first ten eigenvalues and 33-point samples of each mass-normalized
eigenfunction are stored for every cell. The finest-grid first three values
of Omega², with Omega=omega cs/a, are:

| Branch | K | First | Second | Third |
|---|---:|---:|---:|---:|
| Q | 2 | 9.944927904 | 39.37537758 | 88.75687144 |
| Q | 8 | 9.943868945 | 39.28990372 | 88.63572934 |
| R | 2 | 9.957283081 | 39.35716049 | 88.74412315 |
| R | 8 | 9.955945281 | 39.23045527 | 83.65250947 |

All 120 returned values are positive. Cholesky factorization of every full
mass and stiffness matrix succeeded. The smallest mass-matrix eigenvalue is
positive in every cell. Increasing eta leaves the assembled stiffness matrix
bit-for-bit unchanged and decreases each ordered eigenvalue, as expected when
only the positive scalar inertia increases. No static profile or stiffness
measurement therefore determines K, although the dynamic spectrum changes.
Ordered eigenvalues alone do not track the identity of a mixed mode across
parameters; the supplied eigenfunctions permit that subsequent comparison.

For this declared dimensionless family, both registered vacuum normalizations
are restored separately using omega=(a/cs)Omega and d=cs²/a. Rescaling a while
fixing the dimensionless background also rescales physical B and rho; these
are not fits of one observed slab. No H-dependent time evolution is included.

## Numerical accuracy and conserved quadratic energy

The eight-point positive quadrature assembly is a sum of squares and cannot
obtain positivity by canceling large signed energy terms. A separate original-
form assembly uses twelve quadrature points and the actual density gradient.
The largest scaled matrix difference is 4.115e-16. The independent original-
form Rayleigh quotients agree with the eigensolver to 3.411e-10 relatively;
the largest normwise generalized-eigenvector residual is 2.920e-10.

For the semidiscrete solution z(t), the assembled equations are

    M z_tt+H z=0,
    E_h=[z_t^T M z_t+z^T H z]/2.

Symmetry and time-independent coefficients give
dE_h/dt=z_t^T(M z_tt+H z)=0 exactly. Positive Cholesky factors and the
independently integrated modal energies check the sign and normalization of
this discrete invariant. No independent time-stepper or time-integration
error claim is made in this eigenvalue task.

The 128-to-256-node relative change is at most 0.0029992 over the first ten
values. The fine/coarse change ratio is at most 0.26013, consistent with
second-order eigenvalue refinement for this piecewise-linear discretization.
All returned sequences decrease in this run. Since the meshes have 65,129,257
elements, they are not nested; empirical monotonicity is not being used as a
nested-space theorem. The 0.30% refinement change is finite evidence, not a
certified continuum error bound.

## Discriminating controls

Removing the original density-potential cross block leaves two positive
Dirichlet sectors in every cell. Restoring it lowers the fundamental mode
but does not violate the exact positive-square theorem for the balanced slab.

The nonadmissible trial xi=1, psi=0 detects why boundaries matter. Omitting
the required endpoint term changes the original-versus-square identity by
−0.01615946217 in Q and −0.01789254477 in R. Restoring the endpoint term
reduces the residual below 3.5e-17. These are intentional failed premises,
not eigenfunctions of the Dirichlet physical problem.

A separate periodic constant-density supported/subtracted control uses the
original quadratic form with rho=1, A=.5. It reproduces the analytic
two-branch dispersion to 6.78e-15 scaled error. At k=1 and eta=.01 its
lower Omega² is −0.9622372448. Wrongly applying the hydrostatic slab square
formula to that nonhydrostatic background changes it to +0.9608144218.
The test therefore detects the precise false extension that would conflate
the two backgrounds. The actual hydrostatic slab spectra remain positive.

Finally, the lowest Dirichlet modes have clearly nonzero scalar flux at both
walls (roughly 0.24–0.27 in the stored mass-normalized units), despite zero
potential values. This checks that no extra zero-flux condition was imposed.
Fixed potential makes the perturbative boundary energy flux vanish through
psi_t=0, without requiring A psi'=0.

## Provenance and limits

The one numerical process completed successfully in 2.126426 seconds. The
runner recorded a 120-second wall limit, a 110-second CPU cap, a cooperative
one-numerical-thread limit and a 1 MiB log cap. No memory or affinity limit is
claimed. Python 3.9.6, numpy 1.26.2 and scipy 1.11.4 were used. The manifest
validates against current input and output hashes. No queue/index file was
used as a mutable numerical input. There were no failed numerical attempts;
the intentionally wrong-boundary and wrong-background controls are retained
as successful tests. All writes are inside the assigned run directory.

This is binary64 evidence about two declared finite isothermal slabs with
external wall support and positive nonzero fields. The exact FGF-011 theorem
supplies the sign over its stated function space; these calculations verify
the discretization and quantify the low spectrum. They do not settle free
boundaries, three-dimensional modes, variable scale, non-isothermal matter,
zero-field degeneracy, nonlinear collapse, cosmology, metric modes or the
main filtered-MONO framework. No empirical mode or bound on K was measured.

## Stop and next implication

The requested finite checkpoint is complete; extending this same grid is not
needed to establish the scoped sign. The substantive next step is to choose
and justify a physically relevant boundary/background class and retain its
exact energy boundary terms before applying stability or K-inference claims.
If the intended target is the operative filtered-MONO model, derive its actual
matter/field/metric perturbation energy first; this Q/R scalar slab cannot be
used as its stability certificate.
