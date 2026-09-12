# DF2 with fixed global a0: nonlinear action test

Date: 2026-09-12. **Status: OPEN, conditional static-sector calculation.**
No full relativistic theory, empirical fit, or Lean certificate is claimed.

## Outcome

The exponential AQUAL action was varied and its full axisymmetric nonlinear
field equation solved for DF2's published stellar profile, with a uniform
host field and the global input a0 unchanged. The host distance changes the
answer; a putative local dark-energy density was not used.

| Conditional central-distance scenario | DF2 / host distance (Mpc) | Physical separation (kpc) | g_ext/a0 | Global LOS RMS (km/s) |
|---|---:|---:|---:|---:|
| JWST DF2, SBF host | 17.6 / 21.3 | 3700.799 | 0.003300 | 18.290 |
| JWST DF2, alternative PNLF host | 17.6 / 17.9 | 308.168 | 0.039992 | 17.871 |
| Close-association control | 17.6 / 17.6 | 69.887 | 0.182624 | 14.925 |
| Legacy equal-distance control | 20 / 20 | 79.417 | 0.159821 | 16.662 |

These are computed equilibrium global **total second moments**, including any
streaming contribution, not directly the observed masked aperture dispersion.
The two equal-distance rows are controls, not distance determinations.
The assumed host baryonic point mass is 1e11 solar masses; it is not a measured
mass posterior. The other environmental sources, tides and formation history
are absent. No statistical exclusion or acceptable-fit claim follows.

The new distance source reports DF2 at 17.6 ± 0.6 Mpc and NGC 1052 at
21.3 ± 1.7 Mpc, while also discussing a closer PNLF host estimate.
Central values therefore do not justify automatically treating the projected
separation as the physical separation. They also do not supply the joint
distance posterior needed to rule out association.
[Tang et al., arXiv:2606.05144v2](https://arxiv.org/html/2606.05144v2).

## What was actually derived

The stipulated nonrelativistic action is

\[
 S_A=-\int dt\,d^3x\left[
 \frac{a_0^2}{8\pi G}{\cal G}(|\nabla\Phi|/a_0)+\rho_b\Phi\right],
 \quad {\cal G}(y)=y^2+2(1+y)e^{-y}-2 .
\]

Fixed-boundary variation gives

\[
 \delta S_A=\int dt\,d^3x
 \left[\frac{\nabla\cdot(\mu\nabla\Phi)}{4\pi G}-\rho_b\right]\delta\Phi,
 \qquad \mu(y)=1-e^{-y}.
\]

Thus the external field enters the **total** potential gradient; in coordinates
aligned with physical external acceleration, \(\Phi=u-g_e z\). It is not an
algebraic acceleration boost pasted onto a Newtonian spherical solution.
The flux Jacobian derived from this action is

\[
 D_{ij}=\mu\delta_{ij}+y e^{-y}\hat p_i\hat p_j,\quad
 \lambda_\perp=1-e^{-y},\quad
 \lambda_\parallel=1+(y-1)e^{-y}.
\]

Both eigenvalues are positive for y>0 and tend to zero at y=0. No ellipticity
floor is inserted. This static convexity statement does not establish
relativistic stability or eliminate a propagating clock degree of freedom.

For a steady collisionless tracer with zero outer surface stress, integrating
its Jeans equation independently derives

\[
 \langle v_{\rm los}^2\rangle_{\rm global}
 =\sin^2i\,\frac{\int\rho_b (R/2)u_R\,d^3x}{M_*}
 +\cos^2i\,\frac{\int\rho_b z u_z\,d^3x}{M_*}.
\]

It is necessary for equilibrium, not proof that a nonnegative distribution
function realizes the assumed spherical density in a nonspherical potential.
The detailed action, EFD Green function and analytic anisotropic virial
benchmarks are in [bridge/REPORT.md](bridge/REPORT.md).

## Fixed inputs and separate aperture reference

Throughout,
\(a_0=9.3619\times10^{-11}\ {\rm m\,s^{-2}}\).
The relation \(a_0=(c/2)\sqrt{G\rho_\Lambda}\), with mass density
\(\rho_\Lambda\), remains input: its coefficient is not derived.
For a cosmological constant the same vacuum density does not switch off
inside DF2.

The source is a spherical Abel deprojection of the circularized Sérsic profile:
n=0.6, projected axis ratio 0.85, major effective radius 22.6 arcsec.
We use LV=1.1e8 solar luminosities at 20 Mpc, times adopted M/LV=2,
rather than the distinct rounded 2e8-solar-mass normalization.
At 17.6 Mpc this is Mstar=1.70368e8 solar masses and circular Re=1.777892 kpc.
This sphericalization and constant population normalization are assumptions,
not an inferred three-dimensional shape or a population likelihood.
[van Dokkum et al., arXiv:1803.10237v1](https://arxiv.org/pdf/1803.10237v1).

An independent isolated, spherical, isotropic Jeans calculation gives the
following **circular Re-aperture reference**, not an EFE aperture prediction:

| Adopted M/LV | Newtonian (km/s) | Exponential AQUAL (km/s) |
|---:|---:|---:|
| 1 | 5.322 | 16.788 |
| 2 | 7.527 | 20.076 |
| 4 | 10.645 | 24.067 |

The M/L values are sensitivity choices, not posterior weights. The corresponding
isolated global AQUAL value at M/L=2 is 18.304 km/s, close to the full PDE's
far-host result. Its finite-aperture value is higher, not a rescue produced by
using a small central aperture under these isotropic assumptions.

Published summaries give KCWI 8.4 ± 2.1 km/s and MUSE
10.8(+3.2,-4.0) km/s within its effective-radius aperture; MUSE's
full-systematics 95% upper limit is 21 km/s. These are different extractions,
not independent measurements to multiply into a joint likelihood here.
[Danieli et al.](https://arxiv.org/abs/1901.03711),
[Emsellem et al.](https://www.aanda.org/articles/aa/pdf/2019/05/aa34909-18.pdf).
The exact revised KCWI body and likelihood were not recovered; its abstract
was verified, and the older PDF has different numbers. See the explicit
version caveat and missing spatial weights in [data/SOURCES.md](data/SOURCES.md).
No unsupported sigma-level exclusion is assigned.

## Numerical verification

The fresh canonical archive is [run_001/manifest.json](run_001/manifest.json).
Its six subprocesses all exited 0:

- 8 field/geometry unit tests and 5 stellar-profile/Jeans unit tests.
- 17 existing exponential-AQUAL external-field/orbit regression tests.
- Three-grid stellar-reference calculation.
- Independent discrete-energy/Hessian audit: ten numerical checks.
- Main nonlinear study: three symbolic identities and five numerical gates.

The main study solved 13 PDE cases, and the independent audit solved five.
Fine DF2 meshes are 97 by 193, compared with 49 by 97. Changes in global LOS
RMS are at most 0.107%. Doubling the far-host and close-control domains changes
the RMS by 0.000102% and 0.000840%, respectively, with approximately preserved
central spacing. These are observed convergence differences, not rigorous
continuum error bounds. The largest fine-grid analytic benchmark moment error
is 0.197% (isolated Plummer); Newtonian and EFD controls are below 0.048%.
Every archived nonlinear solve meets the original 3e-10 relative residual target.

The Q1 cylindrical elements vary a common discrete energy. The Hessian is
differentiated, not replaced by frozen-mu iteration. The reported reaction/load
balance follows discrete partition of unity; it is not an independent test of
the physical exterior boundary. The exterior monopole boundary is approximate
and therefore explicitly domain-tested.

Two bugs were detected before archival: small-y primitive cancellation and
large external-background flux cancellation. Both have failing-test history
and arithmetic fixes; neither changed mu, a0 or the convergence tolerance.
See [bridge/NUMERICAL_REVIEW.md](bridge/NUMERICAL_REVIEW.md) and
[COMMANDS.md](COMMANDS.md). No numerical failure was relabeled an empirical PASS.

## Exact remaining obstruction and next calculation

The repository's relativistic P/W/gamma action has **not** been shown to
produce this physical exponential AQUAL action with measured G and SI a0.
The bridge audit quotes and hashes its load-bearing definitions. Solving this
new static PDE cannot establish its slip, PPN parameters, DOF count, matter
Ward identity, FLRW viability, or CMB response. It does not repair that bridge.

For the conditional static theory, the next unavoidable empirical calculation
is a collisionless equilibrium/selection model in the solved external-field
potential, projected through the actual KCWI/MUSE masks and weights, using
independent stellar-population and joint host-distance/environment constraints.
A globally averaged moment alone cannot supply that likelihood.

For the requested **same-action** theory, the next unavoidable calculation
remains the physical weak-field reduction of the frozen relativistic action,
with its cosmological branch and proper matter normalization, before identifying
its flux with exponential AQUAL. Neither task licenses reconstructing new
coefficient functions or fitting a local a0 to DF2.

## Credit, scope and provenance

Carl Zimmerman proposed using the apparently dark-matter-deficient galaxy as
a direct challenge to his global dark-energy acceleration-scale framework.
That question and the stipulated normalization motivated this bounded study.
AQUAL and its external-field effect are established MOND ideas, not discoveries
claimed here. The new repository contribution is the explicit full nonlinear
finite-source solver, current-distance scenarios and reproducible audit.

Baseline inspected: 593612171; concurrent Claude commits e35651209 and 29b58ae82
arrived during this work. They concern other cosmological-history calculations;
their titles were inspected, but they are not audited or used as evidence here.
No earlier scientific artifact was edited. Computation-audit, source checking,
independent action review and final mathematical self-review enforced the
separation between numerical success and physical theory closure.
