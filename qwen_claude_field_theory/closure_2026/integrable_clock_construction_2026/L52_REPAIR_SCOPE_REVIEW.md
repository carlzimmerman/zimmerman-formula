# L52 review: a useful Schur identity is not yet a coherent static repair

Reviewed against remote main 351426c4ff7d8661450b589a88c34719c497eca1.
Self-review using Mathbox proof-audit and computation-audit, not independent
human refereeing. Credit Claude/Fable's L52 for proposing the series arrangement;
Carl Zimmerman's exact exponential law and primordial-clock direction remain
the target. No claim of global novelty. Full gravity goal **OPEN**.

## Reproduced evidence and scope

`python3 fable_independent_2026/L52_marginal_sweep.py` reproduced 68 PASS,
0 FAIL, child exit 0 in 7.9542 s under a 120 s subprocess timeout. Python 3.9.6,
SymPy 1.14.0, mpmath 1.3.0. Source SHA256 before/after:
`8add27102cb0df188243075359ba27fdd5a14cf883d0bca05d2967975c3ef5be`.
These are execution results, not acceptance of all 68 interpretations.
E3d/D4/F2/F6/F7 include literal-True assertions; C0 assigns the count rather
than deriving all constraints. The full gravitational Dirac system is missing.
The source uses g_N=2 J_Y w at line 633, whereas THE_ACTION section 3 uses
g_N=J_Y w. A consistent source normalization is required before pricing kappa.

## Exact counterexample to extending the unscreened force identity

Use normalized quadratic energy, with positive Sigma, lambda, xi:

    E = Sigma |W|^2/2 + lambda |grad(phi)-W|^2/2
        + xi^2 (Delta phi)^2/2 + rho_source phi.

Variation gives W=lambda grad(phi)/(Sigma+lambda) and

    Sigma_eff = lambda Sigma/(Sigma+lambda),
    Sigma_eff Delta phi - xi^2 Delta^2 phi = rho_source.

The response change divided by the Newtonian Fourier response is therefore

    1/(Sigma_eff+X) - 1/(Sigma+X),   X=xi^2 k^2,

not 1/lambda except at X=0. At Sigma=lambda=X=1 it is **1/6**, whereas the
unscreened additive-Newtonian claim predicts **1**. This is a local linear
constant-coefficient counterexample to a claimed universal response identity,
not a numerical prediction for Saturn or a refutation of every nonlinear repair.

More generally let P=lambda(V-W)=dF/dW. Keeping the coherence energy on V gives

    div P - xi^2 Delta^2 phi = rho_source.

On a sphere, after integration, P_r-xi^2 (Delta phi)' is the enclosed-source
flux. P_r alone is not g_N. Thus V=W+P/lambda does not imply V=W+g_N/lambda.
L52 E3a differentiates an assigned Delta_eff; F1 differentiates an assigned
kappa GM/r^2. Neither varies or solves this coherent equation. The correct next
step on L52 is a normalized nonlinear static solve, then metric/clock variation
and Dirac closure. Do not import a zero ephemeris cost into IC39.

## Exact exponential-law architectural distinction

For the user's mu(y)=1-exp(-y), s=y(1-exp(-y)) and the extra force is
Delta=y exp(-y). Hence

    dDelta/ds = (1-y)/(exp(y)+y-1),

negative for y>1 (at y=2: -0.119202922022117556). A convex auxiliary carrying
only this extra force cannot implement the full law using L52's monotonicity
assumption. This is not an obstruction to the total-potential AQUAL operator:
its longitudinal derivative is 1+(y-1)exp(-y)>0 for y>0. The two architectures
must remain distinct. L52's saturated RAR/C-family is not this exact law.

## Isolated auxiliary constraint check, not a full gravitational count

For H=p_v^2/2+Sigma w^2/2+lambda(v-w)^2/2, primary p_w=0 has secondary
(Sigma+lambda)w-lambda v=0. Their actual Poisson matrix is

    [[0, -(Sigma+lambda)], [Sigma+lambda, 0]].

Its determinant is (Sigma+lambda)^2. Secondary preservation fixes the primary
multiplier to lambda p_v/(Sigma+lambda); no tertiary constraint arises in this
isolated regular mechanical model. This validates the elementary auxiliary
elimination, not L52's full clock/metric/matter DOF bookkeeping. All three
symbolic calculations above were executed with SymPy and assertions, exit 0.

## Route decision

Retain the series technique as a conditional option. Do not substitute L52's
different kernel and extra MOND scalar for the IC39 construction. IC40/41
instead attack IC39's next unsolved time-preservation gate with unchanged action
coefficients and additional initial-data freedom. No failed route was deleted.
