# Independent scoped audit of the proposed positive-baryon lemma

12 November 2026. Analytic review only; no observational likelihood or profile fit.

## Hypotheses

r>0, continuously differentiable inward radial acceleration magnitude g(r)>0, isolated spherical pointwise algebraic gravity with constant a>=0 and G>0. The Newtonian baryonic field is gb=G Mb(<r)/r². Nonnegative spherical density is equivalent locally to Mb' >=0. This does not transfer directly to a nonspherical disk, external-field AQUAL solution, signed effective source or nonlocal modified inertia. Central point masses may be allowed as positive integration constants, but distributional shells need the enclosed-mass form instead of a local logarithmic derivative. A physical interpretation also needs positive total enclosed mass, finite boundary conditions and the specified branch.

## Local bounds: passed

Let s=d ln g/d ln r.

Simple-mu gives gb=g²/(g+a), hence

    d ln Mb/d ln r=[(2+s)g+2(1+s)a]/(g+a).

For -2<s<-1, nonnegative density is equivalent to

    a <= g(2+s)/[-2(1+s)].

For the quadratic law g²=gb²+a gb, implicit differentiation gives

    d ln gb/d ln g=2(gb+a)/(2gb+a).

Thus d ln Mb/d ln r>=0 is equivalent to

    (2+s)gb+(1+s)a>=0.

For -2<s<-1, writing R=(2+s)/(-1-s)>0 gives a/gb<=R. Since g=gb sqrt(1+a/gb), the monotone map x/sqrt(1+x) yields

    a <= g(2+s)/sqrt(-1-s).

For either law, s>=-1 gives no upper bound from this condition alone. At s=-2 only a=0 survives; s<-2 admits no a>=0 with positive gb and nonnegative local baryon density. Equality at the bound means zero local baryon density, not absence of enclosed baryon mass. These bounds are necessary and locally sufficient for nonnegative density of the inverse spherical profile, not for acceptable populations, chemistry, total mass or formation.

## Finite-shell bounds: passed with explicit mass definition

Let r2>r1>0 and **Mi=ri² gi/G be effective Newtonian-enclosed masses inferred from the fixed total acceleration**, not baryonic masses. The condition being tested is Mb2(a)>=Mb1(a).

For simple-mu, Mbi=Mi gi/(gi+a), so positivity is exactly

    g1 g2(M2-M1)+a(M2 g2-M1 g1)>=0.

If M2>M1 and M2/r2<M1/r1, the second coefficient is negative and

    a <= g1 g2(M2-M1)/(M1 g1-M2 g2).

If M2=M1 the bound becomes a=0; if M2<M1 no a>=0 is feasible under r2>r1. If M2>M1 but M2/r2>=M1/r1, there is no finite upper bound from that shell. This shell condition certifies nonnegative integrated density between the two radii; it does not guarantee the density is nonnegative at every unresolved point inside the shell.

For the quadratic law, at the equality boundary Mb1=Mb2=m>0,

    Mi²=m²+(a/G)m ri²,
    m²=(M1² r2²-M2² r1²)/(r2²-r1²),
    acrit=g1(M1/m-m/M1).

Under the same strict inequalities M2>M1 and M2/r2<M1/r1, 0<m<M1 and acrit>0. It is an actual upper bound, not merely a candidate crossing: g2<g1 and

    d ln[Mb2(a)/Mb1(a)]/da
      =1/sqrt(a²+4g1²)-1/sqrt(a²+4g2²)<0.

The ratio starts above one at a=0 and crosses once. At M2/r2=M1/r1 the common-m formula has m=0 and acrit is infinite; treat it as the no-finite-bound limit rather than dividing by zero. Equal effective masses again force a=0. The formula is ill-defined outside its branch and should not be mechanically evaluated on noisy central values that violate the branch conditions.

## Observational and gravitational-observable scope

Noisy enclosed-mass tables need their joint covariance, physical profile constraints and an interval/latent-profile feasibility calculation. Independent-error finite-difference slopes or central-value bound violations are not calibrated significances. Enclosed-mass points may already come from a chosen halo/tracer model; NFW extrapolated masses are not direct model-independent force samples. A finite set of shell inequalities is weaker than a nonnegative density reconstruction between nodes.

A globally identical acceleration potential Phi and identical no-slip potential Psi=Phi produce the same weak-field light deflection and dynamical potential. Relabelling the positive baryonic inverse profiles while preserving that entire metric therefore cannot be distinguished by additional observables that depend only on that fixed metric. Independent mass-profile/population/gas information, boundary/field-equation information or non-gravitational probes are needed to break that degeneracy.

The word globally is load-bearing. Matching g only on measured kinematic annuli does not fix the potential gradients outside them; lensing integrates along a larger path and could discriminate those different completions. Likewise nonspherical multipoles, gravitational slip, time dependence and extra stress can differ despite equal spherical circular-speed curves. The invariant-metric statement is a scoped observational-equivalence result, not a theorem that lensing never supplies new information.

## Verdict

The supplied local and finite-shell formulas are correct within the hypotheses. Safe application is a positivity feasibility bound for one fixed spherical law, not an exclusion significance or a validated baryon model. The fixed-metric degeneracy statement is also correct when the entire relevant metric, not merely sampled circular accelerations, is held fixed.
