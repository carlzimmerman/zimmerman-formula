# Coupled cluster calibration and the sign of the remaining force

This is a bounded direct derivation from AFG-008 and elementary spherical gas
mechanics. It uses the existing X-COP central reductions as measurements, not
raw photon likelihoods or direct lensing accelerations. No new literature or
mechanism is imported. The starting core is
`a = kappa c sqrt(G rho_Lambda)` with kappa adopted, and either constant vacuum
`a` or the separate `a(z)=a(0) sqrt[0.315(1+z)^3+0.685]` branch. The two registered
normalizations and the distinct Q, R and inherited unfiltered M laws are all
carried through. Nothing below derives a relativistic completion.

## 1. One physical calibration must move both sides

Use the same observed angular shell before and after a calibration change.
Write the distance ratio as d, gas number/mass density ratio as eta, thermal
pressure ratio as pi, and stellar mass-to-light ratio as upsilon. All four are
positive constants with radius in the controlled family considered here.
Composition, angular shape, redshift and redshift-dependent dimming are held
fixed. Rescale every physical radius by d, rather than comparing different
angular shells at a fixed stated physical radius.

The gas volume integral gives `Mgas'(d r)=eta d^3 Mgas(r)`. Stellar luminosity
scales as `d^2` at fixed redshift and fixed angular flux, so
`Mstar'(d r)=upsilon d^2 Mstar(r)`. Consequently

    B' = eta d Bgas + upsilon Bstar.                         (1)

For a spherical pressure-based hydrostatic reduction, define positive inward
acceleration `gH=-(1/rho) dPth/dr`. The chain rule gives

    gH' = pi/(eta d) gH.                                    (2)

Thus the full conditional equality to test is

    F(eta d Bgas + upsilon Bstar; a) = pi/(eta d) gH.         (3)

Uniform density normalization cancels out of gH only when pressure is derived
from that same density and a fixed temperature, meaning pi=eta. It does NOT
cancel when independently reconstructed pressure is held fixed. Equation (3)
keeps this distinction explicit. It does not assert that the catalogued
M_FORW responds exactly like every possible real reconstruction pipeline.

For Q, equation (3) has an independent algebraic form:

    [eta d Bgas + upsilon Bstar]^2
      + a[eta d Bgas + upsilon Bstar]
      = [pi/(eta d)]^2 gH^2.                                (4)

For R and M, the forward functions themselves must be used. No Newtonian
missing-mass estimate is inserted in any equation.

## 2. The calibration has observable consequences

Introduce elementary observation maps for an optically thin gas with fixed
composition and unchanged angular shapes. Let ell be the ratio of the
band-integrated X-ray emissivity coefficient. Its actual dependence on
temperature, abundances, detector response and unresolved structure has NOT
been calculated here. With `S_X proportional to integral n^2 Lambda dl` and
`y proportional to integral P_e dl`, define amplitude ratios chi and psi.
For an ideal single-temperature gas, let tau be the temperature ratio:

    chi = eta^2 ell d,    psi = pi d,    tau = pi/eta.        (5)

Elimination gives the coupled closure condition

    d = psi^2 ell/(chi tau^2).                              (6)

Equation (6) is a conditional test of a proposed correction: one cannot freely
choose distance, density, pressure, temperature and emissivity while claiming
that all three measured thermal signals are unchanged. For example, if all
amplitudes, temperature and emissivity are independently fixed to their old
values, equations (5)-(6) force `d=eta=pi=1`. There is then no calibration
freedom in this family to remove the gravitational residual. The cached files
do not provide these independent constraints or their joint errors.

The executable routes all set upsilon=1, hold a fixed within its branch, and
solve the SAME coupled equation (3):

* Density at fixed pressure/distance: `d=pi=1`, eta free. Then gas B rises by
  eta while gH falls by eta. At fixed ell=1, chi=eta^2 and tau=1/eta. To hide
  the change in X-ray brightness requires ell=eta^-2, an additional
  independently testable demand. These are constructed corrections.
* Distance preserving X-ray amplitude and temperature, with ell=1:
  `eta=pi=d^-1/2`. Then `B'=sqrt(d) Bgas+Bstar`, `gH'=gH/d`, and
  the required SZ amplitude ratio is `psi=sqrt(d)`.
* Distance preserving X-ray and SZ amplitudes, with ell=1:
  `eta=d^-1/2`, `pi=d^-1`. Then the SAME gas-source change occurs but
  `gH'=gH/d^(3/2)`, and temperature must change by `tau=d^-1/2`.

These are different observation models, not interchangeable distance errors.
Distance is treated as a reconstruction calibration while a stays fixed to its
registered value. A change of cosmological parameters that also changes
rho_Lambda, H(z) or the adopted a0 requires a separate coupled cosmological
calculation; these d roots are not such a calculation.
In the last route a substantial temperature change also changes emissivity in
general; ell=1 is an explicitly conditional slice, not a self-consistent
spectral plasma calculation. Equation (6), with a measured emissivity response,
is the equation that a complete forward model must obey.

Every residual `log[F(B')/gH']` in these three one-parameter families increases
strictly with its positive nuisance parameter because the source increases and
the required gH decreases. Each shell therefore has at most one equality
root. Roots are constructed independently only to diagnose what is needed.
For a single parameter shared over several shells, the exact scalar minimax
solution has equal and opposite smallest/largest log residuals. Its remaining
largest multiplicative mismatch is a descriptive incompatibility of the
central profiles within that family, not a confidence level. It is not a
general exclusion of the full four-parameter or radius-dependent family.

The invariance `F(c B;c a)=c F(B;a)` for Q and R does not remove this test: a is
fixed to one registered branch, and gas and stellar accelerations respond
differently under distance changes. Whether independent data actually fix
the nuisance combinations is still unresolved.

## 3. A sign constraint on additional gas support

Take radial velocity u positive outward, scalar material acceleration
`A=partial_t u+u partial_r u`, positive inward gravitational magnitude
`g=F(B;a)`, and an additional isotropic pressure Pnt. Elementary radial Euler
balance is

    A = -g -(1/rho) d(Pth+Pnt)/dr
      = gH + gnt - F(B;a),
    gnt = -(1/rho) dPnt/dr.                                 (7)

This uses conventional local gas inertia and places the framework's modified
acceleration in the gravitational force. The a0 scaling alone does not prove
that matter obeys this momentum equation; it is an explicit mechanical
assumption of the diagnostic, as is the spherical application of F.

The observed central reductions require `Delta=gH-F(B;a)>0`. If the additional
pressure decreases outward, `gnt>=0`, so

    A >= Delta > 0.                                        (8)

For static equilibrium, (7) instead demands
`dPnt/dr = rho Delta > 0`: the extra pressure must INCREASE outward. A positive
pressure itself is not enough; its gradient has the wrong sign for ordinary
outward support. This is a sign obstruction, independent of the magnitude
assigned to the additional decreasing pressure. Anisotropic stress, magnetic
tension, sources, changed density/temperature reconstruction, or time-dependent
dynamics are not covered by this scalar-pressure assumption.

For a steady radial flow, A=u du/dr. Integrating (8) gives a further directly
testable bound that does not need the gas density derivative:

    u(r2)^2-u(r1)^2 >= 2 integral[r1,r2] Delta(r) dr.         (9)

It applies to both inflow and outflow, since it concerns the signed velocity
squared. If the right side is positive, the outer absolute radial speed is
at least its square root because the inner squared speed is nonnegative.
Extra decreasing pressure makes the speed requirement larger. The numbers are
conditional minimum radial bulk speeds, NOT temperatures, velocity dispersions,
observed flows or exclusions based on an unprovided spectroscopic bound.

The local quantity `sqrt(2r/Delta)` is also tabulated as a constant-acceleration
displacement timescale. It is only a dimensional diagnostic; Delta varies with
radius, and this quantity is not a cluster age or an integrated time evolution.

## 4. Continuity prevents treating the speed bound as a steady-flow solution

A steady spherical source-free flow must additionally obey
`r^2 rho u = constant`. Logarithmic differentiation gives

    u du/dr = (u^2/r)[-2-d ln rho/d ln r].                  (10)

The velocity may be inward or outward. If density falls more slowly than
`r^-2`, the bracket is negative, so (10) contradicts (8). If the mass flux
vanishes then u=0, and the contradiction still holds. Therefore an explanation
using steady radial flow and outward-decreasing scalar extra pressure requires
a density slope steeper than `r^-2` wherever Delta is positive.

This can be tested without taking numerical second differences of gas mass.
The declared interpolation on each adjacent gas-mass interval is exactly
`Mgas=C r^s`, where `s=ln(M2/M1)/ln(r2/r1)`. Therefore the density on each open
interval is `rho=(s C/4 pi) r^(s-3)`, and (10) becomes

    u du/dr = (1-s) u^2/r.                                 (11)

All 189 gas intervals overlapping 100–1000 kpc have s>1. In addition, all 252
evaluated shell/branch combinations lie strictly inside gas intervals, have
s>1, and have Delta>0. This is a direct sign contradiction for the specified
steady, source-free, spherical gas-flow model on the central reconstructed
profiles, rather than merely a large constructed flow velocity. A contradiction
at these interior shells already precludes a solution across the full interval;
no claim of interval-certified Delta positivity is needed for that conclusion.

This is conditional on treating the log-linear gas-mass interpolant as the gas
density reconstruction. Its derivative jumps at knots and is not a newly
measured density profile. Alternative unresolved density structure, mass
sources, changing thermodynamics, nonspherical stresses, or genuine time
dependence require their own observation/dynamics model. Uniform eta and d
rescalings preserve s, so they do not change this continuity sign as long as a
positive residual remains. The inequality (9) alone never constructed a
self-consistent steady flow.

## 5. Domain and data limitations

All seven clusters have their own stellar profile. The 100, 300 and 1000 kpc
fiducial shells and integration intervals lie within all three original radial
supports. The controlled distance transformations change the radii to d times
these values without leaving their corresponding transformed angular supports.
Gas and stellar components are read separately, M_FORW supplies gH, and no NFW
mass is fitted or used dynamically. The duplicated NFW column serves only to
cross-check the R/R500 versus kpc radius conversion.

The force integrals use the same explicitly specified log-linear interpolation
of positive masses as the original computation. The code splits quadrature at
all profile knots and checks against independent dense trapezoidal quadrature.
Residual positivity is checked at 3601 logarithmic radii plus all profile knots,
not established by a formal interval enclosure between every point.

The numerical data are binary64 central-profile calculations. Existing profile
errors cannot provide a joint thermal/distance calibration likelihood without
covariances and the underlying observation/reconstruction model. No priors,
significance, lensing inference, universal empirical claim, or explanation of
the correction's origin is invented. These are executable discriminants and
requirements that a physical or measurement explanation must meet.
