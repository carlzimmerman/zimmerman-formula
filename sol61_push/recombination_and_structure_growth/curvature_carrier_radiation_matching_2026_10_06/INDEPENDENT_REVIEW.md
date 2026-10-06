# Independent radiation-to-EdS carrier matching audit

**Primary verdict: proved as written for the prescribed sharp metric and scalar matching problem.** The amplitude root and conserved charge are exact. The report also correctly identifies that its nontrivial radiation branch is not a solution of the full Einstein–carrier system with ordinary trace-free radiation. This is a prescribed-history failure and initial-condition cost, not a no-go for all self-consistent smooth coupled cosmologies.

## Frozen inputs and explicit hypotheses

Inspected final REPORT.md SHA256 `adbee0bad31df6772dc8142f835b7108c0812cb87104d30f13828f09f4c60cdc`, checks.py `1f30f7fa0cad331980ede5c586867cd0f253079e91e9ee92abbabfc7f07e1524`, and the parent's raw action/stress report `sol61_push/main_theory/claude_continuation_2026_10_06/REPORT.md` (`d94923dc6453ed12285c1ebb6c94514bf19baa6e1f521fa49180115befa9d762`). Author provenance records inspected HEAD `8b7eacc1bb5f6e1f97c51400457a281dc8d22146`. This review independently reconstructs the scalar matching and stress rather than transferring a healthy finite EdS perturbation result into radiation.

Assume signature (-,+,+,+), M>0, xi>3/16, te>0, fe=|chi_e|²>0, no bare scalar mass or constant vacuum term in this declared action, and the prescribed C1 FRW scale factor. The scalar is complex, normalized as two canonical real fields. The finite-start positivity statement additionally needs `delta_e=2xi fe/M<1`. The actual ordinary radiation is not solved for here; `rho_r=3M/(4t²), p_r=M/(4t²)` are benchmarks of the prescribed pure-GR metric. No microscopic radiation–matter transition or real cosmic fit is constructed.

## Independent scalar matching and finite curvature step

Metric continuity fixes `tau=t+te/3`, `tau_e=4te/3`. Radiation has H=1/(2t), EdS H=2/(3tau); both equal 1/(2te) at the join. Their Ricci scalars are respectively zero and 4/(3tau²), hence the right Ricci value is 3/(4te²). H is continuous, so its derivative and R have finite steps but no delta functions.

Varying the scalar in the retained action gives `(Box-xi R)chi=0`, or `chi_ddot+3H chi_dot+xi R chi=0`. On radiation the general solution is `C0+C1/sqrt(t)`. Matching its derivative to the specified circular EdS value gives

`C1=-2te^(3/2)chi_dot_e=(3/4)chi_e sqrt(te)(1-2i omega)`.

Matching its value then gives

`C0=chi_e-C1/sqrt(te)=chi_e(1/4+3i omega/2)`.

No extra independent radiation mode remains after both complex matching conditions are imposed. The circular EdS exponent is `s=-1/2+i omega`, with `s²+s+4xi/3=0`; therefore `omega²=4xi/3-1/4>0`. At the join the friction coefficient 3H is the same on either side, so the field equations imply `chi_ddot_rad-chi_ddot_EdS=xi R_EdS chi_e`. This independently confirms the finite scalar-acceleration step. Continuity of chi and chi_dot is the correct no-surface-source condition; no stronger C2 matching is available for the sharp R step.

A constant U(1) rotation may make chi_e real without changing observables. With `z=sqrt(te/t)`, expansion gives

`chi/chi_e=(1+3z)/4+(3i omega/2)(1-z)`.

Thus

`f/fe=[(1+3z)/4]²+(9 omega²/4)(z-1)²`

`=1+(3/2)(z-1)+3xi(z-1)²`.

This identity is not a large-xi approximation. The cancellation of matched imaginary components at z=1 explains the sensitivity of a small join amplitude to earlier phases.

## Exact positivity root and large-xi interpretation

Write y=z-1>=0 and `s_c=Se/M`, avoiding confusion with the scalar power-law exponent. Since `Se=8xi²fe`, `delta_e=s_c/(4xi)` and

`F/M=1-delta_e[1+(3/2)y+3xi y²]`.

The bracket has derivative 3/2+6xi y>0 for all y>=0. For 0<delta_e<1 it crosses 1/delta_e exactly once. Solving the positive quadratic root gives precisely the report's a=3xi delta_e, b=3delta_e/2 expression. F is positive exactly between that crossing and the join on this prescribed history. For a finite start zs, monotonicity makes endpoint positivity necessary and sufficient, yielding

`Se/M<4xi/[1+(3/2)(zs-1)+3xi(zs-1)²]`.

At fixed nonzero Se/M and xi going to infinity, the fraction tends to `(3Se/(4M))(z-1)²`, rather than to zero. Therefore the positive root tends to `z*=1+2/sqrt(3Se/M)` and the stated dimensionless t*/te follows. A choice Se/M=0.4 gives the supplied approximately0.12524 result. It is not an observational epoch or a coupled metric endpoint. In particular, positivity of F tests the tensor coefficient only, not all perturbative health.

## Full metric variation: independent radiation stress and trace

Varying the nonminimal term before inserting R=0 is essential. The actual Jordan RHS stress is

`T_chi,munu=T_can,munu+2xi[f G_munu+(g_munu Box-nabla_mu nabla_nu)f]`.

For homogeneous FRW this gives

`rho=|chi_dot|²+2xi(3H²f+3H f_dot)`,

`p=|chi_dot|²+2xi[-(2H_dot+3H²)f-f_ddot-2H f_dot]`.

Put `f=A0+D t^(-1/2)+A1/t`, where `A0=|C0|²`, `A1=|C1|²`, and D is the real interference coefficient. In radiation the D contribution to `3H²f+3H f_dot` cancels identically; the D contribution to the pressure improvement also cancels. Since `|chi_dot|²=A1/(4t³)`, this yields

`rho=(3xi/2)A0/t²+(1/4-3xi/2)A1/t³`,

`p=(xi/2)A0/t²+(1/4-3xi/2)A1/t³`.

These independently reconstructed signs/factors agree. Canonical kinetic stress alone is not the physical source dictionary of this action. The negative stiff RHS coefficient on the matched xi>3/16 branch does not by itself prove a physical ghost; nonminimal gravity requires the constrained kinetic analysis.

The matched norms are `A0=fe(3xi-1/2)` and `A1=3xi fe te`. Relative to the prescribed radiation benchmarks this gives

`rho_chi/rho_r=delta_e(3xi-1/2)(1-z²)`,

`p_chi/p_r=delta_e(3xi-1/2)(1-3z²)`.

The conservation equation follows termwise: the t^-2 branch has p=rho/3, and the t^-3 branch has p=rho with a proportional to sqrt(t). At the join rho_chi=0, but p_chi/p_r=-2delta_e(3xi-1/2), so satisfying the00 equation alone cannot establish the full prescribed metric.

Most decisively, the exact trace is

`3p_chi-rho_chi=-(3xi-1/2)|C1|²/t³`

`=-3xi fe te(3xi-1/2)/t³`.

It is nonzero for the stipulated branch. The Einstein trace with no vacuum term is `-MR=T_ordinary+T_chi`. The prescribed radiation has R=0 and ordinary traceless radiation has T_ordinary=0, so this nonzero carrier trace is incompatible. Moving the `2xi f G_munu` term to the geometric side changes the notation to F but not this conclusion; at R=0 its traced G term vanishes anyway.

Exceptions must be kept distinct: C1=0 would remove the stiff trace and the radiation U(1) charge; xi=1/6 is the conformal trace-zero coefficient but does not admit this real circular EdS frequency; chi_e=0 is the trivial carrier. None realizes the stipulated nonzero charged match. Other matter with compensating trace or a different R(t) changes the premises. This exact contradiction excludes the prescribed ordinary-radiation metric for this match, not a general backreacted cosmology.

## Charge and source meaning

The canonical U(1) current of `-|partial chi|²` can be oriented as `j0=2 Im(conjugate(chi) chi_dot)`. Nonminimal xi R f preserves that symmetry. The report intentionally uses Q=a³ Im(conjugate(chi)chi_dot), half this canonical charge. The normalization is explicit and consistent.

Direct multiplication gives `Im(conjugate(C0)C1)=-(3/2)fe omega sqrt(te)`; the decaying-square contribution to `Im(conjugate(chi)chi_dot)` is real and drops out. Since `a³=ae³(t/te)^(3/2)`,

`Q=(3/4)ae³fe omega/te=ae³fe omega/tau_e`.

It is constant and exactly equals the EdS value. This is conservation of an internal charge, not positive dust energy, cold mass abundance or protection of F. The example shows these implications can separate even under exact matching and the same varied action.

## Backreaction ordering and bounded evidence

The illustrative condition |rho_chi|=rho_r gives `z_back²=1+1/[delta_e(3xi-1/2)]`. Its time ratio is the stated inverse. The xi going to infinity density ratio at the F root is `1+sqrt(3Se/M)>1`, proving the asymptotic ordering at fixed positive Se/M. It does not establish the ordering uniformly near xi=3/16. The report correctly restricts finite examples to xi>=1 and explicitly makes no all-xi claim. More fundamentally, the Einstein trace is already wrong before any arbitrary order-one threshold: backreaction need not wait until the displayed crossing.

The symbolic script verifies31 identities and selected exact-radical evaluations. The improvement mutation removes actual metric-variation terms and fails6 checks; removing phase matching fails14; asserting prescribedGR on-shell fails its additional pressure interpretation test. These preserved failures are meaningful for the corresponding obligations. All four manifests have been independently validated against current declared inputs and results. REPORT is not an execution input, so its final run-summary addition does not stale them. No script was rerun or author input edited by this peer.

Passed: matching value/derivative and curvature step, charge normalization/conservation, amplitude profile, finite-start bound/root, full stress factors and conservation, trace discrimination, limited ordering and finite computation interpretation. The smallest remaining arrow is a self-consistent smooth radiation–dust–carrier solution with the desired late charge/response and F>0 over a specified finite interval. It cannot be supplied by relabeling this prescribed history or its charge as cold dust.
