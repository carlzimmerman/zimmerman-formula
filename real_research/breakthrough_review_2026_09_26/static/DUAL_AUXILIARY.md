# A joint auxiliary equation from convex duality

This CD26-5 result concerns the simultaneous canonical U/Z constraints at
fixed spatial geometry, positive lapse and carrier canonical data. It does
not infer a gravitational solution from a solution of those two constraints.
It applies to the old perspective/PQ potentials when their positive
constraint solution exists, and to the newly proposed reciprocal-invariant
vacuum potential below. No CD26-4 source or result is rewritten.

## The new equation

Use `m=M_P^2 cN>0`, `a=D ln N`, `z=P_h Z`, `<z>_h=0`, `t=1+z>0`.
Let `epsilon_exc` be the fixed nonnegative excitation canonical energy
density, excluding the specified vacuum potential. Define

\[
 F_0[z]=\int N\,d\mathrm{vol}_h\left[
 m|Dz|^2-2m a\cdot Dz+\frac{\epsilon_{\rm exc}}{1+z}
                         +V_0 F(1+z)\right],
\]
\[
 \langle BU,z\rangle=2m\int N\,DU\cdot Dz\,d\mathrm{vol}_h,
\]
\[
 E_g[U]=\frac m2\int N\,d\mathrm{vol}_h
  \left[G\big(J(DS_hU)+\ell\Delta_h S_hU-\theta\big)
                         +\ell a\cdot DS_hU\right].
\]

The actual auxiliary Hamiltonian, up to terms independent of U and z, is

\[
 H_{\rm aux}[U,z]=F_0[z]+\langle BU,z\rangle-E_g[U]. \tag{1}
\]

It is a saddle: convex in z, concave in U. Calling its raw joint Hessian
positive would be incorrect. Let `F0*` be the convex conjugate on the
mean-zero space with `F0=+infinity` outside `t>0`. Eliminating z gives

\[
 \inf_z H_{\rm aux}[U,z]=-F_0^*(-BU)-E_g[U].
\]

Therefore the **new single joint-constraint equation** is

\[
 \boxed{\nabla I[U]=0,\qquad I[U]=E_g[U]+F_0^*(-BU),\qquad
 z[U]=\nabla F_0^*(-BU).} \tag{2}
\]

In particular,

\[
 \nabla I=\nabla E_g-B^*z[U],\qquad
 \boxed{I''=E_g''+B^*[F_0''(z)]^{-1}B.} \tag{3}
\]

The inverse is on the mean-zero constraint space; it is not an inverse of
the constant spatial mode. Equation (2), rather than separately varying a
positive U energy after discarding the carrier source, is the actual
canonical coupling. Where a twice differentiable formulation is available,
(3) is its positive Schur operator. Monotonicity gives the corresponding
uniqueness result without assuming a pointwise Hessian of J at zero.

## A useful global lower bound from the compensator

For the specified C4 ramp, `G(Y)>=Y-delta/2` everywhere. Since the leaf is
closed and `a=D ln N`, the complete compensator cancels the affine Laplacian
under the measure. Consequently

\[
 \boxed{E_g[U]\ge\frac m2\int N J(DS_hU)\,d\mathrm{vol}_h
       -\frac m2(\theta+\delta/2)\int N\,d\mathrm{vol}_h.} \tag{4}
\]

This holds even though the local gate is necessarily off somewhere on a
compact theta-positive leaf. The boundary identity is
`integral N(Delta_h W+a dot DW)=integral div_h(N DW)=0`.
It is a global functional bound, not the false assertion that the gate is
globally on. The fixed compensator is essential to (4).

The actual XC4 monotone tail has
`h_mono(y)=h_star+b log((y+y_p)/(y_star+y_p))`, `b>0`. Thus
`J(p)=4a0^2 integral_0^(|p|/a0) h_mono(y)dy`
grows as `4a0 b |p| log(|p|/a0)` and is superlinear. The unmodified RAR
phantom would not supply this same tail/coercivity argument; the operative
nu_mono definition matters.

## A global theorem on each fixed spectral space

Work on a smooth compact connected three-dimensional leaf without boundary.
Fix smooth `N>0`, smooth nonnegative `epsilon_exc`, positive `V0`, and a
finite-dimensional smooth mean-zero spectral space for U and z, invariant
under the intrinsic heat operator. On that space `B` is an isomorphism.
For the new proposed vacuum potential take

\[
 F(t)=1+(t+t^{-1}-2)^2=1+(t-1)^4/t^2,\quad t>0. \tag{5}
\]

It obeys

\[
 F''(t)=\frac{2(t-1)^2(t^2+2t+3)}{t^4}\ge0,
 \quad F(1)=1,\quad F'(1)=F''(1)=F'''(1)=0.
\]

For every U, `F0(z)+<BU,z>` has a unique interior minimizer. Here is a
finite-dimensional proof rather than an import of a continuum maximum
principle into a truncated solver. Positivity and `<t>_h=1` bound the
finite spectral coefficients, so the closed domain `t>=0` is compact.
At a boundary minimum `t(x0)=0`, smoothness gives `t(x)<=C dist(x,x0)^2`
locally. The potential grows as `t^-2`; its integral then dominates
`integral_0^r s^(2-4)ds=+infinity` in three dimensions. Thus finite energy
excludes the boundary. The gradient square is strictly convex on
mean-zero z and the remaining potential is convex, proving uniqueness.

The finite-dimensional implicit function theorem now gives
`(F0*)''=[F0'']^-1>0`. The gate functional is convex; hence I is strictly
convex. It is also coercive: `F0*(-BU)>=-F0(0)`, equation (4) holds, heat
is injective on the fixed spectral space, and the superlinear J tail plus
finite-dimensional norm equivalence makes the right side grow faster than
`||U||`. Therefore I has a unique global minimizer. Its z[U] is the unique
positive solution of the **joint** variational Galerkin U/Z equations.
This allows arbitrary finite canonical data under the declared hypotheses;
it is not a small-amplitude implicit-function claim.

For continuum admissible solutions, the same monotonicity identities imply
uniqueness whenever they can be tested in the energy spaces: subtract the
two U/Z equations and add the two convexity pairings. Strict convexity of
F0 forces z1=z2; the isomorphism of the mean-zero elliptic B then forces
U1=U2. Continuum existence, estimates uniform in spectral dimension,
convergence of Galerkin solutions, and regularity of the simultaneous
constraint map have not been proved here. Heat injectivity at each finite
dimension is not a uniform lower bound as dimension increases.

## A sharp equation that distinguishes the vacuum choices

On a homogeneous leaf with N=1, z=0, no carrier excitations, and the
inactive gate, let `lambda>0` be a spatial Laplacian eigenvalue and
`v2=V0 F''(1)`. The exact linearized auxiliary Schur coefficient is

\[
 \boxed{I''_\lambda=\frac{(2m\lambda)^2}{2m\lambda+v_2}
       =\frac{2m\lambda^2}{\lambda+v_2/(2m)}.} \tag{6}
\]

This is a fixed-geometry canonical constraint response on a spatial slice,
not the physical baryonic gravitational response after solving the lapse
and spatial metric equations. The latter cannot be inferred from (6).

For PQ, `V0 F(t)=V0/t+V0 zeta(t-1)^2`, so
`v2=2V0(1+zeta)` and the infrared Schur operator behaves as lambda squared.
For (5), `v2=0` and (6) is exactly `2m lambda`. Thus the reciprocal quartic
vacuum preserves its nonlinear positive barrier while removing the vacuum
curvature contribution to this linear auxiliary operator. This is a
calculated distinction, not a transfer of PQ's proof to a new action.

## The exact filtered-MOND mismatch still survives

No convex-dual rearrangement changes the force law. For any fixed smooth
nonconstant v, put `U=lambda v`, `W=lambda S_h v`. Since `J(0)=0`, for
sufficiently small positive lambda,

\[
 J(\lambda\|DS_hv\|_\infty)
       +\ell\lambda\|\Delta_hS_hv\|_\infty<\theta. \tag{7}
\]

Then `f=G=0` everywhere: the nonlinear gated J force vanishes exactly.
On a flat constant-lapse leaf the compensator vanishes as a U functional,
while the original ungated J first variation is nonzero; its radial
pairing is `integral J_p(DW) dot DW>0`. Since heat has no zero eigenvalues,
the ungated variational operator cannot vanish for a nonconstant U.
In the deep regime `J(lambda p)~(8/3)sqrt(a0) lambda^(3/2)|p|^(3/2)`;
the ungated phantom response has order lambda^(1/2), whereas the inactive
auxiliary response is linear after its nonsingular finite-mode elimination.

This is an exact open-neighborhood mismatch, not an unestimated small
interface correction. The new vacuum potential repairs a distinct
auxiliary issue; it does not restore the original global MOND target.
Any next action must explicitly choose between retaining this activation
threshold and demanding the ungated law for arbitrarily weak sources.

`run1/` records bounded symbolic checks and a one-harmonic variational
control using the actual nu_mono tail. That control illustrates (2); the
finite-space theorem and the mismatch proof above are analytic.
