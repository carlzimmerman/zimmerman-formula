# Mass budget, current matching, and the remaining theory problem

2026-11-14. User-authorized correction and research continuation. This checkpoint corrects the crossing-speed argument, verifies the existing grading repair, evaluates the actual profiles and follows the strongest new XJ1 lead. It does not adopt a model or claim a closed theory.

## What changed

The local CJ1 completed-form note and PAPER72 source now distinguish an algebraic speed intersection from a derived physical transition. At a common r200 the exact simple-law effective mass divided by q Mb is

    [1 + sqrt(1 + 4 q^2 v*/v200)] / (2 q),  q = 1 + X.

The old surplus-below/deficit-above explanation had the direction reversed. For X=5.41 equality is at 1.184842884 v*, not v*. This conditional comparison does not supply the budget of a truncated halo. The corrected source also distinguishes a rescaled cold profile, an unscaled form-B profile and an actual solution of the algebraic force law.

The deposited PAPER72 v1.4 PDF, supplement and receipt were preserved. The edited TeX explicitly says it is an undeposited local correction. Its historical scorecard quotations are pinned to the exact scorecard at the v1.4 paper commit, with provenance in before_correction/; otherwise later Claude updates make old quotations uncheckable. This pin does not replace the current corrected CJ1 source or relax its commit checks.

WLJ1's per-footing grading repair was already present before this turn. We added seven full-grader regression tests and reproduced all six saved outputs byte for byte. A reconstructed shared-flag mutation fails. No historical result was overwritten.

## Actual mass calculation

See [calculation/README.md](calculation/README.md). The calculation covers 321 halo masses, four redshifts, two footings and four settled radii: **10,272 cases**, with independent physical-unit and source-convention checks.

- FZS1/JNT2 preserve their implemented patch mass to 6.67e-16 relative precision. This is bookkeeping conservation, not verification of the local force equation.
- At z=0 and f=2 the uncapped retained-source law demands more than the whole cosmic patch cold charge in 172/240 canonical and 186/250 alternative active haloes. With all explicit Bar baryons as the law source, the counts are 240/240 and 250/250. These are finite grid counts, not abundance fractions or population exclusions.
- Galaxy Xsh is about 56–60 per retained central baryon, whereas the speed argument uses X=5.41 per baryon. The calculation records the retained, patch and 200c scopes separately. If M_cond=eta M_b,patch on one consistent scope, the intersection becomes eta a0/(10 q H); eta is not generally one. This is a conditional identity, not a proposed replacement transition.
- The cluster non-Bar reservoir also contains nominal baryons outside r200c. It is reported separately from the cosmic cold charge.
- XJ1 preserves the supplied B profile, which can already contain caps, leftover terms and other components. Preserving B alone does not establish the raw algebraic law.

The new [finite-charge bound](calculation/BUDGET_BOUND.md) gives a direct admissibility test. For the exact raw law with source b(r) and available cold charge Q, C<=Q if and only if a0 b r^2/G <= Q(Q+b). For a fixed point source this gives R_budget=sqrt(G Q(Q+b)/(a0 b)); for a continuous nondecreasing source, the first crossing bounds the possible raw-law interior. In the plotted canonical z0 halo the retained-source bound is 430.277 kpc, the all-Bar bound 194.190 kpc, and the prescribed f=3 radius 447.329 kpc. These are distinct source conventions, not a new selected transition. The representative calculation checks 64 haloes and both source conventions, with 76 crossings inside the patch.

## Latest mechanism and a new necessary condition

See [latest_review/REVIEW.md](latest_review/REVIEW.md) and [JUNCTION_THEOREM.md](latest_review/JUNCTION_THEOREM.md). The new XJ1 caustic cases are useful post hoc candidate profiles. Their forest results are not a dynamical solution, and their good labels do not select them over the reference cosmology.

For a moving spherical interface, a conserved current with no surface reservoir must satisfy

    [J^r] - Rdot [J^t] = 0,
    J^mu = n^mu rho_Q - lambda P^mu/Q.

The theorem retains the full QX17 polarization flux. An exactly stationary inner state sets lambda_in=0. A stationary boundary cannot therefore join it to positive, inward-flowing polarization-free dust. A moving boundary or nonzero polarization transport can change that conclusion, but must satisfy the explicit flux equation in the theorem, the constitutive equation and the metric/stress equations together.

The finite check covers 7,110 active caustic snapshots. Of them, 3,706 would require exterior outflow for an expanding front with a static interior under pure advection. That statement is conditional on the Newtonian advective identification, and is not a no-go for the full polarization current. The other cases and degenerate zero-outer-density cases are retained in the evidence.

There is also a constructive partial result, proved and checked in [TRANSPORT_PATH.md](latest_review/TRANSPORT_PATH.md). A convex interpolation between two cumulative profiles with the same total charge admits an explicit velocity that solves continuity, preserves positivity and has zero endpoint flux. An exponential mixing schedule gives a conditional bounded-velocity path with asymptotic arrival. Its timescale remains arbitrary, and momentum, polarization, energy and stability remain unsolved. This is kinematic feasibility, not a dynamical completion.

## Latest supernova update

[The separate review](latest_sn_review/REVIEW.md) independently reproduces AGB4's small Pantheon+ age slope and AGB5's larger original-table slopes. The latter means the broad claim that the published slope is merely a host-mass step cannot be carried forward. The current evidence depends on residual definition and standardisation. AGB5's frozen result is NOT EVALUABLE; its disclosed post-results amendment gives REQUIRED / FRAGILE. The bootstrap errors and structural fits were inspected, not independently rerun. None of these host regressions tests a0 or settles the gravity theory.

## What would count as closure

The immediate missing object is one tracked halo with a finite-width transition that obeys the actual charge budget, E2/E3/E4, and energy/stress matching throughout its evolution. A density profile or a freely chosen transport velocity is not that object. The selected caustic and settling rate must arise from the equations and initial conditions, and stability and observational predictions must then be checked.

Neither kappa=1/2 nor the cosmic charge share has been derived by this work. The matter sector S_m is still an input to the action, so these gravity/halo checks do not constitute a theory of all interactions. The user's final-theory/TOE objective remains open. This checkpoint gives explicit necessary conditions and a precise next field-equation problem rather than a claim of completion.

## Navigation

- `PLAN.md`: target and disjoint work scopes.
- `calculation/`: full data, scripts, five successful bounded runs, one preserved serialization-failure record, and diagnostic figure.
- `latest_review/`: latest XJ1 review, junction theorem, reproducible checks and accepted run identified in its review.
- `INDEPENDENT_REVIEW.md`: independent audit and any final addendum.
- `before_correction/`: original local sources and authenticated v1.4 historical scorecard.
- WLJ1 `CODEX_GRADER_VERIFICATION_2026_11_14.md`: existing fix, regression and output comparison.
- Root `CLAUDE_HANDOFF_MASS_BUDGET_2026_11_14.txt`: concrete continuation handoff.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
