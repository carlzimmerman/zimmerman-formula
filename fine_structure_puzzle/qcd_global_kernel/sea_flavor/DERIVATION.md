# The complete leading sea insertion at fixed regulator

## Source convention and a normalized baryon

Work at e=0 on a fixed background g. A source coordinate a denotes a spacetime
point, a vector index and the regulator integration weight. Repeated source
indices are summed or integrated with that weight. Set eta=e A and expand

\[
D_f(\eta)=D_0+m_f+q_f\eta_a V_a+
 \tfrac12q_f^2\eta_a\eta_b W_{ab}+O(\eta^3),\quad S_f=(D_0+m_f)^{-1}.
\]

The Euclidean factors of i are included in V and W. This convention avoids an
extra guessed sign when using continuum versus link-current vertices. W is
symmetric in a,b and is zero for a continuum Dirac operator linear in eta;
it is generally nonzero for gauge links. Improved-action vertices and source
derivatives of the baryon dressing/interpolator belong to the same expansion.

Let L be the change in the sea log determinant, summed over flavors. At zero
source define

\[
\ell_{f,a}=\operatorname{Tr}(S_f V_a),\quad
h_{f,ab}=\operatorname{Tr}(S_fW_{ab}-S_fV_aS_fV_b),
\quad L_a=\sum_fq_f\ell_{f,a},\quad L_{ab}=\sum_fq_f^2h_{f,ab}.
\tag{1}
\]

Cyclicity makes h symmetric. For a proton contraction B(eta), including all
identical-quark Wick contractions, the normalized QCD correlator is

\[
C(\eta)=\frac{\langle B(\eta)e^{L(\eta)}\rangle_0}
                   {\langle e^{L(\eta)}\rangle_0},\qquad C_0=\langle B\rangle_0.
\]

Differentiate the quotient before making any vacuum-symmetry simplification:

\[
C_{ab}=\langle B_{ab}\rangle+
 \operatorname{Cov}(B_a,L_b)+\operatorname{Cov}(B_b,L_a)
 +\operatorname{Cov}(B,L_{ab})+\kappa(B,L_a,L_b).
\tag{2}
\]

Here kappa is the joint third cumulant, e.g.
\(
\kappa(B,X,Y)=\langle BXY\rangle-\langle B\rangle\langle XY\rangle
-\langle BX\rangle\langle Y\rangle-\langle BY\rangle\langle X\rangle
+2\langle B\rangle\langle X\rangle\langle Y\rangle.
\)
This subtraction is stronger than keeping the ordinary covariance of B with
XY when one-current means are nonzero. In a charge-conjugation invariant
vacuum their means vanish, reducing the last term to Cov(B,L_a L_b). B need
not itself be charge-conjugation even. No positivity of these covariances is
assumed. The two identical-u contractions in a proton do not change the sea
trace algebra, but must both be present in B, B_a and B_ab.

## An exact two-plus-one reduction, including omitted classes

For delta=ms-ml and common flavor-independent vertices, use the operator
identity, without expanding delta,

\[
S_l-S_s=\delta S_lS_s=\delta S_sS_l.
\]

Consequently the **complete charge-weighted single-current sea loop** is

\[
L_a=\frac{\delta}{3}T_a,\qquad
T_a=\operatorname{Tr}(S_lS_sV_a).
\tag{3}
\]

The two-current same-loop insertion is a different object:

\[
L_{ab}=\frac59h_{l,ab}+\frac19h_{s,ab}
       =\frac23h_{l,ab}+\frac19(h_{s,ab}-h_{l,ab}).
\tag{4}
\]

Combining (2)-(4) gives a reduced **complete sea correction** to the normalized
two-current proton kernel:

\[
\boxed{C^{sea}_{ab}=
 \operatorname{Cov}\!\left(B,\frac59h_{l,ab}+\frac19h_{s,ab}\right)
 +\frac{\delta}{3}\{
 \operatorname{Cov}(B_a,T_b)+\operatorname{Cov}(B_b,T_a)\}
 +\frac{\delta^2}{9}\kappa(B,T_a,T_b).}
\tag{5}
\]

The term left to add is the valence-only kernel <B_ab>. Equation (5) uses the
actual 2+1 gauge measure and actual valence masses; it does not reweight the
ensemble to a symmetric theory or truncate in delta. In particular a measured
same-loop temporal moment does not determine the two extra cumulant classes.

For completeness the same-loop difference can also be evaluated without a
subtraction of nearly equal traces. With P=S_l S_s,

\[
h_{s,ab}-h_{l,ab}=\delta\operatorname{Tr}
 [-P W_{ab}+P V_a S_s V_b+S_lV_a P V_b].
\tag{6}
\]

At a finite nonsingular regulator, analyticity near delta=0 gives the first
allowed orders:

| Class | Exact explicit factor | First allowed order |
|---|---|---|
| Same-loop two-current sea | 5 h_l/9+h_s/9 | delta^0 |
| One valence current, one sea loop | delta times a covariance | delta^1 |
| Two separate one-current sea loops | delta^2 times a joint cumulant | delta^2 |

These are allowed orders, not guarantees that their coefficients are nonzero.
At fixed ml and fixed valence masses the leading mixed coefficient is
\([\operatorname{Cov}_0(B_a,T_b^0)+\operatorname{Cov}_0(B_b,T_a^0)]/3\),
where T_a^0=Tr(S_l^2 V_a), and the leading two-loop coefficient is
kappa_0(B,T_a^0,T_b^0)/9. Changes of the sea measure enter only at the next
order for those two classes. Flavor symmetry does not force these proton
coefficients to vanish. The benchmark exhibits nonzero coefficients.

The first-order same-loop coefficient is path dependent. Its explicit loop
variation is h'_l/9 at fixed ml, but -h'_l/9 at fixed average mass
(2ml+ms)/3; the response of the measure and valence contractions must also be
included. The explicit factors in (3) and (5) remain correct on both paths.
They do not bound a physical-mass truncation or justify exchanging the chiral,
continuum, volume and small-curvature limits. Vertex/mass improvement factors
that differ by flavor require extra terms. A bare additive-mass identity alone
does not settle a renormalized mass-dependent-current convention. Charm and
heavier flavors must be added explicitly for a theory that contains them;
their nonzero charges are not removed by the u,d,s cancellation.

## A complete sea estimator rather than an alpha fit

With independent zero-mean noise of E[eta eta^dagger]=1, a split-even trace
estimate is

\[
\widehat T_a=\frac1{N}\sum_r\eta_r^\dagger S_sV_aS_l\eta_r.
\tag{7}
\]

It is unbiased by cyclicity. Multiplication by delta/3 is performed before
the ensemble covariance, avoiding independent noisy estimates of l and s.
For T_a T_b use independent noise pools or the off-diagonal U-statistic
\(\sum_{r\ne s}\widehat T_{a,r}\widehat T_{b,s}/[N(N-1)]\).
Reusing the same noise in an uncorrected product creates a finite-noise bias.
The same-loop trace h is not a product of two one-current traces: estimate its
composite matrix trace directly, or use independently paired propagator
estimators together with its W contact. Gauge sample covariances/cumulants
also require the appropriate finite-sample correction or a consistent large-N
estimator, and autocorrelation control. Flavor cancellation does not remove
gauge noise or guarantee an economical calculation on a curved regulator.

The light-minus-strange and split-even strategy is **known after translation**
from Harris et al., arXiv:2301.03995v2, equations (11)-(19), not a new physical
prediction. Their equations (6),(7) distinguish the two sea topologies. Their
actual preliminary variance test is flat QED_L at a heavy pion mass. The v2
revision of 1 May 2026 corrects equation (8), an approximate variance formula;
no exact Gaussian factorization of gauge covariances is used here. The added
content of (5) is a direct, contact-complete normalized-baryon formulation and
its transfer to the declared curved vacuum, not a global novelty claim.

## Photon convolution, mass matching, and the vacuum

Let G_ab(g)=<A_a A_b> be the canonical free-photon covariance on that SAME
regulated geometry. Gaussian integration and u=e^2 give

\[
\partial_u C\big|_0=\tfrac12G_{ab}C_{ab}+C_u^{ct},\qquad
M_u=-\lim_{T\to\infty}\frac1T
 \left[\frac{G_{ab}C_{ab}}{2C_0}+\frac{C_u^{ct}}{C_0}\right].
\tag{8}
\]

This uses a flat, or otherwise justified transfer-matrix, proton mass
extraction. On a compact sphere no flat large-T limit is silently assumed;
the mass used for matching is obtained in its declared flat reference theory.
The local terms C_u^ct contain mass, strong-coupling, improvement and operator
renormalization insertions along the chosen parameter path. A charged proton
also needs a declared gauge fixing or gauge-invariant electromagnetic dressing.
Its derivatives are included in B. Equation (8) is a finite-regulator leading
derivative, not a subtracted dispersion estimate or finite-alpha result.

In the unconditioned vacuum there is no baryon B. The leading effective sea
action insertion after photon integration is

\[
I_g=-\tfrac12G_{ab}\left[
 \tfrac59h_{l,ab}+\tfrac19h_{s,ab}+\tfrac{\delta^2}{9}T_aT_b\right]
 +S_u^{ct},\qquad W_u=\langle I_g\rangle.
\tag{9}
\]

No mixed valence-sea term exists in this vacuum. Any nonzero one-current
vacuum mean is retained by (9); charge conjugation normally sets it to zero.
The canonical free-photon determinant is independent of u and hence does not
contribute to W_u, but its metric response remains part of W itself. Photon
normalization/Jacobian conventions must be kept consistent with local gravity
counterterms. If t=log(radius), V=Omega exp(4t), and T_g is the derivative of
the e=0 QCD effective action including its measure, then exactly

\[
\rho_u(g)=\frac1{4V}\{\langle\partial_tI_g\rangle
                 -\operatorname{Cov}(I_g,T_g)\}.
\tag{10}
\]

The first term includes G_t, h_t, T_a,t, vertices, regulator weights and local
metric counterterms. Replacing it by only a trace-current cumulant loses
contacts. At fixed regulator this gives all sea flavors and all photon-current
topologies at O(u). A global H-linear response still requires evaluating (9),
(10) on the entire specified background family with controlled limits; flat
propagators or setting a momentum q=H do not do so.

For a matching path p_i(u), add p'_i partial_i to both proton and vacuum
responses, with p' fixed by a declared nonsingular calibration Jacobian. This
includes the strong-scale response and all required quark-mass directions.
There is no theorem here equating I_g to the strong trace insertion. If the
small-H coefficient A and its derivative exist on that path,

\[
R_u=\frac{A_u}{M^3}-\frac{3A M_u}{M^4},\qquad
\left.\frac{dR}{d\alpha}\right|_{0}=4\pi R_u.
\tag{11}
\]

Matching M fixes M_u=0 only on that particular path. Equations (5),(9),(10)
identify the missing data for (11); they do not supply A or A_u, select alpha,
or prove that these limits commute. Higher orders are needed for the full
dependence on finite alpha.
