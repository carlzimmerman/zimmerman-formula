# Independent operator review of KT33

Reviewer: sibling agent `filter_review`, 2026-11-04. This is a focused
implementation and computation audit, not an independent rerun of the full
observational scan. The reviewed claim is the fixed-width completion

    Phi[rho] = N rho + S* Phi_ph[S rho],

with the simple nu law, the frozen KT25 parameters and ordinary matter
coupling. The width is held fixed during variations. No adaptive-width action,
universal system-mass rule, ephemeris fit or wider-galaxy claim is verified.

## Discrete variation and Gaussian adjoint

The inherited finite-volume Laplacian L is self-adjoint in the inner product
`<x,y>_W = x^T W y`, with W equal to the cell volumes. Its normal-gradient and
divergence operators are weighted adjoints, including the outer Dirichlet
face. The inherited nonlinear UX5 QUMOND routine, however, evaluates nu using
both normal and interpolated tangential gradients while retaining only the
normal flux divergence. The missing tangential-transpose variation means
that this nonlinear routine is not an exact discrete energy gradient.

An independent 48-by-32 full-axisymmetric test used an asymmetric positive
background and two nonspherical, zero-mass perturbations. Analytic Jacobian
cross responses were 2.577452676856945 and 2.5784046981497912 for the inherited
routine: relative reciprocity defect 3.6922880785e-4. On the identical grid,
the cell-energy construction gave 2.5833409815070585 and
2.5833409815070567, a relative defect of 6.88e-16. This is a finite countercheck
of the inherited discretization, not an error estimate for its observations.

The new implementation uses `G = (Crr,Cth)`, `N = 4*pi*L^-1`, and

    U_ph[S rho] = -(1/(4*pi)) sum_i W_i Psi(|G N S rho|_i),
    Psi'(q) = [nu(q)-1] q.

Its derivative is exactly the implemented

    Phi_ph = -L^-1 W^-1 G^T W ([nu-1] G N S rho),
    Phi = N rho + S* Phi_ph.

The 4*pi factors cancel in the chain rule. This also makes the nu=1 phantom
contribution exactly zero. At S=I the code gives this energy discretization
of ordinary QUMOND. It is not algebraically identical to the inherited
nonvariational face routine at finite resolution; both plain and source-only
controls are therefore retained.

The Gaussian implementation's radial factor, spherical-Bessel coefficient,
even-Legendre normalization on the half sphere and cell-volume weights are
consistent. With H the weighted-self-adjoint harmonic approximation and
`d=H1`, the code uses

    S = H diag(1/d),       S* = diag(1/d) H.

Consequently source mass and the outer constant-potential mode are preserved:
`1^T W S = 1^T W` and `S*1=1`. Reapplying S as the outer operator would be
incorrect after column normalization; the implementation uses S* explicitly.
The finite harmonic truncation, orthonormalized angular basis, normalization
and identity exterior are numerical approximations to the declared Gaussian,
not additional physical parameters or a new fitted width.

A separate analytic nonspherical check used
`f=r^2 P_2(cos(theta)) exp(-r^2/(2a^2))`. For `b=a^2/(a^2+sigma^2)`, its
Gaussian convolution is

    b^(7/2) r^2 P_2(cos(theta)) exp(-r^2/(2(a^2+sigma^2))).

At a=6 kpc and sigma=5 kpc, the maximum interior error relative to the exact
peak was 0.0022459852 on the base grid and 0.0005495749 on the doubled grid.
The factor 4.087 reduction supports the expected angular quadrature
convergence. This test is more informative about anisotropic sources than
the almost exact spherical-Gaussian control.

## Boundary, gauge and finite-resolution qualifications

Because `G1=0`, the finite cell-energy phantom source has zero weighted total.
It includes a compensating boundary contribution and should not be described
as the exact isolated continuum source on a finite domain. Its interior
observables require domain convergence. The final check doubles the outer
domain by appending shells while preserving every existing node. For the
best corrected candidate on each footing, the resulting change in cO is
below 5.4e-10; changes in circular speed are below 2.6e-11 km/s. This isolates
the boundary effect from the slight regridding in the earlier outer2 test.

The preliminary `mw/refinement_run` correctly records a failed validation.
Its lmax=24 representation has small negative density tails, with integrated
negative mass up to 6.45e-5 for the selected cases, and its unscaled gauge
tolerance is too strict at the smallest radial cells. These failures were
not erased or handled by clipping the density. Clipping would destroy the
linear filter and its stated adjoint.

The accepted `mw/final_checks_run` uses a doubled spatial grid and lmax=48,
with selected tripled-grid/lmax=64 controls. Its recorded `passed` is true.
Across its checked best and width-extreme cases, integrated negative mass is
at most 3.17e-6 at the production resolution. For the best cases it drops
below 2.75e-8 on the finer grid. These are measured truncation errors, not a
proof that the finite operator preserves positivity on every possible input.

Adding the arbitrary potential constant 12345 changes gradients at observed
radii 4--30 kpc by less than 9.7e-10 in solver units. The larger errors near
r=0.005 kpc are compared with the practical roundoff scale
`128*eps*(max(abs(Phi_ph))+12345)` multiplied by each gradient row's absolute
coefficient sum. All ratios to that scale are below 0.166. This is an
epsilon-scaled numerical tolerance, not a proved operation-count error bound.
The direct invariant `S*1=1` is satisfied to about 8.5e-15. Together these
checks support gauge stability at the measured precision.

The analytic reciprocal-pair errors in the final selected checks are at
most 3.63e-13 relative. The half-sphere Milky Way subspace imposes reflection
symmetry, so a zero total force there would not independently validate
momentum conservation for an asymmetric isolated source. The separate
periodic spectral realization tests a nonspherical multi-mode density in a
fixed external field: source-only internal force is about 3.44287e-4 while
corrected force is below 3e-14 at resolutions 16, 24, 32 and 48. The density
itself is inversion-even; the external field breaks that system symmetry.
Its two-mode response also
reproduces the independent analytic audit. These periodic results support
the intended continuum map and must not be conflated with a general
isolated-grid momentum certificate.

## Cassini kernel and the inherited origin term

The outer Gaussian changes the potential Green kernel from 1/r to
`f(r)=erf(r/(sqrt(2)*sigma))/r`. The reviewed trace-free Hessian factor is

    T(r) = r^3 (f''-f'/r)/3 = P_regularized_gamma(5/2,r^2/(2*sigma^2)).

The flux calculation must include both the T-weighted historical integrand
and its additional T' term. The independent analytic phantom-density
integral and the finite-annulus surface correction in `cassini_v2.py` have
the correct factors and signs. The stable gamma expressions and angular
reference subtractions do not change the defined operator.

The inherited source-only integral has a real boundary defect after the
source is smoothed. With source width s>0, positive external field eta and
`c=sqrt(2/pi)/(3*s^3)`, the inner surface limit is

    b_inner = (4/15) c eta nu'(eta)
            = -2c/[15 eta sqrt(1/4+1/eta)].

Thus, in the infinite outer-domain limit, the physical source-only
trace-free Hessian is `q_hessian=q_flux+b_inner`. The term is not zero as the
excluded inner sphere shrinks. It equals -0.14159222566552934 on canonical
and -0.16106180007580947 on alt. This derivation was independently checked
before reviewing its implementation. For positive outer Gaussian width,
`T=O(r^5)` removes this inner term; the new reciprocal predictions are
unaffected by the inherited omission.

The frozen `cassini/run_002` distinguishes the reproduced archival flux
control from the physical source-only Hessian. This separation is necessary.
Its reciprocal magnitude is 1.09159062581 times the inherited ceiling on
canonical and 1.61965965793 on alt. The finest reciprocal flux and density
routes differ by at most 1.75e-15 in dimensionless q, and numerical refinement
changes the result by less than 7.4e-14 relatively. The finite convergence
evidence supports rejection of this fixed candidate under the stated
quadrupole criterion. It is not interval arithmetic or a full ephemeris fit.
Signed Q2 remains explicitly a repository convention; the graded quantity
is its magnitude. The possible isotropic Hessian component is not graded.

## Observational scope and disposition

The reviewed base-grid scan covers all 1375 originally allowed prior cells
on each footing. It reports no corrected four-cut passes on either footing.
The nine saved canonical cells and thirty stored alternate cells also lose
their four-cut passes. No original matter parameters or widths were refitted.
The physical half-space factor is included in the new full gas-mass check;
the inherited half-mass comparison remains visible rather than being waived.

The closest corrected alternate-footing candidate has cO=76.84818446 on the
accepted doubled-grid check and 77.01247870 on the tripled-grid check, versus
the unchanged cut 59.89250005. The canonical best has cO=183.07692364 and
183.41502333, respectively. The tested discretization changes are much
smaller than these rejection margins. The integration report owns the final
production-grid scan counts and manifest validation; this reviewer did not
repeat that scan independently.

Disposition: **the discrete variational construction and the reviewed finite
checks are consistent, conditional on the recorded numerical tolerances;
the fixed candidate fails the Cassini criterion and the reviewed Milky Way
candidate comparisons.** This is a failure of the specified fixed-width
completion at the tested premises. It does not rule out every nonlocal
theory or justify changing the filter after seeing the failures.

## Independent evidence and review provenance

The independent scripts and observed outputs are copied without rerunning
from `/private/tmp/kt33_review` to
`validation/independent_review/{legacy_reciprocity,gaussian_l2}.{py,json}`.
`validation/independent_review/provenance.json` records original paths,
commands, exit codes, hashes and the copy mapping. The scripts record the
direct source hashes actually observed before and after each calculation,
versions, domain and measured runtime. They are bounded review evidence,
not v2 runner manifests or independent astrophysical reruns. P4 source and
the MW source observed during the respective checks were unchanged within
those executions. Original repository files were not edited by this review.

Code and recorded outputs reviewed: KT25 and UX5/P4 reference operators;
`mw/mw_reciprocal.py`, `verify_refinement.py`, `verify_final.py`; selected
pilot, saved, base-grid, preliminary-refinement and final-check results;
the Cassini v1/v2 formulas, tests and final derivation; and the periodic
validation implementation and tests. No external source authentication was
needed for these internal algebra and implementation checks.

Final mathematical proofreading covered this new review only: notation,
sign conventions, display integration and evidence references. No original
mathematical file was corrected and no unresolved mathematical-token issue
was identified in this review's displayed formulas.
