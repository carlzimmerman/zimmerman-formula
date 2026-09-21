# Swarm work packets

Baseline: `be1e8c6326230c3c917b984516a6c67d3b17b1b3`. Every task below starts **not started / claim open**.

Each task inherits the [program evidence and coordination contract](PROGRAM.md). The time estimate is an allocation for reaching a decision, not a promise to solve the problem. Outputs belong only in the named packet directory.

## A1 — Select the half, or prove the remaining freedom

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** With s fixed independently of a0, identify an additional physical condition that forces lambda=1 in kappa=1/(2 lambda), or certify that the stated conditions leave lambda free.

**First discriminator.** Apply every proposed selector to W_lambda for lambda=1/2, 1, 2. Channel exchange, saturation and a single dimensionful scale already survive this family; they cannot by themselves select the half.

**Method and week-one boundary.** Try three genuinely distinct routes: a symmetry/Ward identity, an independently normalized response measurement, and a matching condition to the covariant action. Write the selector before solving it. Formalize the strongest selection or nonselection theorem, with scale and field redefinitions explicit. The existing counterfamily is inherited evidence. This packet must test a new explicit selector or give a new obstruction to that selector; interpret A2 rather than duplicate its likelihood.

**Success.** An explicit noncircular selector eliminates every competing lambda in its declared class; alternatively a certified family establishes the precise underdetermination and leaves lambda=1 as a declared postulate. Merely reproducing the already certified W_lambda family does not count as new scientific progress.

**Rejection or inconclusive.** Reject any argument that defines s=2a0, assumes unit susceptibility, or replaces a dimensionless coefficient by a second scale and then forbids it by naming. Failure of one selector does not prove no future action can select the half.

**Read these inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`
- `real_research/reviews/kappa_unit_response_2026_09_20/UnitResponse.lean`
- `fable_independent_2026/L226_kappa_and_the_free_function.py`
- `deepseek_push/lean/PD12_completion_independence.lean`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/A1`

**Deliverables:** `selection_contract.md`, `Selector.lean`, `counterfamily.json`.

## A2 — Measure normalization continuously, with independent scale inputs

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** none

**Target.** Determine what existing data actually identify about lambda or kappa, without treating a deep-law exponent or two fixed model comparisons as an intercept likelihood.

**First discriminator.** Trace every PD10 precision number to actual rows and likelihood code. Perturb the normalization while holding the deep power-law exponent fixed; test whether the claimed slope statistic can distinguish it.

**Method and week-one boundary.** Reuse the existing galaxy-weight/bootstrap audit; add continuous normalization profiling and shared distance, inclination, stellar mass-to-light and gas covariance. Keep external s calibration independent and trace any cosmology dependence. Start with mock recovery and a small declared pilot, not a catalog-wide discovery claim.

**Success.** A reproducible profile likelihood or posterior with calibration priors, data lineage and injected-parameter recovery; report whether 1/2 is distinguishable from nearby values, rather than just inside an interval.

**Rejection or inconclusive.** If nuisance freedoms make normalization unidentifiable, return an identifiability bound and the missing measurement. Do not promote hard-coded PASS strings or footing agreement to a sub-percent measurement.

**Read these inputs:**

- `deepseek_push/PD10_zero_mode_measured.py`
- `fable_independent_2026/L232_sparc_parameter_free.py`
- `fable_independent_2026/L232_robustness_audit.py`
- `fable_independent_2026/L232_ROBUSTNESS_REPORT.md`
- `real_research/reviews/particle_free_validation_2026_09_20/README.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/A2`

**Deliverables:** `normalization_protocol.json`, `fit_recovery.py`, `normalization_report.md`.

## A3 — Find an independent curvature or response-shape prediction

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** A1

**Target.** Does the mechanism predict a second dimensionless quantity, such as mu_second(0)/mu_prime(0)^2, beyond the adjustable acceleration normalization?

**First discriminator.** For rational and exponential channels with the same p(0)=0 and p_prime(0)=1, compare the second derivative and finite-field response. This distinguishes a real shape prediction from normalization alone.

**Method and week-one boundary.** Derive the response jet from each explicitly allowed action; remove coefficients absorbed by rescaling y. Classify remaining independent shape parameters and connect one to an orbital observable. At the degenerate y=0 boundary use right derivatives and state regularity. Rational-versus-exponential controls already exist. Use them as regression controls; the new target is a physically derived restriction beyond those controls.

**Success.** A scale-independent observable fixed by the specified mechanism, with a conditional Lean identity and a counterexample family for weaker assumptions; bounded literature comparison before any novelty claim. Reformatting an existing curvature or finite-shape counterexample alone is not a new result.

**Rejection or inconclusive.** If all curvature is independently tunable, record that the mechanism predicts only a universality class. Do not call another algebraic consequence of the same assumed mu an independent physical input.

**Read these inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/ACTION_ROUTE.md`
- `real_research/reviews/orbital_shape_law_2026_09_20/README.md`
- `deepseek_push/lean/PD12_completion_independence.lean`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/A3`

**Deliverables:** `response_jet.md`, `ResponseJet.lean`, `shape_comparison.json`.

## B1 — Choose and reconcile one action version

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** Produce one explicit candidate action with fields, coefficient functions, matter metric, independent parameters and boundary conditions; establish which static and cosmological packages are actually limits of it.

**First discriminator.** Compare operator placement, time-dependent coefficients, the definition of Y and the rational auxiliary action term by term. A shared label does not make different actions equivalent.

**Method and week-one boundary.** Create a version/translation table and derive the static reduction without inserting its target mu. Keep incompatible candidates as separate model IDs. Particle-free permits gravitational fields and their Noether charges; record all propagating degrees of freedom and free initial data rather than disguising them as no extra component.

**Success.** A traceable action-to-equations map, or an exact obstruction identifying the term that prevents a common embedding. All downstream computations name a single version.

**Rejection or inconclusive.** If no common action exists yet, preserve independent static and cosmological candidates. Do not combine their favorable predictions into one theory.

**Read these inputs:**

- `qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md`
- `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`
- `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/FULL_VARIATION.md`
- `real_research/clock_2026/L290_ymod_carrier.py`
- `real_research/clock_2026/L297_complete_action.py`
- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/B1`

**Deliverables:** `action_contract.md`, `model_versions.json`, `static_reduction.py`.

## B2 — Derive physical stress, both metric potentials and conservation

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** B1

**Target.** Derive delta S/delta g, the scalar/clock equations and their Ward identity; determine separately the sources of the dynamical potential Psi and the Weyl potential (Phi+Psi)/2. Use ds^2=-(1+2Psi)dt^2+a^2(1-2Phi)dx^2, c=1, matching the clock code.

**First discriminator.** On a static spherical ansatz with lapse and radial metric varied independently, compare the actual source with the claimed (w-1)rho active density. Check whether an inferred Poisson density is being added again as physical stress.

**Method and week-one boundary.** Vary before gauge fixing. Track anisotropic pressure and boundary terms. Establish on-shell conservation and compute the weak-field gravitational slip. Audit the L305 prescription g_N,b+GM_act/r^2 against this derivation. Formalize a finite algebraic Ward identity if feasible; retain the variational bridge as a separate obligation. Start with L279 and its coupling-removal control, then identify the genuinely missing full-carrier variation. Record a notation translation for static packages that name the dynamical potential Phi.

**Success.** One coupled source prescription with conserved total stress, explicit Phi and Psi equations, and an unambiguous no-double-counting rule usable by cluster and galaxy solvers.

**Rejection or inconclusive.** A conservation residual, unsupported identification of the dynamical and Weyl potentials, or double-counted source rejects the proposed reduction. A missing derivation is open, not proof the theory is false.

**Read these inputs:**

- `real_research/clock_2026/L298_phantom_stress_tensor.py`
- `real_research/clock_2026/L303_phantom_trace_energy.py`
- `real_research/clock_2026/L304_phantom_active_mass.py`
- `real_research/clock_2026/L305_phantom_rar_boost.py`
- `fable_independent_2026/L278_clock_sourced_poisson_lensing.py`
- `real_research/clock_2026/L279_quasistatic_slip_from_action.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/B2`

**Deliverables:** `metric_variation.md`, `ward_check.py`, `source_dictionary.json`.

## B3 — Audit physical modes and the range of validity

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** B1

**Target.** Find the physical kinetic/gradient modes after constraints, including the zero-field and zero-wavenumber strata, and bound where the effective theory is usable.

**First discriminator.** Compute the constraint rank and reduced kinetic matrix at a generic point and at y=0 and k=0 separately. Recheck whether the clock projector contributes mixing omitted by a fixed-foliation calculation.

**Method and week-one boundary.** Use exact or high-precision rank/Schur checks and an independent reduction. Check ghosts, spatial stability, ellipticity and the first nonlinear interaction after canonical normalization. Give a bounded strong-coupling estimate with assumptions; a full nonlinear well-posedness theorem is a later project.

**Success.** A documented healthy parameter region for named backgrounds, or a reproducible ghost/constraint/strong-coupling obstruction. Positive determinant alone is insufficient.

**Rejection or inconclusive.** No propagation claim from an overdetermined least-squares evolution or singular-variable rescaling. Finite parameter scans remain finite evidence; failure to prove global health is not a global no-go.

**Read these inputs:**

- `real_research/clock_2026/L287_dirac_count_clock_lapse.py`
- `real_research/clock_2026/L281_ellipticity_all_y.py`
- `real_research/clock_2026/L282_scalar_dispersion_from_action.py`
- `real_research/clock_2026/L300_exact_a1_arbiter.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/B3`

**Deliverables:** `mode_contract.md`, `reduced_operator.py`, `rank_and_health.json`.

## B4 — Find one parameter point that survives local constraints

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** B1

**Target.** Can one unchanged coefficient set meet local metric, preferred-frame, screening and gravitational-wave constraints while retaining a galaxy-scale effect?

**First discriminator.** Intersect the actual passing PPN corner with the claimed healing-length floor and the operator choice in B1. Do not reuse a floor from a different kernel or coupling.

**Method and week-one boundary.** Reproduce existing local gates at the same point and label the measured versus bare G conversion. Use current primary-source bounds with equation/units provenance. For any amended coupling rederive tensor and photon propagation; sharing a matter metric alone does not prove the graviton characteristic cone.

**Success.** A nonempty explicitly stated joint region, or a bounded incompatibility theorem for the chosen action. Supply the exact parameter file for other lanes.

**Rejection or inconclusive.** Passing different tests at different parameter points is not a joint solution. If bounds are source-limited, publish the symbolic intersection and mark numerical exclusion provisional.

**Read these inputs:**

- `real_research/clock_2026/L280_alpha2_reconciliation.py`
- `fable_independent_2026/L47_xi_collision.py`
- `fable_independent_2026/clock_swarm_2026/CK02_replacement_coupling.py`
- `fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/B4`

**Deliverables:** `common_point.json`, `local_gate_report.md`, `reproduce_local.py`.

## C1 — Solve the cosmological background before perturbing it

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** B1

**Target.** Derive a consistent FRW background and conserved charge from the chosen action, including the lapse equation and scalar evolution.

**First discriminator.** Insert the claimed chi=Ct and G1,G2 proportional to a^-3 history into the unmodified Euler-Lagrange equations; compute all residuals before any fit.

**Method and week-one boundary.** Keep lapse N until variation; solve background equations and continuity jointly. Distinguish action coefficients from background-dependent effective coefficients. Record which density amplitude is an integration constant and which is predicted.

**Success.** A regular background with convergent residuals and explicit initial data, or a proof that the imposed history is not a solution of the chosen action.

**Rejection or inconclusive.** Replacing constants by epoch-dependent values after variation changes the model unless derived. If a background needs a revised operator, issue a new model version and invalidate dependent evidence.

**Read these inputs:**

- `real_research/clock_2026/L283_frw_background_and_dust_fate.py`
- `real_research/clock_2026/L290_ymod_carrier.py`
- `real_research/clock_2026/L291_frw_ymod_carrier.py`
- `real_research/clock_2026/L297_complete_action.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/C1`

**Deliverables:** `background_equations.md`, `background_solver.py`, `background_residuals.json`.

## C2 — Build constraint-preserving FRW perturbations

**Priority:** P0 · **Allocation:** 2 agent-days · **Depends on:** C1, B3

**Target.** Derive the actual physical cosmological evolution operator and show that its constraints propagate, instead of identifying a frozen Minkowski growth root with expanding-universe evolution.

**First discriminator.** Differentiate the constraint equations along the proposed evolution. Check invariance under nonsingular variable rescaling and recover a controlled GR limit.

**Method and week-one boundary.** Eliminate constraints analytically or use a documented differential-algebraic formulation. Reproduce one independently derived matter-era mode and refine tolerances/time steps. Cover radiation, equality and late time only after the first background interval works. Week-one minimum is one verified sector plus the exact unresolved extension.

**Success.** An action-derived operator whose Hamiltonian/momentum residuals converge and whose physical modes are gauge/variable consistent; export a documented interface for transfer-function work.

**Rejection or inconclusive.** A least-squares fit of incompatible equations, dropped constraint or imported identical CDM equation cannot pass. If full evolution is unfinished, return the smallest failed equation and a runnable failing case.

**Read these inputs:**

- `real_research/clock_2026/L291b_frw_ymod_carrier.py`
- `real_research/clock_2026/L300_exact_a1_arbiter.py`
- `real_research/clock_2026/L301_exact_growth_budget.py`
- `real_research/clock_2026/L306_s8_closure.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/C2`

**Deliverables:** `frw_operator.md`, `evolve_constrained.py`, `constraint_convergence.json`.

## C3 — Prove or refute adiabatic seeding dynamically

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** C2

**Target.** Does evolution suppress an independently initialized relative-entropy mode, or is adiabaticity still an initial-condition assumption?

**First discriminator.** Correct physical/comoving wavenumber bookkeeping: k_phys=k_com/a. Compare independent adiabatic and isocurvature basis evolutions; a static Jeans response is not an initial-condition theorem.

**Method and week-one boundary.** Derive regular superhorizon modes of the actual equations. Evolve a basis through horizon entry and measure the transfer matrix for curvature and relative entropy, including their covariance and cross-correlation. Define the statistical isocurvature fraction from spectra; do not set it equal to (1-R)^2 by assertion.

**Success.** A quantified attractor/basin theorem or convergence-backed transfer matrix showing which entropy amplitudes decay and over which epochs; otherwise an explicit surviving mode and its required primordial bound.

**Rejection or inconclusive.** R approximately 1 in a quasistatic ansatz is insufficient. If no dynamical erasure occurs, retain the initial-condition parameter and pass it honestly to the Boltzmann lane.

**Read these inputs:**

- `real_research/clock_2026/L307_seeding_gate.py`
- `real_research/clock_2026/L296_doublet_selfenergy.py`
- `real_research/clock_2026/L308_referee_audit.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/C3`

**Deliverables:** `initial_mode_basis.md`, `entropy_transfer.py`, `seeding_matrix.json`.

## C4 — Predict the gravitational charge abundance, or expose its freedom

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** C1

**Target.** Can a particle-free gravitational Noether component obtain its required abundance from an attractor or boundary condition independent of the observed missing-mass density?

**First discriminator.** Vary the conserved-charge initial amplitude by factors 0.1, 1 and 10, with all action coefficients fixed. Determine whether the late density retains this memory.

**Method and week-one boundary.** Derive charge conservation and any allowed exchange term from the action. Check the basin and energy budget of a proposed attractor; compare its timescale to expansion. A free charge is permitted as a model parameter, but is not an abundance prediction.

**Success.** A noncircular abundance mechanism with a specified basin, or a formal parameter-count/identifiability statement that the amplitude remains free.

**Rejection or inconclusive.** Setting Omega_chi to the benchmark matter density and recovering its growth does not explain that density. Do not introduce a particle species to close this packet.

**Read these inputs:**

- `qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md`
- `real_research/clock_2026/L290_ymod_carrier.py`
- `real_research/clock_2026/L306_s8_closure.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/C4`

**Deliverables:** `charge_abundance.md`, `charge_sensitivity.py`, `abundance_status.json`.

## D1 — Connect the action to a Boltzmann calculation

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** C2, C3

**Target.** Produce an honest bridge between action-derived perturbations and CMB observables; determine precisely when a generic fluid proxy is equivalent.

**First discriminator.** Inventory which CLASS variables/couplings the existing wrapper actually supplies. Reproduce its control with the same settings, identifying generic fld and mond_a0=0 explicitly.

**Method and week-one boundary.** Derive the map for delta rho, delta p, velocity, anisotropic stress, metric constraints and initial conditions. Implement the smallest supported subset or provide a minimal patch/interface contract if the engine lacks it. Locate each model own acoustic peaks and retain full spectra. Day-one preparation can proceed before C2/C3; physical promotion cannot.

**Success.** A validated action-to-engine map and one controlled spectrum with error checks, or an exact list of missing operators demonstrating the proxy limitation. A full observational likelihood is stretch work beyond the first adapter.

**Rejection or inconclusive.** Agreement of a nearly pressureless fluid with CDM is a proxy result unless the map is proved. Fixed multipole samples are not automatically peak-height ratios; no sigma claim without a likelihood.

**Read these inputs:**

- `real_research/clock_2026/L292_cmb_ymod_carrier.py`
- `real_research/clock_2026/L295_baryonic_cmb_face.py`
- `real_research/clock_2026/L308b_cmb_tolerance_scan.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/D1`

**Deliverables:** `boltzmann_mapping.md`, `engine_adapter_or_patch.diff`, `spectrum_controls.json`.

## D2 — Compute an actual growth and small-scale consistency bound

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** C2

**Target.** Quantify growth and scale-dependent suppression from the derived operator at common primordial normalization; obtain a bound on observable error, not only on an instantaneous sound term.

**First discriminator.** Evolve the new operator and its control separately from matched initial conditions. Compute transfer ratios across declared k,z values and check whether accumulated effects exceed local estimates.

**Method and week-one boundary.** Propagate background and initial-condition uncertainties; integrate the actual matter power window for sigma8. Separate a linear transfer diagnostic from nonlinear forest flux modeling and thermal-history assumptions. Reuse existing forecast machinery only with its seed and conventions pinned. If C2 supplies only a matter-era sector, report conditional late-time growth. Absolute primordial-normalized P(k) or sigma8 additionally requires reviewed C3 initial covariance and a radiation-era transfer mapping from D1, or explicitly declared external transfer inputs; do not imply those were derived here.

**Success.** Convergence-backed D(k,a), transfer/P(k) and sigma8 differences, with a justified regime of accuracy or a reproducible scale-dependent failure.

**Rejection or inconclusive.** Two calls to the same growth function prove code identity only. Small instantaneous coefficients do not themselves establish a uniform 1e-4 growth bound.

**Read these inputs:**

- `real_research/clock_2026/L306_s8_closure.py`
- `real_research/clock_2026/L308_referee_audit.py`
- `fable_independent_2026/L224_sector_perturbations.py`
- `fable_independent_2026/L225_flux_power.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/D2`

**Deliverables:** `growth_error_budget.md`, `transfer_compare.py`, `growth_grid.json`.

## D3 — Rebuild the primordial and BBN exclusion in consistent units

**Priority:** P0 · **Allocation:** 0.5 agent-days · **Depends on:** none

**Target.** Determine which primordial-amplitude routes are actually excluded after restoring action normalization, units, continuity and reheating assumptions.

**First discriminator.** Dimensionally audit each conversion involving H_inflation, density, Planck scale and reheating temperature in SI and natural units independently.

**Method and week-one boundary.** Rederive the conditional bound with all c, hbar and G factors and specify the background equation of state and energy exchange. Test at one agreed physical reference value in both units. Do not use an invalid primordial exclusion as a premise that gravity is the only seed.

**Success.** A dimensionally identical bound in two conventions with named cosmological assumptions, or a corrected/withdrawn exclusion identifying the failed step.

**Rejection or inconclusive.** If the relevant inflationary action or reheating history is unspecified, return a conditional inequality, not an absolute kill or proof of survival.

**Read these inputs:**

- `real_research/clock_2026/L296_doublet_selfenergy.py`
- `real_research/clock_2026/L283_frw_background_and_dust_fate.py`
- `real_research/clock_2026/L307_seeding_gate.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/D3`

**Deliverables:** `unit_dictionary.md`, `primordial_bound.py`, `bound_comparison.json`.

## E1 — Reconcile the cluster mass budget before new fitting

**Priority:** P0 · **Allocation:** 0.5 agent-days · **Depends on:** none

**Target.** Identify precisely whether each quoted cluster requirement denotes excess mass or total mass, and reproduce a consistently normalized combined profile.

**First discriminator.** Trace the 2.2 requirement to its definition, separate baryons from excess, replace the literal lensing PASS with an unevaluated obligation, and integrate the actual sum whose slope is claimed. Derive the asymptotic scaling of the actual L304 expression: test the u~1/r, rho_act~u^3 branch and its logarithmic enclosed-mass growth against the extrapolated sqrt(r) claim. This is a check of that formula, not a derived full-action halo.

**Method and week-one boundary.** Recompute radial integrals with the inner cutoff and outer anchor explicit, preserving the 1/v(r) factor. Track the provenance of the 0.42 term. Evaluate sensitivity to cutoff and overdensity independently; classify fitted anchors and assumed priors.

**Success.** A reconciled total/excess mass table and actual combined slope with reproducible uncertainties; this is a bookkeeping prerequisite, not a self-consistent cluster solution.

**Rejection or inconclusive.** If the threshold or normalization source is ambiguous, leave the comparison unscored. A constant set from another profile is an input, not an emergent prediction.

**Read these inputs:**

- `real_research/clock_2026/L294_cluster_caustic_ymod.py`
- `real_research/clock_2026/L308_referee_audit.py`
- `real_research/clock_2026/L309_three_sector_cluster.py`
- `real_research/clock_2026/L304_phantom_active_mass.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/E1`

**Deliverables:** `mass_budget.md`, `reconcile_profile.py`, `mass_definitions.json`.

## E2 — Solve coupled infall and self-gravity

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** B2, E1

**Target.** Does a conserved particle-free carrier produce the required cluster profile when its own gravity and the baryons are included consistently?

**First discriminator.** Insert the current inflow profile into both continuity and the derived force equation, instead of holding a baryon-only free-fall speed fixed while adding mass afterward.

**Method and week-one boundary.** Attempt a spherical boundary-value/time-dependent solve with cosmological boundary density and flux explicit. Vary inner cutoff and outer radius; enforce the field equations and conservation. Record caustic/shell-crossing limitations and stop before applying a single-stream fluid beyond its domain.

**Success.** A converged joint solution over a stated radial range, or a controlled obstruction such as insufficient flux, unavoidable singularity or incompatible boundary conditions.

**Rejection or inconclusive.** Adding independently normalized profiles is not a coupled solution. Failure of a single boundary choice does not exclude the whole theory; describe the tested family.

**Read these inputs:**

- `real_research/clock_2026/L294_cluster_caustic_ymod.py`
- `real_research/clock_2026/L299_phantom_halo_selfconsistent.py`
- `real_research/clock_2026/L309_three_sector_cluster.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/E2`

**Deliverables:** `infall_contract.md`, `coupled_infall.py`, `residual_and_mass_grid.json`.

## E3 — Predict lensing and kinematics from the same cluster solution

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** B2, E2

**Target.** Can one parameter/boundary choice predict both projected lensing and tracer dynamics without an added particle halo?

**First discriminator.** Project Phi+Psi for lensing and use Psi for dynamics in the B2 metric convention, for the same solution; compare this with simply treating active density as the lensing source. The Weyl potential itself is (Phi+Psi)/2.

**Method and week-one boundary.** Build a synthetic cluster first, including projection, pressure/velocity anisotropy and aperture choices. Then identify one usable public/local cluster with independent baryonic and lensing information, full covariance where available, and frozen nuisance ranges. No mergers/cosmological ensemble simulation is promised in week one.

**Success.** A joint prediction and mock-recovery test, followed by a bounded real-data pilot if data and upstream derivations are ready; otherwise a concrete observational identifiability limit.

**Rejection or inconclusive.** Factor-of-two agreement with a virial estimate is not a likelihood or a resolved hydrostatic tension. Different best-fit parameters per observable do not pass a common-model test.

**Read these inputs:**

- `real_research/clock_2026/L304_phantom_active_mass.py`
- `real_research/clock_2026/L309_three_sector_cluster.py`
- `fable_independent_2026/L278_clock_sourced_poisson_lensing.py`
- `real_research/clock_2026/L279_quasistatic_slip_from_action.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/E3`

**Deliverables:** `joint_cluster_protocol.json`, `project_observables.py`, `joint_cluster_report.md`.

## F1 — Validate the rational field law in real geometries

**Priority:** P0 · **Allocation:** 1.5 agent-days · **Depends on:** none

**Target.** Calculate how source extent, disk flattening and boundary fields change the rational-action orbital prediction, with a measured numerical error.

**First discriminator.** First inventory candidate geometry, independent mass information and admissible radial coverage without selecting agreement; use that inventory to choose the smallest useful geometry grid. Inspect the implemented mu: existing candidate solvers use simple/standard kernels, not automatically mu=1-(1+g/b)^-2. Recover the analytic spherical and Newtonian controls before disks.

**Method and week-one boundary.** Use h,h/2,h/4 grids and R,2R domains; check source flux, PDE residual and observable convergence. Include the exact enclosed-mass-gradient correction at quarter fraction: beta=-1/4+3m/8. Select a small matrix of geometries that can distinguish the target responses.

**Success.** Validated numerical errors and geometry corrections for the actual rational operator, with a declared regime where the quarter-slope prediction can be tested.

**Rejection or inconclusive.** If corrections overwhelm the 4/3 versus alternatives separation, retire the spherical instrument for those objects and use full forward modeling. This does not refute the action.

**Read these inputs:**

- `real_research/reviews/orbital_shape_law_2026_09_20/README.md`
- `real_research/reviews/particle_free_validation_2026_09_20/README.md`
- `real_research/reviews/mi_aqual_solve_framework_kernel_2026.py`
- `qwen_claude_field_theory/theory_2026/aqual_solver_2026.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/F1`

**Deliverables:** `geometry_contract.md`, `rational_geometry_solver.py`, `convergence_table.json`, `candidate_admissibility.csv`.

## F2 — Build one held-out orbital test

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** F1

**Target.** Can suitable data discriminate the normalization-free quarter-slope relation with independently calibrated baryonic inputs? A separate full-curve comparison must state how its acceleration normalization is treated.

**First discriminator.** Inventory admissible geometry, independent baryonic masses and covariance without looking for objects close to 4/3. SPARC disks are useful benchmarks, not automatically spherical exteriors.

**Method and week-one boundary.** Freeze selection, observable, nuisance model, competing responses and decision rule. Run injection/recovery and adversarial systematics, then reserve a held-out subset. Fit raw velocities jointly with slope; do not select a noisy quarter-slope crossing and treat it as independent. Consume A2 provenance/covariance findings when available, but the quarter-slope branch does not require identification of lambda. The sample inventory begins in F1 on day one.

**Success.** A runnable frozen protocol with recovery and coverage checks, plus a held-out pilot only if an admissible sample and adequate precision exist.

**Rejection or inconclusive.** If no usable sample exists, publish that instrument limitation and specify the missing observation. The previous 2.7% ideal mass-ratio target is planning arithmetic, not achieved precision or guaranteed significance.

**Read these inputs:**

- `real_research/reviews/particle_free_validation_2026_09_20/README.md`
- `real_research/reviews/particle_free_validation_2026_09_20/precision_budget.py`
- `real_research/data/sparc_master_clean.csv`
- `real_research/data/SPARC_table.txt`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/F2`

**Deliverables:** `orbital_protocol.json`, `mock_recovery.py`, `heldout_or_feasibility_report.md`.

## F3 — Turn field-orbit reciprocity into a scale-dependent discriminator

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** none

**Target.** Determine whether a measurable correction to E^2(1-2 beta)=2 distinguishes the local AQUAL action from a screened fourth-order completion.

**First discriminator.** At matched physical external acceleration, derive the linear response operator with the screening term retained; check whether the local Green-function premise still applies.

**Method and week-one boundary.** Derive Fourier-space tensor response and its large/small r/xi limits, then compute one controlled real-space source. Compare local AQUAL, QUMOND and the actual screened candidate under identical geometry. Formalize a limit/remainder lemma if possible; otherwise report numerical bounds as such.

**Success.** An explicit, scale-dependent correction or a protected-limit theorem with an applicability domain; it must survive field/background matching and independent force normalization.

**Rejection or inconclusive.** No transplant of the local identity into a nonlocal/fourth-order model without derivation. The known AQUAL/QUMOND asymptotic distinction itself is not a new discovery.

**Read these inputs:**

- `real_research/reviews/field_orbit_reciprocity_2026_09_20/README.md`
- `real_research/reviews/field_orbit_reciprocity_2026_09_20/Reciprocity.lean`
- `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/F3`

**Deliverables:** `screened_reciprocity.md`, `response_kernel.py`, `reciprocity_limits.json`.

## F4 — Make redshift evolution an independently measurable test

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** Can a high-redshift observation distinguish the action actual pressure/density law from selection-induced apparent a0 evolution?

**First discriminator.** Trace the chosen a0(z) mapping back to the action; keep pressure and density prescriptions separate. Measure whether published masses use the same dynamics being tested.

**Method and week-one boundary.** Reuse the existing posterior propagation and high-z audit; add a forward-model identifiability test for one candidate or survey bin including beam smearing, pressure support, inclination and stellar/gas mass calibration. Freeze the mapping and selection before comparison.

**Success.** One quantitatively specified observational design or existing-data pilot that identifies the redshift signal independently, with a likelihood-based precision target.

**Rejection or inconclusive.** A fitted apparent a0, or statistical error that omits mass/dynamical systematics, does not establish fundamental scale evolution. Do not reinterpret DESI phenomenological parameters as this action background without a bridge.

**Read these inputs:**

- `fable_independent_2026/L273_desi_a0z_band.py`
- `fable_independent_2026/L275_desi_chains_bands.py`
- `fable_independent_2026/L276_data_vs_models_a0z.py`
- `fable_independent_2026/L274_a0z_theories_chart.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/F4`

**Deliverables:** `redshift_protocol.json`, `highz_mock.py`, `independence_report.md`.

## G1 — Derive the two-body force from momentum conservation

**Priority:** P0 · **Allocation:** 0.5 agent-days · **Depends on:** none

**Target.** Find the correct isolated comparable-mass force for the selected particle-free action, including the test-particle limit and conserved total momentum.

**First discriminator.** For the provisional rule g1=sqrt(a0 G M2)/r, g2=sqrt(a0 G M1)/r, set a0 G=r=1 and masses 1,4: opposing forces have magnitudes 2 and 4. This rule cannot be assumed as the static isolated action-derived pair force.

**Method and week-one boundary.** Read the current PD20 working file if available, but pin it separately if uncommitted. Derive force from the action stress flux/translation identity. Compare the known deep-MOND virial theorem with its exact hypotheses; do not label a known two-body formula novel. Formalize the unequal-mass conservation obstruction and the admissible conditional relation.

**Success.** A momentum-consistent mass-ratio law with correct limits, or an exact no-go for the proposed pair prescription. A conditional Lean algebra theorem remains valid even when its physical premises fail.

**Rejection or inconclusive.** Equal masses hide the force mismatch; passing that case alone is insufficient. Do not superpose isolated test-body responses in a nonlinear field theory.

**Read these inputs:**

- `deepseek_push/lean/PD18_wide_binary_face.lean`
- `deepseek_push/PD19_referee_report.md`
- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/G1`

**Deliverables:** `two_body_derivation.md`, `TwoBody.lean`, `mass_ratio_checks.json`.

## G2 — Solve binaries in the actual external field

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** G1, B4

**Target.** Determine whether any wide-binary observable retains discriminating power after the Galactic field, comparable masses, screening and population nuisances.

**First discriminator.** Compare g_internal, g_external and separation/xi over the actual sample. An isolated deep-MOND plateau may never be reached in the relevant environment.

**Method and week-one boundary.** Reuse existing feasibility results, with the correct kernel. Solve a small grid in mass ratio, separation and orientation with momentum/flux controls. Forward project orbit phases and eccentricities; model unresolved companions, chance alignments and selection before forecasting precision.

**Success.** A source-derived prediction table with controlled errors and one feasible registered observable, or a quantified null/insensitivity result for the sample.

**Rejection or inconclusive.** No mass-free label when the estimator depends on baryonic masses. Do not amend existing frozen preregistrations or claim future data have been observed; place a proposed protocol in this packet only.

**Read these inputs:**

- `real_research/reviews/mi_wb_gext_kappa_route_2026.py`
- `real_research/reviews/mi_wb_dr3_feasibility_2026.py`
- `fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md`
- `prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/G2`

**Deliverables:** `binary_prediction_grid.json`, `binary_forward_model.py`, `binary_feasibility.md`.

## G3 — Use a common screening length across system sizes

**Priority:** P2 · **Allocation:** 1 agent-days · **Depends on:** B4

**Target.** Can the same screening length explain local constraints, binaries and extended low-acceleration systems without retuning per object?

**First discriminator.** List the dimensionless pairs (r/xi,g/a0) for the already identified globular/galaxy/binary candidates and locate where models actually separate.

**Method and week-one boundary.** Use full response profiles, independent stellar-mass and external-field estimates, and dynamical/anisotropy nuisance ranges. Begin with mock size scaling, then at most a few well-documented systems. Combine with B4 allowed region instead of fitting xi anew in every system.

**Success.** A viable common interval or a bounded inconsistency between source classes, with an explicit degeneracy analysis.

**Rejection or inconclusive.** Conflicting fits under different kernels are not a common-parameter exclusion. Unknown binary fraction or tidal state may make an individual system inconclusive.

**Read these inputs:**

- `fable_independent_2026/L47_xi_collision.py`
- `fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md`
- `qwen_claude_field_theory/closure_2026/FINAL_THEORY_CANDIDATE_2026-09-05.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/G3`

**Deliverables:** `size_ladder.csv`, `screening_joint_fit.py`, `common_xi_report.md`.

## H1 — Separate BH-star gas-layer location from opacity thickness

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** Can the observations identify the absolute Balmer-layer radius and density independently of the claimed g=a0(rho_gas) relation?

**First discriminator.** Trace whether each radius is a thickness N_H/n_H, a photospheric radius, a launch radius or a measured absolute layer radius. For opacity distinguish total neutral hydrogen from the n=2 population.

**Method and week-one boundary.** Build an input/parameter provenance table from the primary source and CLOUDY outputs if available. Recompute the opacity argument with level populations and units; quantify radius-density degeneracy. Fix the wind-band test to test membership in the stated interval, not the union of incompatible model assumptions. Determine whether fitted U describes an illuminated boundary or an attenuated interior field; opacity alone does not establish that every geometric radius inference is invalid. Record this distinction in radius_identifiability.md.

**Success.** An independent radius-density constraint with its covariance, or a clear proof/quantification that existing information only measures thickness or another radius.

**Rejection or inconclusive.** If no absolute layer location is measured, the population-wide transition coincidence remains untested. Do not infer its radius by imposing the transition to be tested.

**Read these inputs:**

- `real_research/reviews/bhstar_p1_empirical_rigor.py`
- `real_research/reviews/bhstar_s1_u_route_void.py`
- `real_research/reviews/bhstar_r1_wind_kinematics.py`
- `real_research/papers/CFJC_RFC0001_bhstar_regime_coincidence.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/H1`

**Deliverables:** `bhstar_input_lineage.csv`, `radius_opacity_audit.py`, `radius_identifiability.md`.

## H2 — Turn the quartic relation into a noncircular population test

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** H1

**Target.** Test whether r_B^4 n_H c^2 mu_gas m_p/(4 G M^2)=1 is an independently predicted population relation or an algebraic restatement of an imposed transition.

**First discriminator.** Read the exact Lean hypotheses: identify the assumed equality g=a0(rho). Then perturb the independent measured inputs rather than imposing R proportional to sqrt(M).

**Method and week-one boundary.** Define a dimensionless residual and full shared-error covariance. Separate Newtonian gravity GM/R^2 from dynamical/effective gravity in the atmosphere. Estimate mass exponent, intercept and scatter without deriving a radius from the same equality. Test a nonconstant-density alternative and selection effects in mocks.

**Success.** A falsifiable per-object/population protocol with independently constrained inputs and recovery of slope/intercept; a real-data result only if H1 supplies the requisite measurements.

**Rejection or inconclusive.** Mass cancellation under an assumed radius-mass law is not evidence the intercept equals one. A local gas-density substitution for a cosmological scale requires its own physical bridge.

**Read these inputs:**

- `real_research/reviews/bhstar_t1_kepler_predictions.py`
- `real_research/reviews/bhstar_p1_empirical_rigor.py`
- `fable_independent_2026/lean_2026/I11_bhstar_kepler.lean`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/H2`

**Deliverables:** `quartic_test_protocol.json`, `quartic_mocks.py`, `population_test_status.md`.

## H3 — Derive a local-density transition from the field equations

**Priority:** P2 · **Allocation:** 1 agent-days · **Depends on:** B1, H1

**Target.** Is there a covariant, dimensionally consistent mechanism linking the cosmic normalization to a local gas-density scale in a radiation-supported envelope?

**First discriminator.** Write exactly which action quantity is replaced by rho_gas in a0=(c/2)sqrt(G rho). Test whether this replacement follows from a field equation or is a new constitutive postulate.

**Method and week-one boundary.** Derive the local equilibrium/perturbation limit including radiation and pressure gradients. Seek a regime/boundary criterion separating cosmic and gas-density behavior, and test one counter-regime such as another ordinary gas-supported environment. Keep any new operator as a new model with its own local gates.

**Success.** A derived local criterion with conserved equations and an independent observable, or a restricted obstruction showing the density substitution is unsupported for the current action.

**Rejection or inconclusive.** Dimensional agreement and a number near unity do not supply this bridge. If the operator is absent, publish the missing physical input rather than another rearrangement.

**Read these inputs:**

- `real_research/reviews/bhstar_k1_regime_coincidence.py`
- `real_research/reviews/bhstar_l2_pressure_census.py`
- `real_research/reviews/bhstar_t1_kepler_predictions.py`
- `real_research/reviews/kappa_unit_response_2026_09_20/README.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/H3`

**Deliverables:** `local_density_bridge.md`, `local_regime_check.py`, `regime_counterexample.json`.

## H4 — Compute radial stability instead of fitting a mass ceiling

**Priority:** P1 · **Allocation:** 1.5 agent-days · **Depends on:** none

**Target.** Determine which maximum-mass/stability statement follows from a self-consistent envelope profile rather than a calibrated global beta threshold.

**First discriminator.** Reproduce the n=3 polytropic control and distinguish its thermodynamic mass relation from a radial-stability criterion. Trace any normalization inherited from the desired ceiling.

**Method and week-one boundary.** Construct one controlled hydrostatic profile with a stated equation of state and boundary conditions; solve the radial eigenvalue/variational problem with the appropriate relativistic corrections and radiation pressure. Recover a known benchmark from its primary equations before the modified case. Week one may end at a validated benchmark plus the exact missing profile. A negative Rayleigh quotient supplies an instability witness; a positive value for one trial function does not certify stability. Stability requires the lowest eigenvalue or a justified lower bound. Use the compactness radius of the same mass-bearing equilibrium, distinguishing it from a wind/photospheric radius.

**Success.** A converged sign of the fundamental squared frequency along a bounded sequence, or a precise instability/underdetermination result. Report any inferred ceiling with sensitivity to entropy, rotation and profile assumptions.

**Rejection or inconclusive.** A homogeneous Gamma_1 or surface compactness estimate does not establish stability of an extended stratified object. No tuned literature ceiling can serve as its own independent validation.

**Read these inputs:**

- `real_research/reviews/bhstar_q1_quartic_first_principles.py`
- `real_research/reviews/bhstar_n1_ceiling_bracket.py`
- `real_research/reviews/bhstar_g2_sms_ceiling_audit.py`
- `real_research/reviews/bhstar_m1_quartic_beta.py`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/H4`

**Deliverables:** `stability_contract.md`, `radial_mode_solver.py`, `mode_convergence.json`.

## Q1 — Reconcile incoming work and pin the actual inputs

**Priority:** P0 · **Allocation:** 0.5 agent-days · **Depends on:** none

**Target.** Give each worker a nonduplicated obligation and a verifiable base even while other agents commit new results.

**First discriminator.** Diff relevant paths against the pinned base and check whether each task missing step has already been completed with raw evidence, rather than merely announced.

**Method and week-one boundary.** Record source hashes, model IDs, superseding proofs and uncommitted inputs. Assign one owner per packet. Reuse completed work only after checking the exact hypotheses and current code; downgrade stale evidence when a dependency changes.

**Success.** A reviewed assignment board and input manifest with explicit inherited, superseded and still-open obligations.

**Rejection or inconclusive.** Commit date, headline or number of PASS checks is not proof of completion. Uncommitted files may be inspected but cannot silently become the shared published baseline.

**Read these inputs:**

- `fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md`
- `deepseek_push/PD19_referee_report.md`
- `real_research/reviews/particle_free_validation_2026_09_20/claim_register.json`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/Q1`

**Deliverables:** `assignment_board.json`, `delta_audit.md`, `input_manifest.json`.

## Q2 — Audit the load-bearing Lean and computational bridges

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** Identify exactly what each selected certificate proves, what is assumed and where a symbolic/physical bridge remains outside Lean.

**First discriminator.** Compile the load-bearing theorem files afresh and print their axioms; inspect full statement dependencies for hidden asserted conclusions, trivial implications and sorryAx.

**Method and week-one boundary.** Record toolchain/import versions, source hashes, commands and exit status. Audit chosen numerical checks for hard-coded booleans and shared implementation errors; require a perturbation or counterexample control that can fail. Formalize missing algebra only when it removes a real dependency.

**Success.** A premise-to-conclusion inventory and reproducible certificate package for the small set of load-bearing claims, with the exact unformalized bridges named.

**Rejection or inconclusive.** Lean certification of an assumed equality does not test that equality in nature. Passing the compiler without the intended theorem or with new unproved axioms does not pass.

**Read these inputs:**

- `real_research/reviews/kappa_unit_response_2026_09_20/UnitResponse.lean`
- `real_research/reviews/orbital_shape_law_2026_09_20/OrbitalShape.lean`
- `real_research/reviews/field_orbit_reciprocity_2026_09_20/Reciprocity.lean`
- `deepseek_push/PD19_referee_report.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/Q2`

**Deliverables:** `certificate_inventory.json`, `lean_logs/`, `bridge_audit.md`.

## Q3 — Check novelty and construct fair discriminators

**Priority:** P1 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** For the strongest surviving result in each lane, separate a new theorem/method/prediction from a known result, a reformulation and a new formalization.

**First discriminator.** Compare exact hypotheses with the known deep-MOND two-body virial relation and AQUAL/QUMOND external-field solutions. A search returning nothing is not evidence of global novelty.

**Method and week-one boundary.** Read primary papers and record version, equation, notation translation and bounded search scope. Include other particle-free actions as comparators; use standard cosmology as a benchmark only, not as a required ontology. Check whether each claimed alternative prediction is really universal or parameter/profile dependent.

**Success.** A source-supported contribution matrix and at least one fair discriminating observable for a surviving model; derivative formalization is labelled accurately.

**Rejection or inconclusive.** No priority claims from a DOI timestamp alone, invented sigma significance, or blanket statements such as every competing halo must have one slope.

**Read these inputs:**

- `real_research/reviews/field_orbit_reciprocity_2026_09_20/README.md`
- `real_research/reviews/orbital_shape_law_2026_09_20/README.md`
- `fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/Q3`

**Deliverables:** `literature_matrix.md`, `sources.json`, `discriminator_table.md`.

## Q4 — Integrate a week-one result that could be released

**Priority:** P0 · **Allocation:** 1 agent-days · **Depends on:** none

**Target.** Produce a coherent week-one account with one strongest result and an exact remaining-gap list, rather than aggregate incompatible passing lanes.

**First discriminator.** Select only outputs with reviewed input ancestry and model identity; inspect contrary results and failed routes before drafting the main claim.

**Method and week-one boundary.** Reserve day seven for independent critical-step reconstruction and clean reruns. Assemble a theorem/obstruction or reproducible instrument paper outline, artifact manifest and next-week decision. This packet can integrate negative/inconclusive outcomes and does not depend on every task succeeding.

**Success.** A reviewable manuscript outline with an exact scoped abstract, raw evidence and limitations, plus an updated next-action queue. Direct-main repository integration is authorized; external publication is a separate action.

**Rejection or inconclusive.** Do not call the theory established or unique from internal consistency, finite scans or Lean counts. No Zenodo upload, submission or email is part of this work order.

**Read these inputs:**

- `real_research/reviews/particle_free_validation_2026_09_20/README.md`

**Owned output directory:** `real_research/swarm_week_2026_09_20/work/Q4`

**Deliverables:** `WEEK_ONE_REPORT.md`, `paper_outline.md`, `release_manifest.json`, `NEXT_QUEUE.json`.
