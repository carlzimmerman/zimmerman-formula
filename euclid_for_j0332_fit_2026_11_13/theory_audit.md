# FOR J0332 theory and field-equation audit

## Scope that can currently be fitted honestly

A smooth, isolated, stationary, stellar-only, mu_K=0 **unscreened AQUAL branch**
can be fitted using the exact axisymmetric field equation and line-of-sight
deflections. A spherical algebraic force is a benchmark or approximation only.
Such a result is conditional on that branch, deprojection, and stellar-mass
prior. It does not establish a full pass or exclusion of the adopted screened
v3s action. The local record supplies a reusable axisymmetric AQUAL solver,
but does not establish a uniform screened-v3s error bound for this object.

The adopted reference is
`closure_2026_11_07/FINAL_THEORY_2026_11_07.md`; its precise action must be read
with `closure_2026_11_06/QX17_covariant_field_equations/RESULT.md` and the adopted
blend correction in `closure_2026_11_07/QX17D_blend_field_equations/RESULT.md`.
QX17 explains that the original printed action's independent P field must
enter through the **Legendre replacement** of J, not an additional copy of
the same acceleration Lagrangian. The one-page FINAL action prints both J
and P.A-W; treating both as separate copies would double-count this sector.
For implementation, use QX17's explicit Legendre action and QX17D's corrections.

## Exact unscreened static equations and lensing convention

Use physical gravitational potentials Phi and Psi, with units velocity squared:

    ds² = -(1 + 2 Phi/c²)c²dt² + (1 - 2 Psi/c²)dx².

At leading static weak-field order, Phi=Psi and

    div[mu(|grad Phi|/a0) grad Phi] + mu_K² Phi = 4 pi G rho_b
    mu(x) = x/(1+x).

The galaxy branch adopted in `EQUATIONS_IN_ORDER.md`, parameter table, sets
mu_K=0. In cylindrical axisymmetry (R,z), that branch is

    (1/R) d_R[R mu Phi_R] + d_z[mu Phi_z] = 4 pi G rho_b
    mu = sqrt(Phi_R²+Phi_z²)/(a0+sqrt(Phi_R²+Phi_z²)).

The actual acceleration vector is -grad Phi. Only with spherical symmetry
and the isolated regular flux condition does this reduce to

    gN = G M3D(<r)/r²,
    g = (gN + sqrt(gN²+4 a0 gN))/2.

Do not apply that scalar relation componentwise to an oblate Newtonian field;
the resulting vector generally has nonzero curl and is not the AQUAL solution.

For a physical lens-plane position xi and a line of sight l,

    alpha_hat(xi) = (1/c²) integral grad_perp(Phi+Psi) dl
                  = (2/c²) integral_-infinity^infinity grad_perp Phi dl
    alpha_reduced(theta) = (Dls/Ds) alpha_hat(Dl theta).

Thus the spherical check is

    alpha_hat(R) = (4R/c²) integral_0^infinity g(sqrt(R²+l²))/sqrt(R²+l²) dl.

The first integral has factor 2 for the full line of sight; the last has factor
4 because it uses only its positive half. Weak-field equality of lensing and
dynamics is the intended prescription, not a proof that all finite-PN or
screening terms vanish. QX19's C2 is a scoped blend/slip carry check.

## Screened v3s system and parameters that remain conditional

QX17 uses c=1, K=4 pi G, and the precise Legendre action

    L = [R - 2 Lambda + 2 mu_K²(Q-1)²]/(4K)
        + P.A - W(K|P|) - gamma_L F(Pi) + lambda n.P,
    W(p) = (a0²/K)[-p/a0 - ln(1-p/a0)],
    gamma_L = K Lstar²/2,
    Pi = D.P,
    F(Pi) = b² f(Pi/b), b=rho_DE.

The adopted f is zero for nonpositive argument, pure q^6 near zero, C4 and
convex through its layer, and q²/2 at q>=1. Its construction is in
`action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/ac21_i6.py`
and `form.json`. The pure-power coefficient for f is 122363904/44610575.

For SI weak-field use, define K_SI=4 pi G, P as mass/area, Pi as mass/volume,
gamma_L=K_SI Lstar²/2, and W as energy density. Then the full leaf constitutive
law, translated from QX17D/QX17B, is

    E = [1 + gamma_L F'(Pi)/c²] grad Phi + gamma_L grad F'(Pi)
    E = K_SI W'(K_SI |P|) P_hat
    K_SI P = a0 E/(a0+|E|).

At leading Newtonian order with mu_K=0, the coupled system is

    laplacian Phi = K_SI (rho_b + Pi),   Pi=div P,
    grad Phi + gamma_L grad F'(Pi) = K_SI W'(K_SI|P|) P_hat.

It is not just a prescription to turn off modifications whenever local
acceleration is large. The screening is a derivative/charge effect.
The gamma_L F'/c² term, W/c² and gamma_L F/c² source contributions, curved
leaf derivatives and the rest of the metric equations belong to the full
weak/PN or covariant treatment. The exact non-GR normal energy density in
QX17/QX17D, in their c=1 convention, is

    rho_extra = (mu_K²/(2K))(Q²-1) + W + Pi + gamma_L F(Pi).

QX17D corrects the stress term 2F h_mn to Pi F'(Pi) h_mn. Simply substituting
F' for Pi_+ without that metric correction is not the adopted action.

The full khronon equation is a current conservation law,

    nabla_m[n^m rho_Q - lambda P^m/Q] = 0,
    rho_Q = J_P/Q + mu_K²(Q-1)/K,
    J_P = nabla_m[(1 + gamma_L F'(Pi))P^m]       (c=1).

Its background charge/initial condition and nonzero mu_K are not determined
by this lens catalog. In a full model they cannot silently be replaced by an
arbitrary extra lens halo. The restricted galaxy fit explicitly sets mu_K=0.

Lstar is **not uniquely fixed**: the record says Lstar >=21.7pc canonical,
>=22.9pc alternate, a lower bound only. QX17C's numerical benchmark chooses
these lower-bound values, which is a permissible conditional fixture rather
than a measurement of Lstar. D10's floor is itself conditional on the adopted
globular-cluster stellar M/L and other astrophysical assumptions.

At Lstar=21.7pc, (Lstar/8.7kpc)²=6.22e-6 and
(Lstar/12.3kpc)²=3.11e-6. These are smooth-scale power-counting diagnostics,
**not rigorous uniform deflection-error bounds**. Their use needs bounds on
actual derivatives and the response operator, specified Lstar, and boundary
conditions. QX4's `iter3_bounds.py` merely evaluates (Lstar/R)² at the lower
bound; QX19 multiplies a related diagnostic by max f''=6.24 for its own SPARC
carry. Neither is an object-specific FOR J0332 screened solve or a uniform
statement for every Lstar above the floor.

`closure_2026_11_06/QX17C_fd_spherical_solver/RESULT.md` explicitly says its
smooth-ball test leaves screened-star granularity untested. Its isolated
screened Sun approaches the unscreened law very slowly, illustrating why
R>>Lstar alone is not a universal theorem about every source distribution.

## Reusable solvers and implementation contract

The direct reusable simple-mu solver is
`closure_2026_11_06/QX4_udg/aqual.py`:

- Conservative finite volume in x=ln(r), theta in [0,pi/2], with axial and
  equatorial symmetry. This solves the axisymmetric PDE even though it does
  not use cylindrical coordinates.
- `Grid(r_min,r_max,nr,nt,p=2)`; `grid.deposit(rho_fn,nsub=6)`;
  `solve(grid,M,a0,mu_one=False,tol=1e-8,maxit=400,omega=.7,Phi0=None)`.
- Units kpc, km/s, Msun. G=4.30091e-6 kpc (km/s)²/Msun;
  `a0_kpc(a0_SI)` converts to (km/s)²/kpc.
- M is mass **per northern-hemisphere cell**. Its sum is half the total
  galaxy mass for an equatorially symmetric model. RHS is 4 pi G M;
  do not double the per-cell masses.
- Zero radial flux at r_min, zero flux at axis and plane; constant Dirichlet
  Phi=0 at the outer sphere. A constant outer value is a gauge choice for
  mu_K=0; angularly constant boundary data still approximate isolated
  asymptotics and require an outer-radius ladder for an oblate source.
- Its solve return includes residual and iteration count; reaching maxit is
  not success. Recompute/check the final nonlinear residual before accepting.
- The finite inner boundary omits central enclosed mass unless explicitly
  corrected. For a high-n Sersic cusp, check omitted fraction, mass-deposit
  convergence and inner-radius convergence rather than assuming it is tiny.
- LOS interpolation/projection, arbitrary inclination and lens-plane imaging
  are not implemented by this module. They require their own spherical
  benchmark, interpolation/grid ladder and outer-tail control.

`closure_2026_11_06/QX8_sparc_exact_field/qx8.py` reuses this solver. Its README
reports Plummer, Kuzmin, mass-deposit, residual and grid checks. Those validate
the old uses, not automatically a new inclined-Sersic lensing implementation.
`prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py` instead uses an older
exponential nu kernel and performs extensive work on import: it is not a
drop-in solver for the adopted simple-mu law.

The screened solver in `closure_2026_11_06/QX17C_fd_spherical_solver/qx17c.py`
is one-dimensional, uses a raw quadratic positive-charge stiffness and a
smooth ball, and must be adapted for a Sersic profile/adopted blend. Its
outer boundary matches a decaying mode about the spherical law. It is useful
as a screened benchmark, not an exact oblate lens solver. D10's
`doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` solves a coupled screened
axisymmetric Plummer/external-field problem, but also predates the adopted
blend and is not an off-the-shelf arbitrary-density image-lensing solver.

An isolated deep-MOND potential grows logarithmically: it cannot satisfy
Phi(infinity)=0. Its gradient does have a well-defined isolated asymptotic
and a finite deflection. If mu_K is nonzero, adding a constant changes
mu_K² Phi, so the previous gauge freedom disappears and a physical outer
matching prescription is required. Uniform external acceleration also changes
the nonlinear field and must enter as a field boundary condition; fitting an
external lens-plane shear alone does not implement that external-field effect.

## Oblate deprojection and radius convention

Let qobs=0.8099213 be the observed minor/major axis ratio. For an oblate density
stratified on m²=R²+z²/qint², viewed at inclination i from its symmetry axis,

    qobs² = cos²(i) + qint² sin²(i),
    qint² = [qobs²-cos²(i)]/sin²(i),
    i >= arccos(qobs) ~=35.9 degrees.

Thus projected q alone does not determine a three-dimensional density. At
edge-on inclination qint=qobs; approaching the lower allowed inclination
gives an arbitrarily thin intrinsic model and needs an explicit thickness
prior. Choose a physical inclination/thickness prior and report it.

For a major-axis Sersic scale Re_major, let rho_sph(m) be the exact spherical
Abel deprojection normalized to total mass M and that radial scale. Then

    rho_oblate(R,z) = rho_sph(sqrt(R²+z²/qint²))/qint

has total mass M and projects to the required elliptical Sersic with qobs and
Re_major. This follows because the projection Jacobian is qint/qobs.
For a geometric-mean/circular-area radius Re_geom, use
Re_major=Re_geom/sqrt(qobs). Do not apply that conversion twice.

There is a real convention discrepancy to resolve from the released image
model: SED README calls `eclipse_effective_radius` "not circularised", while
the official PyAutoGalaxy Sersic API cited by the root has
`elliptical_effective_radius=effective_radius/sqrt(q)`, consistent with its
effective_radius parameter being a geometric-mean scale. The portal's
`coolest_sersic.json` gives a lens MAP theta_eff=1.139181789arcsec,
q=.8133792204,n=5.868719100, whereas the CSV median gives Re=1.062149656arcsec,
q=.8099213,n=5.663353615. Different MAP and median parameters prevent a simple
ratio test. Fit/check the released pre-PSF VIS lens image against the actual
elliptical coordinate before choosing a convention; retain a convention
sensitivity if unresolved. Source and lens components must not be confused.

## Optional exact field sensitivity

At fixed density, u=d Phi/d ln(a0) satisfies the linearized PDE

    div[A grad u] = div[mu L grad Phi],
    A = mu [I + L ghat ghat^T],
    L = d ln mu/d ln x = 1/(1+x),  ghat=grad Phi/|grad Phi|.

Its deflection derivative follows by the same LOS projection. Finite
differences of separately converged AQUAL solutions are a simpler independent
check. Boundary data must be differentiated consistently. At fixed shape and
coordinates, homogeneity also implies d ln(alpha)/d ln(M) = 1-S_alpha for
the unscreened mu_K=0 system, with homogeneous boundary conventions.

No Lean work was undertaken in this audit. Existing Lean kernels certify
their stated algebraic premises; they do not certify a new PDE discretization,
posterior, observational likelihood, or full physical action fit.
