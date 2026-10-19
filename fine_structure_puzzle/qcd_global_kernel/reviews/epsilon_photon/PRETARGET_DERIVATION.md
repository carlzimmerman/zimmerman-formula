# Independent pretarget photon/pion determinant derivation

2026-10-19; saved before any new `epsilon_photon/` author target is opened. Both completed review directories remain read-only. Scope: the first O(u) nonconstant-photon contribution at epsilon order epsilon² around a constant SU(2) orientation, including its coupled massless nonconstant-pion gauge block. This is not the complete NLO QCD+QED epsilon functional or full curved QCD.

## Quadratic operator and gauge cancellation

Set `U0=a0 I+i a.tau`, `s=a1²+a2²`, `Q=I/6+tau3/2`, and canonically normalize the photon with Maxwell action `Fmunu²/4`; put e in `D U=∇U-i e A[Q,U]`. Pauli algebra gives `Tr([Q,U0][Q,U0]dag)=2s`. The norm of the U(1) Killing vector in canonically normalized pion tangent coordinates is `F sqrt(s)`.

There is one tangent fluctuation `piG` along that Killing vector. To the retained quadratic epsilon order, its action together with the photon is

`S_quad=1/2 <A,delta d A> +1/2 ||d piG +/- m A||²`,

`m²=u F² s`.

The sign of the mixing depends on the tangent orientation and drops out of the determinant. The seagull is `uF²s/2 integral A_mu A^mu`. Nonconstant pion mass/Dashen terms are O(epsilon⁴) versus Laplacian O(epsilon²); inserting them into this photon block affects the next epsilon order and is excluded here.

In covariant Lorenz gauge, add `||delta A||²/(2xi)`. On closed S4 decompose A into transverse and exact parts. For a scalar eigenfunction of eigenvalue lambda>0, normalize its exact vector as `dY/sqrt(lambda)`. The photon longitudinal coefficient a and pion coefficient b have block

`[[lambda/xi+m², +/-m sqrt(lambda)], [+/−m sqrt(lambda),lambda]]`.

Its determinant is exactly `lambda²/xi`, independent of m. Therefore the longitudinal-photon and piG determinant ratio to m=0 is one, mode by mode. Equivalently, at first O(m²), the longitudinal seagull `+(xi m²/2) sum 1/lambda` is canceled by the two derivative-mixing insertions `−(xi m²/2) sum 1/lambda`. This cancellation is required before interpreting a seagull as a physical partial contribution.

In Landau gauge, only A_T remains and `integral A_T dot d piG=0` by integration by parts. The mixing then vanishes, and the seagull is precisely the surviving transverse contribution. This is the same determinant ratio, not an extra gauge assumption.

Abelian Lorenz ghosts are governed by the prime scalar Laplacian and have no orientation-dependent interaction. Their determinants, the Hodge Jacobian and the gauge-fixing normalization cancel from this source ratio. The constant ghost/scalar gauge parameter is omitted: it does not generate a longitudinal vector. Divide by the residual global U(1) once; its action rotates the charged orientation angle, whose normalized Haar integration contributes the same constant group volume. Fixed/stabilizer endpoints s=0 do not create a new propagating scalar mode. The scalar collective coordinate is handled by the compact group integral, not included as a second piG zero mode.

There is no harmonic one-form on S4 (`H1(S4)=0`), so there is no additional flat photon vector mode. A coupling-dependent free gauge normalization such as `−(1/2)log u` is orientation independent and has zero fixed-u H derivative. It must be factored consistently rather than taking an unregularized raw free partition ratio at u=0.

Thus the complete coupled *nonconstant quadratic photon/pion* source ratio at this epsilon order is

`W_gamma(U0)=(1/2) log det_T(Delta1+m²)/det_T Delta1`

`= (u F² s/2) Tr_T Delta1^−1 +O(epsilon⁴)`.

Two other nonconstant pion directions are unchanged. This does not include the distinct nonconstant-pion source tadpole from the compact-chiral route, higher nonlinear interactions, or all same-order local curvature matching.

## Transverse spectrum and ultraviolet coefficient

The transverse rough-vector spectrum is `H²[l(l+3)−1]`. Adding Ricci=3H² gives the Hodge eigenvalue

`lambda_l=H²(l+1)(l+2)`,

`d_l=l(l+3)(2l+3)/2`, `l=1,2,...`.

The lowest level is lambda=6H² with multiplicity 10. No l=0 transverse mode is supplied. These formulas follow directly from primary gauge-sphere source (2.13) at d=4.

Hodge decomposition gives `K_T=K_full_Hodge1−K_scalar_prime`. The full one-form operator has local heat coefficients `tr I=4`, `tr(RI/6−Ric)=−R/3`. Subtracting the scalar coefficient R/6 yields transverse coefficient `−R/2`. In dimensionless proper time x=H²t,

`K_T(x)=1/(2x²)−1/x+O(1)`.

Consequently `Res_(p=1) zeta_T(p)=−1`, with

`zeta_T(p)=sum_(l>=1) d_l/[(l+1)(l+2)]^p`.

For a common regulator `d=4−2epsilon` (or the corresponding fixed-S4 spectral pole),

`G_T=(1/V)Tr_T Delta1^−1`, `G_T,div=−R/(32pi²epsilon)`.

The negative curvature pole is consistent with positive individual bare spectral terms: the quadratic divergence and local subtraction are separate. It is not a negative covariance assertion.

## Defined zeta finite part

Let n=l+3/2, A=5/2 and c=1/4. The multiplicity is `n³−9n/4` and the eigenvalue is `n²−c`. A Hurwitz expansion gives

`zeta_T(p)=sum_(k>=0) (p)_k c^k/k! [zetaH(2p+2k−3,A)−(9/4)zetaH(2p+2k−1,A)]`.

Only k=0,1 have poles at p=1. Their residue is `−9/8+1/8=−1`. Their finite terms are `zetaH(−1,A)+1/8+2psi(A)`. The regular tail sums to `−2psi(A)+psi(3)+psi(2)`, hence

`FP zeta_T(1)=2/3−2gamma`.

In the explicit finite-part prescription

`G_T,zeta=FP (H²/Omega)(mu²/H²)^epsilon zeta_T(1+epsilon)`,

`G_T,zeta=(H²/Omega)[2/3−2gamma−log(mu²/H²)]`, `Omega=8pi²/3`.

A finite change adds a local multiple of R. This chosen finite part is not a physical matching condition.

## Compact ratio, metric derivative and charge response

For the inherited compact partition `Z(x,y)=<exp(xa0−ys)>`, define `q=<s>`, `c_as=Cov(a0,s)`, `v_s=Var(s)`, `x=F²M²V`, `y=uCV`. Put

`J(H)=F² V G_T/2`, `h=uJ`.

Integrating the orientation-dependent transverse determinant gives

`Z_with_photon/Z_without_photon=1−h q+O(epsilon⁴)`,

`delta W_gamma=h q`.

This is the O(u) photon correction with the LO compact y dependence resummed. It is not the result of Taylor-expanding the entire compact partition in u. Its seagull was retained only after the longitudinal/mixing determinant cancellation above.

At fixed renormalized parameters and mu, `D=V partial_V=x partial_x+y partial_y`,

`delta rho_gamma=[(Dh)q+h(x c_as−y v_s)]/V`.

For the displayed zeta scheme, write `L_T=2/3−2gamma−log(mu²/H²)`:

`J=F² L_T/(2H²)`, `DJ=J/2−F²/(4H²)`.

The logarithmic term in DJ must not be dropped by holding a numerical tadpole shape constant fixed while varying H.

Since q_x=c_as and q_y=−v_s, the first fixed-source charge derivative is

`partial_u delta rho_gamma = (1/V){(DJ)(q−y v_s)+J[x c_as−2y v_s−xy k_as_s+y² k_sss]}`,

where `k_as_s=<delta a0 (delta s)²>` and `k_sss=<delta s³>`. At u=0 this simplifies to `[(DJ)K(x)+J xK'(x)]/V`, where the inherited `K=2[I2(x)/I1(x)]/x`. At x=y=0 it is `(DJ)/(2V)`.

Common orientation/source-independent factors cancel from the appropriately normalized coupling difference; independent charge-dependent local contacts do not. The absolute free photon anomaly is another known term and is not re-derived or counted as new here.

## Curvature counterterm check and limitations

The photon pole in the compact source action is

`delta W_gamma,div=−uF² R V s/(64pi²epsilon)`.

If the Euclidean curvature operator is literally `+uF² k15 R Tr(QUQUdagger)=uF²k15 R(5/9−s)`, its orientation pole is canceled by `delta k15=−1/(64pi²epsilon)`. Under the standard `delta k15=beta15/[16pi²(d−4)]`, this corresponds to photon beta15=1/2. This was derived from the coupled operator and transverse heat trace, then compared with the primary source's photon term 1/2. The accompanying U-independent curvature contact must be tracked separately because the displayed k15 operator also has a constant component.

This photon agreement does not resolve the separately recorded pion/k15 off-shell-versus-form-factor bridge. It does not fix finite k15 or any pure-source curvature term. A full common-regulator pion+photon+curvature assembly remains required. The epsilon regime requires F/H large and M/H, Mc/H small with x,y O(1); fixed physical mass/charge H→0 leaves that regime. No full QCD, global H-linear coefficient, proton denominator or alpha value is derived.

## Source authentication

Primary cached source: De Cesare, Di Pietro, Serone, arXiv:2212.11848v1, 2022-12-22; PDF SHA256 `677ed007e8e1e6696c2ce60fd21637cb7818349f841f0b4b488dc8df6b2ad06c`. Exact transverse spectrum (2.13), scalar spectrum (2.16), gauge decomposition/prime determinant (2.29)-(2.32) inspected directly. The loop-source inconsistencies recorded in the earlier review are not used in this new spectral/gauge derivation.

Primary cached curvature source: Kubis–Meissner arXiv:hep-ph/9908261v2, 2001-05-15; SHA256 `6c4267db298d51fdf8df0205edeaa5dede792b4b014eb88cd2397e58025bdb72`. Its literal (4.7),(4.8) operator and beta are facts already authenticated visually; no finite fitted LEC is imported. The current derivation independently predicts only the photon part of that comparison.
