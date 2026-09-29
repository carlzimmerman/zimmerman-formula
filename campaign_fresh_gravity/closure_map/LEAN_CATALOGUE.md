<!-- Lean corpus catalogue (fable_independent_2026/lean_2026). Compiled 2026-09-28 by reading committed files (agent-assisted); nothing in the repo was edited to produce it. -->
> **Provenance and reliability.** This file was compiled by a delegated reader of the committed repository and then spot-checked by hand. The compile results and counts (137 files, 116 compile, 21 fail, 9 real sorry in 4 non-certificate files, standard axioms only) come from a fresh comment-aware scan and per-file compiles; I re-ran the five proposed certificates myself and they compile. The per-file one-line descriptions were not re-verified.
> Where it disagrees with a committed script output, the script wins. It is a map, not a result: nothing here says the theory is closed.

file | compile | tracked | thm+lemma | def | #print-axioms in src | zaudit axioms | 0-binder thm | pure-numeric thm | hyp-binders | norm_num tokens | header (author's own scope line)
-|-|-|-|-|-|-|-|-|-|-|-
AS019_deep_mass_slopes | OK | N (untracked) | 7 | 0 | 0 | choice,sound,propext | 0 | 0 | 78 | 1 | AS019 -- Deep-law source mass conventions (Lean 4 certificate).
AS026_axioms | FAIL | N (untracked) | 0 | 0 | 18 | - | - | - | - | 0 | (none)
AS026_exact_inverse_qline | OK | N (untracked) | 20 | 2 | 0 | choice,sound,propext | 2 | 0 | 30 | 3 | AS026 -- Exact inverse of the algebraic a0 line (Lean 4 certificate).
AS026_exact_inverse_qline_axioms | OK | N (untracked) | 20 | 2 | 18 | choice,sound,propext | 2 | 0 | 30 | 3 | AS026 -- Exact inverse of the algebraic a0 line (Lean 4 certificate).
AS036_physical_vs_phantom_monotonicity | OK | N (untracked) | 20 | 1 | 0 | choice,sound,propext | 0 | 0 | 42 | 1 | AS036 -- Physical monotonicity versus phantom monotonicity (Lean 4 certificate).
AS036_physical_vs_phantom_monotonicity_axioms | FAIL | N (untracked) | 0 | 0 | 20 | - | - | - | - | 0 | (none)
AS037_api_probe | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
AS037_api_probe2 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
AS037_api_probe3 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
AS037_api_probe4 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 1 | (none)
AS037_api_probe5 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
AT1_AT3_acceleration_trigger_certificates | OK | Y | 5 | 0 | 0 | choice,sound,propext | 0 | 0 | 26 | 0 | # AT1–AT3 — the acceleration-triggered carrier: algebraic certificates
ActiveDensity | OK | Y | 4 | 0 | 0 | choice,sound,propext | 0 | 0 | 28 | 0 | R01 -- CERTIFY THE ACTIVE-DENSITY FACTORIZATION AND ITS ASYMPTOTE.
C01_mass_scaling | OK | Y | 3 | 2 | 0 | choice,sound,propext | 0 | 0 | 20 | 1 | C01 -- Lean certificate for the cluster mass-scaling fork (opus_48 cluster_massindep_2026/C01).
CV1_gate_offplateau_certificates | OK | Y | 8 | 0 | 8 | choice,sound,propext | 0 | 0 | 12 | 0 | # CV1 — V0 for the C-H/K branch: the gate's off-plateau and the region kernel's force algebra
CV2_covariant_reduction_certificates | OK | Y | 5 | 0 | 5 | choice,sound,propext | 0 | 0 | 22 | 0 | # CV2 — V0 for the C-H/K branch: certificates for its reductions
CV3_gate_rule_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 4 | 0 | # CV3 — V0's varied gate: the rule for what it may read
ClosureResume20260926 | OK | Y | 16 | 3 | 16 | choice,sound,propext | 3 | 3 | 48 | 1 | # Closure-resume certificates, 2026-09-26
DE13_gradient_repair_certificates | OK | Y | 8 | 0 | 8 | choice,sound,propext | 0 | 0 | 21 | 1 | DE13 -- can a gradient stiffness repair DE12's obstruction? Certificates for the structural steps.
DE7_gate_action_certificates | OK | Y | 12 | 0 | 12 | choice,sound,propext | 0 | 0 | 68 | 4 | DE7 -- the vacuum gate varied as an action term: certificates for the algebra and calculus the lane rests on.
DE_vacuum_gate_certificates | OK | Y | 17 | 0 | 17 | choice,sound,propext | 2 | 2 | 94 | 2 | # DE1–DE2 — the vacuum gate read at four epochs: algebraic certificates
DoorsAuxiliary20260926 | OK | Y | 7 | 1 | 7 | choice,sound,propext | 3 | 1 | 22 | 4 | Exact finite spectral/real inequalities underlying the lapse-weighted auxiliary
DoorsCausal20260926 | OK | Y | 8 | 0 | 8 | choice,sound,propext | 0 | 0 | 28 | 0 | # Constant-coefficient causal-completion algebra, 2026-09-26
DoorsTransport20260926 | OK | Y | 18 | 3 | 18 | choice,sound,propext | 0 | 0 | 22 | 3 | # Same-clock transport: exact scoped certificates (2026-09-26)
FL2_dark_slot_certificates | OK | Y | 6 | 0 | 6 | choice,sound,propext | 0 | 0 | 18 | 0 | # FL2 — V0's dark slot with FK1's kick potential: the algebra behind the field-side checks
FL3_swirl_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 12 | 0 | # FL3 — the dark fluid's swirl and the clock: the algebra behind the lane
G07_statistical_virial | OK | Y | 5 | 0 | 5 | choice,sound,propext | 0 | 0 | 30 | 1 | # G07 -- THE STATISTICAL VIRIAL (reduced form): the max-entropy identity
H046_health_forces_n | OK | Y | 48 | 15 | 9 | choice,sound,propext | 9 | 0 | 116 | 8 | H046 -- IS n = 2 FORCED BY THE HEALTH CONDITIONS? (Agent J)
H047_noether_charge_clustering | OK | Y | 28 | 9 | 17 | choice,sound,propext | 5 | 0 | 56 | 5 | H047 -- DOES THE NOETHER-CHARGE FREE DUST CLUSTER? Lean certificate.
I01_bhstar_wave | OK | Y | 11 | 3 | 10 | choice,sound,propext | 1 | 1 | 86 | 10 | # I01 — Wave I: exact certificates for the BH* absorption (arXiv:2609.09274)
I02_bhstar_ceiling | OK | Y | 3 | 0 | 3 | choice,sound,propext | 0 | 0 | 54 | 5 | # I02 — Wave J: the SMS ceiling as a closed-form function of the GR coefficient
I03_bhstar_regime | OK | Y | 2 | 2 | 1 | choice,sound,propext | 0 | 0 | 24 | 0 | # I03 — Wave K: the Balmer-layer regime invariance (the framework's strong-a0 layer)
I04_bhstar_ktable | OK | Y | 2 | 0 | 2 | choice,sound,propext | 1 | 1 | 2 | 2 | # I04 — Wave L: the K-table absorption and the central-β falsification
I05_bhstar_quartic | OK | Y | 2 | 0 | 2 | choice,sound,propext | 0 | 0 | 16 | 5 | # I05 — Wave M: the Eddington-quartic beta bound (the certified two-sided band)
I06_bhstar_bracket | OK | Y | 2 | 0 | 2 | choice,sound,propext | 0 | 0 | 32 | 6 | # I06 — Wave N: the certified two-sided bracket on the global GR ceiling
I07_bhstar_conditional | OK | Y | 3 | 0 | 3 | choice,sound,propext | 0 | 0 | 22 | 0 | # I07 — Wave P: the regime coincidence as an exact conditional identity
I08_bhstar_quartic_fp | OK | Y | 1 | 0 | 1 | choice,sound,propext | 0 | 0 | 20 | 0 | # I08 — Wave Q: the Eddington quartic constant from first principles
I09_bhstar_kinematic | OK | Y | 2 | 0 | 2 | choice,sound,propext | 0 | 0 | 22 | 0 | # I09 — Wave R: the wind-kinematic radius identities
I10_bhstar_void | OK | Y | 1 | 0 | 1 | choice,sound,propext | 0 | 0 | 8 | 0 | # I10 — Wave S: the void theorem (the U-route is ionizing-opaque)
I11_bhstar_kepler | OK | Y | 1 | 0 | 1 | choice,sound,propext | 0 | 0 | 16 | 0 | # I11 — Wave T: the Kepler-grade law KP1
I12_bhstar_dial | OK | Y | 2 | 0 | 2 | choice,sound,propext | 0 | 0 | 44 | 0 | # I12 — Wave U: the photosphere-gravity law — THE DIAL IS AN OBSERVABLE
I13_bhstar_pulsation | OK | Y | 16 | 4 | 12 | choice,sound,propext | 3 | 0 | 98 | 5 | # I13 -- GAS-PRESSURE KERNEL AND HOMOLOGOUS TRIAL-QUOTIENT ALGEBRA
I14_phantom_vacuum_wall | OK | Y | 34 | 7 | 29 | choice,sound,propext | 2 | 0 | 92 | 7 | # I14: exact statements for a specified Dirichlet difference form
I15_suN_lattice_gap | OK | Y | 10 | 2 | 10 | choice,sound,propext | 0 | 0 | 46 | 3 | # I15 -- THE SU(N) STRONG-COUPLING GAP, UNIFORM IN N
I16_volume_gap_window | OK | Y | 5 | 1 | 5 | choice,sound,propext | 0 | 0 | 30 | 2 | # I16 -- THE VOLUME-DEPENDENT STRONG-COUPLING WINDOW (doorG's partial theorem, certified rung)
I17_bhstar_audit | OK | Y | 8 | 0 | 8 | choice,sound,propext | 3 | 2 | 46 | 6 | # I17 — Audit of the BH* regime coincidence (lane L323)
I18_qso1_naked_bh | OK | Y | 18 | 8 | 16 | choice,sound,propext | 8 | 1 | 76 | 35 | # I18 — The naked-black-hole rotation law at z = 7.04 (A2744-QSO1; lane L324)
I19_ym1_bdl_threshold | OK | Y | 18 | 10 | 10 | choice,sound,propext | 7 | 4 | 50 | 22 | # I19 — D-YM1: the explicit strong-coupling threshold (BDL extension to Kogut–Susskind SU(N))
I20_velocity_floor | OK | Y | 5 | 1 | 5 | choice,sound,propext | 1 | 0 | 18 | 1 | # I20 — The velocity floor: around an isolated point mass the framework's circular speed never
I21_ym1_combinatorics | OK | Y | 6 | 3 | 6 | choice,sound,propext | 2 | 0 | 16 | 0 | # I21 — D-YM1 (L326): the combinatorial skeleton of the BDL extension, machine-checked
I21_ym1_polymer_threshold | OK | Y | 15 | 8 | 13 | choice,sound,propext | 7 | 1 | 26 | 21 | # I21 — D-YM1, second independent route: the space-time polymer-expansion threshold
I22_virial_floor | OK | Y | 4 | 1 | 4 | choice,sound,propext | 0 | 0 | 26 | 0 | # I22 — The virial floor: every isolated spherical system obeys ⟨v²⟩ ≥ (2/3)√(G M a0)
I22_ym1_dobrushin | OK | Y | 8 | 0 | 8 | choice,sound,propext | 0 | 0 | 28 | 7 | # I22 — D-YM1 Euclidean companion: the Dobrushin mass-gap arithmetic for Wilson SU(N)
I23_psf_floor | OK | Y | 3 | 0 | 3 | choice,sound,propext | 1 | 1 | 12 | 1 | # I23 — No real image is sharper than its PSF (the basis of the QSO1 narrow-cube artifact test, L327)
I23_rar_inversion_below_baryons | OK | Y | 7 | 1 | 7 | choice,sound,propext | 0 | 0 | 30 | 0 | # I23 — The dark-fraction inversion, and why galaxies below their own baryons are outside every model
I23_ym3_hardy_class | OK | Y | 7 | 1 | 7 | choice,sound,propext | 0 | 0 | 22 | 4 | # I23 — D-YM3 closed class-wide: the Hardy-marginal 1/4 is the Laplacian's Hardy constant
I24_c2_channel_phantom | OK | Y | 14 | 10 | 14 | choice,sound,propext | 2 | 2 | 48 | 2 | # I24 — The khronon's c₂ channel carries a moving phantom; the price lands on the aether's acceleration
I25_chk_universal_coupling | OK | Y | 4 | 8 | 4 | choice,sound,propext | 0 | 0 | 8 | 0 | # I25 — C-H/K boosts every minimally coupled source alike: no "additive" dark carrier
I26_switch_forest_threshold | OK | Y | 7 | 1 | 7 | choice,sound,propext | 1 | 0 | 24 | 1 | # I26 — L342's bound-region switch at the Lyman-α forest epoch: the switch variable from the constraint
I27_kick_escape | OK | Y | 5 | 1 | 0 | choice,sound,propext | 0 | 0 | 34 | 1 | # I27 — the triggered carrier's kick: why galaxy interiors empty, and why the phantom only adds decays
I28_selection_inflates_retention | OK | Y | 4 | 0 | 0 | choice,sound,propext | 1 | 1 | 2 | 1 | # I28 — why the own-dense-set clearing statistic overstates what is left (L379)
KM_khronon_momentum | OK | Y | 14 | 17 | 14 | choice,sound,propext | 0 | 0 | 70 | 1 | # KM — certificates for the khronon-momentum lanes (real_research/khronon_momentum_2026, KM1–KM2)
L279_lensing_algebra | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 14 | 0 | # L279 -- the algebra downstream of the candidate's derived quasi-static system
L280_alpha_ppn | OK | Y | 4 | 4 | 4 | choice,sound,propext | 0 | 0 | 18 | 0 | # L280 -- the clock host's preferred-frame parameters: exact identities
L281_ellipticity | OK | Y | 3 | 1 | 3 | choice,sound,propext | 0 | 0 | 8 | 0 | # L281 -- uniform ellipticity of the candidate's scalar operator for every field strength
L282_dispersion | OK | Y | 6 | 4 | 5 | choice,sound,propext | 0 | 0 | 20 | 0 | L282 -- the algebraic core of the candidate's scalar dispersion (real_research/clock_2026/L282_scalar_dispersion_from_action.py).
L283_frw_dust | OK | Y | 8 | 0 | 5 | choice,sound,propext | 3 | 3 | 16 | 3 | L283 (CK12) -- algebraic core of the FRW background and the dust's fate (real_research/clock_2026/L283_frw_background_and_dust_fate.py).
L284_jeans_identity | OK | Y | 3 | 0 | 3 | choice,sound,propext | 0 | 0 | 22 | 2 | L284 (CK12, perturbations I) -- the algebraic core (real_research/clock_2026/L284_dust_perturbations.py).
L290_ymod_carrier | OK | Y | 8 | 1 | 0 | choice,sound,propext | 0 | 0 | 14 | 1 | L290 -- the algebraic core of the Y-modulated carrier (real_research/clock_2026/L290_ymod_carrier.py).
L291_frw_ymod_carrier | OK | Y | 3 | 0 | 0 | choice,sound,propext | 0 | 0 | 10 | 1 | L291 -- the algebraic core of the carrier on FRW (real_research/clock_2026/L291_frw_ymod_carrier.py).
L293_cluster_cusp_ymod | OK | Y | 2 | 0 | 0 | choice,sound,propext | 0 | 0 | 6 | 2 | L293 -- the algebraic core of the cluster-cusp kill (real_research/clock_2026/L293_cluster_cusp_ymod.py, 2/3).
L294_cluster_caustic_ymod | OK | Y | 2 | 1 | 0 | choice,sound,propext | 0 | 0 | 6 | 0 | L294 -- the algebraic core of the cold-caustic cluster leg (real_research/clock_2026/L294_cluster_caustic_ymod.py, 5/5).
L295_baryonic_cmb_face | OK | Y | 4 | 2 | 0 | choice,sound,propext | 4 | 3 | 0 | 3 | L295 -- the certified arithmetic of the framework's no-dark-matter CMB face
L296_doublet_selfenergy | OK | Y | 1 | 0 | 0 | choice,sound,propext | 0 | 0 | 0 | 3 | L296 -- the certified arithmetic of the doublet's second-order verdict
L297_complete_action | OK | Y | 3 | 1 | 0 | choice,sound,propext | 0 | 0 | 1 | 1 | L297 -- the algebraic core of THE COMPLETE ACTION (real_research/clock_2026/L297_complete_action.py, 4/4).
L298_phantom_stress_tensor | OK | Y | 5 | 0 | 0 | choice,sound,propext | 0 | 0 | 24 | 0 | L298 -- the phantom's stress tensor; the algebraic core of the null-tangential theorem and the EoS window
L299_phantom_halo_selfconsistent | OK | Y | 5 | 0 | 0 | choice,sound,propext | 0 | 0 | 18 | 0 | L299 -- the phantom halo, self-consistent: the algebra of the emergent D-series mass law.
L300_exact_a1_arbiter | OK | Y | 3 | 0 | 0 | choice,sound,propext | 2 | 2 | 2 | 3 | L300 -- the exact a = 1 arbiter: the amendment of L291b/L291c. The machine lane
L302_exact_budget_corollaries | OK | Y | 11 | 0 | 0 | choice,sound,propext | 10 | 10 | 4 | 10 | L302 -- the exact-growth-budget corollaries (L301's theorem block). All numbers are the exact-rational
L303_phantom_trace_energy | OK | Y | 4 | 0 | 0 | choice,sound,propext | 0 | 0 | 14 | 0 | L303 -- the phantom's positive-energy trace theorem (real_research/clock_2026/L303_phantom_trace_energy.py).
L304_phantom_active_mass | OK | Y | 4 | 0 | 0 | choice,sound,propext | 0 | 0 | 10 | 0 | L304 -- the phantom's active-mass face (real_research/clock_2026/L304_phantom_active_mass.py, 4/4).
L305_phantom_rar_boost | OK | Y | 1 | 0 | 0 | choice,sound,propext | 0 | 0 | 8 | 0 | L305 -- the phantom-boosted RAR (real_research/clock_2026/L305_phantom_rar_boost.py, 3/3).
L330_frozen_density | OK | Y | 4 | 0 | 4 | choice,sound,propext | 1 | 0 | 20 | 2 | # L330 — the moving-source gate: algebraic certificates
L340_chk_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 34 | 2 | # L340 — C-H/K, the filtered-khronon completion: algebraic certificates
L341_frw_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 32 | 1 | # L341 — the FRW gate for C-H/K: algebraic certificates
L342_switch_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 24 | 0 | # L342 — the bound-region switch x = 9 R3/(4 K^2): algebraic certificates
L350_L352_chk_gate_certificates | OK | Y | 7 | 0 | 7 | choice,sound,propext | 0 | 0 | 38 | 0 | # L350–L352 — C-H/K's lambda-channel against cosmology, and L342's switch against GW170817 and Gauss:
L353_kernel_invisible_certificates | OK | Y | 6 | 0 | 6 | choice,sound,propext | 0 | 0 | 28 | 0 | # L353 — a kernel-invisible dark component in C-H/K: algebraic certificates
L357_L361_vacuum_gate_certificates | OK | Y | 7 | 0 | 0 | choice,sound,propext | 0 | 0 | 26 | 0 | # L357–L361 — the vacuum gate and the bound-region kernel: algebraic certificates
LR1_j09_window_law | OK | Y | 5 | 1 | 5 | choice,sound,propext | 0 | 0 | 10 | 2 | # LR1 — J09 central window law, Lean certificate (M-roads Lean roadmap)
LR2_j09p_window_law | OK | Y | 6 | 1 | 6 | choice,sound,propext | 0 | 0 | 24 | 0 | # LR2 — J09p general-p window law, Lean certificate (M-roads Lean roadmap)
LR3_m05_moments | OK | Y | 6 | 0 | 4 | choice,sound,propext | 4 | 0 | 4 | 4 | G2a
LR3b_m05_reduction | OK | Y | 6 | 2 | 5 | choice,sound,propext | 2 | 0 | 4 | 6 | G2a: linear substitution step
LR4_G2b_full_bank | OK | Y | 8 | 0 | 5 | choice,sound,propext | 0 | 0 | 22 | 15 | LR4 / LR5 conductor bank (Z7-wave, 2026-09-27)
LR4b_cov_discharge | OK | Y | 14 | 2 | 8 | choice,sound,propext | 2 | 0 | 28 | 21 | ### LR4b: cov discharge ASSEMBLY (Z7-wave successor lane)
LR4b_probe_draft | OK | N (untracked) | 2 | 0 | 0 | choice,sound,propext,sorryAx | 0 | 0 | 8 | 0 | Per-slice substitution (conductor bank, zero-sorry): r = sqrt(u^2+w^2).
LR4c_m05_i23 | OK | Y | 20 | 3 | 11 | choice,sound,propext | 6 | 0 | 32 | 28 | ### LR4b: cov discharge ASSEMBLY (Z7-wave successor lane)
LR5_ed2_bound | OK | N (untracked) | 2 | 0 | 2 | choice,sound,propext | 0 | 0 | 6 | 1 | LR5: Lean leg of the J06 bound chain E[D^2] >= 3 E[Dv^2]^2 / E[v^4]
M01_ad_bias_direction | OK | Y | 4 | 1 | 0 | choice,sound,propext | 0 | 0 | 22 | 0 | M01 -- Lean certificate for the asymmetric-drift a0-bias DIRECTION (opus_48 muse_a0z_2026/M01).
M01_alg_spine | OK | Y | 32 | 10 | 32 | choice,sound,propext | 5 | 0 | 66 | 18 | # M01 — The algebraic spine of the window-ratio family, machine-checked
MS1_MS2_mond_sector_door_certificates | OK | Y | 8 | 0 | 8 | choice,sound,propext | 0 | 0 | 8 | 0 | # MS1–MS2 — the MOND-sector door: which switch variable keeps the carrier kernel-invisible once the gate is varied
Mondlean | OK | Y | 190 | 5 | 0 | choice,sound,propext | 22 | 8 | 782 | 24 | Mondlean — Lean 4 / mathlib formalization of the load-bearing MATHEMATICS behind the de Sitter–MOND
N03_small_spine | OK | Y | 26 | 15 | 26 | choice,sound,propext | 10 | 0 | 12 | 18 | # N03 — The small algebraic spine, machine-checked
NSA_navier_stokes_audit | OK | Y | 21 | 3 | 21 | choice,sound,propext | 1 | 1 | 66 | 7 | # NSA — certificates for the Navier–Stokes audit lanes (real_research/ns_audit_2026, NSA1–NSA7)
PairObstruction | OK | Y | 4 | 0 | 0 | choice,sound,propext | 1 | 1 | 10 | 1 | R06 -- LOCK DOWN THE UNEQUAL-MASS CONSERVATION OBSTRUCTION (PD20/PD21 audit).
PushSlip20260926 | OK | Y | 15 | 0 | 15 | choice,sound,propext | 0 | 0 | 80 | 0 | Scoped CD26-2 certificates for IC27/IC28 algebra. These statements do not
Q01_r6_core | OK | Y | 8 | 2 | 4 | choice,sound,propext | 4 | 0 | 0 | 5 | # Q01 — the first-flight ladder certified as exact R-core polynomial integrals
R01_r8_core | OK | Y | 5 | 2 | 1 | choice,sound,propext | 1 | 0 | 0 | 2 | # R01 — the m=8 rung of the first-flight ladder certified as an exact R-core polynomial integral
SW06_local_nogo | OK | Y | 3 | 1 | 2 | choice,sound,propext | 0 | 0 | 30 | 0 | # SW06 -- the LOCAL no-go for a shared-metric phantom (horn A, single field)
TemporalSeparation_SKELETON_uncompiled | FAIL | Y | 12 | 4 | 0 | - | - | - | - | 0 | TemporalSeparation.lean
V01_chord_moment_2d | OK | Y | 23 | 5 | 15 | choice,sound,propext | 9 | 0 | 40 | 15 | # V01 - the volume-chord moment chordMomentVol = 3/4 (M01's conjectured item)
X01_ladder_core | OK | Y | 7 | 2 | 3 | choice,sound,propext | 3 | 0 | 0 | 4 | # X03 — the first-flight ladder: corrected r4, first r10 certificate, new r12
XC1_strong_coupling_certificates | OK | Y | 12 | 0 | 12 | choice,sound,propext | 1 | 1 | 30 | 5 | # XC1 — G8, the strong-coupling gate on C-H/K: algebraic certificates
XC2_wellposedness_certificates | OK | Y | 9 | 0 | 9 | choice,sound,propext | 0 | 0 | 30 | 1 | # XC2 — nonlinear well-posedness of C-H/K, scoped: algebraic and analytic certificates
XC3_filter_foliation_certificates | OK | Y | 5 | 0 | 5 | choice,sound,propext | 0 | 0 | 24 | 0 | # XC3 — the filter's own foliation vertices: certificates for the inequalities
XC4_recipe_decision_certificates | OK | Y | 5 | 0 | 5 | choice,sound,propext | 2 | 2 | 12 | 4 | # XC4 — the 2026-09-26 recipe decisions: certificates for their mathematics
XC5_lapse_convexity_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 28 | 1 | # XC5 — the MOND constraint with a non-constant lapse: certificates
XC6_soft_leg_certificates | OK | Y | 4 | 0 | 4 | choice,sound,propext | 0 | 0 | 30 | 0 | # XC6 — the heat filter's metric variation: the soft-leg lemma
ZD01_phantom_ceiling | OK | Y | 10 | 2 | 10 | choice,sound,propext | 0 | 0 | 54 | 0 | # ZD01 — The Phantom Ceiling (the dark-acceleration cap)
ZD02_mass_accounting | OK | Y | 12 | 1 | 10 | choice,sound,propext | 0 | 0 | 50 | 10 | # ZD02 — The Mass-Accounting Laws (the RAR in mass form)
ZD03_efe_suppression | OK | Y | 7 | 1 | 7 | choice,sound,propext | 0 | 0 | 46 | 0 | # ZD03 — The EFE Suppression Theorem and the Cluster Dark-Stripping Radius
ZD04_phantom_envelope | OK | Y | 5 | 1 | 5 | choice,sound,propext | 2 | 2 | 14 | 3 | # ZD04 — The Phantom Envelope (the enclosed-mass ceiling)
ZD12_phantom_halo | OK | Y | 6 | 1 | 5 | choice,sound,propext | 1 | 0 | 28 | 2 | # ZD12 — The Phantom Halo Laws (agent-derived, independently verified)
_as131_probe | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_as131_probe2 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_as131_probe3 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_probe | OK | N (untracked) | 1 | 0 | 0 | choice,sound,propext | 0 | 0 | 0 | 0 | (none)
_probe2 | FAIL | N (untracked) | 0 | 1 | 0 | - | - | - | - | 0 | (none)
_probe3 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_probe4 | FAIL | N (untracked) | 1 | 1 | 0 | - | - | - | - | 1 | (none)
_probe5 | FAIL | N (untracked) | 0 | 1 | 0 | - | - | - | - | 0 | (none)
_probe6 | FAIL | N (untracked) | 0 | 1 | 0 | - | - | - | - | 0 | (none)
_probe7 | FAIL | N (untracked) | 0 | 1 | 0 | - | - | - | - | 0 | (none)
_probe_c03 | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_probe_c03b | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_probe_c03c | FAIL | N (untracked) | 0 | 0 | 0 | - | - | - | - | 0 | (none)
_probe_v01 | FAIL | N (untracked) | 1 | 0 | 0 | - | - | - | - | 0 | (none)