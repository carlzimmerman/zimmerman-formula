# Independent nonlinear-modulus existence and energy audit

**Primary verdict: proved as written under the declared fixed-source Newtonian hypotheses.** The sufficient stiffness threshold, constructive unique positive solution, finite relative-energy minimum and finite-stiffness spherical force tail follow from the action. These statements are restricted to the static cutoff-modulus problem. They do not prove positivity of the full gravitational action, a dynamical/causal stability theorem, a matter equilibrium, or a vacuum selector.

## Final inspected inputs and dependencies

Frozen author REPORT.md SHA256 `7adb5d15a30e6843ead2b3180b0e7eeb4e3e2ed63824dc72c288c23cd20d13e1` and checks.py SHA256 `fcbb411115187ad57cb8f305173e0517d802e420e1ece838c13be74dcb48723c`. The parent action report is pinned at `e8944e5812b259eb2805be8547aeac2ccb4329c57ba980249db60efa1fc927b0`, and ROOT_FORCE_TAIL.md at `790123beb25b3d0153def80542e851374e634c3035a35a58f8d34952f96ec693`. The parent INDEPENDENT_REVIEW independently derived the action/charge normalizations and compact-source restriction; no parent input is modified here. This audit reconstructed the inequalities and operator/energy arguments from the raw declared action before accepting the author's verdict. The primary-source anchor is the already authenticated NR action recorded by the parent; no new external causal result is imported.

The leaves are: elementary kernel inequalities; explicitly normalized positive heat Green kernel; Newtonian compact smooth source; completeness of C0 under the uniform norm; initial fixed source and boundary data. The bounded computations corroborate the algebra and a discrete example, not the continuum theorem.

## Independent global derivative bounds

Write `b(t)=sqrt(1+1/t)-1=1/[t(sqrt(1+1/t)+1)]`. For positive t,

`0<b(t)<=1/(2t)` and `b(t)<=1/sqrt(t)`.

Differentiating the actual p35 cutoff gives

`c_T=2T t² b(t)/(T²+t²)²`,

`q_T(y,T)=4T integral_0^y t³ b(t)/(T²+t²)² dt`.

Consequently

`0<=q_T<=2T integral_0^infty t²/(T²+t²)²dt=pi/2`.

The integral is pi/(4T), obtained by t=T tan theta. The exact second derivative has ratio

`(partial_T c_T)/c_T=(t²-3T²)/[T(T²+t²)]`.

This ratio lies between -3/T and 1/T. Since the first derivative integrand is positive,

`|q_TT|<=3 q_T/T<=3pi/(2T0)` for T>=T0.

The independent small-field bound follows by replacing b(t) by t^(-1/2) and `(T²+t²)²` by T^4:

`q_T<=4T^-3 integral_0^y t^(5/2)dt<=8y^(7/2)/(7T0³)`.

Thus `h(x)=min(pi/2,8y(x)^(7/2)/(7T0³))` bounds the exact nonlinear source on the entire positive cone. For a compact smooth Newtonian body, y is bounded with exterior decay r^(-(n-1)); h decays as r^-k, k=7(n-1)/2>n. Therefore h belongs to C0, L1 and L2 for every n>=3. All constants and signs agree with the author's argument; no n=3 normalization was silently substituted into general n.

## Constructive existence and genuine uniqueness scope

Set `kappa=a0²/(2 Omega_(n-1)G_n)` and u=T-T0. The exact varied modulus equation is

`(-Delta+m²)u=(kappa/Z)q_T(y,T0+u)`.

The positive Green kernel has heat representation

`G_m(x)=integral_0^infty exp(-m²s)(4pi s)^(-n/2)exp(-|x|²/(4s))ds`.

Its mass is 1/m² by integrating the Gaussian first. Applying the massive operator and integrating the heat equation in s gives the unit delta normalization. This independently fixes the sphere/force-normalization-sensitive factor; it is not an arbitrary Yukawa coefficient.

The map `A[u]=(kappa/Z)G_m*q_T(y,T0+u)` preserves the closed C0 box

`0<=u<=B=kappa pi/(2Zm²)`.

It has uniform Lipschitz constant `L=3kappa pi/(2Zm²T0)`. Under L<1, successive Picard differences are bounded by B L^j, so the geometric series converges in the complete box. Passing the limit through the Lipschitz map supplies a solution; comparing two fixed points forces equality. The same estimate gives the abstract Picard error quoted by the author. Numerical grid errors are not included in that continuum bound.

The positive Green kernel and nontrivial positive source give u>0 at every finite point, despite u approaching zero at infinity. No monotonic-in-iteration premise is required: q_TT need not have a fixed sign, so positivity of the iterates does not mean the iterates increase.

For any positive-T bounded decaying classical solution outside the chosen box, a negative minimum of u contradicts the positive source and massive operator. A positive maximum gives u<=B. Both extrema are attained when nonzero because u tends to zero. A bounded homogeneous massive C0 solution vanishes by the same comparison. Therefore every such solution is a box fixed point, proving the stated uniqueness, rather than merely uniqueness of an arbitrarily restricted numerical iterate. This does not establish uniqueness below the sufficient threshold. Rotation of a unique solution to the spherical source gives the same solution, hence radiality.

## Regularity and finite energy are actually justified

For the heat kernel, `||grad heat_s||_1<=sqrt(n/(2s))`; integrating against exp(-m²s) gives grad G_m in L1. Convolution with the continuous bounded forcing therefore makes u and grad u continuous. Newtonian y can have a norm cusp at a field zero, but q_T vanishes as y^(7/2), with y derivative O(y^(5/2)). The composition is locally C1 after this first bootstrap. Subtracting the forcing value in the second-derivative Green integral gives a residual O(distance), integrable against the local distance^-n Hessian kernel. This supplies C2 local regularity without the false inference that arbitrary continuous forcing alone yields C2.

The nonlinear forcing is bounded by h in L2. The elementary convolution L2 inequality using G_m and grad G_m in L1 gives u in H1. Positivity, h in L1 and the Green mass also give u in L1. These facts are sufficient for the asserted finite relative energy, and they use the smooth compact source, not an unregularized point-source action.

## Independent modulus-energy Hessian and minimum

The correct functional is at fixed Phi_N/source:

`Erel[u]=integral [Z|grad u|²/2+Zm²u²/2-kappa(q(y,T0+u)-q(y,T0))]dx`.

The subtraction matters: in n=3 the bare q term has the usual logarithmic isolated MOND IR divergence. Without subtracting this T-independent baseline, claiming a finite global minimum would be misleading. For u>=0 the nonlinear difference is bounded by h u, so the energy is finite on H1 and bounded below by the positive gradient/mass quadratic minus `kappa ||h||_2 ||u||_2`. Its weak first variation is exactly the modulus equation; the verified H1 solution makes it vanish for all admissible H1 tests.

Independently differentiating twice gives

`delta²Erel[w,w]=integral [Z|grad w|²+(Zm²-kappa q_TT(y,T0+u))w²]dx`.

Using the uniform derivative bound gives

`delta²Erel>=Z||grad w||_2²+(Zm²-3kappa pi/(2T0))||w||_2²`.

The same condition L<1 makes this uniformly strictly positive. Integrating the bound along a segment of the nonnegative H1 cone proves a strict global cone minimum, including unbounded H1 competitors for which T>=T0 almost everywhere; the uniform h bound keeps the functional integrable. For positive-T finite-energy competitors with negative u on some set, clipping u to max(u,0) lowers the gradient and mass terms and increases q, hence lowers its negative contribution. The extension beyond the cone is therefore justified in the stated admissible class.

This Hessian differentiates **only T with Phi_N held fixed**. Holding the Newtonian source potential fixed is legitimate for the reduced NR modulus equation because the Phi variation first constrains Phi_N from the prescribed rho independently of T. It is not evidence of a positive coupled gravitational block: the Phi/Phi_N cross-gradient action is a saddle, and varying the matter configuration, time propagation or a metric adds other obligations. No full-action stability assertion should be inferred from this restricted minimum.

## Nonlinear, finite-stiffness tail and physical force

At any fixed finite parameters covered by the theorem, u tends to zero. Hence the exact source has

`q_T(y,T0+u)=[8/(7T0³)]y^(7/2)(1+o(1))`.

For spherical compact support, this is a positive regularly varying radial tail A r^-k. The Green convolution retains the leading tail times its mass. The author's displacement split at sqrt(r) is valid: on the inner part the source ratio tends uniformly to one; on the outer part bounded forcing divided by r^-k is dominated by an exponentially small kernel tail. The heat-kernel inequality

`exp(a|z|)<=sum_sign exp(a sign.z)`

and Gaussian moment integration give

`integral exp(a|z|)G_m(z)dz<=2^n/(m²-na²)` for 0<a<m/sqrt(n),

which verifies the claimed exponential-tail domination. Thus

`u=8kappa y^(7/2)/(7Zm²T0³)(1+o(1))`

at finite Z, with no large-Z limit needed. This is a leading coefficient only; the report correctly avoids carrying the parent's stronger two-remainder estimate into the nonlinear theorem without additional estimates.

Integrating the actual varied physical Poisson equation gives `r^(n-1)(Phi'-nu Phi_N')=C_flux`. Regular central flux without an added singular mass fixes C_flux=0, even when the deep-MOND central force is only Hölder continuous. Therefore g=nu(y,T)g_N is exact; no gradient of T was dropped. The nonlinear cutoff-induced inward force-magnitude correction is

`Delta g=16kappa a0 y^6/(7Zm²T0^6)(1+o(1))`

`=8a0³ y^6/[7 Omega_(n-1)G_n Zm²T0^6](1+o(1))`.

The signed outward radial acceleration changes by -Delta g. The n=3 tails are respectively r^-7 for u and r^-12 for the force correction. This genuinely strengthens the prior perturbative result within the proven class, while T0, V0, a0 and any vacuum dictionary remain supplied inputs.

## Computation audit and obligations

The frozen 21 passing checks verify symbolic constants and a bounded discretized example. I independently checked the transformed kernel quadrature, radial Green weights and center normalization: t=y v² gives exactly the script's `4y² integral v³ c_T dv`; the three-dimensional radial Green convolution has the stated exp/sinh factors and center limit. The 1201/2401 grids, 32 Gauss nodes, radius24 and at most30 iterations are a finite-domain approximation; truncation of the extended source beyond radius24 is real, and a small grid change is not a continuum error certificate. The report explicitly respects that limitation.

The revised pure-Yukawa control now removes the actual particular-tail candidate and recomputes the leading radial operator residual. The all-stiffness witness violates the strict contraction condition, while the omitted-T-gradient control loses the actual variation term. Each rejects one unchanged obligation rather than promoting a failed run into an alternative theory. The four standard manifests are independently validated against current input/output hashes. No scientific inputs, controls or parent files were changed by this review.

Passed: action sign/normalization, global kernel bounds, positive map, strict contraction, uniqueness scope, regularity bootstrap, finite relative energy, restricted Hessian, finite-Z tail, physical force flux and finite computation interpretation. Out of scope: full QUMOND/gravity positivity, causal modes, self-consistent matter equilibrium, observational viability and any vacuum/32pi selection. No blocking mathematical gap remains in the stated theorem.
