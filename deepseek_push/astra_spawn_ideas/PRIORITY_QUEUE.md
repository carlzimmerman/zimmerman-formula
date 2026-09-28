# PRIORITY_QUEUE — next-wave work order (2026-09-28)

Purpose: with limited compute, dispatch ONLY the seeds that build the final theory
with first-principles derivations. Supersedes pure sequential refill (AS088+).

Status legend: QUEUED = next in line; DONE = hash-verified completed; SKIP = ruled out / superseded.

## Tier 0 — THE ACTION SPINE (first-principles derivations of the theory's own equations)

These seeds derive actual equations of the framework (stress, Ward identities,
constraints, lapse/gate terms, EFE, PPN, GW, four-form vacuum). Everything else
in the catalog either feeds these or consumes them.

| ID | Seed | Why it matters | Status |
|----|------|----------------|--------|
| AS651 | four_form_metric_variation_fixes_the_legendre_vacuum_energy | closes the k01 sequel: the E*/B-obligation candidate for the vacuum datum (AS075 B-i..B-iv); κ premise hunt | QUEUED |
| AS652 | four_form_flux_equation_with_a_mond_dependent_scale | four-form flux at the MOND scale — the mechanism that could fix λ=1 | QUEUED |
| AS653 | general_flux_power_fixes_acceleration_homogeneity | flux-power homogeneity: the deep-slope premise in action form | QUEUED |
| AS658 | gauge_invariance_and_local_degree_count_of_a_three_form | DOF count of the vacuum sector (wave-sector gate) | QUEUED |
| AS669 | topological_flux_integral_and_metric_volume_dependence | vacuum stress volume dependence — requirement-13 adjacent | QUEUED |
| AS137 | derive_the_ordinary_matter_ward_identity | baryon conservation in the full action | QUEUED |
| AS138 | derive_the_total_diffeomorphism_identity_with_heat_fields | diffeo Ward identity incl. heat fields | QUEUED |
| AS142 | derive_the_carrier_legendre_transform_without_freezing_t_c | exact carrier Legendre transform | QUEUED |
| AS147 | derive_the_diagonal_u_1_noether_current | the U(1) current (conserved charge) | QUEUED |
| AS151 | extract_all_primary_constraints_of_the_localized_action | the constraint algebra — Dirac-Bergmann of the real action | QUEUED |
| AS156 | derive_the_spatial_diffeomorphism_generator_for_heat_fields | spatial diffeo generator | QUEUED |
| AS127 | derive_reciprocal_lapse_density_directly | the lapse-density reciprocity, derived not assumed | QUEUED |
| AS131 | derive_the_heat_field_metric_stress | heat-field stress tensor from the action | QUEUED |
| AS132 | derive_the_fixed_compensator_stress | compensator stress | QUEUED |
| AS133 | derive_the_terminal_heat_boundary_condition | boundary condition derivation | QUEUED |
| AS145 | derive_the_gate_contribution_to_the_lapse_equation | gate term in the lapse equation | QUEUED |
| AS215 | construct_a_criterion_b_characteristic_ordering_test | criterion B as a characteristic-ordering test | QUEUED |
| AS204 | bound_a_curved_leaf_heat_force_derivative | curved-leaf force control (EFE prerequisite) | QUEUED |
| AS206 | derive_the_metric_variation_of_the_intrinsic_laplacian | metric variation of Δ — curved-leaf machinery | QUEUED |
| AS208 | bound_the_first_metric_derivative_of_the_heat_operator | heat-operator metric derivative bound | QUEUED |

## Tier 0b — OBSERVABLE DERIVATIONS (testable predictions from the action)

| ID | Seed | Why | Status |
|----|------|-----|--------|
| AS226 | derive_measured_newton_g_in_the_reciprocal_high_k_limit | G_N from the theory, not adopted | QUEUED |
| AS228 | derive_independent_galactic_spatial_and_lapse_potentials | potential split — the metric's two channels | QUEUED |
| AS229 | compute_projected_vacuum_contribution_to_lensing_slip | lensing slip from vacuum — observable | QUEUED |
| AS232 | derive_beta_from_a_second_order_static_weak_field_equation | PPN β | QUEUED |
| AS233 | derive_the_high_acceleration_preferred_frame_vector_response | preferred-frame response (α-related) | QUEUED |
| AS234 | derive_alpha2_from_a_longitudinal_moving_source_response | PPN α₂ | QUEUED |
| AS236 | derive_cosmological_versus_local_g_for_the_centered_clock | G_cosmo vs G_local          | QUEUED |
| AS238 | derive_the_tensor_dispersion_on_homogeneous_occupied_flrw | GW dispersion on FLRW | QUEUED |
| AS239 | test_tensor_propagation_through_an_inhomogeneous_carrier_region | GW propagation | QUEUED |
| AS240 | compute_gravitational_wave_amplitude_transport | GW amplitude transport | QUEUED |
| AS245 | compute_the_external_field_correction_from_the_filtered_action | EFE **from the filtered action** — the EFE bridge (AS043.C01) | QUEUED |
| AS247 | construct_a_same_action_shapiro_delay_integral | Shapiro delay from the same action | QUEUED |
| AS252 | match_the_cosmological_einstein_coefficient_to_measured_newton_gravity | the cosmological G coefficient | QUEUED |
| AS263 | derive_the_time_dependent_projector_commutator | | QUEUED |
| AS285 | construct_an_action_consistent_growth_equation_in_a_restricted_quasistatic_band | growth equation from the action | QUEUED |

## Tier 1 — GATE AUDIT + FIRST-PRINCIPLES STATUS (cheap, decisive)

| ID | Seed | Why | Status |
|----|------|-----|--------|
| AS500 | logical_independence_and_redundancy_of_the_thirteen_closure_gates | the gate lattice itself — what must actually close | QUEUED |
| AS1923 | compact_three_form_topology_and_coefficient_selection | three-form topology picks the coefficient | QUEUED |
| AS1928 | vacuum_energy_equation_of_state_required_by_the_scale_relation | EoS implied by a0-ρ_Λ | QUEUED |
| AS1959 | clock_sector_energy_contribution_to_vacuum_normalization | clock energy → vacuum normalization | QUEUED |
| AS1986 | first_principles_elimination_of_an_environmental_fitting_function | kill the environmental fudge | QUEUED |
| AS1987 | first_principles_elimination_of_a_source_conversion_fitting_function | kill the source-conversion fudge | QUEUED |
| AS1988 | first_principles_elimination_of_a_filter_profile_choice | derive the filter profile | QUEUED |
| AS1989 | first_principles_status_of_the_mono_tail_parameter | MONO tail: derived or adopted? | QUEUED |
| AS1990 | first_principles_status_of_the_splice_construction | splice: derived or adopted? | QUEUED |
| AS1991 | first_principles_status_of_the_vacuum_energy_value | vacuum magnitude: derived or adopted? | QUEUED |
| AS1997 | closure_witness_with_explicit_empirical_falsifier | the falsifier-bearing closure witness | QUEUED |
| AS1999 | minimal_repair_preserving_already_derived_first_principles_results | minimal repair protocol | QUEUED |
| AS2000 | complete_same_action_first_principles_closure_witness | the final milestone | QUEUED |

## Tier 2 — hold (dependencies not ready / superseded)

- AS088–AS124 statistical/entropy chain: partially superseded by AS076/077 verdicts (σ² = C/2
  survives only at r_in→0, R = r_M). Keep AS100 (equilibrium closure dependency theorem) and
  AS104 (uniqueness by relative entropy) as fillers only.
- AS376–AS499 observables/methodology: consumers of Tier-0 derivations; run after.
- AS1719+ spectral moment stack: high technical debt, low theory value.
- Child lanes named in earlier results (AS043.C01 EFE curved-leaf, AS069.C01 dynamical λ,
  AS071.C01 joint law, AS073.C01 non-autonomous objective) map onto AS245/AS233/AS127+AS300s.

## Dispatch rule
Refill order = Tier 0 → Tier 0b → Tier 1 → filler only if all three exhausted.
Every dispatch still carries: manifest-exact filename + pinned task_sha256 + the standing
framework contract + Lean hard bar + honest bounds.
