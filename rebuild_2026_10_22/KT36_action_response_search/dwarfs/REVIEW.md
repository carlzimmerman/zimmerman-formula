# Independent review of the 3 kpc isolated dwarf discriminator

**Claim reviewed.** The universal ell=3 kpc reciprocal Gaussian law, with simple
nu and the original KT15 sample, Plummer radii, luminosities, gas prescription,
stellar mass-to-light range and two-sigma cuts, predicts the saved isolated
spherical virial dispersions. It performs much worse than plain isolated
QUMOND on that same sample.

**Primary verdict: computationally verified only in the stated isolated
spherical range, conditional on numerical convergence.** The analytic
reduction, l=1 vector convolution, adjoint virial weight, Gaussian-mixture
representation, units and sample conventions check out. No force or virial
normalization defect was found. The deficits are large compared with the
observed numerical changes. This is not the primary satellite external-field
grade, and no theorem that the isolated result bounds every external-field
configuration has been supplied.

The independent audit includes a fresh bounded inspection of all saved grades
and independent angular integrals of the three-dimensional Gaussian. It does
not repeat the full dwarf solver. New audit files are confined to `review/`;
original data, inputs and completed runs remain unchanged.

## Decisive result and continuous mass-to-light range

Both saved radial resolutions give 4/24 reciprocal passes on canonical and
5/24 on alternate, versus 19/24 plain isolated passes on each footing and
3/24 Newtonian passes. Independent recomputation of all 11,808 saved scalar
grade comparisons reproduces these counts. The sample selection and fields
match the CSV and original KT15 records exactly; the original 41-point
Upsilon grid is unchanged.

The isolated dispersion is strictly increasing over the entire continuous
Upsilon range, not only at the sampled points. For fixed radius, the smoothed
Newtonian source field is proportional to
`M=Upsilon L+1.33 M_HI`. For simple nu, writing x=g/a0,

    A(g)=a0 (sqrt(x^2+4x)-x)/2,
    d[A(g)/a0]/dx = [(x+2)/sqrt(x^2+4x)-1]/2 > 0.

The inequality follows from `(x+2)^2=x^2+4x+4`. The vector-convolution radial
kernel K1 is nonnegative, the tracer and virial weights are nonnegative, and
the unsmoothed Newtonian contribution increases strictly with M. Thus sigma^2,
and hence sigma, increases strictly with Upsilon. Its maximum on [1,3] is
therefore the value at 3. A continuous acceptable interval exists exactly when
the predicted endpoint interval intersects the observational two-sigma band.
Applying this endpoint test to the saved numerical predictions gives the same
counts as the 41-point grid, so there is no missed weight-grid island in these
recorded curves. This argument does not supply a rigorous discretization error.

For the three extensively checked objects, the table takes the largest
Upsilon=3 prediction over both radial grids, doubled domain, and both independent
mixture-quadrature orders:

| Object | Canonical maximum [km/s] | Alternate maximum [km/s] | Observed two-sigma lower bound [km/s] |
|---|---:|---:|---:|
| Sculptor | 3.541170 | 3.563151 | 6.4 |
| Fornax | 7.279239 | 7.402557 | 9.9 |
| Leo I | 5.397012 | 5.414638 | 6.4 |

Even adding the recorded upper bound for the omitted measurement tail to sigma^2
leaves the largest alternate values below 3.563526, 7.404016 and 5.414948 km/s.
This is only that tail correction, not a bound on all numerical errors. The
unadjusted deficits are at least 0.985 km/s, whereas the largest selected change
across the recorded checks is 0.001127 km/s. These objects fail throughout the
continuous allowed Upsilon range within the stated numerical evidence.

The result is a serious failure of the isolated counterpart of the original
dwarf test. It is not legitimate to transfer the old 1D satellite EFE label
directly to this new reciprocal law. The finite isolated problem is physically
well-defined; a real satellite calculation must include its background under
the same unsplit law. An external field cannot simply be assumed to preserve
the isolated value as a universal upper bound without a proof or computation.

## Analytic normalization audit

For an isolated spherical smoothed source, the phantom equation reads
`div grad Phi_ph=div[A(g_source) rhat]`. Regularity at the origin removes the
homogeneous inverse-square integration term, so the inner phantom gradient is
exactly `A(g_source) rhat`. Translation-invariant Gaussian convolution commutes
with the gradient. Therefore the outer operation acts on this vector field,
not on its radial scalar magnitude.

Taking the observation axis along r, the original three-dimensional convolution
has angular factor

    2pi integral_-1^1 mu exp(z mu) dmu
      = 4pi (z cosh z-sinh z)/z^2,   z=rs/ell^2.

Combining it with the normalized `(2pi ell^2)^(-3/2)` Gaussian gives

    K1(r,s)=sqrt(2/pi) s^2 ell^-3 exp[-(r-s)^2/(2ell^2)]
            * exp(-z)(z cosh z-sinh z)/z^2.

This agrees with `isolated.py`. The l=0 density kernel replaces the final
factor by `(1-exp(-2z))/(2z)`. The l=1 numerator has derivative z sinh z>0
and vanishes at zero, proving K1>=0. Its small-z coefficients through z^9 are
correct. The first omitted positive term before multiplying by exp(-z) is
`z^11/518918400`; below the .1 switch its size is negligible at the stated
floating precision. The code's finite series is a numerical approximation,
not an exactly evaluated infinite series.

The audit independently integrated the normalized three-dimensional Gaussian
angular factor at eight radius pairs, including both sides of the z=.1
switch. Its l=0/l=1 results agree with the implementation to a maximum relative
error of 1.35e-13. This independent quadrature checks normalization and the
stable forms; it is not interval-certified arithmetic.

For unit-normalized tracer density p, the global spherical virial theorem gives

    sigma_los^2=(4pi/3) integral p(r) r^3 g(r) dr.

The 1/3 is the global line-of-sight average. It does not require a locally
isotropic velocity tensor in an otherwise spherical, stationary system.
Surface terms must vanish as in the inherited isolated equilibrium model.
Inserting the unsmoothed Plummer force and density gives
`sigma_N^2=pi G M/(32a)`, agreeing with the implemented analytic Newtonian term.
There is no extra 4pi, mass factor, or second outer Gaussian missing here.

The discrete transpose is also correct: if `vir_i` includes the measurement
quadrature weight, then
`sum_i vir_i sum_j K1_ij A_j w_j = sum_j [w_j sum_i vir_i K1_ij] A_j`.
This is exactly the accumulated `dual` array; both radial quadrature weights
occur once.

The independent source/tracer construction follows from

    p_a(r)=integral_0^infinity exp(-t) rho_sigma(t)(r) dt,
    sigma(t)^2=a^2/(2t).

Indeed the integrand is `t^(3/2) exp[-t(1+r^2/a^2)]/(pi^(3/2)a^3)`, whose
gamma integral is precisely `3[1+r^2/a^2]^(-5/2)/(4pi a^3)`.
Convolution adds ell^2 to each Gaussian variance. The vector identity

    S_ell[x rho_sigma]=(sigma^2/(sigma^2+ell^2)) x rho_sqrt(sigma^2+ell^2)

follows by completing the square, or by differentiating the Gaussian
convolution. For unnormalized `x exp(-r^2/(2sigma^2))`, it yields the fifth-power
amplitude used in the vector-Gaussian check. Moving this vector convolution
to the tracer virial weight gives exactly the mixture adjoint density and
the `4pi r^3/3` factor in `mixture_geometry`. The substitution
`t=[u/(1-u)]^2` has Jacobian `2u/(1-u)^3`, matching the program.

## Tail, implementation and test coverage

The continuum tail statement is correct for the original measurement radius:
nonnegative finite source mass gives `g_source(s)<=GM/s^2`, and
`A<=sqrt(a0 g_source)`. The vector-convolution magnitude is then bounded by
the scalar Gaussian convolution of `sqrt(GMa0)/s`, equal to
`sqrt(GMa0) erf(r/(sqrt(2)ell))/r`. This proves

    0<=sigma_ph,measurement_tail^2
      <=sqrt(GMa0)[1-M_Plummer(R)/M]/3.

It does not bound input-density truncation, kernel quadrature, or all omissions
when the integral has been moved to the adjoint variable. The plan and result
properly limit its meaning. It must not be added once and advertised as a
certified total-error bar.

The inherited assumptions are preserved: projected half-light radius R2 is
the Plummer a; luminosity uses solar V magnitude 4.83; gas mass contributes
1.33 M_HI and shares the adopted Plummer profile. The measured catalogue
dispersion is compared with a global virial prediction under the inherited
approximation. These modeling premises were not independently revalidated.

The physical-unit conversion is consistent: G is in
`kpc (km/s)^2 / solar_mass`, a0 in `(km/s)^2/kpc`, and the virial integral
produces `(km/s)^2`. The change from KT15's rounded G and kpc constants to the
MW solver's physical constants is disclosed and is negligible for the large
deficits. The historical primary external-field approximation is not reused.

The saved maximum control errors are 5.20e-5 for relative source/input mass,
5.23e-5 for the independent Newtonian Plummer integral, and 4.95e-5 for the
Gaussian and vector-Gaussian peak errors. All 24 objects are run at both radial
resolutions. Only Sculptor, Fornax and Leo I receive the doubled-domain and
independent Gaussian-mixture checks; those selected checks cannot be promoted
to independent-representation coverage of every object. The new audit checks
all saved classifications but does not extend their physical convergence domain.

The acceptance flag checks the prescribed mass/kernel thresholds and maximum
selected dispersion change. It does not certify every mathematical operation
or every observational premise. Positivity, independent representation,
analytic Newtonian normalization, and the large focus-object deficits together
support the numerical conclusion at the stated scope.

## Provenance

The reviewed author artifacts have SHA-256:

- `isolated.py`: `a6a4f77e9e117d252b600a87c12202ae44f511754b66d30c07be7e1caa4b83f4`
- `PLAN.md`: `61a8d3e31b284a2c5fb6fffa57c358556693f47c35894da054203aafe113ab7c`
- `run_001/results.json`: `9e832a16f9d21fbebc98e491658fb6824cb8bfb7e2642f0f2fc1c88d1c9037b3`
- `run_001/manifest.json`: `33074a3a3aee2464848114c8bfd37dac42a1fa7bc0a13dd0595f268c3087221b`

The independent bounded audit is `review/audit.py`, with its prewritten
`review/contract.json` and `review/run_001/{results,manifest}.json`. It completed
with all finite checks passing. The author and audit manifests were validated
using the installed mathbox `validate_manifest.py MANIFEST --root "$PWD"`.
No fresh full scan was run by the reviewer. The analytic derivations above are
independent reconstruction, not deductions from the author's success flag.

The strongest safe conclusion is substantial isolated dwarf under-support by
this fixed 3 kpc law on the original sample, including continuous-Upsilon
failures for the three selected classical dwarfs. It materially weakens the
broader candidate despite its separate MW/Cassini result. A primary satellite
verdict requires the new law's actual external-field/background calculation.
