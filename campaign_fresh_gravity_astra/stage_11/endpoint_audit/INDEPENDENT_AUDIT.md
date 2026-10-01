# Independent endpoint-turn proof audit

**Primary verdict: proved as written**, under the stated smooth, strictly positive, compact-background hypotheses and the original H¹₀ fixed-wall domain. No missing functional-analysis implication was found within those hypotheses. The positive gap is obtained from the regular quadratic form and compactness, not from strict positivity alone or from extending a singular change of variables beyond its domain.

Auditor `/root/metric_intake`, 2026-09-30. The root-origin candidate was checked against the original completed FGF025 and FGF023 derivations. The new FGF026 author's derivation was **not** read or used. Exact source hashes are recorded in `audit_result.json`. This is proof-only: no spectrum, continuation computation, numerical control or observational acceptance is claimed.

## Claim card and dependency graph

Let D=d*>0, with the regular Q/R SD1 equilibrium smooth through [0,D], B,rho,g,q,lambda,J,C,cs² positive there, bounded coefficients, and positive bounded kinetic weights. Let w=chi', R=rho q/lambda>0, M=U''−T_chi−q²/lambda, with Jw''=Mw−CR. Assume w>0 on [0,D) and w(D)=0. The perturbation domain is the **entire** real H¹₀(0,D)^3 for u=(xi,psi,eta), without any added trace or regularity condition on eta/w.

The audited conclusions are: the first endpoint zero is simple; the weighted-square identity remains valid on this actual domain by integrability and trace control; the original quadratic form has a positive L² gap and H¹ coercivity on this fixed interval; that coercivity survives small changes in the endpoint of the same smoothly continued equilibrium; and a nonempty first-turn family is supplied by small positive initial w. Every conclusion is conditional on the chosen local diagnostic action, not on a proved physical metric theory.

Dependencies: background ODE -> simple endpoint zero -> Hardy/trace bounds -> exact energy identity on H¹₀ -> nonnegativity and trivial kernel -> regular-form derivative bound and compactness -> fixed-domain gap/coercivity -> operator-form continuity under interval rescaling. The local small-w construction separately realizes the hypotheses; it does not furnish a numerical length or calibrated astrophysical boundary data.

## 1. Simplicity and endpoint asymptotics

Since w(D)=0 and w is positive immediately to the left, its left derivative obeys w'(D)<=0. If w'(D)=0, the equilibrium identity gives w''(D)=−CR(D)/J<0. Taylor expansion then yields w(D−h)=w''(D)h²/2+o(h²)<0 for small h>0, a contradiction. Therefore a=−w'(D)>0.

Smoothness gives w(D−h)=a h+O(h²) and w'(D−h)=−a+O(h), hence w'/w=−1/h+O(1). In particular w is bounded above and below by positive multiples of h near D. Away from D, w and 1/w remain bounded on compact subintervals. Strict CR(D)>0 is used; the argument does not cover vanishing endpoint density or q.

## 2. Actual H¹₀ domain: weighted terms, traces and identity

For eta in H¹₀, the one-dimensional absolutely continuous representative satisfies eta(D−h)=−integral_(D−h)^D eta'(s) ds. Therefore

|eta(D−h)|²/h <= integral_(D−h)^D |eta'|² ->0.

This is stronger than merely eta(D)=0 and proves the needed weighted trace limit. The right-end Hardy inequality is

integral_0^D eta(x)²/(D−x)² dx <=4 integral_0^D eta'(x)² dx.

For a smooth trace-zero test, write f(h)=eta(D−h), integrate (f²/h)'=2ff'/h−f²/h², discard the nonpositive far-end boundary term and apply Cauchy–Schwarz. Approximation by compactly supported smooth functions extends the inequality to H¹₀: the quotients are Cauchy in L², and their limit agrees with eta/(D−x) on every interval away from D.

Since |w'/w|<=K[1+(D−x)^−1], multiplication eta ->(w'/w)eta is a bounded map from H¹₀ to L². Thus

w(eta/w)'=eta'−(w'/w)eta

belongs to L²; the third energy square is finite on the full domain. Also, near D,

(R/w)(eta+wxi)² <=2(R/w)eta²+2Rw xi²,

and eta²/w is bounded in integral by a constant times eta²/h, controlled by Hardy (or h^-1<=D h^-2). All coefficients away from D are regular. The fourth square is therefore integrable too.

Finally (w'/w)eta² ->0 at D because eta²/h ->0 and eta² ->0. At the left endpoint w>0 and eta=0, so the added boundary term vanishes there as well. The original fluid/potential boundary terms vanish from their ordinary traces.

These statements do **not** require eta/w to be bounded, to belong to H¹, or to have zero trace. For example, eta=theta(x)(D−x)^(3/4), where theta is smooth, vanishes near the left endpoint and equals one near D, belongs to H¹₀; eta/w diverges like h^(-1/4). Its weighted derivative square is nevertheless integrable and the extra endpoint term tends to zero. Excluding this test would change the physical perturbation domain.

To extend the identity rigorously, one may integrate the product rule on [0,D−h] and use the above finite integrals and trace limit. Alternatively, the original quadratic form and all weighted square maps are continuous on H¹₀ by these bounds; equality on compactly supported smooth triples extends by density. Both routes justify the root candidate's four-square equality on the full original domain. Neither route assumes an H¹ trace of eta/w.

## 3. Strict positivity does not replace the gap argument

The four terms are nonnegative. If Q=2V=0, the fluid derivative term implies xi'=0, hence xi=0 by its endpoint values. Then the fourth square has coefficient R/w>0 at every interior point and forces eta=0 almost everywhere. The potential-gradient square gives psi'=0 and the Dirichlet condition gives psi=0. This proves strict positivity with no lost endpoint modes.

To establish a quantitative fixed-domain lower bound, return to the ORIGINAL FGF023 form

Q=integral{cs²[(rho xi)']²/rho−2(rho xi)'psi
 +(lambda psi'^2−2q eta psi'+Jeta'^2+m eta²)/C}dx.

Its diagonal leading gradient coefficients are cs²rho,lambda/C,J/C, all uniformly positive. Expanding [(rho xi)']² introduces only bounded zeroth/first-order coefficients. Young inequalities absorb each mixed derivative term into an arbitrarily small portion of the positive gradients plus a multiple of ||u||². Hence for fixed A_G>0,B_G>=0,

Q[u]>=A_G||u'||²−B_G||u||².

This regular estimate contains no 1/w and remains valid at the endpoint zero.

Suppose inf_{||u||=1}Q=0. A minimizing sequence is bounded in H¹ by this estimate. On a finite interval it has a weak-H¹, strong-L² subsequence; in one dimension this compactness also follows from the uniform 1/2-Hölder estimate |u(x)−u(y)|<=||u'||sqrt(|x−y|), uniform bounds and subsequence compactness. The limit is still in H¹₀ and has L² norm one. The positive weighted gradient part is weakly lower semicontinuous. Every bounded-coefficient term of the form integral a(x)u_i u_j' converges, since its first factor converges strongly in L² and the derivative weakly in L²; zeroth-order terms converge strongly. Thus Q[limit]<=liminf Q=0, contradicting strict positivity.

It follows that Q>=lambda0||u||² for some lambda0>0. Combining this with the derivative estimate gives

||u'||² <=(1+B_G/lambda0)Q/A_G,
||u||² <=Q/lambda0,

and therefore Q>=c*||u||²_H¹ with a finite positive c*. This establishes the missing step that strict positivity by itself would not supply. Positive bounded kinetic weights are equivalent to the L² norm on this fixed interval, so the corresponding generalized longitudinal squared-frequency infimum is positive as well. There is no numerical value or uniform-in-background lower bound.

## 4. Same full interval slightly past the turn

All background state variables are finite and the ODE is smooth at D because B,rho remain positive; w=0 is not a singularity of the ODE. A local continuation beyond D therefore exists, preserving B,rho>0 for a sufficiently small neighborhood. Hold the left initial data fixed.

For each nearby d, identify the original domain [0,d] with [0,1] through x=dy, using U(y)=u(dy). In the ORIGINAL form, coefficients become rho(dy),rho'(dy),lambda(dy),q(dy),m(dy), together with factors d and 1/d. Since d stays near D>0, these coefficients converge uniformly to their D values. The same holds for the density-gradient expansion. Cauchy–Schwarz therefore gives

|Q_d[U]−Q_D[U]|<=epsilon(d)||U||²_H¹(0,1), epsilon(d)->0.

The fixed-domain coercivity at D transfers under this bounded rescaling. Choosing epsilon smaller than its coercivity constant proves positivity for the same full continued [0,d] equilibrium for sufficiently small d−D>0. Because w'(D)<0, this includes a segment with negative w, but does not reuse the positive-weight identity through that segment. The original regular form and the attained gap are essential.

Each d has its own solution-induced right-wall field values, pressure and total mass, held fixed during that member's perturbation problem. This is the same initial-data continuation family, not a moving-wall evolution at fixed right-wall values and not a replacement by a shorter symmetric neighborhood. No claim of arbitrary continued length, arbitrary boundary solvability or isolated-object stability follows.

## 5. Nonempty first-turn construction

With B_i,rho_i>0, chi_i=0 and parameter w_i>0, the initial g_i and a_ref are independent of w_i. The cosh potential has U'(0)=0 and Q/R T(g_i,a_ref)>0, so w'(0)=−k with fixed k=T/J>0. Consider initial w_i in a sufficiently small closed neighborhood of zero. Smooth dependence and local boundedness of the ODE give a common short existence interval and retain B,rho>0. By continuity, shrink this interval and the initial-data neighborhood so w'<=−k/2 uniformly.

Choose w_i>0 small enough that 2w_i/k lies in that common interval. Then w(2w_i/k)<=w_i−(k/2)(2w_i/k)=0, so continuity gives a first zero at some D in (0,2w_i/k]. The solution stays in the required regular positive domain and w>0 before that first zero. The preceding theorem applies. This is a constructive existence argument for the same left-data class; it does not compute a length, demonstrate failure of an older sufficient bound, or calibrate endpoint data.

## Obligation matrix and physical limits

| Obligation | Status |
|---|---|
| Simple first zero and asymptotic sign | Passed using CR(D)>0 |
| Weighted integrability for all H¹₀ eta | Passed by Hardy; no condition on eta/w imposed |
| Vanishing singular-looking endpoint trace | Passed by local Cauchy–Schwarz |
| Exact identity on original domain | Passed by truncation or controlled density approximation |
| Strict positivity | Passed using interior R/w and all endpoint values |
| Positive gap and H¹ coercivity | Passed via regular-form bound plus compactness |
| Same full continued-domain stability | Passed locally by regular-form norm continuity |
| Nonempty first-turn family | Passed by uniform local ODE control for small w_i |
| Numerical/empirical acceptance | Not performed |
| Physical metric/core vacuum compatibility | Not resolved |

The result remains within the added unfiltered Q/R diagnostic action with MOND constitutive source B'=C rho. Both positive registered reference normalizations can be used separately; constant-vacuum reference and frozen H(z) reference families remain distinct. The actual variable scale does not gain literal pointwise constant-vacuum compatibility through this proof. No M action, filtered-MONO metric, photon coupling, free-boundary, 3D, nonlinear or observational theorem is supplied. The proof advances the finite wall-stability boundary; it does not close the physical theory.

## Pinned norm and family qualifications

The separately pinned `QUALIFICATIONS.md` is consistent with and required for a dimensionally explicit reading of the abstract norm estimates. Product H¹/L² norms mean norms after a fixed positive reference scaling of length and each field, for example x/L_ref, xi/L_ref, psi/V_ref² and dimensionless eta, or equivalently fixed dimension-balancing component weights. This preserves all compactness, positivity and continuity arguments while changing numerical constants. Unweighted sums of dimensionally different physical fields are not asserted to be observables. The actual positive kinetic quadratic form restores the squared-frequency interpretation.

For the same IVP continued to a different d, background mass is M(d)=integral_0^d rho dx and dM/dd=rho(d)>0. Thus this family does not have constant mass across its members. Fixed mass is the perturbation constraint around each individual selected equilibrium. Right-wall data and pressure are also induced separately. The gap and the permitted post-turn length increment are existential and unquantified; no calibrated interval width, numerical lower bound, or example beyond the old sufficient shortness region is claimed.
