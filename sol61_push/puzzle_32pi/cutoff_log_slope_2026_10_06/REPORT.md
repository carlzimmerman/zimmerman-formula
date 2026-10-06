# Strict decrease of the retained cutoff logarithmic slope

For the exact UV-normalized retained cutoff, p_A(u)=d ln A(exp u)/du is strictly decreasing at every finite real u. Its limits are3/2 and1. A direct integration-by-parts covariance identity proves this without a convolution theorem or a finite-grid monotonicity inference. Consequently A(T)T^-beta has no finite minimum for any real beta: for1<beta<3/2 its unique finite stationary point is a strict global maximum. This is a mathematical discriminator for a declared power-law potential factor, not a full nonminimal action, all-selector obstruction, novelty claim or32pi derivation.

## Exact object and normalization

Use precisely the parent/Claude retained kernel

b(y)=sqrt(1+1/y)−1,
e(y,T)=b(y)/[1+(y/T)²],
A(T)=2 integral_0^infinity y e(y,T)dy,
T=exp u>0.

Let h(y)=yb(y)=1/[sqrt(1+1/y)+1]. Changing y=T tan theta and then tan theta=exp v gives

A(exp u)=2 exp u J(u),
J(u)=integral_R f(u+v) g(v)dv,
f(s)=h(exp s), g(v)=1/(2cosh v).

Both factors and J are positive. In particular the kernel factor is1/(2cosh v), not sech v with a missing factor2. Define t(s)=1/sqrt(1+exp(-s)),
ell(s)=f'(s)/f(s)=(1−t(s))/2.

Then0<ell<1/2 and ell'(s)=−t(s)[1−t(s)²]/4<0 for every finite s. The kernel logarithmic derivative is g'/g=−tanh v, whose negative is strictly increasing.

## Admissibility of differentiation and integration by parts

Globally f<=1/2, f(s)<=exp(s/2) and g(v)<=exp(-|v|). At fixed finite u the product obeys

f(u+v)g(v)<=exp(u/2+3v/2) for v<=0,
f(u+v)g(v)<=exp(-v)/2 for v>=0.

These are integrable and tend to zero at both endpoints. Also |f'|<=f/2 and f''=f(ell²+ell'), with bounded factors. All needed u and v derivatives are integrable, with local-u uniform domination. Thus differentiating J, normalizing the density and integrating partial_v(fg) cause no unproved boundary or divergent-moment term.

Define the probability measure

dmu_u(v)=f(u+v)g(v)dv/J(u).

Integration by parts gives

0=integral_R partial_v[f(u+v)g(v)]dv
 =J(u)[<ell(u+v)>−<tanh v>].

Therefore p_A=1+J'/J=1+<ell>=1+<tanh v>. Either expression is exact.

## Strict all-finite-u identity

Differentiate the second score representation in u. Since tanh v is independent of u and the normalized weight derivative is ell−<ell>,

p_A'(u)=Cov_mu(ell(u+v),tanh v).

In particular the apparently ambiguous original derivative <ell'>+Var(ell) is equal to this covariance, not to the negative first term alone. It may not be proved negative merely by discarding its positive variance.

For independent v,w from the same positive full-support measure,

p_A'(u)=1/2 integral_R²
 [ell(u+v)−ell(u+w)][tanh v−tanh w]dmu_u(v)dmu_u(w).

All factors are bounded, so this double integral is absolutely convergent and Fubini is justified. For v!=w, the first difference has the opposite sign to the second; their product is strictly negative. The measure has positive density on all finite real coordinates and assigns the diagonal zero measure. Hence p_A'(u)<0 at EVERY finite u. No sampled inequality or imported strict-convolution theorem supplies this proof.

## Uniform strict derivative bound

The same measure gives a rigorous all-finite-u lower bound, not only a sign. Because0<ell<1/2 pointwise and its mean lies strictly inside that range,

Var(ell)=<ell²>−<ell>² < <ell>/2−<ell>² <=1/16.

Also tanh²v<1 at every finite v, so Var(tanh v)<1. Both variances exist by boundedness. Cauchy–Schwarz applied to centered variables therefore yields

|Cov(ell,tanh v)|<=sqrt[Var(ell)Var(tanh v)]<1/4.

Combining with the strict negative sign proves **−1/4<p_A'(u)<0 for every finite real u**. The strict interior/full-support measure excludes an endpoint-only variance distribution. This bound can support a separate declared nonminimal counterfamily, but does not by itself define that action or choose its normalization.

## Limits and mathematical power-law screen

As u tends to−infinity, f(u+v)/exp(u/2) tends to exp(v/2), bounded by it, and exp(v/2)g(v) is integrable. Also ell(u+v) tends to1/2. Dominated convergence in the numerator and denominator therefore gives p_A→3/2. As u tends to+infinity, f→1/2 and ell→0, dominated by g/2, giving p_A→1. The same limits recover A(T)~sqrt(2)pi T^1.5 near0 and A(T)~pi T/2 near infinity.

For a mathematical tilted potential V_beta(u)=c A(exp u)exp(-beta u), c>0 constant, its logarithmic derivative is p_A−beta. If beta<=1 it is strictly positive; if beta>=3/2 strictly negative. There is no finite stationary point in either case. For1<beta<3/2, continuity, the limits and strict monotonicity give exactly one zero. At that zero

V_beta,uu=V_beta p_A'<0.

Both endpoint values tend to zero for this beta range, so it is the unique strict global maximum. Any regular monotone field reparameterization preserves the sign of this curvature at a stationary point. An actual nonminimal gravitational model still requires its own frame/source equations, positive kinetic conditions, curvature/matter terms and definition of the multiplier; this report does not substitute a mathematical tilt for those obligations. Extra potential terms, additive offsets inside the tilted function or different kernel normalization change the premise.

No value of beta or T here is selected physically. The numerical beta=5/4 example is a declared mathematical check of a maximum, not target fitting. The theorem specifically closes the retained-A log-slope leaf needed by the separate nonminimal-F route; it does not decide every possible F or interaction.

## Bounded checks and provenance

checks.py derives the exact elementary h/kernel logarithmic derivatives and variable-change Jacobian. Independent numerical moments over v in the full real line evaluate both <ell'>+Var(ell) and the tanh covariance at u=-30,-15,-5,0,5,15, with stable endpoint evaluation. Separate centered slope differentiation checks the result. Three off-diagonal pairs corroborate orientation, and one mathematical tilted stationary point corroborates negative curvature. These are bounded arithmetic checks of the implementation, not a proof for all u.

The first development preflight had41/42 because SymPy did not automatically identify exp(v)/(1+exp(2v)) with1/(2cosh v). Rewriting the same expression in exponentials gives the exact zero; the unchanged Jacobian formula is correct. The failed code/output are preserved in preflight/checks_a.py and preflight/results.json. The repaired preflight42/42 corroborated the original sign-only proof. The a standard records pinned that earlier sign-only revision and are retained historically; after adding the uniform derivative bound, fresh b standard records pin the current report/code. Named records and controls are listed separately in RUNS.json. Controls omit the positive variance, reverse monotone covariance orientation or call the mathematical maximum a minimum.

Source inputs are the actual local retained kernel and authenticated parent cutoff action/proof; no external log-concavity theorem or new data were used. This theorem does not assert novelty, whole-action health or32pi. The remaining physical implication belongs to the actual nonminimal source/vacuum action, not this integral identity.
