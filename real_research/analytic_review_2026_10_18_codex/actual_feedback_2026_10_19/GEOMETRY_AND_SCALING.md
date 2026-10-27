# Actual smooth hollow-halo geometry and uniform fixed-warmth scaling

Date: 2026-10-19. Owner: `/root/actual_geometry`. Base repository revision:
`62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Scope: analytical derivations only;
no numerical integration, scientific code, discretized arrays, or scientific
process was used. This is a new temporary artifact, with no repository edit.

## Inputs and exact scope

The following raw sources were read:

* `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`,
  SHA-256 `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
* `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`,
  SHA-256 `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
* `real_research/analytic_review_2026_10_18_codex/finite_halo_2026_10_18/BOUNDARY_MATCHING.md`,
  SHA-256 `eab2312cf87a23267dd639c064ee8fb39a5b07d809e27ffae0b3eedd1557b774`.

These define an actual family of targets but do not select numerical values of
the four radii or the fraction. The results below exhibit actual members of
that same family; they do not establish a feedback estimate for an independently
selected, unspecified member. The exact DF inverse, exact mass profile and
exact force law are retained. The new choice is a baryon-dominated radial scale
and a small, positive tether fraction. Neither a cold limit nor a tracer
replacement is taken in the asserted fixed-warmth statements.

## 1. An explicit nonempty subfamily with uniformly monotone frequency

Put `r_M=M_b/A`, `A=sqrt(a_0 M_b/G)`. Choose

\[
0<\epsilon\le 1/4096,\qquad \ell=\epsilon r_M,\qquad f=\epsilon^2,
\qquad(r_0,r_1,r_2,R)=\ell(1,2,3,4).
\tag{1}
\]

Write `rho=r/ell` and `M(r)=A ell p(rho)`. Then the *actual* specified cutoff
gives

\[
p(\rho)=\rho S(\rho-1)\quad(1\le\rho\le2),\qquad
p(\rho)=\rho\quad(2\le\rho\le3),
\]
\[
p(\rho)=3+\int_3^\rho[1-S(u-3)]\,du\quad(3\le\rho\le4).
\tag{2}
\]

Outside this range continue by zero inside and constant outside, as in the raw
source. We use exact integrals to define the profile, with no evaluation of them.
In particular `0<=p<=rho`, `p'>=0`; where `p''>0` necessarily `rho<=2`.

### Elementary derivative bounds for the actual S

On `0<z<1`, put `b(z)=-1/z+1/(1-z)`, so

\[
S=(1+e^{-b})^{-1},\quad b'=z^{-2}+(1-z)^{-2},\quad
b''=-2z^{-3}+2(1-z)^{-3},
\]
\[
S'=S(1-S)b',\quad
S''=S(1-S)\{b''+(1-2S)(b')^2\}.
\]

Symmetry reduces absolute derivative bounds to `z<=1/2`. There
`S<=e^2 e^{-1/z}`. With `u=1/z>=2`,

\[
S'\le e^2e^{-u}(u^2+4)\le8,
\]
\[
|S''|\le e^2e^{-u}(u^4+2u^3+8u^2+32)
\le256/e^2+54/e+64<160.
\tag{3}
\]

The last bounds use the elementary maximum of `u^m e^{-u}` and `e>2`;
these are analytic inequalities, not numerical evaluations. Thus

\[
0\le p'\le17,\qquad |p''|\le336.
\tag{4}
\]

For later use set

\[
B_p=\rho^2p''-\rho p'-3p,
\quad C_p=2(p')^2+2pp''-10pp'/\rho+5p^2/\rho^2.
\]

Since a positive `p''` occurs only for `rho<=2`, and `p/rho<=1`,

\[
B_p\le1344,\qquad C_p\ge-8\cdot336-10\cdot17=-2858.
\tag{5}
\]

### Exact epicyclic derivatives

Normalize squared angular momentum by `lambda=L/(GM_b ell)` and frequency by
`Omega_*=(GM_b/ell^3)^{1/2}`. Write `kappa_i=Omega_* K_i` and use prime for
`rho` derivatives in the rest of this section. Direct differentiation of the
*actual* circular laws gives

\[
\lambda_{cf}=\rho[1+\epsilon p],\qquad
\lambda_{ct}=\rho[1+(1-f)\epsilon p]-f^2p^2/\rho,
\tag{6}
\]

\[
K_f^2=\frac{1+\epsilon(p+\rho p')}{\rho^3},\qquad
K_t^2=\frac{1+(1-f)\epsilon(p+\rho p')-f^2(p^2/\rho)'}{\rho^3},
\tag{7}
\]

\[
(K_f^2)'=\rho^{-4}[-3+\epsilon B_p],\qquad
(K_t^2)'=\rho^{-4}[-3+(1-f)\epsilon B_p-f^2C_p].
\tag{8}
\]

For (1), `1344 epsilon<=1` and `2858 epsilon^4<=1`. Therefore

\[
(K_f^2)'\le-2\rho^{-4},\qquad (K_t^2)'\le-\rho^{-4}.
\tag{9}
\]

This proves strict monotonicity on the *entire* closed actual shell, including
both tapers, without leaving a taper inequality to check. Also, from (6),

\[
1/2\le\lambda_{ci}'\le2,\qquad 1/128\le K_i^2\le2.
\tag{10}
\]

Indeed the only negative contribution in `lambda_ct'` is at worst
`34 epsilon^4`; the upper bound follows from `p+rho p'<=72` and
`|(p^2/rho)'|<=35`. These inequalities imply the common quantitative gap

\[
\partial_\lambda\widetilde\Omega_i(0,\lambda)
=K_i'(\rho)/\lambda_{ci}'(\rho)
\le-1/(1024\sqrt2),
\tag{11}
\]

where `widetilde Omega=Omega/Omega_*`.

### Deep-cubic and core restrictions are preserved

The parent requires `r_0 >> f r_M` for controlled use of the deep-cubic law and
`r_0>2 f^2 r_M/(1-f)` for its global circular-well proof. Here

\[
f r_M/r_0=\epsilon,\qquad
\frac{2f^2r_M}{(1-f)r_0}=\frac{2\epsilon^3}{1-\epsilon^2}<1.
\tag{12}
\]

Thus the small-parameter family improves the stated deep-cubic control rather
than violating it. It still has two positive species and the exact `M=Ar`
law annulus. Its law annulus is baryon dominated; no dark-dominated annulus is
asserted by this subfamily construction.

## 2. One positive warmth delta can be selected uniformly in epsilon

Use dimensionless potential `phi=Phi/(GM_b/ell)`. Let

\[
V_p(\rho)=-\int_\rho^\infty p(u)u^{-2}\,du,\qquad
V_{p^2}(\rho)=\int_\rho^\infty p(u)^2u^{-4}\,du.
\]

Then the exact potentials are

\[
\phi_f=-1/\rho+\epsilon V_p,
\qquad
\phi_t=-1/\rho+(1-\epsilon^2)\epsilon V_p+\epsilon^4V_{p^2}.
\tag{13}
\]

They form smooth families all the way to `epsilon=0` on every compact radial
interval bounded away from zero. All physical derivative bounds required by the
exact inverse are therefore uniform for `0<=epsilon<=1/4096`. The common
dimensionless intrinsic scale is

\[
H(\rho)=\frac{(\rho-1)^2(4-\rho)^2}{27},\qquad d\rho/d\xi=H(\rho).
\tag{14}
\]

The normalized target is always a scalar multiple of the *same* function
`u_0(xi)=p'(rho(xi))`; its quantitative exponential edge bounds, intrinsic
logarithmic derivatives and weight-comparison constants are independent of
epsilon. Uniformity of the orbital Taylor expansion follows from (10), (13)
and (14). The nonlocal-exclusion bound in the raw inverse uses only a positive
lower bound for `lambda_c'` and an upper radius bound, which are uniform here.
The edge-distance-to-H ratios are fixed by (14). Circular energies stay a
uniform negative distance below escape: at epsilon=0 they are `-1/(2rho)`,
and (13) is a uniformly small perturbation on the closed shell.

Consequently there is one `delta_0>0`, independent of epsilon and of species,
such that every tube `0<=t<delta_0^2` stays strictly inside the hollow shell,
below escape, and in the uniform local geometry. The inverse error estimates
have uniform constants `||E_{delta,epsilon}||_{X_s->X_s}<=C_s delta`, and their
one-derivative smoothing bounds are uniform as well. Choose one *fixed*
`0<delta<delta_0` small enough for the X_5 inverse and the two positivity
estimates. This is a single choice, made before epsilon is taken smaller for a
feedback estimate. It never tends to zero as epsilon tends to zero.

There is no hidden need to invert in every X_s by a separate smallness
condition: invert first in X_5 and use the one-derivative smoothing identity
`q=e-E_delta q` inductively. For each fixed s this gives a uniform X_s bound.

## 3. Exact normalization and uniform distribution scaling

Define

\[
v_*=(GM_b/\ell)^{1/2},\qquad
j=J/(GM_b\ell)^{1/2},\quad e=E/(GM_b/\ell),
\quad \tau=\Omega_*t_{physical}.
\tag{15}
\]

The phase Jacobian is

\[
dr\,dv\,dL=(GM_b\ell)^{3/2}\,d\rho\,d\widetilde v\,d\lambda.
\]

Thus the dimensionless DF and susceptibility are

\[
\widetilde F_i=\frac{(GM_b\ell)^{3/2}}{M_b}F_i,
\quad
\widetilde w_i=-\partial_e\widetilde F_i
=\frac{(GM_b\ell)^{3/2}}{M_b}\frac{GM_b}{\ell}w_i.
\tag{16}
\]

The exact target shell densities per `d rho` are

\[
\widetilde\mu_f=\epsilon(1-\epsilon^2)p',\qquad
\widetilde\mu_t=\epsilon^3p'.
\tag{17}
\]

All pieces of the raw inverse are linear in their target once the target
potential is fixed: H_0, the residual e, q and the reconstructed H. Its norms
use the weight u, so a scalar multiplier of u cancels exactly from the relative
norm. The operator itself depends on the normalized potential through (13),
but has the uniform bounds just proved. It follows that the actual exact DFs
have the form

\[
\widetilde F_f=\epsilon(1-\epsilon^2)\mathfrak F_{f,\epsilon},
\quad \widetilde F_t=\epsilon^3\mathfrak F_{t,\epsilon},
\]
\[
\widetilde w_f=\epsilon(1-\epsilon^2)\mathfrak w_{f,\epsilon},
\quad \widetilde w_t=\epsilon^3\mathfrak w_{t,\epsilon}.
\tag{18}
\]

For each fixed derivative order, the normalized functions in (18) have bounded
C^m norms uniformly in epsilon, with delta fixed. This holds in physical
dimensionless variables and invariant coordinates, and after passage to
`(j,lambda)` or `(a,lambda)` with `a=sqrt(j)`. To justify the edge extension
explicitly: each derivative of the inverse formula introduces only finitely
many inverse powers of H and distance to an endpoint; every such factor is
dominated by the fixed exponential flatness of p'. The normalized H derivatives
have the same uniform weighted bounds. The flat energy cap and the arbitrary
smooth extension below t=0 in the raw construction also have uniform constants.
Thus extension by zero at the lambda ends and at the top energy cap preserves
all these uniform derivative estimates. At j=0 use the existing smooth lower
extension in t, or equivalently the even smooth extension in a.

In particular (18) is an actual susceptibility estimate, not just small total
mass. It supplies the O(epsilon) source norm required for a perturbative
boundary feedback estimate, with constants that can depend on the fixed delta.

## 4. Uniform action frequency and period regularity

This section gives a direct argument for the period regularity used above. In
a fixed compact chart one can take `1/2<=lambda<=6` and `0<=j<=j_*`, with
one sufficiently small `j_*>0` independent of epsilon; all these orbits stay
in `1/4<=rho<=8`. The occupied lambda range is contained in `[1,5]` by (6).
The potentials on the enlarged radial chart are smooth uniform perturbations
of Kepler, their circular wells are uniformly nondegenerate, and compactness
gives the common j_* and the uniform Morse charts. Thus no changing-domain
or endpoint chart is hidden in the parameter-uniform assertions. In
a neighborhood of each nondegenerate circular well let

\[
y=\operatorname{sgn}(\rho-s)\sqrt{2[U(\rho,\lambda)-E_c(\lambda)]},
\qquad \rho=R(y,\lambda,\epsilon).
\]

The parameter-dependent Morse coordinate and its inverse have uniformly
bounded derivatives because the potentials have uniform C^m bounds and their
second derivatives at the well have a common positive lower bound. If
`eta=e-E_c` and `b=sqrt(2 eta)`, then

\[
T(\eta,\lambda,\epsilon)
=2\int_{-1}^1\frac{R_y(bz,\lambda,\epsilon)}{\sqrt{1-z^2}}\,dz,
\]
\[
j(\eta,\lambda,\epsilon)
=\frac{2\eta}{\pi}\int_{-1}^1
\sqrt{1-z^2}R_y(bz,\lambda,\epsilon)\,dz.
\tag{19}
\]

The odd terms cancel in these integrals, so they are smooth functions of eta
at eta=0 with uniform bounds on every fixed derivative. Since
`partial_eta j=T/(2pi)>0`, the inverse eta(j,lambda,epsilon) and
`widetilde Omega=2pi/T` are uniformly smooth. This is a proof using exact
integral representations, not a numerical period calculation.

The occupied actions satisfy `sup j<=C delta^2`, uniformly in epsilon.
Combine the derivative bound from (19) with (11) and, if necessary, make the
single fixed choice of delta smaller. Then throughout the entire closed
occupied action set, for both actual species,

\[
\partial_\lambda\widetilde\Omega_i(j,\lambda)\le-c_*<0,
\tag{20}
\]

where c_*>0 is independent of epsilon. In particular no interior critical
point of the actual frequency occurs for these fixed-warmth members, and the
strong boundary transversality condition in raw (ND) also holds. Equation (20)
uses continuity plus a uniform bound on `partial_j partial_lambda Omega`; it
does not infer a nonzero derivative merely from qualitative strict monotonicity.

## 5. Scaling of the actual feedback kernel and its limits

If perturbation masses are normalized by M_b and potentials by GM_b/ell, the
actual shell kernels become

\[
\widetilde P_{ff}=\widetilde P_{ft}=\widetilde P_{tf}
=-1/\max(\rho,\rho'),
\]
\[
\widetilde P_{tt}
=2\frac f\epsilon\int_{\max(\rho,\rho')}^\infty p(u)u^{-4}\,du
=2\epsilon\int_{\max(\rho,\rho')}^\infty p(u)u^{-4}\,du.
\tag{21}
\]

Together with (18), all free-sourced entries of the actual boundary feedback
operator carry epsilon, tether-to-free carries epsilon^3, and tether-to-tether
carries epsilon^4. Uniform frequency transversality and source regularity hold
for a common fixed delta. Therefore a boundary singular-integral estimate with
constants depending only on these uniformly bounded inputs proves
`||K_+||<=C_delta epsilon`. The independent spectral work package must establish
that estimate (including its frequency and harmonic weights); (21) alone is
not its proof. Once that estimate is proved, choosing epsilon still smaller is
a legitimate choice of an actual member of the existing exact family and
Neumann inversion is genuine, without a new spectral hypothesis.

Radial locality alone does not exclude embedded modes for an arbitrary fixed
member: local kernels can support oscillatory eigenfunctions, and no sign or
unique-continuation estimate follows from finite interaction range. In this
subfamily it is the uniform small *susceptibility* in (18), after dimensionless
normalization and at fixed positive warmth, that can close the full inversion.

## 6. A separate exact identity: epicyclic extrema need not be full critical points

For any of the actual smooth central potentials let `K(s)=kappa(s)^2`, now in
arbitrary consistent physical or dimensionless units. At the circular well,

\[
U_{rrr}=K'-3K/s,\qquad
U_{rrrr}=K''-3K'/s+15K/s^2.
\tag{22}
\]

The radial oscillator normal form gives

\[
\partial_J\Omega(0,L)
=\frac{U_{rrrr}}{8K}-\frac{5U_{rrr}^2}{24K^2}
=\frac{K''}{8K}+\frac{7K'}{8Ks}-\frac{5(K')^2}{24K^2}.
\tag{23}
\]

This follows by expanding the exact period integral in (19), or by the
quadratic, cubic and quartic one-dimensional oscillator normal form. At a
circular stationary epicyclic frequency,

\[
K'(s_c)=0\quad\Longrightarrow\quad
\partial_J\Omega(0,L_c(s_c))=K''(s_c)/(8K(s_c)).
\tag{24}
\]

Consequently a nondegenerate epicyclic maximum/minimum has a *nonzero full
action gradient*. If every zero of K' is simple, compactness proves that
`grad Omega` remains nonzero throughout a sufficiently narrow warm tube,
even though the extra circular-line derivative demanded by raw (ND) fails.
This is a proved improvement of the bare critical-point test; no assertion
that all actual members satisfy its simple-zero premise is made.

The boundary geometry at such a stationary point is also favorable. Because
`partial_LL Omega(0,L_c)=kappa''/(L_c')^2`, its local normal form starts with

\[
\Omega-\Omega_c
=\frac{\kappa''}{4\kappa}J
+\frac{\kappa''}{2(L_c')^2}(L-L_c)^2
+O(J^2+J|L-L_c|+|L-L_c|^3).
\tag{25}
\]

The two leading coefficients have the same sign. A source amplitude vanishing
as J^beta has frequency pushforward density O(|nu-nu_c|^{beta+1/2}) in this
local model: solve for J and integrate L over an interval of length
O(sqrt(|nu-nu_c|)). Nonzero angle harmonics of a radial C^gamma test function
vanish at least as J^{gamma/2}; the shell potential harmonic is O(J^{1/2}).
Thus the response amplitude has beta>0 and a vanishing boundary density.
This resolves the *local scalar threshold geometry* at a simple epicyclic
extremum. It does not by itself constitute all operator-valued bounds required
by raw Lemma T for arbitrary profiles.

## 7. Why no statement about arbitrary unpinned members is justified

There are actual deep-cubic profiles where kappa_f is nonmonotone. A useful
fully analytic uniform obstruction follows by evaluating the raw inner-taper
inequality at z=1/4. Let q=exp(8/3), s=S(1/4)=1/(1+q), and

\[
c_0=\tfrac14S'(1/4)+\tfrac1{16}S''(1/4)-4S(1/4)
=\frac{s}{81}(1012-4536s+3200s^2)>0.
\tag{26}
\]

Indeed q>7 implies s<1/8, and q<27 implies s>1/28; elementary exponential
series bounds give both. Hence `c_0>445/2268`. At this z, with
`u=r/Delta=r_0/Delta+1/4>=1/4`, the left minus the `4rS` term in raw (7.1)
is `r[u S'+u^2 S''-4S]>=r c_0>=r_0 c_0`, since S',S'' are positive here.
Therefore if `r_0> (6804/445) r_M`, the free frequency derivative is positive
somewhere in the inner taper for *every* Delta, whereas it is negative at the
flat edges. Such choices are consistent with the deep restriction (take f
small, or simply r_0 sufficiently large). Thus uniform monotonicity of the
whole source family is false. This does not prove a full action-frequency
critical point, by (24), and does not disprove a full work bound.

The actual new results are (9), (18), (20), (21) and (24), with their exact
quantifiers. The full arbitrary-fixed-member feedback theorem remains a
different target; a proof for the explicitly selected subfamily must retain
that distinction.
