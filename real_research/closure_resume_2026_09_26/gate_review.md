# Independent review of a constrained L361 gate promotion

2026-09-26. Review of the root agent's explicit proposal, independently reconstructed from `real_research/g03_audit_2026/L361_bound_region_kernel.py`, especially its displayed action at lines 17–22 and executable `Lag`. This review contains hand derivations; the root agent owns the separate symbolic verification and provenance run. Starting task revision was `4e16ccf585f6fcc775a2f9d62ac30d329212e0af`; shared HEAD advanced externally to `03524d209b7ca0c3900f47ccf5dfe42f9187d7c3` by completion. This audit made no merge/commit and modified no existing action/source files.

**Claim and verdict: correct only after a stated restriction.** The multiplier promotion is exactly equivalent to substituting the proposed field-dependent gate into L361, and it correctly exposes the previously omitted geometry/clock variation. The rational gate has a smooth extension across \(K=0\) on a patch with strictly positive \(R=R^{(3)}+\sigma_{ij}\sigma^{ij}\). This is a useful partial constructive compatibility lemma. It is not a smooth global completion at \((R,K)=(0,0)\), is not admissible on unrestricted negative \(R\), and does not prove unchanged dynamical degrees of freedom or health of the promoted gravity theory.

## 1. Independently reconstructed derivative and multiplier sign

Let \(\mathcal L_0(f)\) be exactly L361's nonrelativistic density after replacing \(M^2\) by \(m^2(1-f)\). Hold \(\rho_b,\phi,\psi,w,\chi\), their derivatives, the spatial metric used for contractions, and constants fixed when differentiating with respect to \(f\). Its \(f\)-dependence is affine, and

\[
B\equiv\frac{\partial\mathcal L_0}{\partial f}
=\rho_b(\chi-\psi)
+\frac{2m^2\psi w+a_0^2Q(|\nabla w|^2/a_0^2)-|\nabla w|^2-m^2\chi^2}{8\pi G}.
\]

All four terms in the numerator have the proposed signs. In particular, differentiating the two occurrences of the screening mass is necessary: the mixed \(-2M^2\psi w\) supplies \(+2m^2\psi w\), whereas \(+M^2\chi^2\) supplies \(-m^2\chi^2\).

For

\[
\mathcal L_c=\mathcal L_0(f)+\lambda[f-F(u)],
\]

the algebraic equations are \(f=F(u)\) and \(\lambda=-B\). Consequently, after solving these two equations, variation of any remaining field \(z\) gives

\[
\delta_z\mathcal L_c\big|_{f,\lambda\text{ solved}}
=\left.\delta_z\mathcal L_0\right|_f+B\,\delta_zF(u).
\]

The gate term is **plus** \(B F'(u)\delta u\). This agrees with direct variation of the reduced action \(\mathcal L_0(F(u))\), including integrations by parts when \(u\) contains derivatives of \(z\). With a covariant measure, variation of the multiplier term's measure vanishes on \(f-F=0\); the ordinary measure/contraction variations of \(\mathcal L_0\) remain and must still be included.

As an algebraic elimination problem, the pair is nonsingular: the equations' Jacobian with respect to \((f,\lambda)\) has determinant \(-1\). Thus these two auxiliary variables need no independent initial data. This statement is about the **added algebraic pair**, not the degree count of the resulting metric/clock system, because the substituted function depends on derivatives of those fields.

## 2. Ratio and rational gate

Define \(\alpha=27\Lambda/4>0\), \(A=\alpha R\), \(x_c>0\), and for \(K\ne0\),

\[
u=\frac{A}{K^4},\qquad F(u)=\frac{u}{u+x_c}.
\]

Then

\[
f=\frac{A}{A+x_cK^4},\quad
f_K=-\frac{4Ax_cK^3}{(A+x_cK^4)^2},\quad
f_R=\frac{\alpha x_cK^4}{(A+x_cK^4)^2}.
\]

On \(K\ne0\) the first derivative also equals \(-4uF'(u)/K\). This apparent denominator is removable at \(K=0\) **when \(A>0\) is held fixed**: the rational expression gives

\[
f\to1,\qquad f_K\to0,\qquad f_R\to0,\qquad
B f_K=-\frac{4Bx_c}{A}K^3+O(K^7)
\]

for bounded smooth \(B\) and fixed positive \(A\). The \(f\) function is analytic in \(K\) in a neighborhood of such a point. The proposal therefore removes the bare ratio singularity on this domain without introducing a new dimensional scale. A bounded scalar function does not by itself bound its solution-dependent coefficient \(B\), so the smoothness assumption on the remaining fields is part of this local statement.

For \(R=0,K\ne0\), \(f=0\) and \(f_K=0\), but \(f_R=\alpha/(x_cK^4)\) is nonzero. Therefore exact switch-off on a homogeneous flat background does **not** alone remove gate variations or their mixing in perturbation equations. Whether the accompanying \(B\) and its variation vanish must be checked in the actual background and quadratic action.

The density \(R^{(3)}+\sigma^2\) and \(K\) are not independent under a full geometric variation. These partial derivatives isolate two contributions; the total variation includes the shear, curvature, lapse, metric-contraction and clock variations as well. For a tensor perturbation with vanishing first-order \(\delta K\), second-order \(\delta K\) and \(\delta R\) terms can still contribute. This review does not infer a tensor speed from these derivatives.

## 3. Essential domain restrictions

**Joint zero.** There is no continuous extension to \(R=K=0\). Within the nonnegative-curvature domain, along \(A=dK^4\), \(d>0\), the limiting value is \(d/(d+x_c)\). Along \(A=0,K\ne0\) it is 0; along \(K=0,A>0\) it is 1. A choice of value at the origin cannot reconcile these paths.

**Negative curvature.** \(R^{(3)}\) can be negative, and adding the nonnegative shear square does not establish \(R\ge0\). At \(A=-x_cK^4\), with \(K\ne0\), the gate has a pole. For \(-x_cK^4<A<0\), \(f<0\); for \(A<-x_cK^4\), \(f>1\), so \(M^2=m^2(1-f)<0\). Thus the formula cannot yet be used as a globally physical activation fraction. Even an expanding spatially flat background lies on the boundary \(R=0\); generic small signed curvature perturbations require an explicitly specified treatment of \(R<0\).

Clipping \(R\) to its positive part changes differentiability and the variational problem; it is not implicit in the proposal. An alternative smooth extension or restricted solution domain is a further modeling input to be stated and checked. This review does not select one.

**Lack of uniform regularity near a transition.** A second derivative is

\[
f_{KK}=\frac{4Ax_cK^2(5x_cK^4-3A)}{(A+x_cK^4)^3}.
\]

At half activation, \(A=x_cK^4\),

\[
f=\tfrac12,\qquad f_K=-\frac1K,\qquad
f_{KK}=\frac1{K^2},\qquad f_R=\frac1{4R}.
\]

Fixed-positive-\(R\) regularity is therefore not uniform as a family of transition patches approaches the joint zero. Further, \(f_{KK}\) changes sign at \(x_cK^4=3A/5\). The term \(B f_{KK}\) is one contribution to a kinetic Hessian, but it is not the whole constrained kinetic operator; these signs do not establish a ghost or its absence. They identify exactly why a constraint/principal-symbol calculation remains necessary.

## 4. What the construction changes and what is now justified

The precise progress is an action-level **variation identity**: the prescribed-mask equations are promoted to a field-dependent variational model with its missing \(B\,\delta f\) coupling displayed. This makes the next constraint analysis concrete. It is not a mechanism deriving \(F\), its threshold, or the carrier's transport from the vacuum, and it does not eliminate the freely specified \(\rho_d\) in L361.

The rational gate differs from the empirical hard switch. On \(u>0\) it has \(0<f<1\), so inactive-region suppression is a tail rather than exact exclusion and a finite interior \(1-f\) produces some screening. It needs its own predictions and likelihood checks. Its half-activation location agrees with the hard threshold \(u=x_c\), but equality at one contour does not preserve the previous halo/forest/shear results.

There is also a normalization convention to record. The displayed \(u=27\Lambda R/(4K^4)\) is \(\widetilde x\Omega_\Lambda\). L359's \(p=1\) argument is \(\widetilde x\Omega_\Lambda/\Omega_{\Lambda0}\). To use the same half-activation contour as its threshold \(x_{c0}\), the current variable's threshold is \(x_c=\Omega_{\Lambda0}x_{c0}\). Leaving the normalization absorbed into an independently fitted \(x_c\) is fine; identifying the numerical parameters without this factor is not.

## 5. Minimal next check

Keep this lemma as local constructive evidence. Derive the constrained quadratic metric/clock/auxiliary operator on one specified \(R>0,K\ne0\) transition background using the full \(B\delta f\) terms; separately specify and test the background/negative-\(R\) extension. Count physical modes after constraints and determine the kinetic and characteristic signs. A nonsingular \((f,\lambda)\) algebraic subsystem alone cannot replace that calculation.

Review coverage: full proposed algebraic multiplier identity, exact L361 \(f\)-derivative, rational gate first/second partial derivatives, fixed-positive-curvature and joint-zero limits, negative-curvature admissibility, and empirical normalization. No observational predictions or complete covariant variation were computed here. Mathematical prose/delimiters were self-reviewed; no prior artifacts were edited.
