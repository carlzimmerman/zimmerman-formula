# Follow-up execution cards

Baseline: `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`. All twenty cards start **not started / open**. Read [FOLLOWUP.md](FOLLOWUP.md) before claiming one. These refine existing packets; the parent owner coordinates subdivision instead of duplicating it.

## R01 — Certify the actual active-density asymptote

**Refines:** E1, B2. **Dependencies:** none. **Allocation:** 0.5 agent-days.

**Exact target.** For B,D>0, 0<K<2 and u>0, prove rho_act=(2/3)(2-K)D u^3 from the displayed rho and w. With u(B+u)=A/r, A>0, prove r*u -> A/B and r^3*rho_act -> (2/3)(2-K)D(A/B)^3.

**First calculation.** Cancel B+2u/3 exactly before fitting any radial slope. Use the rationalized positive root u=2A/[r(B+sqrt(B^2+4A/r))] to avoid cancellation at large r. This audits the L304 surrogate, not the complete covariant stress.

**Deliverables:** ActiveDensity.lean with domains and limit hypotheses; exact_factorization.py; asymptotic_remainder.md.

**If supported:** Pass the coefficient and a finite-radius remainder bound to R02/R03; feed the source identity to B2 for its physical interpretation.

**If refuted or inconclusive:** If the published profile is inconsistent with the factorization, isolate the equation/version mismatch. A failed Lean tactic is not a mathematical refutation; retain the symbolic result with its formalization status.

**Source inputs:**

- `real_research/clock_2026/L304_phantom_active_mass.py`
- `real_research/clock_2026/L298_phantom_stress_tensor.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R01`. Include the shared result template and a manifest.

## R02 — Replace the fitted power with a shell-mass theorem

**Refines:** E1. **Dependencies:** R01. **Allocation:** 0.5 agent-days.

**Exact target.** For an exact shell rho=C/r^3, C>0, r>=r0>0, certify M(r)=M0+4*pi*C*log(r/r0). Bound the integral correction from the R01 asymptotic remainder for the actual profile.

**First calculation.** Reproduce the apparent exponent near 0.578 for a pure logarithm on the same sampled radial interval with r0=1000, then change r0 while holding the outer sample fixed. Track the interior mass M0 separately; starting a cumulative integral at the first grid point sets it to zero.

**Deliverables:** ShellMass.lean; cutoff_sensitivity.py; corrected_mass_comparison.json.

**If supported:** Replace the square-root extrapolation in a proposed patch, preserving its old output for comparison. Send physical predictions to R03 and the feedback question to R04.

**If refuted or inconclusive:** If the finite observed interval still resembles a power, label it a local approximation and bound its error; do not promote it to an asymptotic theorem or replace the central mass by zero.

**Source inputs:**

- `real_research/clock_2026/L304_phantom_active_mass.py`
- `real_research/clock_2026/L311_phantom_law.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R02`. Include the shared result template and a manifest.

## R03 — Derive corrected velocity curvature and its observable domain

**Refines:** F2, E1. **Dependencies:** R02. **Allocation:** 0.75 agent-days.

**Exact target.** Conditional on g^2=a0*G*M_total(r)/r^2 and circular motion, derive v^4=a0*G*M_total and beta=(1/4)d log M_total/d log r. For M_total=Mbase+C_log*log(r/r0), obtain beta=C_log/(4*M_total) and its curvature. Derive the curvature invariant C_beta=d beta/d log r+4*beta^2: C_beta=0 for the logarithmic mass model, while C_beta=beta/2 for a positive square-root contribution over a constant base mass. These are conditional shape relations, not new empirically established laws.

**First calculation.** Compare the logarithmic and square-root continuations using the same independent mass at an anchor radius, then the same local derivative as a separate matching experiment. Do not force both matches if the models lack that freedom. Before proposing an observation, estimate the covariance cost of a second derivative of the rotation curve; curvature can be formally distinctive yet observationally unusable.

**Deliverables:** VelocityCurvature.lean; matched_profile_comparison.py; observable_domain.md.

**If supported:** Choose radii where the predictions differ after mass, anisotropy and boundary uncertainties. Hand a frozen forward comparison to F2/R18; use R05 first for lensing.

**If refuted or inconclusive:** If the full metric equations do not license the starting force law, retain this as a conditional instrument calculation. If finite-range differences are below nuisance uncertainty, report the precision limit rather than declaring a detection.

**Source inputs:**

- `real_research/clock_2026/L305_phantom_rar_boost.py`
- `real_research/clock_2026/L311_phantom_law.py`
- `real_research/clock_2026/L312_law_implications.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R03`. Include the shared result template and a manifest.

## R04 — Test whether self-gravity stabilizes or amplifies the profile

**Refines:** E2, C4. **Dependencies:** R01, B2. **Allocation:** 1 agent-days.

**Exact target.** After B2 identifies a genuine additional source, test the conditional deep feedback system rho=A_g*g^3 and g^2=a0*G*M/r^2. It implies dM/d log r=K_g*M^(3/2), K_g=4*pi*A_g*(a0*G)^(3/2), rather than an imposed square-root mass. Within the same conditional feedback system, derive beta=K_g*sqrt(M)/4 and d beta/d log r=2*beta^2, then compare its sign/curvature with R03. Do not promote any of these diagnostic continuations to a physical solution before B2 licenses the source.

**First calculation.** For positive constants derive M^(-1/2)=M0^(-1/2)-(K_g/2)*log(r/r0). Test the finite-radius singularity against the first radius at which the deep, static or source approximation fails. A singular toy continuation does not refute a model outside that approximation.

**Deliverables:** Feedback.lean or exact differential identity; feedback_ode.py; validity_vs_singularity.md.

**If supported:** If the growth obstruction lies inside the valid domain, derive the necessary regulating change: pressure, finite supply, changed branch or coupling. Each candidate must appear in the action/EOM and pass conservation before a new solve.

**If refuted or inconclusive:** If rho_act is only effective bookkeeping, prohibit re-insertion as a second source and return to B2. If the approximation fails first, solve through that transition with a new controlled operator instead of extrapolating the toy singularity.

**Source inputs:**

- `real_research/clock_2026/L299_phantom_halo_selfconsistent.py`
- `real_research/clock_2026/L305_phantom_rar_boost.py`
- `real_research/clock_2026/L311_phantom_law.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R04`. Include the shared result template and a manifest.

## R05 — Separate density slope, lensing slope and dynamical source

**Refines:** B2, E3. **Dependencies:** B2, R02. **Allocation:** 1 agent-days.

**Exact target.** Derive projected lensing and dynamics from the same physical potentials: ds^2=-(1+2Psi)dt^2+a^2(1-2Phi)dx^2, Weyl potential=(Phi+Psi)/2. A 3D density slope is not directly a shear slope.

**First calculation.** For a controlled spherical source, compute the Abel projection, mean interior surface density and DeltaSigma separately, with inner core and outer cutoff explicit. Compare to direct null-geodesic/weak-field potential integration where applicable.

**Deliverables:** projection_dictionary.md; joint_projection.py; cutoff_and_slip_grid.json.

**If supported:** Pass a mock observable and covariance model to E3/R18. Mark which signatures are preserved when anisotropic stress changes slip.

**If refuted or inconclusive:** If only an inferred Poisson density is available, label its projection conditional on a metric bridge. Do not call a ratio of virial mass estimates M_lens/M_X without modeling those observables.

**Source inputs:**

- `real_research/clock_2026/L279_quasistatic_slip_from_action.py`
- `real_research/clock_2026/L304_phantom_active_mass.py`
- `real_research/clock_2026/L309_three_sector_cluster.py`
- `real_research/clock_2026/L310_instrument_sweep.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R05`. Include the shared result template and a manifest.

## R06 — Lock down the unequal-mass conservation obstruction

**Refines:** G1. **Dependencies:** none. **Allocation:** 0.25 agent-days.

**Exact target.** For positive masses prove m1*sqrt(m2)=m2*sqrt(m1) iff m1=m2. Apply it only to the proposed isolated static per-body ansatz; derive and state the translation-conservation obligation for its intended action.

**First calculation.** Use masses 1 and 4 with a0*G=r=1: the opposing force magnitudes are 2 and 4. Check separately the test-particle limit and the exactly equal-mass case.

**Deliverables:** PairObstruction.lean; mass_ratio_counterexamples.json; premise_scope.md.

**If supported:** Preserve PD20/PD21 as conditional algebra, withdraw the unsupported action-derived amplitude in a proposed correction, and route the actual force calculation to R07.

**If refuted or inconclusive:** If a completion supplies additional time-dependent field momentum or external force, derive that contribution and its boundary conditions explicitly. It defines a different physical problem; it cannot be inserted silently to excuse a static isolated force imbalance.

**Source inputs:**

- `deepseek_push/lean/PD20_two_body_factor.lean`
- `deepseek_push/lean/PD21_law_of_nature.lean`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R06`. Include the shared result template and a manifest.

## R07 — Derive the correct mass-ratio force from the action

**Refines:** G1. **Dependencies:** R06, B1. **Allocation:** 1 agent-days.

**Exact target.** Derive a two-source force from the action translation identity or stress-flux surface integral. Establish which hypotheses permit import of the known isolated deep-MOND virial theorem.

**First calculation.** Read the primary virial theorem in full and translate normalization, point-mass/extended-body limits and boundary terms. Recover the small-mass limit and equal-and-opposite forces before producing an equal-mass amplitude.

**Deliverables:** two_source_stress.md; PairForce.lean for the justified algebra; literature_hypotheses.json.

**If supported:** Treat known virial content as inherited mathematics. A novel result must be an action-specific correction, controlled finite-size term or applicability theorem; give the benchmark to R08.

**If refuted or inconclusive:** If screening or external fields break the virial hypotheses, derive their boundary/work terms rather than apply the isolated formula. Return the exact missing bridge for B1/G1 if no common action is available.

**Source inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`
- `real_research/reviews/kappa_unit_response_2026_09_20/ACTION_ROUTE.md`
- `deepseek_push/lean/PD18_wide_binary_face.lean`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R07`. Include the shared result template and a manifest.

## R08 — Validate a nonlinear two-source solver independently

**Refines:** G2. **Dependencies:** R07, F1. **Allocation:** 1 agent-days.

**Exact target.** Resolve force from two independent evaluations: the matter/source force and a field-stress flux integral, on a finite-size two-source regularization of the selected operator.

**First calculation.** Run mass ratios 1, 1/4 and 1/100 at one separation, then halve source radius and mesh size independently. Check total-force cancellation, analytic isolated controls and boundary sensitivity.

**Deliverables:** two_source_solver.py; force_balance_convergence.json; regularization_limits.md.

**If supported:** Use the convergence error to bound finite-size/mass-ratio corrections and feed the validated solver to R09. Do not infer an entire continuous parameter range from three cases.

**If refuted or inconclusive:** If source regularization dominates, refine that limit before astrophysical forecasting. If force and stress methods disagree, freeze the amplitude claim and isolate the discretization/operator error.

**Source inputs:**

- `real_research/reviews/mi_aqual_solve_framework_kernel_2026.py`
- `qwen_claude_field_theory/theory_2026/aqual_solver_2026.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R08`. Include the shared result template and a manifest.

## R09 — Classify which binary signatures survive environment and size

**Refines:** G2, G3, F3. **Dependencies:** R08, B4. **Allocation:** 0.75 agent-days.

**Exact target.** Produce a regime diagram in g_internal/g_external, separation/xi and mass ratio, marking isolated, external-field-dominated and screened limits of the actual candidate.

**First calculation.** Calculate these ratios for an admissible pilot population before simulating velocities. Carry the same xi and local-constraint parameter point everywhere.

**Deliverables:** binary_regime_map.csv; matched_environment_grid.py; recoverable_observable.md.

**If supported:** Forward-model the surviving orientation or velocity statistic with contamination and selection through R18; state which mass calibration remains necessary.

**If refuted or inconclusive:** If the accessible systems are fully screened, record the predicted null and redirect effort to larger systems or another independently accessible regime. Do not keep amplifying the isolated plateau headline.

**Source inputs:**

- `real_research/reviews/mi_wb_gext_kappa_route_2026.py`
- `real_research/reviews/mi_wb_dr3_feasibility_2026.py`
- `fable_independent_2026/L47_xi_collision.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R09`. Include the shared result template and a manifest.

## R10 — Stop mixing inequivalent full force laws

**Refines:** B1, A3. **Dependencies:** none. **Allocation:** 0.5 agent-days.

**Exact target.** Compare the rational auxiliary response, the PD21 quadrature law g^2=gN^2+a0*gN, and the L311 deep law with an added active source. Determine exact equivalence or inequivalence with physical s, a0 and mass fixed.

**First calculation.** At one transition acceleration solve each response with the same parameters. Then compare their weak/high-field expansions and scale-independent derivative ratios; a shared leading deep asymptote is insufficient.

**Deliverables:** model_equivalence_table.md; CompletionSeparation.lean; transition_comparison.json.

**If supported:** Assign distinct model IDs when the laws differ. Attach orbital quarter-slope and screening predictions only to the model from which they were derived; hand the distinct curves to R18.

**If refuted or inconclusive:** If a field or parameter transformation allegedly identifies them, derive the transformation of matter coupling and independently measured scales as well. A change of observable or refit is not equivalence.

**Source inputs:**

- `deepseek_push/lean/PD21_law_of_nature.lean`
- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`
- `real_research/reviews/orbital_shape_law_2026_09_20/README.md`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R10`. Include the shared result template and a manifest.

## R11 — Try a genuinely new selector with a noncircular falsifier

**Refines:** A1. **Dependencies:** R10. **Allocation:** 0.75 agent-days.

**Exact target.** Write one new physical equation capable of selecting lambda=1 while keeping s independently fixed. Candidates must supply a microscopic response normalization, a protected matching relation or a derived boundary condition, not channel counting alone.

**First calculation.** Evaluate the proposed equation at lambda=1 and lambda=2 before a long derivation. List every externally fixed quantity and every calibration using galaxy a0. Reject algebraic restatements of kappa=1/2 immediately.

**Deliverables:** selector_assumption_ledger.md; selector_discriminator.py; SelectionOrObstruction.lean.

**If supported:** Prove uniqueness in the declared class and check stability under allowed action perturbations. Send an independently selected response invariant to R12 and a noncircular measurement prediction to A2.

**If refuted or inconclusive:** If both coefficients survive, record the new selector specific obstruction and move to a materially different mechanism. If none survives the budget, retain lambda=1 as a model postulate and pursue its empirical consequences; do not repackage the existing counterfamily as a new result.

**Source inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`
- `real_research/reviews/kappa_unit_response_2026_09_20/THERMAL_ROUTE.md`
- `fable_independent_2026/L226_kappa_and_the_free_function.py`
- `deepseek_push/lean/PD21_law_of_nature.lean`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R11`. Include the shared result template and a manifest.

## R12 — Find a second observable that breaks calibration degeneracy

**Refines:** A2, A3. **Dependencies:** R10. **Allocation:** 0.75 agent-days.

**Exact target.** Identify two observables with linearly independent sensitivities to response shape and independent normalization, after nuisance parameters are included. An invariant such as mu_second(0)/mu_prime(0)^2 is a candidate, not automatically a measurable statistic.

**First calculation.** Compute the Jacobian rank for candidate observables under s, lambda, mass scale and distance rescalings. Try orbital shape plus independently matched external-field response, with all domain restrictions stated.

**Deliverables:** identifiability_rank.py; ObservableDegeneracy.lean; independent_pair_protocol.json.

**If supported:** If a degeneracy is broken, specify the additional measurement and its attainable calibration requirements, then use R18 for mock recovery.

**If refuted or inconclusive:** If the rank remains deficient, give an explicit parameter transformation preserving the observations. Search a new observable with a different dependence rather than collecting more copies of the same relation.

**Source inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`
- `real_research/reviews/orbital_shape_law_2026_09_20/README.md`
- `real_research/reviews/field_orbit_reciprocity_2026_09_20/README.md`
- `deepseek_push/PD10_zero_mode_measured.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R12`. Include the shared result template and a manifest.

## R13 — Determine whether the BH photospheric gravity is independent

**Refines:** H1, H2. **Dependencies:** none. **Allocation:** 0.5 agent-days.

**Exact target.** Distinguish g_fit from g_grav in the atmosphere model. Carry g_fit=g_grav-g_rad+g_dyn with a documented sign convention and derive its effect on the inferred Gamma.

**First calculation.** Eliminate Gamma symbolically from the wave-U chain and recover M=g_fit*R^2/G under its assumptions. Then construct two gravity decompositions with the same g_fit,T but different true mass if the atmosphere permits them.

**Deliverables:** GravityReadout.lean; gravity_decomposition.py; atmosphere_source_audit.md.

**If supported:** If the source model identifies g_grav or bounds the correction, propagate that independent bound to H2/R15 instead of treating the algebraic round trip as a validation.

**If refuted or inconclusive:** If gravity decomposition remains free, report an interval/identifiability obstruction and the needed independent mass or radiation-force measurement. Preserve I12 as a conditional identity.

**Source inputs:**

- `real_research/reviews/bhstar_u1_decircularization.py`
- `fable_independent_2026/lean_2026/I12_bhstar_dial.lean`
- `real_research/reviews/bhstar_p1_empirical_rigor.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R13`. Include the shared result template and a manifest.

## R14 — Separate wind, opacity and photosphere radius information

**Refines:** H1. **Dependencies:** none. **Allocation:** 0.75 agent-days.

**Exact target.** Build separate likelihoods or bounded constraints for launch radius, line-forming radius, photospheric radius and slab thickness. Establish which observable links any two.

**First calculation.** Use the proper wind interval-membership test and invert the factor required for a given radius. For opacity distinguish the ionization parameter at the illuminated boundary from the attenuated interior field and total neutral from excited-state populations.

**Deliverables:** radius_constraint_graph.json; wind_interval_check.py; transfer_boundary_contract.md.

**If supported:** Combine only genuinely independent constraints, including their common mass/continuum inputs, and send the resulting radius-density covariance to R15.

**If refuted or inconclusive:** If the available spectrum fixes only N_H/n_H, construct the surviving radius family and specify a lag, angular size or independently normalized ionizing flux that would break it. Neither large opacity nor a broad wind-factor range alone proves or disproves the transition.

**Source inputs:**

- `real_research/reviews/bhstar_r1_wind_kinematics.py`
- `real_research/reviews/bhstar_s1_u_route_void.py`
- `real_research/reviews/bhstar_t1_kepler_predictions.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R14`. Include the shared result template and a manifest.

## R15 — Design a noncircular population falsifier

**Refines:** H2, F4. **Dependencies:** R13, R14. **Allocation:** 0.75 agent-days.

**Exact target.** Use the dimensionless residual D_B=log[r_B^4*n_H*c^2*mu_gas*m_p/(4*G*M^2)] only when radius, density and mass are constrained independently of D_B=0. Test exponent, intercept and intrinsic scatter separately.

**First calculation.** Compute the sensitivity vector (4,1,-2) with respect to (log r_B, log n_H, log M). Use the full covariance, including shared continuum/line-fit information, to determine whether the intercept is identifiable.

**Deliverables:** population_protocol.json; joint_covariance_mocks.py; measurement_value_table.md.

**If supported:** Freeze the estimator and a held-out population or observation design. Rank missing measurements by reduction of uncertainty in D_B, not convenience.

**If refuted or inconclusive:** If no direct radius exists, publish the required observation and keep the relation a conditional prediction. Do not generate radii from the transition law and then test that same law.

**Source inputs:**

- `real_research/reviews/bhstar_t1_kepler_predictions.py`
- `fable_independent_2026/lean_2026/I11_bhstar_kepler.lean`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R15`. Include the shared result template and a manifest.

## R16 — Challenge the cosmological operator under variable changes

**Refines:** C2, B3. **Dependencies:** C1, B3. **Allocation:** 1 agent-days.

**Exact target.** Build an invariance audit for the physical FRW evolution: constraint propagation, dimensional consistency, physical observable invariance and two independent reductions.

**First calculation.** For a constant-background pencil transform rows and columns by nonsingular matrices and compare generalized physical roots. For a time-dependent change z=S(t)y, include the extra S_dot*S_inverse term; instantaneous generator eigenvalues need not be invariant.

**Deliverables:** operator_transformation_contract.md; constraint_basis_audit.py; physical_mode_comparison.json.

**If supported:** If density/curvature observables agree and constraints converge, promote the operator to C2/D1/R17. Formalize the finite matrix identity, separating it from a full cosmological proof.

**If refuted or inconclusive:** If a root changes only because residual equations are least-squares weighted or a transformed derivative is omitted, identify that computation failure. Do not call it a physical instability or repair it by choosing a convenient variable scale.

**Source inputs:**

- `real_research/clock_2026/L291b_frw_ymod_carrier.py`
- `real_research/clock_2026/L300_exact_a1_arbiter.py`
- `real_research/clock_2026/L306_s8_closure.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R16`. Include the shared result template and a manifest.

## R17 — Test whether baryonic forcing fixes entropy and phase

**Refines:** C3, D1. **Dependencies:** R16. **Allocation:** 1 agent-days.

**Exact target.** Determine the homogeneous entropy mode and the retarded response to an oscillating baryon-photon source separately. Large static susceptibility does not determine time-dependent phase or erase homogeneous initial data.

**First calculation.** Solve a small forced linear system with two distinct initial entropy amplitudes. Then repeat using the reviewed action operator, consistent k_phys=k_com/a, and a stated primordial covariance.

**Deliverables:** forced_mode_control.py; retarded_transfer.py; entropy_phase_report.md.

**If supported:** If an attractor suppresses the mode before the relevant epoch, quantify its basin and residual spectrum, then pass those initial conditions to D1 rather than setting alpha=(1-R)^2.

**If refuted or inconclusive:** If a homogeneous mode survives, retain its amplitude and correlation as initial-condition parameters. A fluid control illustrates the distinction but does not by itself refute or validate the action.

**Source inputs:**

- `real_research/clock_2026/L307_seeding_gate.py`
- `real_research/clock_2026/L308_referee_audit.py`
- `real_research/clock_2026/L296_doublet_selfenergy.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R17`. Include the shared result template and a manifest.

## R18 — Run a blinded discrimination challenge

**Refines:** F2, Q3. **Dependencies:** R10. **Allocation:** 1 agent-days.

**Exact target.** Determine whether one feasible observable distinguishes the surviving models after geometry, calibration and selection, without knowing which model generated the mock.

**First calculation.** Use an independently reviewed candidate population and validated forward models. Freeze nuisance priors, statistic and decision rule; have the integrator withhold the generating model and nuisance draw from the fitting worker.

**Deliverables:** blind_protocol.json; generation_manifest.json; recovery_and_coverage.json.

**If supported:** If discrimination has calibrated power and coverage, freeze a held-out real-data analysis. Require the applicable F1/G2/H1/B2 input first; R10 alone supplies only model definitions.

**If refuted or inconclusive:** If the models are confused, report the degeneracy and minimum missing precision/observable. Never repair the same held-out sample and keep calling it held out; start a new registered version.

**Source inputs:**

- `real_research/reviews/particle_free_validation_2026_09_20/README.md`
- `real_research/reviews/particle_free_validation_2026_09_20/precision_budget.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R18`. Include the shared result template and a manifest.

## R19 — Make the load-bearing claims fail when their premise is wrong

**Refines:** Q2. **Dependencies:** none. **Allocation:** 0.5 agent-days.

**Exact target.** For only the claims used in the current release candidate, replace narrative-only checks with independently computed predicates and preserve the intended evidence boundary.

**First calculation.** Try four controls: integrate a known logarithmic mass profile, perturb channel slope away from one, change pair mass ratio away from one, and use a radius outside the declared wind interval. A relevant check must fail for the intended reason.

**Deliverables:** claim_check_map.json; negative_controls.py; proposed_check_corrections.diff.

**If supported:** Attach fresh logs and printed Lean axioms to Q2/Q4/R20. Count physical premises and observational comparisons separately from algebra and software checks.

**If refuted or inconclusive:** If the advertised gate cannot fail, relabel it as a status assertion or implement an actual test in a proposed patch. Do not broaden thresholds after seeing an unfavorable result or let a failing negative control overwrite the main run.

**Source inputs:**

- `real_research/clock_2026/L309_three_sector_cluster.py`
- `real_research/clock_2026/L312_law_implications.py`
- `deepseek_push/lean/PD21_law_of_nature.lean`
- `real_research/reviews/bhstar_r1_wind_kinematics.py`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R19`. Include the shared result template and a manifest.

## R20 — Choose the strongest surviving result and dispatch the next cycle

**Refines:** Q4. **Dependencies:** none. **Allocation:** 0.5 agent-days.

**Exact target.** Integrate reviewed results as they arrive and select a paper-sized theorem, obstruction or independent instrument; keep the next ready scientific move assigned.

**First calculation.** For each returned result ask: which exact implication changed, which model version did it use, what downstream evidence is stale, and what new discriminator follows? A completed process or more PASS rows is not sufficient.

**Deliverables:** FOLLOWUP_REPORT.md; MODEL_STATUS.json; NEXT_DISPATCH.json; paper_claim.md.

**If supported:** Promote only reviewed claims with raw evidence. Prepare direct-main patches and a reproducible release outline. Run the next nonduplicated ready packet after its prerequisite is checked.

**If refuted or inconclusive:** If a route is refuted, close that branch and preserve its obstruction; select an alternative mechanism with a different failed premise. If no executable route exists, state the exact missing input and keep the scientific claim open rather than fabricate closure.

**Source inputs:**

- `real_research/swarm_week_2026_09_20/TASKS.json`
- `real_research/swarm_week_2026_09_20/RESULT_TEMPLATE.md`

**Owned output:** `real_research/swarm_week_2026_09_20/followup_work/R20`. Include the shared result template and a manifest.
