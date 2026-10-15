# Independent reconstruction of the angular density/shape theorem

15 October 2026. Primary verdict: **proved as written for the specified
Newtonian rest-mass-gravity/current-gauge static configuration energy and
its stated form domain**. This audits the all-`l>=2` coercivity, the physical
dipole translation kernel, and the additional material relabeling nulls.
It does not upgrade any conclusion to Einstein perturbations or to a
dynamical electromagnetic/free-boundary theorem.

The independently assigned raw target was `PROOF.md`, SHA-256
`0b9f3fdb54c22303084a43cf39354de15709995f20e2371fdd4691985e88583d`.
I read that complete proof, its actual pinned joined-body action/proof and
source manifest, and the code/contract. The source hashes agree with the
inherited originals used in my separate Einstein construction. The accepted
`run_exact/manifest.json` validates against current files. This is a fresh
same-team reconstruction by another agent; it is not external review or
formal verification. The proof author's verdict and check count were not
used to infer the mathematical conclusions.

## Claim and dependencies

For every integer `l>=2`, real unit-normalized harmonic Y, smooth independent
interior density tangents `eta_b Y, eta_c Y`, and common normal shape tangent
`hY` at the actual positive-density two-fluid interface, the exact static
energy Hessian subject to the two conserved fluid masses satisfies

\[
 Q_l\ge .01\sum_a\int_0^1\eta_a^2r^2dr
                +.25(l-1)(l+2)h^2.
\]

The dependency chain is: frozen actual spherical equilibrium and wall root;
mass-constrained material/shape Hessian; shape-dependent convex electrostatic
reduction with finite-density Gauss jump; complete fluid and area-wall
Newtonian gravity; elementary uniform estimates. The inherited radial
theorem supplies only the separate monopole conclusion. The angular
derivative calculation is new and was reconstructed rather than assumed
from that radial theorem.

| Obligation | Outcome |
|---|---|
| Two independent material densities and common moving trace | Passed |
| Finite-density Gauss sheet and potential transmission | Passed |
| Electric shape/density cross work | Passed |
| Material pressure-gradient and curvature terms | Passed |
| Fluid gravity including its boundary sheet | Passed |
| Wall/fluid gravity with the correct one-sided trace | Passed |
| Area-mass wall self-gravity for every harmonic | Passed |
| Uniform coercive constants for all `l>=2` | Passed |
| Translation pairing, dipole kernel, relabeling nulls | Passed |
| Exact finite computation and current manifest provenance | Passed within recorded finite range |
| Angular time evolution, radiation, boundary characteristic conditions | Out of scope |
| Full Einstein perturbations or wall microphysics | Out of scope |

## Electrostatic transmission and the crucial cross term

Let `delta phi_-`, `delta phi_+` be the Eulerian potential tangents and
`d_-`, `d_+` the corresponding radial displacement-field tangents at the
unit sphere. Differentiating actual potential continuity and normal Gauss
continuity gives

\[
 \delta\phi_- -\delta\phi_+=\Delta h,
 \qquad d_+-d_-=\zeta\rho_c(1)h,
 \qquad\Delta=E-D.
\]

In particular neither tangent is continuous at the fixed background sphere.
For the physical electrostatic minimizer, `A d=-grad delta phi` inside,
`d=-grad delta phi` outside, and `div d=zeta eta_c Y` inside.
Integration by parts with the two opposite boundary normals gives

\[
 F_e=\zeta\int_\Omega\delta\phi_-\eta_cY
       +\zeta\rho_c(1)h\,\delta\phi_-(1)
       -\Delta h d_+.
\]

Thus the charge/potential pairing is `F_e+Delta h d_+`, rather than
`F_e` alone. The phase-energy derivative supplies
`Delta h(d_-+hD'_- )`, because `Delta H_D=Delta` and
`D'_-=zeta rho_c(1)-2D`. Their sum is exactly the target Eq. (4).
Using the Gauss jump cancels its finite-density coefficient:

\[
 Q_{e,\mathrm{noncurv}}=F_e+2\Delta h d_+-2D\Delta h^2.
\]

Exterior Maxwell electrostatics has
`delta phi_+=b r^(-l-1)Y`, and direct radial integration gives
`F_out=(l+1)b^2=d_+^2/(l+1)`. Completing that square gives precisely
the negative bound in target Eq. (5). The `l=0` fixed-charge case has
`d_+=0` and recovers `-2D Delta h^2`; this is an orthogonal check of the
boundary sign against the actual spherical wall-load derivative.

Additional divergence-free field tangents do not invalidate the reduction.
Their cross pairing with the minimizing tangent is `-Delta h e_n`, and
their boundary cross contribution is `+2Delta h e_n` in the full second
variation. The doubled bulk cross term cancels it. What remains is their
positive convex field quadratic form. This verifies the stated extension
from reduced electrostatics to arbitrary admissible static Gauss tangents.

## Material constraints, fluid gravity and boundary work

The Neumann construction for `rho_a xi_a` realizes arbitrary smooth
`eta_a Y,hY` for `l>=1`, since the volume/source and boundary-flux means
both vanish. Positive boundary densities prevent division by zero in this
construction. The fluids need only share their normal trace; their
tangential displacements and density profiles remain independent.

Differentiating `Energy-sum mu_a M_a` cancels bulk path accelerations,
second shape accelerations, and all local `eta_a h` terms. The equilibrium
chemical relation `2K_a rho_a+Psi_a=mu_a` leaves the surface coefficient
`sum rho_a Psi_a' -2P=-P'-2P`. This reconstructs the pressure-gradient
term in the target without silently discarding a finite-density trace.
The electrostatic curvature term is `+2Delta H h^2`. The area Hessian is
`sigma[L+2]h^2`, as follows by expanding `dA` for a radial graph. The
actual equilibrium wall load then produces
`sigma(L-2)+2GsM+12piGs^2`, with precisely the two gravitational load
terms needed below.

The full perturbed fluid source is its volume tangent plus the boundary
sheet `rho_R hY`. Expanding the Newton kernel in harmonics gives the
pairing in target Eq. (6), including its `2rho_R h U` and `rho_R^2h^2`
terms. I find no frozen-source substitution in this calculation.

## Independently reconstructed area-wall gravity

For a wall element `s dA`, an interior `l`-pole carries the radial factor
`r_wall^(1-l)`. Its first variation therefore gives

\[
 \delta\Phi_{w,-}
       =\frac{4\pi Gs(l-1)}{2l+1}r^l hY.
\]

The exterior tangent has coefficient `-4piGs(l+2)/(2l+1)`; its jump
from the interior tangent is exactly what is required by translating the
background radial derivative discontinuity. This confirms that the common
finite-density fluid edge must pair with the **interior** potential tangent.
Using an exterior tangent in that volume calculation would generate a
spurious sheet contribution.

The spherical-average second wall-potential variation inside is constant,
`-GsLh^2`, obtained by expanding
`integral dA/|x_wall|=integral[r+|grad_S r|^2/(2r)]dOmega`.
Combining it with twice the pairing of the first wall potential and the
complete fluid tangent gives

\[
 Q_{fw}=\frac{8\pi Gs(l-1)}{2l+1}h(U+\rho_Rh)-GsMLh^2.
\]

This is the target Eq. (10). As a nontrivial constraint/trace check, the
conserved-mass monopole has `U+rho_Rh=0`, giving zero second derivative
of the exactly linear spherical interaction `-4piGsMR`. For a translation,
the remaining `-2GsMh^2` cancels the corresponding equilibrium-load term.

For wall self-gravity I independently expand the distance and the two area
elements. The coefficient of epsilon squared in their product is exactly

\[
 \frac1k\left[\frac38(t^2+t'^2)+\frac94tt'
    +\frac12(|\nabla t|^2+|\nabla t'|^2)
    -\frac{(t-t')^2}{2k^2}\right].
\]

Multiplication by `-Gs^2/2` and taking the full second derivative gives
the claimed `-pi Gs^2[4l^2+2l+3+9/(2l+1)]h^2`. The radial coefficient
reproduces the second derivative of `-8pi^2Gs^2 R^3`. Adding the actual
`+12piGs^2` load coefficient produces the target final wall-self term.

The singular divided-difference identity needed here holds for every l,
not only for the finite checked list. An explicit independent proof uses
the generating function. Put `0<z<1`, `a=1-z`, and `t=sqrt(2-2u)`.
The generating series of the polar integrals divided by `2pi` is

\[
 \int_0^2\frac{a^{-1}-(a^2+zt^2)^{-1/2}}{t^2}\,dt
 =\left[\frac{\sqrt{a^2+zt^2}-a}{a^2t}\right]_0^2
 =\frac z{(1-z)^2}.
\]

Its l-th coefficient is l. Coefficient extraction is justified either by
the locally uniformly convergent Legendre generating function with its
endpoint cancellation, or Tonelli using `1-P_l(u)>=0`. Polarization yields
the claimed full double integral `4pi l h^2`. This closes the universal
step independently of finite Legendre checks or an unstated recurrence.

## Uniform bound and the dipole nullspace

The Newton harmonic kernel is bounded by `1/max(r,t)`. Its weighted row
integral is `1/2-r^2/6<=1/2`; symmetric Schur and
`||eta_b+eta_c||^2<=2S` give `I_l<=S`. Cauchy gives
`|U|<=sqrt[2S/(2l+3)]`. These yield exactly
`N_l>=-(32G/5)S-(1008G/5)h^2` for `l>=2`.

For the wall/fluid cross term, `8pi(l-1)/(2l+1)<16`; Young's inequality
then gives `-GsS-128Gs h^2/(2l+3)`. The remaining wall-self ratio
`l/(2l+1)<1/2` gives the stated `-16Gs^2(L-2)` bound. Dividing the
shape terms by `L-2` uses maxima at l=2:
`(l+1)/(L-2)<=3/4`, `1/(L-2)<=1/4`, and
`128/[(2l+3)(L-2)]<=32/7`. These reproduce both coefficients in target
Eq. (14), with no unsupported extrapolation in l. The quoted density,
mass, tension and field bounds follow from the actual inherited fixed-point
body and wall root. Substitution gives the strict `.01` and `.25` margins.

For l=1, spatial translation acts by `eta_a=-h rho_a'`. Translation
invariance of the full energy and both constraints makes this a Hessian
kernel vector paired with every admissible tangent, not merely a zero
diagonal trial. Subtracting it sets h to zero and shifts each eta by
`h rho_a'`. On that slice the electric contribution is positive, the wall
terms vanish, and the same Schur bound leaves a strictly positive density
quadratic form. This proves the asserted physical dipole kernel precisely.
The divergence-free zero-normal-trace material displacements produce no
configuration tangent at all and remain additional relabeling/vortical
nulls. They have correctly not been called strictly restoring modes.

The positive occupied magnetic coefficient contributes a nonnegative static
magnetic square; its shape dependence begins at third order about B=0.
None of this controls velocity/magnetic mixing or boundary radiation.

## Evidence and scope

I inspected the exact code, whose finite Legendre range is `0..16` and
harmonic ratio range `2..64`, and validated its existing Mathbox manifest.
No new numerical experiment was needed: the named uncertainties were the
transmission traces, common-edge gravity and the universal singular kernel;
the independent calculations above decide them analytically. The exact
run supports its implemented identities and bounds, while the universal
estimates here and in the proof supply the all-l argument.

The strongest accepted statement is static angular coercivity modulo the
specified symmetries for this single counted hybrid body. Combined with
the pinned radial theorem it gives static nonnegativity of that hybrid's
configuration energy. Einstein stress/junction corrections change the
gravitational functional and its constraints, so this audit supplies no
GR mode theorem. The remaining dynamical, microphysical and empirical
obligations are exactly those stated in the raw proof.
