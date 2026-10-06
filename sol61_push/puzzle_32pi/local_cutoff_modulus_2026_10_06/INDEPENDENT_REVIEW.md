# Independent local-cutoff action and tail audit

**Primary verdict: proved as written within the declared NR/linear-response scope.** The final b revision incorporates the compact-source asymptotic restriction identified in this review. The varied equations, positive source reaction, general-n charge normalization and leading massive algebraic response are correct. The stated far-field two-remainder formula applies outside a compact spherical baryonic source (or with sufficiently fast enclosed-mass convergence), at fixed positive m,T0 and in the leading large-Z linear response. The author now explicitly restricts the displayed remainder to compact baryonic support; an arbitrary isolated source without a mass-tail condition would not suffice. The action does not determine T0 or an additive vacuum energy.

## Inspected frozen evidence

Author base `1288c215ccf61b97e0ae2c5a2dfb0c53a8a5e02b`; exact inspected inputs:

- REPORT.md SHA256 `e8944e5812b259eb2805be8547aeac2ccb4329c57ba980249db60efa1fc927b0`.
- checks.py SHA256 `fd2ca84d72dd8b179a1660a772c0a36164de0faf82bd9858263c991cdad6d3c4`.
- Parent SOURCE_REVIEW.md SHA256 `a42c30a18c2bf6967259b9167d8c3e9206107ef15a688caa9734c024e76051f6`.
- Actual Claude `sonnet55_push/puzzle_32pi/p35_kernel_tail_fix.py` SHA256 `c869d50c3056894a5499935854c1adea1295d078e23d58bb0b34c5501c93e94c`.

The p35 kernel is read directly; its data runs are not repeated. This review reconstructs the explicit declared NR action rather than importing a covariant theory or treating a run count as proof. The parent's note authenticates the primary action locator arXiv:0911.5464v2 equations 3–6; this peer does not claim a fresh external source retrieval. No external theorem is needed for the following elementary variation and radial integrations.

## Independent variation and force sign

Write S=area of the unit (n-1)-sphere, `z=|grad Phi_N|²/a0²`, `Q=z+q`, and the author's Lagrangian as

`L=-grad Phi.grad Phi_N/(S G_n)+a0² Q/(2S G_n)-rho Phi-Z|grad T|²/2-V(T)`.

With fixed source and fixed admissible boundary data, variation of Phi gives `lap Phi_N=S G_n rho`. Variation of Phi_N gives

`lap Phi=div[Q_z grad Phi_N]`.

Since `q_y=2y chi_T(y)` and z=y², `Q_z=1+chi_T(y)` exactly. All spatial dependence through T must remain under the divergence. Variation of T gives

`Z lap T-V'(T)+a0² q_T/(2S G_n)=0`.

Thus the stated `-Z lap T+V'=J` sign is correct. The matter variation has potential energy rho Phi and physical acceleration `-grad Phi`, consistent with positive rho sourcing the ordinary negative isolated gravitational potential. The nonrelativistic two-potential model does not make modulus stiffness energy a relativistic gravitating stress; no such extrapolation is justified.

The general-dimensional Gauss convention gives `g_N=G_n M/r^(n-1)` with `[G_n]=L^n/(mass time²)`. The field prefactor `1/(2S G_n)` and source term have energy-density units. Dimensionless T gives `[Z]=energy/L^(n-2)`; `m²=V''/Z` is a new inverse squared length. No n=3 tensor/physical-G dictionary has been covertly reused in arbitrary dimension.

## Source reaction and maximum-principle scope

Direct differentiation of the retained p35 kernel yields

`partial_T chi=2 T y² [sqrt(1+1/y)-1]/(T²+y²)²>0`.

Therefore `q_T=2 integral_0^y t partial_T chi(t) dt>0` when y,T>0. At a zero-field constant vacuum, V'(T0)=0. The identical constant T0 cannot solve the modulus equation in a region y>0. This is a sharp within-action obstruction to an unchanged constant cutoff, not a disproof of an approximate screened response.

For `V=V0+Z m²(T-T0)²/2`, Z,m>0, a negative interior minimum deltaT=-d with d>0 has `lap deltaT>=0`; the left side `-Z lap deltaT-Z m² d<0` cannot equal positive J. The argument presumes a positive-T solution exists, proper boundary value T0 or a decay condition that realizes/excludes negative minima, and enough local regularity to evaluate the elliptic equation. The author correctly leaves full nonlinear existence/uniqueness open. V0 differentiates to zero in this NR equation, while changing T0 changes the chosen vacuum minimum.

At fixed m the leading stiffness response is the inverse of `-lap+m²` applied to J(T0)/Z. A uniform perturbative estimate requires deltaT/T0 small on the intended domain; a formal coefficient is not a global error bound for arbitrary finite Z.

## Massive response: why the source is not compact

At small y expand the exact positive derivative:

`partial_T chi=2y^(3/2)/T³-2y²/T³+O(y^(5/2))`,

`q_T=8y^(7/2)/(7T³)-y^4/T³+O(y^(9/2))`.

For a compact spherical baryonic source, outside its support `y=rM^(n-1) r^(-(n-1))`. Set `k=7(n-1)/2`. Then J has leading `A r^-k` and next small-y term `O(r^-4(n-1))`. The radial Laplacian is

`lap r^-k=k(k-n+2) r^(-k-2)`.

Consequently the leading particular solution of the massive equation is `J/(Z m²)`; insertion leaves a residual two inverse powers smaller, corrected at order `r^(-k-2)` for fixed m>0. The homogeneous decaying solution, or convolution contribution of a compact core, is exponentially small compared to this algebraic particular solution. The source is gravitational field energy response extending beyond the matter support, so it cannot be replaced by only a compact Yukawa charge.

For n=3, S=4pi and k=7, the coefficient is precisely

`a0² rM^7/(7pi G Z m² T0³)`.

This is a cutoff-modulus tail, not yet a force correction: one must insert T into the fully varied physical Poisson equation. The asymptotic is for the leading large-Z coefficient; claiming the same remainder for the full nonlinear solution would need extra estimates.

**Asymptotic condition identified and incorporated in final b.** If a noncompact finite spherical density has `M-M_enc(r)~r^-delta` with delta>0, then `y=y_point[1-O(r^-delta)]` and J acquires a correction `O(r^-k-delta)`. For delta<min(2,(n-1)/2), this lies outside the stated combined derivative/small-y remainder. For example, a smooth spherical density with outer slope n+delta realizes such a mass tail. The leading r^-k coefficient remains the total-mass coefficient, but its error estimate changes. Compact support suffices; adequate mass convergence and differentiated asymptotic regularity are alternatives. A decay boundary condition for the linear modulus excludes growing massive homogeneous solutions. With these restrictions the radial tail derivation is sound.

## Source charge: independent general-n calculation

For the point-source idealization `r=rM y^(-1/(n-1))`, positivity permits the following integral rearrangement without conditional cancellation. The source integral is

`int J d^n x =a0² rM^n/[2G_n(n-1)] int_0^infty y^(-1-n/(n-1)) q_T(y) dy`.

Insert `q_T(y)=2 int_0^y t partial_T chi(t)dt`. The outer integral from t to infinity is `(n-1)t^(-n/(n-1))/n`. Thus

`Q_J=a0² rM^n/(n G_n) int_0^infty t^(-1/(n-1)) partial_T chi(t)dt`.

There is no extra two or sphere-area factor. The integrand behaves like `t^(3/2-1/(n-1))` near zero and `T t^(-3-1/(n-1))` near infinity, so it is integrable for all n>=3. q_T saturates at large y, making J finite at the point-source center even though the Newtonian point-source self-energy is not included in this diagnostic.

The inverse-Laplacian radial Green coefficient is `1/[(n-2)S r^(n-2)]`, as its outward flux is minus one. Hence the massless response tail is `Q_J/[Z(n-2)S r^(n-2)]`. At fixed T0, Q_J scales as `rM^n~M^(n/(n-1))` in the point-source family. Extended-body scalar charge also depends on the interior y-profile; this point-source scaling is not a universal statement for arbitrary source families.

At the origin the massless convolution reduces to `deltaT(0)=1/[Z(n-2)] int_0^infty r J(r)dr`. The same positive integral rearrangement gives the more general formula

`deltaT(0)=a0² rM²/[2S G_n Z(n-2)] int_0^infty t^((n-3)/(n-1)) partial_T chi(t)dt`.

For n=3 it becomes exactly the author's `a0² rM²/(8pi G Z) int partial_T chi dt`, finite at both endpoints. The point-source response calculation has not regularized the gravitational action or supplied nonlinear source existence.

## Computation audit and remaining arrow

The frozen 39 passing checks corroborate derivatives, dimensional coefficients, radial Green/Laplacian identities and finite n=3,...,7 arithmetic; the general-n analytic integrations above establish their unrestricted n>=3 interpretation. All four final b manifests validate current declared inputs/results. The final b controls now change actual algebraic ingredients: the massive particular-tail candidate is removed and the leading operator residual recomputed; the cutoff source integrand is removed; and the charge prefactor is doubled. Each fails its relevant unchanged identity. The original a controls only overwrote Boolean flags and are superseded. Their manifests are stale after the input correction and are not current evidence. The b manifests were independently validated against the final hashes above; the source-asymptotic and controls corrections preserve the independent action/charge derivation.

The smallest remaining physical implication is still a covariant action with an independently justified V(T), additive vacuum normalization and constrained healthy response. Nothing here fixes a0, T0, C(T0), measured tensor G, vacuum Lambda or 32pi. The strongest accepted result is a same-declared-NR-action positive source response with a massive algebraic tail under the compact-source/linear-response assumptions above.

## Independent analytic continuation: actual physical force tail

Accepted ROOT_FORCE_TAIL.md, SHA256 `790123beb25b3d0153def80542e851374e634c3035a35a58f8d34952f96ec693`, against the same frozen final b action. This is an analytic peer reconstruction; no further computation or alteration of run inputs was needed.

Spherical integration of the **actual** varied equation gives

`r^(n-1)[Phi'(r)-nu(y,T(r)) Phi_N'(r)]=C_flux`.

For a compact smooth nonnegative source without an additional central singular source, bounded/vanishing central radial flux sets C_flux=0. One need not assume a C² MOND potential at the center: the ordinary deep-MOND central force can scale as sqrt(r), still making r^(n-1)g tend to zero. Adding a free monopole flux would change the source/boundary problem and could dominate the far-field correction, so this condition is essential. It follows exactly that the inward acceleration magnitude is `g=nu(y,T(r))g_N`. Spatial derivatives of T have already been integrated, not discarded.

At first order in 1/Z relative to the same source with constant vacuum cutoff T0,

`Delta g=a0 y [partial_T chi(y,T0)] deltaT`.

Insert `partial_T chi=2y^(3/2)/T0³+O(y²)` and `deltaT=4a0² y^(7/2)/(7S G_n Zm² T0³)+o(y^(7/2))` at fixed m>0. The product is

`Delta g=8a0³ y^6/(7S G_n Zm² T0^6)+o(y^6)`.

This independently confirms the coefficient, positive sign and order. The sign refers to enhanced **inward magnitude**; the outward signed radial acceleration changes by -Delta g. Since `[G_n Zm²]=L²/time^4`, the coefficient has acceleration dimensions. In n=3 it is `2a0³ rM^12/(7pi G Zm² T0^6 r^12)`, not r^-7. The displayed little-o belongs to the far-field asymptotic of the leading linear stiffness coefficient; there are additionally higher 1/Z orders, as the author explicitly states. No uniform nonlinear finite-Z bound follows.

For the massless point-source control or corresponding linear-response source charge, `deltaT~Q_J/[Z(n-2)S r^(n-2)]`. Multiplication by the same derivative gives

`Delta g~2a0 Q_J y^(5/2)/[Z(n-2)S T0³ r^(n-2)]`,

with exponent `(5/2)(n-1)+(n-2)=(7n-9)/2`, hence r^-6 for n=3. Q_J is the previously verified extended modulus-source integral; it is not a new arbitrary material mass or a free central flux. Its positivity fixes the magnitude correction's sign. The massless boundary cutoff remains free.

Both consequences require the same compact spherical source, fixed boundary/regular central flux and ordered linear-response/asymptotic assumptions already audited. They are a concrete force prediction of this NR diagnostic; they do not establish nonspherical behavior, a covariant completion, a MOND amplitude or vacuum selector.
