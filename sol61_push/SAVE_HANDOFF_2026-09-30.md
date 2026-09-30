# Saved research handoff

## Latest checkpoint: coefficient selection obstruction

Newest structural audit: EXPANSION_BRIDGE_COMPLETENESS_RESULTS.md supplies an
explicit covariant T/B-field completion of the expansion action. Restoring
the radius field before variation yields a radial Noether identity: exact
N,sigma,V,P equations imply the angular equation wherever R' is nonzero.
The covariant identity then implies the T equation when metric/polarization
equations hold and grad T is timelike. Six symbolic certificates pass.
This resolves an independent-equation gap for smooth regular vacuum patches
of this specified completion, not for different theories or approximate
numerical profiles. Source conservation, residual-derivative control at the
critical point, global boundaries, full health and beta/U selection remain
unproved. Next: smooth critical connection and conserved source matching;
exact 32π is still unresolved.

Newest critical checkpoint: EXPANSION_BRIDGE_CRITICAL_RESULTS.md proves a
local C=D=R critical-state family for every beta>0, using the scaled map
and Jacobian det=8beta(3lambda−1)>0. Seven symbolic identities and six
finite roots pass. The candidate slopes are asymptotically
S H³r/[beta(lambda−1)] times (2±sqrt(11)); these do not select 32π.
Six two-sided negative-slope offset integrations at beta=10 reach inner
r=1e−6 and outer r=0.1, with endpoint differences reducing by about four
when the gap is halved. The actual critical point remains excluded: no
rigorous smooth crossing or global boundary match is claimed. The inner
preferred-flow mode is appreciable and the outer trace constant has not
been set by a boundary condition. Next: local invariant-manifold proof and
critical W/radius shooting against a conserved source and outer foliation.
Beta, U, full health and exact 32π remain unresolved.

Newest boundary work: EXPANSION_BRIDGE_OUTER_RESULTS.md derives the outer
linear modes from the full necessary radial equations (13 exact identities).
For the specifically normalized flat-spatial de Sitter boundary, Ctheta=0
and P=Cp/r²; this is a boundary choice, not a universal geometry theorem.
A fixed-beta=10 trace scan brackets a finite denominator-event transition
near factor 0.306219, but lower-endpoint cutoffs down to D=−1e−8 retain
nonzero R≈−2.069e−7 and divergent P'. No smooth crossing or cosmological
match has been achieved. Next: solve C=D=R=0 and finite critical slopes,
then connect inner and outer manifolds via desingularization or a BVP.
The event bisection is not a coupling prediction. Beta, U, conserved source,
full covariant completeness and health remain unresolved; no exact 32π.

Latest coupled checkpoint: EXPANSION_BRIDGE_RADIAL_RESULTS.md closes the
necessary radial vacuum system with C'=D P'+R−2C/r and P'=−R/D. Three
symbolic identities pass. A finite weak annulus matches the reduced force
after de Sitter-background subtraction to <6.6e−7 and keeps normalized lapse
and shift residuals <1e−15. This is an IVP, not a conserved source or full
covariant/global solution. Extending zero-offset trace data approaches D=0
near r=0.00107214 with nonzero R; cutoff refinement makes P' grow by factors
of ten. Tiny initial trace offsets avoid that event through r=0.01 but give
different, nondecaying outer P profiles. Next: shoot trace/shift data for
D=R=0 compatibility and cosmological matching at fixed beta, before asking
whether regularity could select a coupling. Beta=10 and U were prescribed in
this finite experiment; exact 32π and vacuum-energy protection remain open.

Newest positive reduction: EXPANSION_BRIDGE_MOND_RESULTS.md eliminates the
weak spherical spatial metric and polarization at leading Theta=3H. Its
reduced action derives b=g−P=GM/r², P²=a0 b and a0=2H/beta, hence the
deep spherical scaling v_c^4=GMa0 under the stated orbital ordering. Nine
symbolic identities pass, with three illustrative beta profiles and validated
provenance. This is conditional on a full matched weak source and trace
boundary condition, not an interacting solution or error theorem. It leaves
C=Lambda/a0²=3beta²/4 unselected. The requested r_star²Lambda=8π uses
r_star=c²/(2a0) and is the same target condition; the vacuum metric horizon
has r_dS²Lambda=3. Next obligations: prove the coupled source/trace dictionary
and independently determine beta and U. Exact 32π remains unresolved.

Latest source test: EXPANSION_BRIDGE_RESULTS.md derives necessary lapse,
shift and polarization equations for the beta M²P³/Theta action. Theta
variation adds a cubic shift current and doubles its lapse contribution.
Constant-expansion slices of the GR mass geometry exist kinematically, but
the C=0 frozen GR ansatz fails the interacting shift equation by
−beta A P²P'/(3H²); its nonconstant clock acceleration forces nonconstant P.
Eleven symbolic identities pass in expansion_bridge_constraints_v2.py with
validated provenance. This excludes a shortcut, not general source solutions.
Read-only review of the N1/N2/N3 puzzle lane summaries found no established
selector to import; their scripts/data were not independently audited here.
Next: coupled source matching if pursuing this branch, while independently
fixing beta and U. No beta selection, self-tuning implementation or exact
32π result has been established.

Next completed audit: DERIVATIVE_BRIDGE_RESULTS.md derives the f(X) bridge's
polarization equation, new lapse stress, scalar current and properly relaxed
local kinetic coefficient. Eight exact identities and four finite sign checks
pass in derivative_bridge_audit_v3.py; two failed attempts are retained.
The fixed-metric sector is not a full Horndeski/gravity stability analysis.
On the checked exponential rolling background, power-law f(X) gives an
evolving bare a0 unless its exponent is zero, under a fixed Newton dictionary.
A new conditional candidate couples P³ to beta M²/Theta, with Theta the unit
normal expansion: Theta=3H gives a0bare=2H/beta and Cbare=3beta²/4.
This ties the scales functionally but leaves beta free, has a Theta=0
singularity, and needs a full action/constraint audit. Because P³ vanishes
through quadratic order on the vacuum, vacuum health cannot select beta.
Next: a microscopic or genuinely nonlinear/global rule fixing that coupling,
or a different interaction entering both sectors without destroying health.
Exact 32π remains unresolved; no full sourced galaxy dictionary is established.

Subsequent source/bridge check: SELF_TUNING_GALAXY_BRIDGE_RESULTS.md verifies
arXiv:2009.01720v1 Secs. 2 and 5.1. Its well-tempered construction cancels
vacuum energy with a rolling scalar but contains the de Sitter scale in the
action. A schematic direct linear identification of that scalar with the
cubic galaxy coefficient fails vacuum-shift invariance by −Kc epsilon P³
and generally makes the coefficient time dependent. Six exact identities and
a bounded execution manifest are saved. This is a restricted compatibility
test, not a no-go theorem for all self-tuning. Next: a derivative-dependent,
shift-invariant galaxy bridge in one action, including re-derived degeneracy
and source equations. No such combined action has yet been established; no
32π prediction is claimed.

VACUUM_OFFSET_SELECTION_RESULTS.md proves that the current linear-lambda
trial family retains an arbitrary additive vacuum energy. Its unique positive
de Sitter vacuum and the previously established local linear stability
conditions survive for every V0>−2√(AB), while the conditional bare ratio
Lambda/a0bare² varies strictly with V0. Independently, changing Kc leaves
the vacuum and quadratic action unchanged and changes that ratio by Kc².
Seven exact symbolic identities pass in vacuum_offset_selection.py; output is
saved in vacuum_offset_selection_checks.json. This closes stability alone as
a coefficient selector in this family, not all possible theories. Exact 32π
and the observed galaxy acceleration dictionary remain unresolved. The next
priority is a physical principle that removes/determines the vacuum offset and
links the remaining galaxy coupling to cosmology; source matching alone cannot
supply the missing prediction. A preliminary self-tuning literature search
was not completed or used as evidence. User requested this checkpoint be pushed
to preserve progress while tokens are low.

The exact 32π coefficient remains unresolved. The completed derivations, audit contracts, scripts, and recorded computations are in this folder. The latest completed result is `CLOCK_CONE_RESULTS.md`, committed as 04ea72785: the exact extrapolated retarded clock response fails the finite-cone analyticity test. This does not establish an instability at real spatial momentum or exclude a bounded effective theory with additional high-frequency physics.

The canonical-clock construction in `CANONICAL_CLOCK_RESULTS.md` links the vacuum and galaxy scales, but leaves a free dimensionless combination. It does not derive 32π without imposing it.

## Unfinished next test

Under that construction's stated assumptions, imposing the target gives

    D(1+D)^2 = 24π(3λ−1),  λ>1,
    G_cosm/G_N = 48π/(1+D)^3.

Consequently D exceeds the positive root of D(1+D)^2=48π, and the cosmological-to-local gravitational coupling ratio is below approximately 0.824. This conditional prediction suggests a primordial-nucleosynthesis test.

An observational exclusion has NOT been completed. Before claiming one, verify the BBN-only interval in Alvey et al., arXiv:1910.10730, and its transfer assumptions: constant couplings during BBN, unchanged particle and nuclear physics, negligible extra clock or surface radiation, and the stated local Newton calibration. A CMB-derived bound cannot be imported automatically into preferred-foliation gravity. Additional radiation or evolving couplings require a separate calculation.

Next priority: finish that conditional observational test, then investigate a causal completion that also fixes the remaining coefficient. Do not describe either task as solved or claim global novelty from repository searches.

## Subsequent completed check

The previously unfinished source transfer is now documented in CLOCK_BBN_RESULTS.md. Equation (9) of the checked primary source gives the BBN-only interval [0.92,1.04] at 95.4% confidence. Under the explicit standard-radiation, constant-coupling transfer assumptions, the candidate's entire R<0.8238741 range is outside it. Twelve computation checks and execution provenance are saved. This closes that restricted observational branch; evolving couplings or additional radiation are separate, unverified modifications. Exact 32π remains unresolved.

The subsequent CLOCK_COEFFICIENT_BOUND.md proves the all-parameter obstruction C>(2/3)R/(1−R)^3. With the same conditional R>=0.92 lower endpoint, C>1197.9167, nearly twelve times 32π. An additive constant would have to cancel more than 91.6% of U0. Changing existing parameters alone cannot rescue this branch. Thirteen symbolic/sample checks and provenance are saved; no independent likelihood was computed.

VARIABLE_CLOCK_RESULTS.md changes the constant-coupling premise via lambda(q). It derives the coupled homogeneous equations and a stable vacuum criterion (S U)''>0 with S=3lambda−1. A linear trial lambda=1+ell q has a unique homogeneously stable vacuum and early instantaneous force-balance roots near lambda=1. Sixteen checks pass. This does not prove an evolving solution, local galaxy matching, full stability or coefficient selection. The next executable test is a constrained radiation-plus-scalar trajectory including kinetic energy.

That trajectory test is now completed for five toy initial conditions in VARIABLE_CLOCK_TRAJECTORY_RESULTS.md. All reach the vacuum over 12 e-folds, including ±10% initial-q offsets at ell=10. The independently evolved H² formulation passes 19 checks with maximum relative constraint residual 2.274e−8; failed/sensitive log-H diagnostics are retained. The radiation-only toy has no observational fit or matter era. Next: inhomogeneous scalar health and cosmological-to-galaxy matching for lambda(q); coefficient selection remains unresolved.

VARIABLE_CLOCK_MODES_RESULTS.md now derives the full quadratic scalar action on the constant-q de Sitter vacuum of the local phenomenological model. An exact mode transformation proves fixed-wavevector future boundedness, scalar decay and metric freezing for the positive linear-coupling family; both scalar kinetic coefficients are positive for nonzero momentum. Fifty symbolic/finite checks pass, including twelve mode evolutions and six direct-equation comparisons. This does not establish radiation-era perturbative health, nonlinear strong coupling, causal completion, galaxy matching or 32π selection. Next: match the cosmological q* boundary to local galaxy gravity rather than assuming the flat-static q0 calibration.

GALAXY_SCALAR_MATCHING_RESULTS.md now tests a frozen-curvature weak-static scalar/flux truncation. Eight finite BVPs show a near-vacuum gradient-retaining branch that differs from pointwise relaxation at high local field, and a small-Z case that tracks the local root. Fifty BVP checks, four coefficient identities and eleven comparison-bound checks pass; two failed mesh attempts are preserved. The matched bare ratio is D³(3x⁴−1)/3, x=q*/q0; the previous Newton rescaling is conditional on local relaxation and changes this by (G_N/G)². No full metric/foliation matching or observed Newton dictionary is established. Next: coupled weak-source ADM matching; do not fit free D and ell and call that a derivation of 32π.

SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md derives necessary stationary spherical lapse, shift, radial-metric, scalar and polarization equations for the local kappa=0 branch; 30 symbolic checks pass. The clock trace feeds back into the scalar, scalar gradients enter a radial metric identity, and stationary coordinate sources have nonzero preferred-frame currents. Physical orbit acceleration depends on N²−exp(2sigma)V² and is not automatically the clock acceleration. The fixed unit-lapse, flat-spatial, constant-scalar mass shortcut fails at ell>0, but a general mass solution is not excluded. The true mass-free vacuum horizon has r_h²Lambda=3; density-radius 8π statements require a coupling dictionary. Next: a conserved compact-source model and coupled radial boundary solve; coefficient selection remains open.
