# Independent cutoff logarithmic-slope audit

Accepted: the retained integral satisfies −1/4<p_A'(u)<0 at every finite u. I reconstructed the variable changes, normalized score identity, strict covariance sign, domination and variance bound directly; neither numerical check counts nor an external convolution theorem supplies the proof. No blocking gap was found. This is the exact retained-A lemma, not a nonminimal action, selector, health or novelty result.

## Frozen inputs and records

Author-observed HEAD `26fe6d3e05753ab87dfc53916e09cb6f174fa9ea`. Inspected SHA-256:

- REPORT.md: `8e3435d1b7a7f809eb795bc53cd2336b47767bed17573b3b0b5fc6aa6d3d3899`
- checks.py: `6b6ce76d0645253b31bbe1139a2919bb10851ca04341dcb26a922e3d44b95071`
- contract.json: `ec9b4207d0946e3c5512264c097036e21bcb3c4e3c22e384f6b95db35e5d3ff9`
- provenance.json: `5ff2c646065be48d5a69d3a6c7a675fe9b2c348010fa329a282ca5193082d03a`

The inherited cutoff report/kernel source is pinned in that provenance. I independently validated main_b, control_variance_b, control_orientation_b and control_minimum_b with the standard validator: all four current records validate. Historical a records/preflights are not pooled into current evidence. No author input was edited; this review is outside execution inputs.

## Raw integral reconstruction

Starting from A(T)=2 integral_0^infinity h(y)/[1+(y/T)²] dy and h(y)=y(sqrt(1+1/y)−1), y=T tan(theta) removes the rational denominator: A=2T integral_0^(pi/2) h(T tan(theta)) dtheta. The second change tan(theta)=exp(v) gives dtheta=exp(v)/(1+exp(2v))dv=dv/(2cosh v). Thus A(exp u)=2exp(u)J(u), J=integral f(u+v)g(v)dv with f(s)=h(exp s), g=1/(2cosh v). The factor2 is correctly retained.

Let t=sqrt[exp(s)/(1+exp(s))]. Then f=t/(1+t), t'=t(1−t²)/2 and ell=f'/f=(1−t)/2. Hence 0<ell<1/2 and ell'=−t(1−t²)/4<0. For a finite u, f(u+v)g(v) is bounded by exp(u/2+3v/2) at negative v and exp(−v)/2 at positive v. These endpoint bounds vanish and are integrable, locally uniformly in u. Since the derivative multipliers ell,ell' are bounded, the differentiated integrals and the integration-by-parts boundary are justified.

For the normalized full-support measure dmu=f(u+v)g(v)dv/J, integrating partial_v(fg) gives E[ell]=E[tanh v]. Therefore p_A=1+E[ell]=1+E[tanh v]. Differentiating the latter expression gives p_A'=Cov(ell(u+v),tanh v). Differentiating the former independently gives E[ell']+Var(ell); both terms are essential. This reproduces the exact reported identity rather than discarding the positive variance.

The pair formula Cov(X,Y)=E[(X(v)−X(w))(Y(v)−Y(w))]/2 is valid because the variables are bounded. ell is strictly decreasing and tanh strictly increasing, so every off-diagonal pair contributes negatively. mu has strictly positive density throughout the real line and the diagonal has zero product measure. The covariance is therefore strictly negative, not merely nonpositive, for every finite u.

For the uniform lower bound, ell²<ell/2 pointwise gives Var(ell)<m/2−m²<=1/16 with m=E[ell]. Also Var(tanh)<E[tanh²]<1. Cauchy–Schwarz now yields |p_A'|<=sqrt[Var(ell)Var(tanh)]<1/4. The strict inequalities require the interior/full-support finite-u distribution, which is available here. Endpoint limits do not invalidate this statement because they are outside finite u. The bound is not claimed sharp.

## Limits and mathematical tilt

For u→−infinity, f(u+v)/exp(u/2) is dominated by exp(v/2); its product with g is integrable. The same domination applies to the ell-weighted numerator. Thus p_A→3/2. For u→+infinity, f→1/2 and ell→0, with domination by g/2, giving p_A→1. The corresponding constants are A(T)~sqrt(2)pi T^(3/2) and A(T)~pi T/2.

Strict monotonicity plus these limits makes p_A−beta vanish exactly once when 1<beta<3/2. At that point, for positive c, V=c A(exp u)exp(−beta u) has V_uu=V p_A'<0. Both endpoints of this tilted potential tend to zero, so this is the unique strict global maximum. For beta outside that open interval its logarithmic derivative has a fixed sign. A regular monotone field redefinition preserves stationary-point curvature sign. Extra additive terms, altered cutoff subtraction or another nonminimal function are changed premises.

## Interpretation of bounded computation

The six full-line quadratures, orthogonal derivative moments, centered differences, pair examples and beta=5/4 root corroborate the implementation over their declared range. They are not the all-finite-u proof. The three controls correctly reject dropping variance, reversing covariance orientation and treating the maximum as a minimum. The historical Jacobian simplification failure was algebraic automation, not a failed variable-change identity, and is transparently preserved.

An actual nonminimal gravitational model still needs its metric/scalar equations, frame transformation, kinetic sign, vacuum stability and physical-source normalization. In particular this lemma alone fixes no beta, cutoff, positive vacuum coefficient or32pi. Those implications belong to the separately audited action.
