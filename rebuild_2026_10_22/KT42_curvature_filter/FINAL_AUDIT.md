# Independent final audit of the KT42 scalar reductions

**Primary verdict: computationally verified only in the stated range.** The
analytic action, adjoint-observable reduction, filtered-Plummer representation
and fixed-filter homology identities are correct under their declared
whole-space/boundary hypotheses. No blocking sign, normalization or omitted
adjoint error was found. The recorded numerical failures exclude the tested
configurations; they are not a continuous-width or all-baryon no-go theorem.

Reviewer: `/root/audit_dynamic_options`, 2026-11-04, separate from the Solar and
dwarf implementers. This review reconstructed the critical identities from the
action and Green functions, read the actual scripts/results and compared the
root's `SCALAR_REVIEW.md`. It did not independently rerun the gravitational
solvers or quadratures. The review is not claimed to be blind to the reports.
`FINAL_AUDIT_INPUTS.json` pins the exact reviewed artifacts. The root separately
owns current-manifest validation and final phase synthesis.

## Normalized claim and dependencies

The model holds p=9/8, ell=3kpc, the original primitive, baryons, acceleration
footings and comparison lines fixed. Only the curvature argument is replaced:

    Delta psi=4 pi G rho, g=grad psi, Hbar=Hess(T_a psi),
    E=|g|^2 R(x+s^p), x=|g|^2/a0^2, s=ell^2 Hbar:Hbar/a0^2.

T_a is a fixed isotropic Gaussian on Euclidean space. Variation returns

    Delta Phi=Delta psi+div A-partial_i partial_j(T_a^* B_ij),
    A=(R-1+xR')g, B=p ell^2 s^(p-1) xR' Hbar.

The dependency chain is: declared action and fixed filter -> full variational
return -> Green/virtual-work observable -> scalar quadrature -> finite
comparison. The first two arrows were reconstructed analytically here. The
finite numerical evidence remains conditional on the implementations,
quadrature convergence and the original observational conventions. No outside
theorem or novelty claim is load-bearing for these identities.

The existing independent MW review, including the finite weighted adjoint,
is `endpoint/FILTER_REVIEW.md`. Its restrictions remain: backward-Euler heat is
an approximation to the Gaussian, and a bounded frozen growth rate is not a
stability theorem. This final review adds the Solar/dwarf scalar reductions;
it does not replace their full numerical manifests.

## Solar: sign, STF kernel and return-filter placement

Let P*=3mu^2-1 and let F be the distributional STF zz derivative of 1/r.
Away from the origin F=P*/r^3. With the convention Delta^{-1}=-1/(4 pi r),
the regular tidal observable pairs a source with -F/(4 pi). Therefore the
source term -partial_i partial_j(T_a B_ij) contributes

    q_B=(1/(4 pi)) integral B_ij partial_i partial_j(T_a F).

The two integrations by parts preserve this positive prefactor. The filter
has been moved onto the observable by adjointness; it has not been dropped.

For the softened point potential psi_a=-erf[r/(sqrt(2)a)]/r, let h_r,h_t be
the radial and tangential Hessian eigenvalues and t=h_t-h_r. Since the STF
projection commutes with the Gaussian convolution,

    T_a F=t P*/3.

This needs the Hessian of the filtered scalar potential. Independently
filtering spherical-basis eigenvalues would be a different operation.

The full point-source Hessian contains an isotropic distributional contact:
Hess(-1/r)=Pf[(I-3nn)/r^3]+(4 pi/3)I delta. Its Gaussian convolution has
the correct finite, nonzero trace. In contrast, the isotropic delta cancels
in **STF Hess(1/r)** itself. Thus the phrase "contact included" in the Solar
derivation must mean correct distributional differentiation/convolution, not
an extra isotropic delta added to F. The actual formulas implement the correct
STF kernel.

The radial second derivative of T_a F is t''P*/3, and its Laplacian is
[t''+2t'/r-6t/r^2]P*/3. Contracting with
B=D[h_t I+(h_r-h_t)nn] yields

    B:Hess(T_a F)
      =D [h_r t''+h_t(2t'/r-6t/r^2)]P*/3.

Azimuthal integration gives the recorded 1/6 coefficient multiplying
r^3 d(r) dlogr. At a=0, h_r=-2/r^3, h_t=1/r^3 and t=3/r^3, so the bracket
is -108/r^8 and q_B=-18 integral d(r)/r^5 dlogr, exactly the inherited
zero-filter expression.

For A, one integration by parts gives q_A=integral A.grad F/(4 pi).
The radial and angular derivatives of F give

    A.grad F = (3C/r^4)[g(1-3mu^2)+eta(3mu-5mu^3)],

which reproduces q_A=(3/2) integral b(r)/r dlogr. Subtracting the coefficient
at angularly independent x0 changes neither integral: each removed angular
polynomial integrates to zero. The code's angular subtraction is therefore a
cancellation control, not a force modification.

The normalization Q2=(3/2)(a0/rM)q is correct for the inherited convention
Phi_2=(Q2/2)[z^2-r^2/3]: the STF zz Hessian of this regular term is 2Q2/3.
The comparison uses its absolute amplitude; all sampled total signed values
in the final Solar report are negative.

## Solar: exterior coefficient versus a central finite-source Hessian

For fixed a>0, Hbar is finite at the point-source origin while |g| diverges.
The leading high-field A is a radial unit vector. It creates an isotropic
potential proportional to r. That cusp has no literal central Hessian, and
its Hessian away from the origin has a directional STF part despite the
potential having no spherical-harmonic l=2 component.

The reported q is consequently **the STF Hessian of the regular l=2 potential
only**. It is not the Hessian of the complete singular point-source potential.
Solar `README.md` now states this distinction explicitly. The isotropic radial
anomaly is a separate planetary/ephemeris obligation and is not cleared by a
small Q2.

Expanding A in eta r^2, the quadrupolar radial/tangential amplitudes begin at
order eta^2 r^4; their l=2 source begins at r^3 and their particular potential
at r^5. Hence that particular l=2 term does not contaminate the regular r^2
coefficient. This statement concerns the l=2 projection, not the full cusp.

The exterior source limit is supported independently by

    0<=C<=R-1<=2/sqrt(z), |A|<=2.

The lower bound uses C>=R-1+zR'=Q'-1>=0, since R'<0 and x<=z. Integrating
Q'-1<=1/sqrt(z) proves the upper bound. A shrinking core therefore contributes
vanishingly to the fixed-exterior-radius Green pairing. For fixed a>0, its
filtered Hbar converges smoothly on compact sets, and B is bounded there;
the B observable has a smooth filtered Green test. The ordinary decaying
far tails remain necessary for the whole-space pairing. These facts support
the exterior distributional limit. They do not permit reversing the limits
and evaluating the Hessian at the center of a shrinking finite Gaussian Sun.

The finite-radius A formula was also reconstructed from the l=2 Poisson Green
solution. If a_r=integral P* A_r dmu, angular integration of div A gives
(5/4)[a_r'-a_r/r-3b/r] as its conventional l=2 coefficient. Integrating by
parts cancels the matching-radius a_r boundary terms and gives exactly

    q_A,eff(R)=(1/(2R^5)) integral_0^R (5a_r+3b)r^4 dlogr
                +(3/2) integral_R^infinity b/r dlogr.

Thus the finite-radius control includes the inner irregular multipole.
It does not quietly substitute the regular coefficient for the finite-source
solution being checked.

## Dwarf: filtered Plummer field and compression at fixed a

The source identity is correct:

    rho_b=M integral_0^infinity e^-t G_sigma0(t) dt,
    sigma0(t)^2=b^2/(2t).

Inserting the Gaussian and integrating t^(3/2) exp[-t(1+r^2/b^2)] gives
Gamma(5/2)=3sqrt(pi)/4 and the normalized Plummer density. Convolution adds
a^2 to the component variance v=a^2+b^2/(2t); each component retains its mass.

With P the enclosed normalized Gaussian mass, Hbar_tt=GM integral e^-t P/r^3
and Hbar_rr=GM integral e^-t[sqrt(2/pi)v^-3/2 exp(-r^2/(2v))-2P/r^3].
These are obtained by differentiating the filtered scalar potential, so they
are the radial eigenvalues of the filtered **Cartesian** Hessian.

Centered compression sends b to b/lambda while a and the uniform external
gradient remain fixed. Writing chi=b^2/(2t), dot v=-2chi. Differentiating the
Gaussian enclosed mass gives

    dot Hbar_tt=GM integral e^-t sqrt(2/pi)chi v^-5/2 exp(-r^2/(2v)),
    dot Hbar_rr=GM integral e^-t sqrt(2/pi)chi v^-5/2
                         exp(-r^2/(2v))(1-r^2/v).

The same variation is 3Hbar+r partial_r Hbar+a partial_a Hbar, or
-b partial_b Hbar at fixed a. Omitting the a derivative would vary the wrong
physical filter. The unfiltered self-gradient variation is 2g+r g'; the
uniform external gradient is not compressed.

Since E_ph=-integral E_ex/(8 pi G) and W_ph=-dE_ph/dloglambda,

    W_ph=(1/(4 pi G)) integral[(A-A_ext).dot g+B.dot Hbar].

Azimuthal integration and division by 3M give 1/(6GM), as implemented.
The Newtonian Plummer contribution is pi GM/(32b). The external tangent
subtraction has zero net angular integral for the centered radial compression
but is correctly retained. The B term pairs with T_a dot H, which is the
adjoint-return contribution in virtual-work form.

The energy finite-difference control changes b at fixed a and differentiates
energy values independently of A/B; it therefore tests the relevant variation.
It is performed on its declared finite annulus, not represented as a new
global energy convergence proof. The full virial quadrature separately receives
radial/angular/mixture and outer-domain checks.

## Recorded finite evidence and claim calibration

Solar `run_002` records 43/43 checks and `verify_001` records 38/38. The latter
contains a distinct periodic 13^3 action derivative/adjoint check, Cartesian
differences of the filtered Green Hessian, finite-Gaussian exterior A checks
at Saturn, additional widths and adaptive radial cross-checks. The action
pairing agrees to floating roundoff; omitting the return filter changes it
from .04493246 to .00563810. The maximum Cartesian contraction discrepancy is
2.172e-9. These are useful orthogonal finite controls, not interval certificates.

The two bracketed Solar crossings are .5470683477 pc and .5237528747 pc, with
adaptive ceiling ratios 1.0000000049 and .9999999986. They establish one
numerical crossing on each specified bracket. The sampled ratio is
nonmonotone beyond the first crossing; no global monotonicity, unique crossing,
or absence of unsampled islands follows. The adaptive error estimates are
reported, and the final report does not claim every requested internal
adaptive tolerance was attained.

For the declared fixed Draco/Upsilon2/eta.01 diagnostic, all nine sampled
widths fail the orientation-averaged screen: W/(3M)<0 through a=.3kpc; at
1kpc the trace-averaged dispersion is approximately3.07km/s, below6.7km/s.
Negative W excludes gravity-only stationary balance with nonnegative kinetic
trace and vanishing confining surface stress. Positive W would be only a
necessary condition, not a distribution function or line-of-sight fit. The
Fornax size control behaves differently, so the comparison does not assert
all dwarfs fail.

The dwarf report's maximum refinement/domain shift1.68e-5 (km/s)^2, energy
derivative error7.88e-9 relative and zero-filter reproduction below1e-10
(km/s)^2 are read from the saved evidence. They were not independently rerun
by this reviewer. The failed Solar JSON-serialization run is retained and
does not support the successful table.

The companion population report was read for synthesis scope, not audited as
a fresh solver here. It tests52 historical KT39 primary-pass cells at three
small widths, with156 negative vertical-force values and468 matching-sign
potential differences. Its current primary-pass count is50 at refinement3,
not52; the two lost cells are identified. This supports the selected-population
claim, not a full1375-cell scan, continuous-width statement or convergence
proof for all52 cells. Root's final synthesis must retain that distinction.

## External-field and physical interpretation

Both scalar diagnostics deliberately impose a **uniform auxiliary Newtonian
external gradient with H_ext=0**. An isotropic whole-space Gaussian preserves
that affine potential, and its zero Hessian contributes no background B.
This is internally consistent with the inherited comparison, including the
fixed-external-field homology variation.

It is not a self-consistent embedding in a spatially varying Galactic field.
For a curvature-dependent energy, a nonzero host Hessian can change the
constitutive state and its response even at the same local gradient. Thus
these results cannot be relabeled as an all-Galactic-environment Solar or
satellite theorem. The fixed diagnostic is sufficient to reject the tested
model configurations against the stated tests, without asserting that every
different embedding, response law or allowed matter stress has been covered.

## Obligation matrix and blocking issues

| Obligation | Status |
|---|---|
| Full action variation and return filter | passed analytically |
| Solar A/B signs, 1/6 factor and Q2 normalization | passed analytically |
| Distributional STF/contact distinction | passed with the explicit interpretation above |
| Regular exterior l=2 coefficient and finite-radius A formula | passed under fixed-a exterior limit and decay hypotheses |
| Finite-source central Hessian equals reported q | not claimed; not generally interchangeable |
| Filtered-Plummer mass normalization and fixed-a homology | passed analytically |
| Dwarf virial sign, external subtraction and 1/(6GM) factor | passed analytically |
| Numerical quadrature accuracy | verified finite controls; not interval certified |
| Actual Galactic Hessian embedding | not addressed |
| Continuous-width/full-baryon exclusion | not established |
| Radial Solar anomaly, full ephemerides and relativistic completion | separate obligations |

**Blocking defects in the stated finite results: none found.** The restrictions
above block stronger universal or theory-complete conclusions; they do not
invalidate the recorded finite tests. No old source, parameter or result was
modified by this review. Mathematical proofreading covered the signs,
normalizations, boundary terms and scope language in this audit; no unresolved
local notation issue remains.

**Active follow-up remains pending:** the Solar owner is now evaluating the
finite-width isotropic planetary anomaly using the existing AZ11/AZ12 cuts,
including the full B return. This audit does not grade that uncompleted branch
or treat the phase as finished. Root will separately review its new derivation
and verify the final run records. The present sign/formula passes apply only
to the sources and outputs pinned in `FINAL_AUDIT_INPUTS.json`.
