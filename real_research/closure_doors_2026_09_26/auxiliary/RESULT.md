# A repaired auxiliary problem for the exact exponential kernel

**Constructive result:** the fixed-metric, fixed-lapse auxiliary equation has a
uniformly convex variational completion using a lapse-adapted heat operator.
The original geometric filter also has a rigorous sufficient convexity bound
in a controlled lapse range. Neither result proves physical-time stability of
the coupled metric and clock.

Base `03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`; input is the exact C-H action
`qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`, not an
inferred model from a passing script. A concurrent task committed XC2 as
`f3b848273e635b81bc328882db0ffb4206d86e45`; its weighted-contraction inference
motivated the discriminator below. This note changes no XC2 source or result.

## Precise problem and exact kernel

On a smooth closed connected spatial leaf, fix a smooth positive lapse N and
metric h; let a=D ln N. Let α=a0/c²>0 and b≥0 (b>0 for genuine smoothing;
b=0 means S=Id). Fix the constant mode of U by its weighted mean. Consider

\[
E[U]=\int N\,dV_h\left[2|DU-a|^2+J(DSU)\right],\qquad
J(p)=2\alpha^2q(|p|^2/\alpha^2).
\]

For x≥0, s=x(1−exp(−x)), the exact constitutive primitive is

\[
q(s^2)=2sx-[x^2+2(1+x)e^{-x}-2]-s^2
=2-2(1+x)e^{-x}-x^2e^{-2x}.
\]

Because dq/ds=2x exp(−x)≥0 and its endpoints are 0 and 2,
0≤q≤2. Its vector integrand is C¹, including at p=0, and
\(|\nabla_pJ|=4\alpha x e^{-x}\le4\alpha/e\).
For p≠0 its Hessian eigenvalues are 4CT and 4CL, with

\[
C_T=\frac1{e^x-1}>0,\qquad
C_L=\frac{1-x}{e^x+x-1}\ge-d,
\qquad d=\frac1{e^2+1}<\frac18.
\]

Differentiating CL gives \(e^x(x-2)/(e^x+x-1)^2\), so its minimum is at x=2.
Consequently J(p)+2d|p|² is convex. The assertion extends through p=0 by the
continuous first derivative and the nonnegative second derivative along every
line away from its zero; it does not pretend J is C² at zero.

## The original weighted claim is too strong

The geometric heat operator S=exp(bΔh) contracts the *unweighted* Dirichlet
norm. The action uses N dVh, in which this S is generally not self-adjoint.
An exact circle counterexample is

\[
N=1+\tfrac45\cos9x>0,\quad
v=\sin x-\tfrac1{50}\sin10x,
\]
\[
\frac1\pi\|D e^{t\Delta}v\|_N^2
=e^{-2t}+\tfrac1{25}e^{-200t}-\tfrac4{25}e^{-101t}.
\]

The value at t=0 is 22/25; its derivative is **154/25>0**. Thus the asserted
weighted contraction fails even on a smooth flat closed leaf. The circle embeds
in the original T³ domain by making all fields independent of the other two
coordinates.

There is also a resolved counterexample using the actual exponential kernel,
rather than an arbitrary negative-Hessian function. Use b=.02,
N=10⁻⁸+exp[1000(cos x−1)], Ubase=exp(b)s(2)sin x and
v=sin x−sin(10x)/10. Direct quadrature of the second variation gives
**−0.02522828926**, stable under grids 2048, 4096, 8192 and 16384. The weighted
gradient-energy ratio is 106.9353. This is numerical evidence about a declared
off-shell fixed-lapse problem, not an on-shell spacetime instability or a ghost.
The exact Fourier counterexample above already disproves the missing analytic
inequality independently of that numerical example.

## Repair 1: a sufficient bound for the unchanged filter

Let rN=Nmax/Nmin. Weighted/unweighted norm comparison gives

\[
\|DSv\|_N^2\le r_N\|Dv\|_N^2,
\qquad
E''[U](v,v)\ge4(1-d r_N)\|Dv\|_N^2
\]

where a classical second derivative exists. The equivalent finite-difference
strong-convexity inequality remains valid through zero gradients. Therefore
rN<exp(2)+1≈8.389 is sufficient for uniqueness; rN<8 is a simpler conservative
bound. This covers a controlled weak-lapse-contrast domain. Failure of this
sufficient bound does not by itself prove nonconvexity for a particular N.

## Repair 2: a new filter matched to the action measure

Define explicitly

\[
\Delta_N f=N^{-1}D_i(ND^if),\qquad S_N=e^{b\Delta_N}.
\]

On the closed leaf, integration by parts gives
\(\langle f,-\Delta_N g\rangle_N=\langle Df,Dg\rangle_N\).
For its orthonormal eigenbasis with eigenvalues λj≥0,

\[
\|DS_Nv\|_N^2=\sum_j\lambda_j e^{-2b\lambda_j}|v_j|^2
\le\sum_j\lambda_j|v_j|^2=\|Dv\|_N^2.
\]

Replace S by this specifically defined SN in E. The result satisfies

\[
E[U+v]+E[U-v]-2E[U]
\ge4(1-d)\|Dv\|_N^2>0
\]

for nonconstant v. This proves strict convexity modulo constants for every
smooth positive N in the declared fixed-geometry problem. A 48-cell weighted
spectral discretization independently checks the contraction, weighted
self-adjointness and the conservative 7/8 bound on the normalized Hessian.

Existence also follows by the direct method on any smooth closed connected
leaf. The nonnegative bounded J and quadratic first term give coercivity on
the weighted-mean-zero H¹ space by Poincaré's inequality. Weighted spectral
contraction makes SN bounded on H¹. The bounded gradient of J then makes its
integral norm-continuous on H¹, as is the quadratic term. The finite-difference
inequality above proves convexity of the complete continuous functional, so
it is weakly lower semicontinuous. A bounded minimizing sequence therefore
has a weak H¹ limit attaining the infimum. Strong convexity makes that minimizer
unique. The same proof applies to the unchanged geometric filter only in the
stated sufficient uniqueness domain rN<exp(2)+1. This argument does not rely
on Fourier diagonalization of the variable-coefficient weighted Laplacian.
The Sobolev/functional-analysis steps are not Lean-formalized here. The weak
first variation exists because J is C¹ with bounded first derivative; no C²
linearization at a zero gradient is needed for this fixed-background result.

This is a genuine change to the action. It requires the weighted heat
constraint \(\partial_zW=\Delta_NW\), whose adjoint now uses the same measure.
At fixed h,
\(\delta_N\Delta_N f=D(\delta\ln N)\cdot Df\); these new lapse vertices and
the full metric/clock variation must be retained. N transforms by a spatially
constant factor under clock relabeling, so ΔN is invariant under that relabeling.
The leading constant-lapse static filter agrees with the old filter, but this
does not establish unchanged nonlinear predictions, physical causality, or DOF.

## Verification and exact remaining implication

`weighted_heat_check.py` ran with bounded resources in `run2`, with 11 checks,
all passing. `run1` is superseded solely because its declared NumPy version was
wrong (the actual version is 1.26.2); the calculation itself passed. `run2` pins
the correct environment and input hashes. The exact Fourier and finite
spectral/transfer lemmas are formalized separately in
`fable_independent_2026/lean_2026/DoorsAuxiliary20260926.lean`.

The next implication is the coupled constraint and retarded physical response
of the *modified* action. An invertible convex auxiliary block does not ensure
a positive metric/clock Schur complement. In particular this repair does not
evade the response/inertia calculations in the parallel route, and the original
general-source QUMOND versus exact AQUAL distinction remains explicit.
