# PRIOR_WORK_INDEX — what this project has already tried

Built 2026-08-17 for the 500-idea overnight run. **Purpose: criterion C6.** Before an idea
is written, run it against this file. If it matches a line here, it is a re-tread — either
drop it or make the `DO:` start from the cited prior work and go somewhere new.

**Verdict key**
- `[RETRACTED]` — a claim this project once made and then **withdrew**. An idea that
  re-derives one of these and reports PASS is the worst possible outcome of the whole run.
  Treat every RETRACTED line as a poisoned target: if a computation lands on it, the
  correct verdict is REFUTED-or-explain-why-the-retraction-was-wrong, never a hit.
- `[SETTLED]` — computed, verified, and closed on this framework's own terms. Re-running it
  wastes a session; contradicting it needs a named defect in the cited script.
- `[OPEN]` — genuinely live. These are the good neighbourhoods. An idea may build here.
- `[TOOL]` — infrastructure/record, not a physics verdict.

Sources: `RETRACTIONS.md` (446 ln), `STANDING.md` (1063 ln),
`qwen_38_experiment/{LEDGER.md, NEGATIVE_RESULTS.md, FINDINGS_HARVEST_2026-08-16.md}`,
`nbody_2026/stage*.py` (87 files), `real_research/reviews/*.py` (759 files),
`prep_2026/**` (227 files).

---

## 0. The failure-mode taxonomy — check EVERY idea against this first

This is the most reusable thing in the corpus. Every retraction below reduces to one of
these ten. An idea whose `DO:` cannot survive the matching test should not be written.

- Solving for the target and calling the output a result (κ=½ solved for ε_tot; solved for K_B; 3 instances). Test: is the new quantity's value fixed by the answer you wanted? [SETTLED] (source: RETRACTIONS.md)
- Freezing a nuisance parameter (Υ in the RAR comparison; amplitude in the footing comparison). Test: refit both sides independently. [SETTLED] (source: RETRACTIONS.md)
- Evaluating at a convenient background point (u=0 where a₀(z) requires u₀≠0). [SETTLED] (source: RETRACTIONS.md)
- Passing a FAVOURABLE claim through unverified while re-deriving adverse ones. The asymmetry is itself the defect. [SETTLED] (source: RETRACTIONS.md)
- Quoting a boundary value as an optimum (3 consecutive instances). Test: assert the argmin is interior. [SETTLED] (source: RETRACTIONS.md)
- Under-converged iteration (25 Picard steps on a fold). Test: vary iteration count, confirm a plateau. [SETTLED] (source: RETRACTIONS.md)
- Pricing a magnitude at the wrong place (collapse boost at virial radius when the rate-limiting step is turnaround). [SETTLED] (source: RETRACTIONS.md)
- Using a fixed a₀ where a₀(z) matters — would have manufactured a CMB problem 24,909× too large. [SETTLED] (source: RETRACTIONS.md)
- Using a degenerate estimator — RAR-scatter minimisation cannot measure a₀. [SETTLED] (source: RETRACTIONS.md)
- Quoting one footing when the two differ. Both footings on every dimensionful result. [SETTLED] (source: RETRACTIONS.md)
- Four extra kill-modes from the qwen autoloop harvest: tolerance-width null-by-construction (the band is so wide some integer must land); definition-shopping (choosing among scheme variants until one matches); no discriminating power (the "hit" and the "miss" are both inside the measurement error); premise-existence failure (the feature being tested does not exist on the real curve). [SETTLED] (source: FINDINGS_HARVEST_2026-08-16.md)

---

## 1. Screening, environment, and local-density a₀

- a₀ ∝ √(Gρ_local) as the normalisation — excluded on the framework's own SPARC environmental test at 10.5σ (STANDING) / 13–34σ on 175 SPARC (memory index). Plus a structural trap: cluster cores are LESS dense than galaxy inners, so no density-monotone floor boosts clusters without boosting galaxies more. [SETTLED] (source: STANDING.md §4; sparc_environmental_a0_test.py, sparc_environment_a0_REAL.py, cluster_a0_from_density_HIS_FORMULA.py)
- Per-galaxy a₀ tracking an independent ambient-density proxy or the large-scale cosmic web — direct test on real SPARC, null. [SETTLED] (source: project_sparc_a0_vs_density_direct.py, project_sparc_a0_vs_cosmicweb.py, prep_2026/cosmicweb_a0/environment_power_confound.py)
- ρ_local-vs-ρ_Λ fork as a BIG-SPARC discriminator — pipeline ready, BIG-SPARC not public; already a decisive null on 175 SPARC. [SETTLED on current data] (source: STANDING.md; memory index project_bigsparc_environmental_fork)
- a₀ is nevertheless LOCAL in the field theory: 𝒜 suppressed ~2–4% inside halos, 13× at 1e6 ρ_dm0 — this is a DIFFERENT statement from "a₀ ∝ √ρ_local" and is the live one. [OPEN] (source: nbody_2026/stage59_local_a0_verdict_2026.py)
- The EFE as a screening mechanism for the sunward anomaly — **there is no relief**. Done as vectors, ⟨g_ext·r̂⟩=0 over an orbit; relief factor 1.0000003×. The earlier "EFE suppresses it to 119–189×" is [RETRACTED] (it scalar-added g_ext, i.e. pointed the Galactic field permanently at the Sun, and reported the orbit phase minimum). (source: RETRACTIONS.md; mi_efe_escape_and_ch23_withdrawn_2026.py, 8/8)
- Collective / clumpy EFE as a booster — redistributes only, −0.95%, wrong sign (deep-MOND sub-additivity + enclosed-mass theorem). [SETTLED] (source: STANDING.md §4)
- The AeST aether's rising θ=3H footing surviving inside a galaxy (is the rolling cosmological scalar screened?) — answered NO. [SETTLED] (source: project03d_aether_stiffness.py, aest_locality_theta_profile.py, theta_3H_coupling.py)
- The curl-sector as a screening/cluster mechanism — DEAD on geometry, not on magnitude: an exact pointwise cancellation leaves the saturated tilt a pure gradient with zero curl for any anisotropy; shortfall 8.0× at an absolute floor, ~176× central. Surviving rider (not a mechanism): η−1 ∝ ε² at 0.1–10%, no free amplitude. [SETTLED] (source: RETRACTIONS.md; curl_sector_cluster_pricing_2026.py, 27/27)
- "The curl-sector spherical-symmetry argument defends the PPN preferred-frame parameters" — **does NOT cover α₁** (the α₁ configuration is axisymmetric, so the curl sector is excited by construction). [RETRACTED] (source: RETRACTIONS.md; aest_radial_aether_eom.py FACT 1)

---

## 2. Kernels, interpolation, and legality (the R1 obstruction)

- The a₀-line g_obs² = g_bar² + a₀·g_bar as an EXACT law — it is the α=1 identity and nothing more. "Exact" is withdrawn. Fitted to data generated at known a₀ it is unbiased on α=1 data but biased +10.3% on Route-A data and −83.6% on α=2 data. [RETRACTED as exact] (source: STANDING.md §0/§1)
- ν = √(1+1/y) as a derived kernel via de Sitter–Unruh / Deser–Levin — the derivation WORKS and yields exactly this, then forces a₀ = 2cH_Λ, excluded at 15.6σ. Never cite dS-Unruh as support for κ=½. [RETRACTED] (source: RETRACTIONS.md; deser_levin_mond_derivation.py, mi_deser_levin_interpolation_2026.py)
- The operative kernel is ν(y) = 1/(1−e^(−√y)), i.e. **Milgrom & Sanders 2008 ApJ 678,131 Eq.(13) at α=½**, adopted empirically by MLS 2016. Crediting the form to MLS 2016 is [RETRACTED]. Single importable definition. [SETTLED] (source: RETRACTIONS.md; real_research/reviews/mi_route_a_kernel.py, 6/6)
- The Bose–Einstein kernel mechanism (ν = 1 + n_BE(√y)) as a derivation — the identity is a trivial rearrangement holding for ANY argument; function and thermal reading are both prior art; the natural bath normalisation gives κ = 0.0733, **11.1σ LOW** (the mirror of Deser–Levin); and a fixed-T bath cannot host a₀(z). [RETRACTED] (source: RETRACTIONS.md; nbody_2026/stage52_*)
- Route A's exponential kernel adopted 2026-08-02: suppresses the Sun's anomaly by 3.3e13, fractional departure 2.7e-22 at the Sun; carried into a Bekenstein–Milgrom field theory that is strictly convex, ghost-free, elliptic, subluminal, with an exact BTFR of coefficient 1. [SETTLED] (source: mi_route_a_exponential_kernel_2026.py 9/9, mi_route_a_field_theory_2026.py 11/11)
- α=2 (K=√(z/(1+z))) as the fix for the solar system — its 1/g residual tail binds at the SUN (Jupiter reflex ≈2233 a₀), leaving 8.5×/12.4× the Mars budget after a full LM ephemeris fit. Not a pass. [SETTLED] (source: STANDING.md; mi_alpha2_sun_reflex_2026.py 7/7)
- "α=2 clears the solar system to 2e-5×, i.e. passing" — evaluated the tail at the PLANETS, not the binding body. [RETRACTED] (source: STANDING.md §5.0)
- Deriving the law from an action, all four families (nonlocal operator-K; local F of the scalar first moment; local+degenerate; nonlocal velocity-bilinear à la Milgrom 1994) — all closed. General obstruction: a fixed potential-independent kernel is diagonal in FREQUENCY, the law is diagonal in ACCELERATION, and A=Ω²R ties the labels. [SETTLED] (source: STANDING.md §4; mi_family4_variational_nogo_2026.py, mi_law_is_nonvariational_2026.py)
- Theorem 3 (no local L(x,ẋ,ẍ) gives the law) — proof CORRECTED and the statement got WIDER: excludes all local L, degenerate or not. [SETTLED] (source: mi_theorem3_corrected_proof_2026.py)
- Theorem 8 (the nonlocal operator action does not supply the amplitude) — mechanism replaced and now KERNEL-INDEPENDENT: on a circular orbit the action's argument is w=cΩ/a₀ while the law's is x=a/a₀, ratio c/v = 300 to 7e5. [SETTLED] (source: mi_theorem8_redone_alpha2_2026.py)
- The off-circular action S = ∫dt m(|ẋ|²f(|ẍ|/a₀) − φ) — written down, circular orbits solve the full 4th-order EL exactly for generic f; but the acceleration Hessian is INDEFINITE (Ostrogradsky runaways, e-folding 0.57 s at Earth) and off circles it gives a different μ (251× weaker at u=0.1). [SETTLED] (source: mi_offcircular_action_2026.py, 44 checks)
- The "four-family no-go" as originally stated — OVER-REACHED; the law does arise variationally in a nonlocal NON-quadratic class (Milgrom's own virial f), on the two-parameter family of circles only. [RETRACTED as stated] (source: STANDING.md §2)
- Legality / single-valuedness of F(Y,Q): U(y) must be strictly increasing; the family J_Y = v/(1−v/s) saturates at U→s; s=½ is NOT the a₀-line (U(2): 0.369 vs 0.449). This is N6 and the origin of the 233× obstruction. Derived treating a₀ as a CONSTANT. [OPEN — this is seeded angle S4] (source: BACKFILL_SPEC.md N6/S4; typeII_legality_independent_2026.py, aqual_efe_a0line_kernel_2026.py)
- The AeST "type-II" question for the quasi-static sector, checked against known limits. [SETTLED as a check, not a verdict] (source: typeII_known_limits_2026.py, typeII_direct_variation_2026.py)
- p=4 member μ₄(x) = x/(1+x⁴)^(1/4) and the general admissibility audit against every published condition. [SETTLED] (source: mi_routeA_admissibility_audit_2026.py 31/31, mi_p4_kernel_pricing_2026.py)
- The extremal-kernel principle settled by linear programming; the unimodality axiom; the Herglotz-admissibility question (declared MALFORMED in its own header). [SETTLED] (source: mi_extremal_kernel_lp_2026.py, mi_unimodality_axiom_2026.py, mi_gate_herglotz_admissibility_2026.py)
- The kernel's spectral measure: sum rule ∫ρ/s ds = K(∞)−K(0) is an IDENTITY, not a property of any particular measure; K(0)=0 and K(∞)=1 are the load-bearing premises. α=2's measure has compact support (0,1), total mass ½, all moments finite; α=1's mass DIVERGES. [SETTLED] (source: mi_loop_edge_alpha2_measure_2026.py 15 checks, mi_laneA_moment_window_alpha2_2026.py 10 checks)
- Boundedness |K|≤1 for z<−1: α=2 violates it on the whole upper half of its own support, but the Euclidean loop never goes there and F(κ)=μ(κ) exactly, so "F bounded in [0,1)" IS μ≤1, a defining property of any interpolating function. [SETTLED] (source: mi_boundedness_thread_closed_2026.py, 17 checks)
- Two-loop a₀ renormalisation: additive channel closed to ALL ORDERS by the exact shift symmetry (Ward identity); multiplicative closed at two loops; graviton sector p-free to all n. Four of six legs never touch the kernel. [SETTLED] (source: mi_twoloop_alpha2_transfer_2026.py, 14 checks)
- Milgrom-2022's frequency-RATIO construction as a rescue for the α=1 planetary anomaly — closed three independent ways (θ enters additively; the kernel is exactly unimodular on the oscillatory branch; Theorem B forces quadrature). [SETTLED] (source: STANDING.md §4; mi_milgrom2022_theta_efe_2026.py)

---

## 3. The dust sector / open problem 2d (R2)

- ρ = Q₀·n with ρ/n = Q₀ independent of any added Y-dependent Q-mass ⇒ the dust mass IS the conserved shift charge and cannot be suppressed locally. Breaking the symmetry frees the charge but NOT the energy (∇_μT^μν=0; transport 690 Gyr). [SETTLED] (source: nbody_2026/stage4, stage5, stage6_break_shift_symmetry, stage6_audit_transport_channels)
- Dynamics sees ρ+3p, lensing sees ρ+p ⇒ no equation of state hides energy from both (M_lens/M_dyn = 29 at the f=1/3 fixed point). [SETTLED] (source: nbody_2026/stage7_the_claim_2026.py)
- c_s² ∝ a⁻³ for every ghost-free K ⇒ the dust cannot be kept warm (the warm route needs c_s²(rec) = 595 c²). [SETTLED] (source: nbody_2026/stage9_construct_the_function_2026.py)
- Endpoint of the collapse is a black hole, falsified 5.8e5× vs Sgr A*. Wave scale 0.18 AU. [SETTLED] (source: nbody_2026/stage1, stage2, stage3)
- The gated Proca (dust-collapse repair) — killed within two hours, three ways: K_eff = 2πG·R_halt² IDENTICALLY (the "188-kpc mass-independent core" was π× the assumed halt radius, a tautology); y ∝ 1/a₀²(z) so the gate OPENS toward recombination (3.25e6× the CLASS cap); KiDS lensing rejects the core at Δχ² ≳ +1.2e3. [RETRACTED] (source: RETRACTIONS.md; stage51 bannered → stage52)
- "Sgr A* falsification REMOVED (0.45%)" and "mass-independent 60–190 kpc core" — both restated the assumed halt radius. [RETRACTED] (source: RETRACTIONS.md)
- Route A′ — the cored two-field halo (χ with p = Kρ^γ) — the surviving γ range is EMPTY: Jeans growth needs γ<4/3, polytrope stability needs γ>4/3, and the transported forest cap gives M_J(today) ≤ 1.4e8 M☉ against 2.51e12 required (≥35× short even as γ→0). Binding-epoch wall z_bind = 10.19. Do NOT cite stage51/52's "the one live alternative". [RETRACTED] (source: RETRACTIONS.md; stage53_route_a_prime_closure_2026.py)
- The two-field window: committed stage12 had ALREADY excluded Route A′ (KiDS Δχ² up to +1698 at A′'s own normalisation) while later stages carried it as live — a T3-class corpus error. [SETTLED] (source: stage10_two_field_construction, stage11_30_200kpc_confrontation, stage12_lensing_stack_fit)
- The second-field escape, four catalogued candidates (k-essence, ungated Proca, promotion-only, fixed-Λ) — ALL DEAD, including one built specifically to clear the three known legs, which died on a SIGN (a gate built from |∇φ| rises outward wherever held dust dominates its own field, anti-supporting 99.27% of the held mass; equilibrium truncates at 653 kpc with 55–61% of the lensing mass piled there). Two reusable theorems: at Γ=4/3 the violation is calibration-INDEPENDENT at 1.16e3× the cap; r_×/R_supp = [M_bar/((π²/3)M_dust)]^(1/3) = 0.194 is fixed by the baryon-to-dust ratio alone — **test that first, it is free.** [SETTLED] (source: second_field_catalog_2026.py, 47/47)
- The NON-charge-built pressure sources enumerated (second condensate with its own charge, gauge field, fermion degeneracy, vorticity/turbulent stress, non-local/gradient energy, finite-T radiation) with a killing filter named per row. [SETTLED as a catalogue] (source: qwen LEDGER D002; dust_filters.py / D001 calibration)
- Cell 3 (the transport channel) — stage54 graded it VIABLE-CANDIDATE, stage63/64 DEMOTED it to CONDITIONAL-DEAD against the Q₀ pin. Do NOT cite the VIABLE-CANDIDATE grade as current. [RETRACTED as live] (source: stage54_y_gate_and_cell3_verdicts, stage63_cell3_transport_1p1d_2026.py)
- Charge-abundance amplitude as the cluster/dust lever — the available coefficient reduces to ρ_charge/ρ_Λ, in which ν₀, Λ_D, Q₀, M and κ all cancel; 10²–10³ too small even if the dark sector's charge were the ENTIRE dark matter content. A genuine no-go. [SETTLED] (source: RETRACTIONS.md; stage42)
- Irrotationality of the dust: a ghost-condensate/P(X) frame is hypersurface-orthogonal so ω_μν = 0 on all 16 components for generic φ(t,x,y,z). **Note for the 500-run: irrotationality is NOT a theorem once the dust rides A^μ (the twist propagates) — but the allowed band is empty by 2.77×.** [SETTLED with the named caveat] (source: mi_darksector_frame_closes_2026.py 18 checks; roadblock R2)
- The IC / shift-charge route ("clusters carry more khronon because they formed where the charge was already dense") — KILLED by the 1-Mpc confrontation, 9/9: smooth accretion ⇒ ξ(halo)→1 for any cold T(k). Do not cite it as resolving clusters or the 2500× objection. [RETRACTED] (source: mi_ic_route_1mpc_confrontation_2026.py, mi_shift_charge_ic_route_2026.py, mi_lyalpha_ic_route_confrontation_2026.py)
- "No dark matter in galaxies" as a RESULT — Ω_dm remains. The only defensible slogan is "no dark-matter PARTICLE". [RETRACTED] (source: RETRACTIONS.md, STANDING.md §5.5)
- Shift-charge suppression in the Galaxy as a theory-side door. [SETTLED — killed by the self-consistent solve] (source: stage4_charge_suppression_2026.py, stage5_selfconsistent_solve_2026.py)
- Whether the Q-sector dust virialises into halos; nonlinear spherical collapse of the AeST Q-sector. [SETTLED] (source: mi_virialisation_verdict_2026.py, mi_ghost_condensate_spherical_collapse_2026.py, mi_shift_charge_clustering_2026.py)

---

## 4. κ — the coefficient (R3)

- κ is **MEASURED, not derived**: 0.551±0.043 (distance-free), 0.465±0.076 (BTFR), combined 0.529±0.034 published / 0.547±0.034 on the Planck-consistent rescale. κ=½ sits 1.19σ away; at least four candidates lie within 2σ. [SETTLED] (source: RETRACTIONS.md, memory index)
- The κ error bar is H₀-CONVENTION-EXPOSED: κ ∝ h^(2q_eff−p), H₀-invariant only at q_eff = 0.500 or 0.730, and neither estimator sits there; a Planck-consistent rescale moves a₀ by +6.5–7.3% = 4.0× the 1.84% statistical error. Always quote κ with its H₀. NOT a direction claim. [SETTLED] (source: kappa_h0_convention_audit_2026.py, 24/24)
- The whole open content reduces to ONE π-free factor of two: because π cancels between √(8π/3) and Z, "κ=½" is identically "Z = 2√(8π/3)". [SETTLED] (source: nbody_2026/stage43_kappa_reduction_one_factor_2026.py)
- "The π-cancellation in a₀ = κc√(Gρ_Λ) is evidence for κ=½" — logically identical to "κ=½ exactly"; at the measured κ=0.551 the π's do not cancel at all. [RETRACTED] (source: RETRACTIONS.md; stage66 PART C)
- "κ=½ is distinctively simple" — NARROWED: at ±7.8% precision all five natural parameterisations admit a simple rational (q≤10), and 5/9 (0.11σ) and 4/7 (0.48σ) sit CLOSER than ½ (1.19σ). Defensible statement is Bayesian only: under a 1/q² simplicity prior ½ leads by ~6:1. [RETRACTED as stated] (source: stage66_kappa_rational_evidence_2026.py)
- The crossover master formula κ² = 8π ε_tot — CIRCULAR: solving at κ=½ returns ε_tot=1/32π, where the 8π is carried over from its own LHS and the residual 4 is κ⁻². [RETRACTED] (source: RETRACTIONS.md; stage43, mi_crossover_master_formula_2026.py)
- ε_tot = 1/(32π) from first principles — TT-gauge kill; five plausible variants span 161.6×. And it is not special among ≤3-factor products of natural horizon fractions. [SETTLED/NULL] (source: RETRACTIONS.md; qwen LEDGER t002; mi_eps_tot_mode_counting_verdict_2026.py)
- "The graviton-bath cancellation is one assumption away from deriving κ" — all SEVEN form-assumptions are load-bearing; the construction is fragile, not nearly-forced. Treat it as a REWRITING of the fit. [RETRACTED as a framing] (source: RETRACTIONS.md stage65; qwen LEDGER t003; mi_graviton_bath_ctp_2026.py)
- "Pure horizon-geometry ratios are EXCLUDED as a route to κ" — NARROWED to pure horizon-geometry MONOMIAL ratios. Non-monomial combinations, a theory-FIXED radius ratio, and the combinatorial factor-of-2 route are untouched by the theorem. [RETRACTED as stated; the narrow version SETTLED] (source: qwen LEDGER t009; stage65 PART B)
- κ² is NOT a GHY-to-bulk action ratio on the Λ static patch at ≤3 combos. [SETTLED] (source: qwen LEDGER t007; mi_pi_free_area_2026.py, mi_wald_entropy_normalisation_2026.py)
- Every published dS-thermodynamic route forces a coefficient ≠ ½ or forces none — table complete. [SETTLED] (source: qwen LEDGER t001; established_paths_to_mond.py, project_routes_to_sign.py, project_forcing_the_coefficient.py)
- The first-law smearing catalog: five named smearings each fix κ per choice; the KILL condition (choice-independent ½) did NOT fire. [SETTLED] (source: qwen LEDGER t006)
- The q-deformed / Tsallis Deser–Levin mirror: the BE route reaches κ=½ only at a q that nothing forces. [SETTLED] (source: qwen LEDGER t005)
- Two-temperature interpolation families: no n gives the a₀-line AND κ=½. [SETTLED] (source: qwen LEDGER t008)
- κ = (2/3)(D−1)/D as a D-dependence — on the do-not-cite list. [RETRACTED] (source: memory index; mi_kappa_from_dimension_2026.py, mi_kappa_D_dependence_rigidity_2026.py)
- K_B = 3/2 from the aether sector as a route to the factor 2 — assumption INVERTED (G_cosmo/G_local is strictly <1, supremum exactly 1, where the candidate needed 4; SZ21 state "G_N > G̃ always" as a theorem), and its "prediction" was a tautology (κ=½ ⇒ K_B=3/2 identically under its own map). [RETRACTED] (source: RETRACTIONS.md; stage46 → stage48 → stage50)
- Re-measuring κ under the operative kernel by RAR-scatter minimisation — the ESTIMATOR IS DEGENERATE: scatter moves 12% across a factor 1.94 in a₀ because Υ absorbs it. [RETRACTED] (source: RETRACTIONS.md; stage49)
- "The operative kernel moves κ toward ½" — rested on that degenerate estimator. [RETRACTED] (source: RETRACTIONS.md)
- "The anchored a₀ fits the RAR BETTER than fitted a₀" — Υ was frozen; refit both sides and they are indistinguishable. Anchoring COSTS 6% in RAR scatter (0.1081 anchored vs 0.1016 free) and buys a cheaper fit, not a better one. [RETRACTED] (source: RETRACTIONS.md; stage49)
- κ=½ vs Milgrom-2020's 1/2π discrimination on SPARC — shape-dependent and NOT resolved: four transition shapes give 1.192×/1.154×/1.059×/0.938× preferred a₀ with the exponential (operative) kernel favouring 1/2π at 0.66σ. No shape reaches 3σ. The banked "2.2σ favours ½" was a ONE-SHAPE (α=1) result. [RETRACTED as banked] (source: STANDING.md §0; mi_routeA_a0_estimator_invariance_2026.py 7/7)
- The unlock for κ: stellar M/L zero point to a few percent + an absolute gas scale. [OPEN] (source: mi_kappa_error_budget_unlock_2026.py, stage67_kappa_precision_path_2026.py)
- The Z-derivation family — radion stabilisation, eta invariants on R³/Z₂, period-ring/Feynman-period arithmetic, dS4 boundary measure, 40 invariants of T³/Z₂, heat-kernel floor, Nariai forcing, strained-horizon O(ε³), Iyer–Wald presymplectic Θ — ALL negative. [SETTLED] (source: derivation_challenge_attempt.py, eta_local_bruning_seeley.py, period_ring_obstruction_2026.py, dS4_boundary_measure_Z_2026.py, forty_invariants_test.py, project_heatkernel_longshot.py, mi_nariai_forcing_2026.py, strained_horizon_O_eps3.py, strained_horizon_wald_theta.py)
- β = μ²Λ_D²/M⁴ = 1 is SELECTED, not derived; it is an INTERIOR point of the ghost/gradient-stable range so stability does not select it; and it is NOT an integer/half-integer brane-tension quantisation (the equivalence table produced is CONVENTION-grade, not a hit). [SETTLED] (source: qwen LEDGER t011, t012; stage20_beta_equals_one_derivation_2026.py; T011_EQUIV_TABLE.md)
- "β=1 derived flat" — never say derived; it is BOUNDARY-PINNED. [RETRACTED as phrasing] (source: memory index, stages 19–22)

---

## 5. Clusters (R4)

- η(R₅₀₀) on the twelve X-COP clusters: **1.865 canonical / 1.722 alt on the operative MS08 kernel**; 2.084/1.917 on the a₀-line kernel. Quote the spread 1.72–2.08 WITH the kernel named. Quoting 2.084/1.917 unqualified is [RETRACTED]. (source: RETRACTIONS.md)
- "Clusters sit at 21.6 a₀ at R₅₀₀" — that field is the CORE; R₅₀₀ is 0.33–0.58 a₀. [RETRACTED] (source: RETRACTIONS.md, memory index)
- η = 2.334 as universal — eRASS1-sample-specific; X-COP gives 1.66–1.81. [RETRACTED] (source: RETRACTIONS.md)
- Missing baryons as the cluster mechanism — closes 7%. [SETTLED] (source: RETRACTIONS.md)
- ANY single-argument law f(g) — a second variable is required at 37–73σ. [SETTLED] (source: stage30_xcop_two_variable_fit_2026.py)
- Positive Helmholtz mass — THEOREM: ρ_eff ≥ 0 forces the extra enclosed mass to GROW outward; the data have it falling in 12/12. [SETTLED] (source: stage31_helmholtz_fit_xcop, stage32, stage33)
- The q-route (bump acting through the gradient coefficient) — q(0)=1 shifts the galaxy RAR by 0.340 dex against a 0.108 scatter, breaking the BTFR theorem. [SETTLED] (source: stage34_q_route_clusters_2026.py)
- The a₀-bump as a GRADIENT term — fits best of any candidate but is NOT derivable from the action; the action's own bump varied properly generates only the excluded mass slot plus a B′ gradient slot failing three ways. [SETTLED] (source: stage35, stage36)
- The derived mixing kernel T(y) — correct shape class, wrong amplitude and sign. [SETTLED] (source: stage39, stage40)
- The a₀-bump response is x/(1+x)² (x = Y/A): single maximum at x=1, half-maxima at 3±2√2, inflection at x=2. **There is NO sub-peak and no golden-ratio-distinguished point on this curve.** [SETTLED — kills a whole class of "golden sub-peak" ideas] (source: FINDINGS_HARVEST_2026-08-16.md S0006)
- The a₀-bump as the live cluster candidate: c_T=1 exact, no-ghost THEOREM, A_max ∈ [2.72,4.46]× fiducial = [4.49,7.36] Mpc⁻² at base_a=1. The published "(2.7–7.4)×" SPLICED units and is 1.66× too wide. [OPEN — still the only live candidate] (source: mi_a0_bump_response_2026.py, mi_a0_bump_health_2026.py, mi_aest_full_matrix_bump_2026.py)
- base_a is built from AeST's K_B and NEVER measured (fiducials 0.1/0.3/0.5); quasi-static phenomenology is K_B-BLIND in every OBSERVABLE (G̃=(1−K_B/2)Ĝ) but NOT in the sector — 5 of 14 K_B-carrying quantities diverge as K_B→0 (c_s² ~ 1/K_B, m_×² ~ 1/K_B, M² ~ 1/K_B). "K_B-blind" as an unqualified claim is [CORRECTED, not withdrawn]. (source: RETRACTIONS.md; kb_small_limit_safety_2026.py 33/33)
- "The kernel already removes 74–89% of cluster DM" — at R₅₀₀ it accounts for 48% and leaves 52%. [RETRACTED] (source: RETRACTIONS.md)
- "68% of ΛCDM DM in clusters" — on the do-not-cite list. [RETRACTED] (source: memory index)
- "48% of cluster χ² removed" (25 unconverged Picard iterations); "10% systematic: baseline 560→39.1" (true 44.5, AND the wrong direction since non-thermal support biases hydrostatic mass LOW); "robust statistic 3.425→1.871" (core-dominated, 34% of points inside 0.1R₅₀₀ where the ratio is 4.205). [ALL RETRACTED] (source: RETRACTIONS.md; stage44_cluster_caveats_verified_2026.py)
- "Canonical footing fits clusters better" — ALT was evaluated at CANONICAL's amplitude (frozen nuisance). [RETRACTED] (source: RETRACTIONS.md)
- "XRISM licenses a large non-thermal component and thereby softens the cluster problem" — withdrawn outright; every primary XRISM measurement is small (A2029 core 2.6±0.3%, Coma centre 3.1±0.4%, X-COP median 5.9% at R₅₀₀). Correct phrasing: "does not relieve, does not close." [RETRACTED] (source: STANDING.md §5.4; clusters_eta_audit.py)
- The cluster acceleration-scale ladder is a METHOD-AND-RADIUS ladder, not one number: 3×–24× spanning CLASH lensing (2.02e-9 = g‡, double dagger), X-ray at r_c/2r_c/3r_c, member dynamics. "Seventeen times" is a real published phrase but its arithmetic is 2.02/1.20 = ratio to McGaugh's a₀; rescaled to this framework it is 21.6×/17.9×. [SETTLED] (source: STANDING.md §5.4)
- The R²-lever cluster mechanism (μ⁻¹ = 3.13 Mpc) — satisfies NEITHER Mistele bound. [RETRACTED] (source: memory index)
- The cluster SIGN theorem — evaluated at u=0 when a₀(z) requires u₀=ν₀Λ_D ≠ 0; the sign is AVAILABLE, not forbidden. [RETRACTED] (source: RETRACTIONS.md)

---

## 6. Cosmology, CLASS/CMB, growth, and the forest

- Real CLASS CMB run at Δχ² = 1.34 over 4998 multipoles; re-run with the DERIVED a₀(z) law gives 0.01σ vs cosmic variance. [SETTLED] (source: stage19_class_rerun_derived_law_2026.py, mi_dbi_cmb_class_run_2026.py)
- MOND is OFF at recombination: a₀(z=1090)/a₀(0) = 6.0e-3, so the parent theory's CMB pass is STRUCTURAL rather than fitted. Never analyse this framework with a fixed a₀ or a Newtonian Jeans length. [SETTLED] (source: RETRACTIONS.md; stage17_a0z_from_the_action_2026.py)
- The DESI-CPL a₀(z) bump ("+6% at z≈0.4") — never self-consistent with w=−1; this was the June "falsifiable prediction" and it is gone. [RETRACTED] (source: RETRACTIONS.md)
- a₀(z)/a₀(0) = (1+z)^{1.5(1+w₀+w_a)}·exp(−1.5w_a z/(1+z)) as the correct law — bump-then-decline, NOT a rise. [SETTLED] (source: memory index project_a0z_evolution_law; a0z_desi_chains_propagation.py, desi_a0z_loop_CLOSED.py)
- "ȧ₀/a₀ ≈ −3e-11/yr, DERIVED" — the correct value is +(3/2)ν₀²H₀ ∈ [4.7e-20, 3.5e-18]/yr: 7–8 orders too large AND wrong in sign. [RETRACTED] (source: RETRACTIONS.md)
- "MUSE confirms rising a₀" — re-graded shared-not-distinctive, and it is a SHARP NULL (any robust a₀ evolution below z~5 falsifies). [RETRACTED as support] (source: memory index; stage21_muse_msa_reexam_derived_law_2026.py, project_a0z_MUSE_DARK_III_confrontation.py)
- AeST λ_J = 2.7 Mpc as a prediction — the k⁴ Jeans term is 11 orders too small; the scalar clusters like CDM. [RETRACTED] (source: RETRACTIONS.md; mi_aest_jeans_nonlinear_verdict_2026.py, mi_cosmo_perturbations_2026.py)
- "Λ_D = Q₀ is the natural choice" (Lam = 1) — EXCLUDED: at Λ_D/Q₀ = 1 the peak sound speed is c_s² = 0.25 during the growth epoch, erasing total matter power at k=0.2. Post-recombination growth needs Λ_D/Q₀ ≤ 1.5–3.1e-6. [RETRACTED] (source: RETRACTIONS.md; stage69_cs2_growth_class_2026.py PART D)
- "The c_s² bump peaks at z ≈ 189" (THE_COMPLETION non-claim 3) — stale; with the committed ν₀ window the peak is at z ≈ 14–29. Reproducing 189 would need ν₀ ≈ 7e-8, 294× below the committed floor. Direction: ADVERSE. [RETRACTED] (source: stage69 PART A)
- "c_s² ≈ 1.1e-8 as an independent small-R normalisation" — it is an EPOCH statement computed at R=1, and R=1 is excluded. There is NO independent small-R normalisation in the corpus. [RETRACTED] (source: RETRACTIONS.md)
- The Lyman-α forest b-cutoff "6–8σ exclusion" — a real physics error manufactured the deficit (kernel evaluated at Newtonian y instead of observed x); corrected to 0.4–0.9σ on the defensible calibration channel. The SIGN is robust, the EXCLUSION is not. Also: the observed cutoff values were unsourceable (Schaye+2000 axis tick labels, not a table) and the ±2.0 km/s error bar was invented. [RETRACTED] (source: STANDING.md §5.1; mi_forest_bcut_data_2026.py + five companions)
- The same kernel-argument error in the growth/σ₈ chain was worth a factor 59: diffuse-IGM amplification 135→8.25, WHIM 722→4.58, required suppression ×10²–10³ → ×7–41. Still 24.5× over at 3σ — reduced, NOT closed. [SETTLED] (source: mi_growth_kernel_argument_audit_2026.py)
- "The forest tightens Λ_D/Q₀ to ≤ 2.3e-9 (672×)" — DEMOTED TO A BRACKET the same day: it priced only the adverse half. The framework's own response gives a 545×–7.7e7× power ENHANCEMENT against a suppression of at most 250×. In force: Λ_D/Q₀ ≤ 2.3e-9 (linear-only) OR looser by orders (response-active) — neither edge established. Symmetric warning: a response big enough to absorb the suppression is big enough to OVERPRODUCE forest structure, which is uncomputed. [OPEN, both edges] (source: RETRACTIONS.md; lyman_alpha_dust_ic_2026.py 22/22, forest_bound_framework_response_2026.py 18/18)
- "Ly-α-safe by construction" — withdrawn as stated; the framework still passes, conditionally on sitting in the bottom decade of the health window. Favourable and structural: c_s²(z=1090) = 1.9e-11·R, so there is NO primordial cutoff — this is not WDM in disguise. [RETRACTED as stated] (source: RETRACTIONS.md)
- Hooper's deciding forest likelihood — confirmed NEVER RELEASED. [SETTLED] (source: memory index stage16; stage15_forest_likelihood_mapping, stage16_lognormal_forest_mock)
- S8 / σ₈: does the χ sector's pressure cutoff alleviate S8? NO. S8 neutral-by-theorem. [SETTLED] (source: stage23_s8_confrontation_2026.py, project_sigma8_evolving_a0.py)
- MI modifying the cosmological BACKGROUND — structurally impossible (Thm 4): comoving FRW makes u an exact zero mode, K(0⁺)=0, the term vanishes identically. cH₀/a₀ = 7.00 is a coincidence of SCALES, not a coupling. [SETTLED] (source: STANDING.md §4; mi_channelA_friedmann_2026.py)
- "Apparent phantom dark energy from modified inertia" — doubly occupied prior art (arXiv:2605.27301; arXiv:2012.03446). [SETTLED] (source: STANDING.md §4; mi_phantom_prior_art_and_exclusivity_2026.py)
- Bulk-flow 1.9× boost — all three routes closed: σ₈ (122σ), RSD fσ₈ (19σ), BAO/LSS shape. [SETTLED] (source: STANDING.md §4)
- Cosmic dawn / JWST early-massive-galaxy collapse: the framework's collapse IS 1.34–1.96× faster than Newtonian and a₀(z) makes the speedup DECLINE with z (2.03× at z=6 → 1.14× at z=25) — a shape no constant-a₀ MOND has. **Price the boost at TURNAROUND (2.3–5.1×), not at the virial radius (≲1.5×).** [OPEN as a discriminator] (source: stage24, stage25, stage26_collapse_acceleration_own_terms_2026.py)
- w = −1 is EXACT at the minimum; with a₀(z) it is w = −1 + O(ν₀²), offset 1e-10–1e-8. The "exactly −1" claim is wrong as stated. [SETTLED] (source: RETRACTIONS.md)
- ν₀ ≤ 2.36e-6 and the committed window [2.14e-5, 1.77e-4] (note these are from different pins — check which applies); Q₀ pinned 0.0024–0.0146 Mpc⁻¹; the X-pin 316–1000 and the X-DILEMMA resolved at OOM grade (horn ≤0.2%/0.5%). [SETTLED] (source: stage56_xpin_verdict, stage58_x_to_q0, stage62_cmb_horn_oom, stage76_nu0_recombination_pin_2026.py)
- The DBI/khronon "natural Lam = 1" reading — see the Λ_D=Q₀ exclusion above. [RETRACTED] (source: mi_dbi_khronon_2026.py correction banner)
- The AeST action was MIS-TRANSCRIBED in `THE_COMPLETION.md` and every document built from it (𝓕 added not subtracted; 𝓕 outside not inside the 1/16πG̃ prefactor; +λ(A·A+1) not −λ). **Use `real_research/bridge1_aest_equations.md` as the reference transcription.** The embedding of 𝓕_Y and K into the source's single −𝓕(𝒴,𝒬) slot is STILL OWED — do not quote it as settled. [RETRACTED + OPEN] (source: RETRACTIONS.md; ppn_verify_transcription_2026.py 38/38)

---

## 7. PPN, preferred frame, and the solar-system limit (R5)

- γ_PPN = 1 and c_T = 1 exactly (the latter an IDENTITY since c₁₃ = 0 for every K_B). [SETTLED] (source: RETRACTIONS.md; prep_2026/gw170817_check/*)
- α₁ = −4K_B ⇒ K_B < 2.5e-5 from LLR — **WITHDRAWN AS A BOUND**, and stage73's "EMPTY WINDOW" with it. Four independent routes, each attacked by two adversarial verifiers: Foster & Jacobson's appendix removes c₁₂₃=0 from the domain BEFORE deriving the formula; α₂ is a simple pole with nonzero residue (infinite on the branch where α₁=−4K_B is right); and the static longitudinal aether kinetic operator IS c₁₂₃, so at c₁₂₃=0 the equation changes TYPE. **Do not quote K_B < 2.5e-5, and do not quote α₁ = 0 either.** [RETRACTED] (source: RETRACTIONS.md; stage74_ppn_fork_adjudicated_2026.py 24/24; alpha2_{regulated_limit,linearised_solve,wellposedness,literature_forensics}_2026.py)
- **IN FORCE: K_B ∈ [2.1e-4, 2) on no-ghost, [2.1e-4, 0.25] with BBN.** SZ21's own fits clear the floor by 475×/1875×. Two adverse riders at equal prominence: every NEIGHBOUR of the theory in coupling space IS PPN-excluded (c₂ ~ 1e-8 generated radiatively reimposes K_B ≲ 4.5e-8), and Sagi 2009 gets FINITE α₁ ~ 1/K with the scalar retained. [SETTLED, with named riders] (source: RETRACTIONS.md)
- α₁ = −4K_B's ARITHMETIC is correct and must not be called wrong — it is a theorem on the regular branch, reproduced from scratch. [SETTLED] (source: RETRACTIONS.md)
- Will's convention: the g₀₀ preferred-frame terms are −(α₁−α₂−α₃)w²U − α₂wⁱwʲU_ij, so the w²U coefficient is (α₂−α₁+α₃), NOT (α₃−α₁). The two conventions MIX α₁ and α₂: |α₂| is convention-robust, |α₁| is NOT (4K_B vs (3/2)K_B). "No verdict depends on the convention because every bound is on |α|" is FALSE and struck. [RETRACTED] (source: RETRACTIONS.md; ppn_scalar_retained_2026.py)
- stage71's c_V² = 1 − K_B is a SIGN SLIP — FJ06 Eq.(15)'s spin-1 row is 1 exactly on the dictionary (triple-confirmed). [RETRACTED] (source: RETRACTIONS.md)
- stage71 B2's "the generic ratio is 0/0" is WRONG (α₂ is a simple pole); stage73 B4's "opposite SIGN to reading L" is struck (the frozen-λ third reading gives −2K_B, same sign — and that reading is itself refuted, since freezing λ violates charge conservation). [RETRACTED] (source: RETRACTIONS.md)
- The subluminality floor K_B ≥ 2/(𝓚₂+1) from c_s² ≤ 1 — a LOWER bound opposing every PPN bound. At SZ21's MOND-compatible fits the window is empty; at the corpus's pinned Q₀ it is open 2.2× at the low edge. New exact identity: c_s² = [4m_×²/((2−K_B)μ²)](1+K_Bλ_s/2) → 2(m_×/μ)². [OPEN, conditional on the α₁ fork] (source: kb_small_limit_safety_2026.py 33/33)
- **STILL GATING EVERYTHING and not yet landed:** α₁, α₂ for the FULL theory with the SCALAR retained, and with it the LOCAL spin-0 speed in the solar system (SZ21 Eq. 30's c_s is COSMOLOGICAL). It turns on one number — whether local c_s exceeds w_⊙ = 1.234e-3 c. [OPEN — the highest-value PPN target] (source: RETRACTIONS.md)
- Cassini Q₂ quadrupole: a 3–15σ tension the AeST/MG realisation INHERITS (Desmond–Hees–Famaey 2024; Park+ 2026). Cassini is NOT a favourable in-hand discriminator. [SETTLED] (source: STANDING.md §5.3; aest_cassini_quadrupole_full.py, mi_cassini_q2_omegac_2026.py)
- s^TX SME boost dipole — NOT LIVE. Margin 1.03e6×/7.09e5× under the operative kernel; 10³⁵⁴ under Route A. Do not cite ~9.6×, 1.50× or 1.24×. [RETRACTED] (source: STANDING.md; mi_stx_alpha2_collapse_2026.py, mi_stx_route_a_retirement_2026.py)
- α₂^MI ~ 1e-8 as LIVE — it is ~1e-13, ~1e6× safe. [RETRACTED] (source: STANDING.md §6)
- MICROSCOPE/WEP: is η=0 structural? Plus the precision-consistency ledger (atomic clocks 1e-18, atom interferometry, binary pulsars, PTAs). [SETTLED] (source: mi_microscope_wep_2026.py, mi_clocks_atominterferometry_2026.py, mi_pulsar_pta_precision_ledger_2026.py, VERIFY_mi_precision_ledger_2026.py)
- The locally-dragged / Machian frame as a repair — largely CLOSED: 39/44 verdicts REFUTED across four routes and 48 verifiers. Carina kills it on data in hand (predicted σ=1.74 km/s vs 6.6±1.2 measured, 4.05σ low, p-independent). The vorticity leg is DEGENERATE (a uniform curl is an exact coordinate rotation; Earth ranging and LLR are blind). Route D's 18–25× is a tuning artefact and withdrawn. [SETTLED] (source: mi_machian_frame_routeA_2026.py, route_b_memory_time_2026.py, mi_hierarchy_falsifier_routeC_2026.py, mi_route_d_dragged_frame_nogo_2026.py, mi_dragged_frame_consolidation_2026.py)

---

## 8. Ephemerides — the R1 obstruction

- Legality forces U → s, hence a CONSTANT sunward anomaly s·a₀ at every planetary distance. Perihelion precession needs s ≤ 1.27e-5; the RAR needs s ≥ 0.219 canonical / 0.173 alt. **GAP 13,600–17,300×.** [OPEN — this is roadblock R1 and the sharpest item in the corpus]
- Bounds verified from primary sources, not quoted: Sereno & Jetzer 2006 Table 1 (Pitjeva EPM2004) inverted through their own Eq.(9) gives δA_R ≤ 3.66e-14 m/s² (Earth, 2σ) and 3.72e-14 (Mars). [SETTLED] (source: STANDING.md §5.0; mi_alpha1_solar_system_2026.py)
- Bare a₀/2 is 1278–1279× over (canonical) / 1544× (alt), post-EFE identical. [SETTLED] (source: mi_efe_escape_and_ch23_withdrawn_2026.py)
- The Fienga+2009 global-refit escape (~200× looser) does not reach — those are OUTER-planet limits, orbits loose enough to absorb a constant acceleration. [SETTLED] (source: STANDING.md §5.0)
- Galaxy data does not REQUIRE α=1: α=1, α=2 and α=∞ fit within 0.0084 dex at fixed a₀ on 175 SPARC; only 5.2% of SPARC points reach g_bar/a₀ > 10 and the sample tops out at 110, against Earth's ~6e7. [SETTLED] (source: mi_tail_exponent_rar_cost_2026.py)
- a₀'s DERIVATION does not depend on α=1 at all — every premise (Herglotz positivity, passivity sup K=1, the unit sum rule, the horizon floor) is satisfied by the other kernels. The reframing is NOT at risk from this liability; only the word "exact" is. [SETTLED] (source: STANDING.md §5.0)
- The disformal lensing construction sends a SECOND bill for the same item: dB/dr = 4×(the ephemeris anomaly) exactly (verified to 4e-9), so on α=1 B varies by 257×/311× across Mercury→Saturn against its own B<1 premise. NOT independent evidence. [SETTLED] (source: mi_disformal_tail_freedom_2026.py)
- An α=1-exclusive audit of the published corpus: only TWO published papers carry an unlabelled α=1 claim. Clean, don't re-flag: CRISPY:84-88, A0_HALF:182, both live submissions, KAPPA. [SETTLED] (source: mi_alpha1_exclusive_class_audit_2026.py)
- The α=1 ephemeris liability recomputed with a₀ LOCAL. [SETTLED as a computation] (source: a0_local_ephemeris_2026.py)
- Planetary-ephemeris upper edge on ω_c; the kernel-at-planets lane. [SETTLED] (source: mi_ephemeris_omegac_edge_2026.py, prep_2026/planetary_doors/laneK_kernel_planets.py, prep_2026/mi_planetary_falsification/*)

---

## 9. Wide binaries / Gaia DR4

- `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are FROZEN. **Never modify them.** A frozen pre-registration is amended in the open, before data, and hash-stamped. [TOOL] (source: STANDING.md §8.6; qwen LEDGER t082 frozen-file guard, 11/11 match)
- In-force target after Amendment 10: **BAND 1.1614–1.1814 canonical / 1.1917–1.2267 alt, edge 1.23**. [SETTLED] (source: memory index, commit 40ca6ad7)
- γ_v = 1.2139 / 1.2592 (Amendment 9) as the settled MG target — the full nonlinear AQUAL-EFE solve shows the registered number is the response tensor's LARGEST EIGENVALUE declared isotropic. Full-solve bracket 1.11–1.16 canonical / 1.13–1.21 alt. Amendment 9(d)(i)'s 2.68σ arm separation does NOT survive. [RETRACTED] (source: RETRACTIONS.md; prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py)
- Superseded γ_v values that must never be cited as current: 1.09, 1.0310, 1.1582, 1.2139/1.2592. [RETRACTED] (source: STANDING.md, memory index)
- The wide-binary AC (acceleration-criterion) gate verdict — WITHDRAWN; γ_v reverts to UNGATED. [RETRACTED] (source: memory index project_wb_gate_fork; mi_wb_gate_fork_2026.py)
- The pipeline `wide_binary_pipeline.py` still hard-codes 1.09 (signal 1.758× too small) — 7-item checklist, 3 BLOCKING. [OPEN, infrastructure] (source: mi_dr4_readiness_audit_2026.py 28/28)
- The s³ gate-opening law and the cubic rise in the separation window every published analysis cuts away. [SETTLED as a prediction, published v4 DOI 21702746] (source: mi_wb_cubic_rise_2026.py, mi_wb_exponent_pipeline_2026.py, mi_wb_dr3_feasibility_2026.py)
- The eccentricity discriminator (MI vs MG in wide binaries) and the full e=0→0.9 signal curve. [SETTLED] (source: mi_eccentricity_widebinary.py, mi_ecc_curve_sweep.py, mi_nonlocal_kernel.py)
- Confrontations already run against published wide-binary analyses: Chae+2026, Saad & Ting 2026, Zhang–Hasani Zonoozi–Kroupa 2026, Milgrom's linear/time-nonlocal no-EFE MOND (arXiv:2503.07106), El-Badry+2021 counts beyond 30 kAU. [SETTLED] (source: widebinary_chae2601_confront.py, widebinary_saadting_2603_confront.py, zhang_kroupa_2026_a0swap_replay.py, milgrom_linear_noefe_wb.py, count_wb_elbadry2021.py)
- The wide-binary + directly-measured galactic-acceleration route to κ, priced. [SETTLED] (source: mi_wb_gext_kappa_route_2026.py, wb_a0_amplitude_budget.py, wb_a0_amplitude_degeneracy.py)
- Directional-EFE kill switch: ARMED and FIRED once (Â = +2.95, p = 0.029, AQUAL-class sign); pure MI predicts exactly zero; needs N ~ 1157. [OPEN] (source: memory index project_directional_efe_test; prep_2026/gaia_dr4_prep/amendment2_derived_efe.py)

---

## 10. RAR / SPARC / BTFR / lensing

- **Before relaying ANY "fails/wash/deficit/too-low" on the RAR, re-run `real_research/rar_framework_a0_mlfit.py` (→ 0.108 dex at Υ=0.70).** The SPARC RAR is convention-COMPATIBLE and NON-diagnostic of 9.36e-11; neither "~20% too low" nor "~20% too high" is robust. [SETTLED — standing working rule] (source: memory index; redteam_rar_framework_a0.py, sparc_rar_honest.py)
- BTFR v⁴ = G M_b a₀ as a THEOREM of the convex field theory with coefficient exactly 1, not a fit. [SETTLED] (source: mi_route_a_field_theory_2026.py, mi_btfr_intercept_kappa_door_2026.py, btfr_honest.py)
- The high-z BTFR as an independent test of a₀(z) — NO, it is gas-confounded. [SETTLED] (source: btfr_evolution_confound.py; stage60_btfr_discriminator_2026.py + its two adversarial referee lanes)
- The shape systematic across four kernels on the full SPARC RAR is 26.3%; it collapses with depth but σ(a₀)_stat grows about as fast, so the best total error is 8.49% and NO depth resolves the κ gap better than 2σ. [SETTLED] (source: mi_routeA_shape_invariant_a0_2026.py, mi_shape_systematic_mechanism_2026.py)
- The a₀-line as the "sharpest single-number a₀ constraint" — it carries an unquoted SHAPE systematic comparable to or larger than the 7.87% gap it is used to probe. [RETRACTED as shape-free] (source: STANDING.md §0)
- The distance-free g_bar estimator on real SPARC (175 galaxies, 2803 quality points). [SETTLED] (source: mi_distance_free_gbar_estimator_sparc_2026.py)
- Weak-lensing RAR from 40 kpc to 2.2 Mpc with NO dark component and no free parameters: χ²/dof = 2.03 canonical / 0.94 ALT (real Mistele+2024 KiDS). The same fit REJECTS adding a dark component to galaxies. [SETTLED] (source: stage12_lensing_stack_fit_2026.py; prep_2026/kids_rar/kids_rar_lambda.py)
- Lensing excludes pure MI at 21σ; all three rescues closed. MI-as-fundamental is CLOSED; the operative arm is MODIFIED GRAVITY since 2026-08-08. [SETTLED] (source: RETRACTIONS.md; mi_mg_arm_standing_2026.py 18/18)
- Per-galaxy a₀ universality (the Rodrigues 2018 challenge) and the RAR scatter as a QUANTITATIVE upper bound on how much a₀ may vary. [SETTLED] (source: project13_a0_universality.py, project_rar_bounds_rho_uniformity.py, sparc_anchor_universality.py, rar_tightness_intrinsic.py)
- Joint (a₀, Υ_3.6) SPARC refits, marginalised-M/L RAR, SED priors — all run on the framework's OWN ν. [SETTLED] (source: rar_joint_a0_upsilon_sedprior.py, rar_marginalized_ml.py, prep_2026/a0_line_mlpriors/*)
- The bulge M/L cannot be pinned and cannot be eliminated either. [SETTLED] (source: mi_bulge_ml_cannot_be_pinned_2026.py)
- The Milky Way vertical-force front: full AQUAL on McMillan-2017 baryons; f_M = 1.30 nails vertical force (+0.2σ) and the Eilers slope (+1.2σ), failing ONLY v_c normalisation ⇒ a baryon-budget problem, not a kernel problem. Route A's vertical-force FLOOR (78.5/82.7) sits above the highest published determination (74), so the kernel over-delivers everywhere. [SETTLED, mixed] (source: mi_aqual_mcmillan2017_2026.py, mi_vertical_force_resolved_2026.py, mi_routeA_sigma_dyn_floor_extended_baryons_2026.py, mi_routeA_box_clearance_verified_2026.py)
- "ZERO cells clear the 2σ box" (mi_aqual_route_a_refit L7a) — a GRID ARTEFACT of a 0.15 step in f_M; three implementations agree the box clears at 1.502σ canonical. [RETRACTED] (source: STANDING.md §0)
- Dwarf-spheroidal closure discrimination — DOWNGRADED by real data: systematics-limited, not sample-limited; per-object scatter 0.38–0.48 dex and the dominant Υ_V error is COHERENT so √N does not help. "N~150, archival" is [RETRACTED]. (source: STANDING.md §3D; mi_dsph_closure_test_real_data_2026.py, mi_forecast_systematics_audit_2026.py)
- ν_vert/ν_rad = 1.0243 — NON-DIAGNOSTIC. [SETTLED] (source: mi_route_a_vertical_radial_ratio_2026.py)
- The non-adiabatic relational σ-spread as a near-term discriminator — repriced DOWN 3–15× (1.45–2.21% max−min vs banked 6.2–14.1%); N(3σ) at the ELT tier is ~2e5–2e7, past the whole CHANCES budget. [RETRACTED as near-term] (source: STANDING.md §4; prep_2026/sigma_spread/*)
- NGC1052-DF2 as an external-field-dominated dwarf test. [SETTLED] (source: mi_ngc1052_df2_efe_2026.py 10/10, mi_dwarf_efe_maths_audit_2026.py)
- The SN-Ia host-step at a₀ — real 6.9σ mass step reproduced and the step-LOCATION coincidence is real, but the decisive tests are UNDERPOWERED-not-null (18% power). DISFAVOURED, not excluded. [SETTLED] (source: STANDING.md §4; mi_snia_power_curve_2026.py)

---

## 11. Standard Model / numerology / shared-number ideas — WALLED

**Read this before writing any idea that connects the framework to an SM number.** The
qwen autoloop spent 95 sessions almost entirely here and produced 95 honest deaths.

- All TOE and Standard-Model claims were PUBLICLY retracted 2026-06-23 to ~40 physicists. Never help revive them. [RETRACTED] (source: RETRACTIONS.md, STANDING.md §0)
- m_p/m_e = α⁻¹·2Z²/5 and variants; α⁻¹ = 4Z²+3; sin²θ_W = 3/13; N_gen = 3 from the Z² cascade; E6/GUT spectrum fits; the Z² = 32π/3 "eta-invariant/topology/holonomy derivation" — all ~0 bits on the framework's own FDR test. [RETRACTED] (source: RETRACTIONS.md)
- **The NUMBER-FIELD OBSTRUCTION:** Z carries √π (transcendental) while flavour observables are algebraic ⇒ the germs are structurally gauge-blind and cannot generate those targets. This kills the whole class, not individual attempts. [SETTLED] (source: mi_number_field_theorem_2026.py, mi_number_field_local_presentation_2026.py, number_field_split_flavor.py, period_ring_obstruction_2026.py)
- The qwen autoloop's 95 ideas: **90 killed blind by the referee (spot-audit found NO mis-sorted discards), 4 harvested and all 4 dead, 1 executed and dead at premise.** Every one was of the form "single shared dimensionless number X does two unrelated jobs". [SETTLED] (source: LEDGER.md rows 0001–0094; FINDINGS_HARVEST_2026-08-16.md)
- The specific shared numbers already tried and killed: φ = 1.618 (rows 0009, 0014, 0016, 0026, 0032, 0059, 0068, 0070, 0082, 0091), 2/3 Koide (0011, 0017, 0021, 0031, 0045, 0061, 0064, 0065, 0069, 0075), 1/3 (0018, 0042, 0055), m_W/m_Z = 0.8814 (0002, 0007, 0020, 0030, 0034, 0080, 0085, 0094), sin²θ_W = 0.2312 (0005, 0035, 0057, 0076, 0078, 0093), sin θ_C = 0.2250 (0013, 0015, 0028, 0040), m_μ/m_e = 206.77 (0039, 0060, 0079, 0081), α⁻¹ = 137.036 (0010, 0014, 0028, 0043, 0069, 0073, 0075), R_dm = 0.387 (0030, 0033, 0036, 0083, 0091), y_t ≈ 0.70 (0036, 0041, 0043, 0058, 0077, 0083, 0086), the footing fork ratio 1.2048 (0084, 0087, 0090), the tetrahedron solid angle 0.5513 (0072, 0088), κ itself (0013, 0027, 0044, 0063, 0093). [ALL SETTLED-DEAD] (source: LEDGER.md)
- √κ ≈ the top Yukawa — DEFINITION SHOPPING: [0.70, 0.75] is crowded with top-sector definition variants and the only sub-percent match uses the FITTED κ as if fundamental. [SETTLED] (source: harvest H0027)
- δ_CKM·ln(m_μ/m_e) = 6.078 ≈ 6 — NO DISCRIMINATING POWER: 6.08 ± 0.19, so the "1.3% miss" and a perfect hit are both inside the error. [SETTLED] (source: harvest H0023)
- y_t·√(m_p/m_e) ≈ 30 — NULL BY CONSTRUCTION: the ±0.030 band maps to N ∈ [28.7, 31.3], three integers in a 2.6-wide window, P(some integer lands) = 1. [SETTLED] (source: harvest H0086)
- sin θ₁₂ = 0.554 vs κ = 0.551 ± 0.043 (0.1σ) — the ±7.8% window also contains sin²θ₂₃ = 0.558; at least two named SM numbers inside 1σ, chance expectation O(1). [SETTLED] (source: harvest discard audit, row 0092)
- E8 / J₃(𝕆), E6 orbifold GUTs, gauged SU(3)_F/Koide, Dirac family-index routes to N_gen, magnetised-torus generations, radion/Casimir — HOST the structure, do not FORCE it; no prediction. [SETTLED] (source: RETRACTIONS.md; the e6_*, s4_*, family_su3_*, koide_*, orbifold_*, z2z2_* review scripts)
- `project_atomos` symbolic regression at SM parameters — NULL, published (DOI 21654272) after an audit withdrew two false claims. Chance alone hits 10 of 19 targets. [SETTLED] (source: STANDING.md §4)

---

## 12. Infrastructure and the integrity record [TOOL]

- Frozen-file guard: hashes `PREREGISTRATION_DR4.md` + all `*_HASH.txt` against git-committed digests; 11/11 match. Run it if an idea touches anything frozen. (source: qwen runs/t082_frozen_guard.py)
- DO-NOT-CITE linter: grep guard over the retracted phrases, wired pre-append in the harness. (source: runs/t083)
- Units checker (10 committed formulas, [m,kg,s] exponent propagation, anti-tautology guard) and the kernel-library regression canary (12 pins reproduce committed numbers). Use these instead of hand-checking C3. (source: runs/t084, t085; qwenlib)
- Ledger-integrity checker and refutation-duty tracker (lists every CONFIRMED row with no linked refutation attempt). (source: runs/t086, t087)
- Negative-results museum builder — currently reports 0 closed doors because the qwen ledger holds no REFUTED/NULL row (every row is DISCARD/CONFIRMED/SCRIPT/NOTE). Builder verified non-vacuous by positive control. **A genuine REFUTED verdict from the 500-run is therefore a first.** (source: NEGATIVE_RESULTS.md, runs/t088)
- The full-corpus CI runner: heavy stages are NORMAL (stage63 ~3 min, stage64 ~8 min); a 60 s timeout falsely flags them red. (source: runs/t081, t081b, t090)
- The physics catalog T011–T136 and the MM/SR/bridge sweeps T101–T136 were **never run** — starved by the seed mill. They remain the highest-value unexecuted content and do NOT count as prior work. (source: FINDINGS_HARVEST_2026-08-16.md)
- Engine positive controls that already work: `bridge_scan` blind-recovers a₀ = c√(Gρ_Λ) at prefactor 0.5006; `mm_search` recovers Koide's 2/3; `sr_engine` blind-recovers a₀-line structure from 3,389 real SPARC points. Re-validating these is not a new result. (source: FINDINGS_HARVEST_2026-08-16.md)

---

## 13. Where the corpus is genuinely THIN — draw ideas here

Recorded because C6 is a filter, not a wall. Nothing below has a prior-work line above.

- **a₀ as a dynamical field with its own equation of motion** (□a₀, boundary conditions at a halo edge, wave solutions and their speed, correlation length, lag behind the density it tracks, behaviour across a shock). The corpus has only ever treated a₀ as a number that happens to vary. [OPEN — seeded angle S1]
- **Inhomogeneous dark energy**: ρ_Λ → P(x)/c² locally, so dark energy is SUPPRESSED wherever the charge is dense. Fractional deficit inside a cluster/galaxy/solar system, ISW, void expansion, SN distances through voids vs walls, ⟨P⟩ vs the ρ_Λ Planck fits. Appears NOWHERE in the corpus despite following from two committed lines. [OPEN — seeded angle S2]
- **The wall |Q−Q₀| = Λ_D as a locus in spacetime**: where is it for the Sun, the Milky Way, a cluster, at both edges of the pinned Q₀ band; is any real object past it; is it crossed during collapse; is there a shell where a₀ = 0 inside a halo. [OPEN — seeded angle S3]
- **Legality re-derived with a₀ as a field** — the monotonicity requirement behind the 233× obstruction was derived treating a₀ as CONSTANT, which the framework itself contradicts. If it holds, the central roadblock deepens; if not, the 233× number needs a replacement. [OPEN — seeded angle S4, the highest-value item in the spec]
- The 𝓕_YQ mixing matrix and the embedding of 𝓕_Y and K into AeST's single −𝓕(𝒴,𝒬) slot. [OPEN, explicitly owed]
- Four repair-space cells from stage53 B3 remain genuinely untried. "No open doors" is never claimable. [OPEN]

---

*Rule 5 of STANDING §8 governs this file too: **never say "the theory is closed."** A
`[SETTLED]` line means the computation was done and does not need redoing — not that the
physics behind it is beyond appeal. Overturning one requires naming the defect in the cited
script, which is exactly the kind of result this run should want.*
