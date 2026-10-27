# FSP-005: independent boundary derivation before target inspection

Recorded 2026-10-19 UTC. This file was written before reading the target
`boundary_heat/INDEPENDENT_DERIVATION.md`, `REPORT.md`, addendum, code, or outputs.
The operator statement in the delegation and primary formulas below are the
inputs. `SOURCE_RECORDS.json` was consulted only to locate exact source bytes.
No target coefficient was supplied in the delegation.

## Claim card and source receipts

For one charged Matsubara conjugate pair, consider

\[
\Gamma_m=\operatorname{Tr}_{\mathbb C^4}\log(-\Delta+m^2)_{\rm rel}
-2\operatorname{Tr}_{\mathbb C}\log(-\Delta+m^2)_D,
\qquad m>0,
\]

on the smooth ball of radius R. Three vector components (two spatial tangents
and A4) are Dirichlet; the spatial normal has
`(partial_r+2/R)A_r=0`. The bundle Laplacian is flat in a Cartesian frame.
There is no additional factor 1/2 in this stipulated complex-pair trace.

Primary inputs checked: Vassilevich, hep-th/0306138v3, (3.58), (5.32),
(5.33), and BGKV, hep-th/9906144v1, Theorem 2.1(4)-(5).
Exact primary URLs:

- https://arxiv.org/pdf/hep-th/0306138v3
- https://arxiv.org/pdf/hep-th/9906144v1

Retained PDF SHA256 values, recomputed locally:

- Vassilevich: e819f9131352f0df3f617be60d4c2fbf47a7d42fcb267aa558cee9c592a71153
- BGKV: 5403c02a2d0c1d0b4dcf5d1dfd5c91fab09fe77950dce860deb5b68a11fc168d

The exact version stamps were also checked using the arXiv PDFs through web
access. Formula extraction and application were checked separately from hashes.
Sources use inward N, L_ab=delta_ab/R, and Robin `(nabla_N+S)Pi_+`.
Thus Pi_+=P_normal, S=-2P_normal/R, and chi=2P_normal-I_4.
The source theorem requires a smooth compact manifold, smooth boundary,
Laplace-type operator, and smooth mixed projectors. These hold for the constant
benchmark, and for any smooth extension of the scalar collar profile below.

## Direct heat contraction

Write the combined heat trace as H(t)=sum a_j t^((j-3)/2), or equivalently
`H(t)=(4*pi*t)^(-3/2) sum A_j t^(j/2)`.
The formal vector-minus-two-ghost trace has

\[
\operatorname{str}I=2,\quad
\operatorname{str}\Pi_+=\operatorname{str}\Pi_-=1,\quad
\operatorname{str}\chi=0,
\quad K=L_{aa}=2/R.
\]

The projector is not constant. In a Cartesian frame, for each of the two
spatial tangent directions,

\[
\chi_{:a}={2\over R}(e_a n^T+n e_a^T),
\quad \operatorname{tr}\chi_{:a}\chi_{:b}={8\over R^2}\delta_{ab}.
\]

Consequently

\[
\operatorname{tr}\chi_{:a}\chi_{:a}=16/R^2,
\quad \operatorname{tr}\chi_{:a}\chi_{:b}L_{ab}=16/R^3,
\quad \operatorname{tr}\chi_{:a}\chi_{:a}S=-16/R^3.
\]

In the a4 integrand, the three groups (universal L cubics, S terms, moving
projector terms) respectively give

\[
{1088\over7R^3},\qquad-{1344\over R^3},\qquad {1152\over R^3}.
\]

Their sum is -256/(7 R^3). Tangential derivatives of the traced S vanish on
the sphere, and ambient Riemann curvature and bundle curvature vanish.
It follows that

\[
\boxed{a_4=-{16\over315\sqrt\pi R}},\qquad
\boxed{A_4=-{128\pi\over315R}}.
\]

Using `log det=-integral dt H(t)exp(-m^2 t)/t`, the corresponding determinant
term is

\[
\boxed{\Gamma_m\big|_{1/(mR)}={16\over315mR}}.
\]

This is a local large-mR asymptotic coefficient. It is not a claim about an
entire determinant or the complete finite-size coefficient of a monopole.

## Independent TE/TM check, including l=0

The exact spatial relative one-form spectrum splits into exact gradients of
scalar Dirichlet eigenfunctions plus transverse TE and TM modes. A4 adds a
second Dirichlet scalar, which the two ghost traces cancel. Hence H is the
sum of the transverse TE and TM traces.

TE has `j_l(kR)=0`, l>=1. TM has `(r j_l(kr))'=0`, l>=1; its normal Robin
condition follows from transversality. Therefore

\[
H=H_D^{\rm scalar}+H_{\partial_r+1/R}^{\rm scalar}
-H_{D,l=0}-H_{\partial_r+1/R,l=0}.
\]

The subtracted roots are `kR=pi q`, q>=1, and `kR=pi(q+1/2)`, q>=0.
Together they form `pi q/2`, q>=1. Poisson summation gives

\[
H_{D,0}+H_{R,0}={R\over\sqrt{\pi t}}-{1\over2}
+O(e^{-4R^2/t}),
\]

so these necessary subtractions have no a4 term. Applying the pure scalar
formula to the two scalar problems gives

\[
a_4(D)=-{2\over315\sqrt\pi R},\qquad
a_4(\partial_r+1/R)=-{14\over315\sqrt\pi R}.
\]

Their sum agrees with the mixed projector result. There is no l=0 TE/TM
mode and no zero eigenvalue to add to this identity.

## Scalar profile: collar jets and convention

Set a=2*pi*n/L+v (signed), m=|a|>0, and

\[
P=-\Delta+(a-1/r)^2+M^2,
\qquad \mu^2=a^2+M^2,
\qquad U=-2a/r+1/r^2.
\]

Only a smooth boundary collar is used. The profile is singular at r=0;
extension through the interior is a separate problem. With inward N=-d/dr,

\[
U_b=-2a/R+1/R^2,\quad
U_{;N}=-2a/R^2+2/R^3,\quad
U_{;NN}=-4a/R^3+6/R^4.
\]

The bulk/surface convention is the integrated Duhamel convention: bulk
total derivatives are integrated by parts and their normal flux is included
in the surface contribution. The first scalar variation is exactly

\[
\delta\Gamma=\int_0^\infty dt\,e^{-\mu^2t}
\operatorname{Str}(Ue^{t\Delta}).
\]

In this convention the needed smeared boundary coefficients derived directly
from (5.31)-(5.32) are

\[
a_2^\partial[U]=(4\pi)^{-3/2}\int_\partial
 {-8\over3R}U,
\]

\[
a_3^\partial[U]={5\over8}U_b-{5R\over16}U_{;N}.
\]

In particular a3[1]=5/8 and a2^boundary[1]=-4R/(3 sqrt(pi)).
The a2 smearing derivative and a3 second-normal-derivative terms vanish
because str(chi)=0. Direct use of unsmeared a4 with E=-U yields an E_N
boundary term; it cancels the integrated bulk Delta E flux. Dropping one
without the other changes the declared bulk/surface convention.

At order R^-1 one must also keep the U_b^2 term multiplying a2[1]. Its
coefficient is fixed by expanding the exact constant-potential surface term
`-8 R sqrt(mu^2+U_b)/3`. One obtains

\[
\Gamma_{a_2}^{\partial}\big|_{R^{-1}}
={1\over R}\left[-{4\over3\mu}+{4a^2\over3\mu^3}\right]
=-{4M^2\over3\mu^3R}.
\]

For M=0 this vanishes: the linear and quadratic perturbations cancel.
The first variation from a3 gives

\[
{1\over\mu^2}\left({5\over8}U_b-{5R\over16}U_{;N}\right)
=-{5a\over8\mu^2R}+O(R^{-2}).
\]

Thus both the boundary value and the normal derivative are load-bearing;
using the boundary mass alone gives twice this odd-in-a term.

All other possible scalar jets at this order can be classified by their
R-scaling. The U_b^3, U_b U_N, and U_NN terms without geometric factors
cancel in the flat Neumann-plus-Dirichlet combination (str chi=0), with the
normal total derivative convention just specified. This also follows by
resumming a constant U_b in the first smeared variation: the flat N/D
image terms cancel. Terms quadratic in derivatives, or higher geometric
weight times any extra U, are O(R^-2) or smaller in the integrated surface
action. The surviving terms are the geometric cubic, K U_b^2, geometric
weight-two times U_b, and geometric weight-one times U_N, as above.

The resulting **local scalar-collar coefficient**, for fixed n and M, is

\[
\boxed{C(a,M)={16\over315\sqrt{a^2+M^2}}
-{4M^2\over3(a^2+M^2)^{3/2}}
-{5a\over8(a^2+M^2)}}.
\]

For M=0 this is `16/(315|a|)-5/(8a)`. This statement assumes the stipulated
scalar operator, not a matrix spin/field-strength perturbation. It is not a
proof of the full smooth monopole operator's boundary/global asymptotics.

## Common four-dimensional PV contract

Choose c0=1, M0=0 and common positive regulator masses for *every* vector
component and both ghost traces, with the original relative/Dirichlet
domains unchanged. One sufficient ultraviolet contract is
`sum c_j=sum c_j M_j^2=sum c_j M_j^4=0`.
At finite R and finite regulator masses define the four-dimensional object
before extracting any sector asymptotics:

\[
\Gamma_{\rm PV}(R)=-\int_0^\infty{dt\over t}
\left[\sum_jc_je^{-M_j^2t}\right]
\sum_{n\in\mathbb Z}\operatorname{Str}e^{-tP_n(R)}.
\]

For a smooth gapped background this common filter is applied before the
Matsubara sum, large-R expansion, and regulator removal. Formal coefficient
extraction produces `sum_n sum_j c_j C(a_n,M_j)`, which is absolutely
convergent at fixed regulator masses: the common PV cancellations remove the
1/|n| and 1/n tails. Absolute convergence of this coefficient series alone
does **not** establish a uniform remainder for the complete determinants.
That interchange remains an explicit analytic obligation.

The regulator term proportional to M^2 cannot be discarded sector by sector
before summing: its sum has a finite large-M limit since

\[
\sum_n {M^2\over(a_n^2+M^2)^{3/2}}\longrightarrow L/\pi.
\]

The odd term has the usual common-PV/resolvent sum; after regulator removal,
away from a_n=0, `sum 1/a_n=(L/2)cot(vL/2)` with symmetric summation. These
identities do not remove the even harmonic divergence or specify its finite
renormalization.

## Allowed local ambiguity and safe scope

On S^1_L times the spherical wall, a local boundary term

\[
\lambda\int_0^L dx_4\int_{S_R^2}d^2x\,K^3
=32\pi\lambda L/R
\]

has exactly the relevant inverse-radius scaling. Other cubic extrinsic
invariants are proportional on this wall. Its finite coefficient must be
fixed by an explicit boundary renormalization condition; regulator removal
alone cannot supply that condition.

**Independent raw verdict:** the constant smooth-ball benchmark is proved
for the stated operator. The local scalar-profile collar extension is
conditional on the declared integrated bulk/surface convention and scalar
operator restriction. Its promotion to a full summed/global coefficient
requires uniform asymptotics, a smooth core and complete operator data, and
a fixed finite boundary counterterm. No alpha fit or physical identification
has been made.
