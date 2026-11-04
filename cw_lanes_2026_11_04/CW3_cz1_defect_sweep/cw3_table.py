#!/usr/bin/env python3
"""CW3: writes CW3_TABLE.md from the hand-audited rows below plus the machine rows in cw3_triage.json / cw3_taint.json.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I cw3_table.py.  Reads files only.  kappa = 1/2 FITTED; not theory closed."""
import os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
CW1 = "NOT RERUN: recomputed in lane CW1 (cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4)"
P3 = "NOT RERUN: priority 3, not cited by the current record"
SUP_WB = "NOT RERUN: superseded; the DR4 banked target computes this with the inverted field"
# (section, lane, file:line, formulation, field used and source, label, verdict-change class)
HAND = [
 # ---------------- 1. named lanes
 ("1", "KT20", "rebuild_2026_10_22/KT20_filter_wide_binaries/kt20.py:9,15", "QUMOND 1D quadrature nu(sqrt(ge^2+h^2)/a0)", "GE = 1.9e-10 (BN11 observed g_e; qwen_claude_field_theory/closure_2026/g01_strict_aqual.py:106) and 2.32e-10 (KT16 observed)", "DEFECT-Q", CW1),
 ("1", "KT21", "rebuild_2026_10_22/KT21_filter_wide_binary_dr3_shape/kt21.py:17,21,49,59", "same form; reads kt20.json", "1.9e-10 inherited from KT20 (2.32e-10 side row)", "DEFECT-Q", CW1),
 ("1", "CFG843", "campaign_fresh_gravity/CFG843_mw_vs_m31_satellites/cfg843.py:11; campaign_fresh_gravity/CFG828_dwarf_excess_rotation_vs_dispersion/cfg828.py:10", "isolated law g_bar nu_e(g_bar/a0) read from CFG828", "none (no external field)", "CORRECT", "-"),
 ("1", "CFG478", "campaign_fresh_gravity/CFG478_satellites_qumond_efe/cfg478_qumond_efe.py:23-29,47", "exact QUMOND flux of (nu(|g_N+g_e|)-1)(g_N+g_e) around a point mass", "g_e = G M_NFW(<R)/R^2, NFW M200 6e14 (the cluster's measured mass, cm14b's host): observed", "DEFECT-Q", "MOVES: chi2/5 Q1 94.6-106.9 -> 70.7-92.7, Q2 78.4-92.3 -> 53.2-74.9, Q3 61.0-74.5 -> 36.6-55.8; boost Q1 1.4-1.8 -> 1.6-2.6; label FORCE+EFE EXCLUDED (robust) holds (p <= 7e-7)"),
 ("1", "cm14b (CFG478's source, cited by CFG447)", "sonnet55_push/cold_mass/cm14b_sifon_table.py:6-7,29,35-36", "reading B: nu((g_N+g_e)/a0) M_b", "g_e = G M_NFW(<R)/R^2, 'the cluster's measured mass'", "DEFECT-Q", "MOVES: reading B chi2 99.7/5 -> 83.9/5, offset +0.81 -> +0.74 dex; EXCLUDED holds"),
 ("1", "UX4", "rebuild_2026_10_22/UX4_dwarf_failures/ux4.py:22-23,29-30,74,334,343", "AQUAL (D10 Solver2D, mu = x/(1+x)); IC 1613 I4 the same solver", "x_e = MOND field of host baryons (MW 6e10, M31 1e11, Hernquist 3 kpc); IC 1613 X1 x_e_mid and the MW+M31 MOND sum", "CORRECT", "-"),
 ("1", "CFG447", "campaign_fresh_gravity/CFG447_efe_blind_force_vs_dr3/cfg447_efe_blind.py:19-23,43,48", "injected gamma = sqrt(nu(y_true)), EFE-blind by design; K1 uses the DR4 pipeline's gamma_of_y", "none in the main reading; K1 uses the pipeline's inverted y_extN", "CORRECT", "-  (its triangle cites cm14b's 99.7, which moves to 83.9 and stays excluded)"),
 ("1", "directional EFE, lane A", "real_research/reviews/directional_efe_2026/laneA_predictions.py:6-18,91-129; confrontation.py:31,42,150", "QUMOND Legendre BVP, uniform external field", "e = Chae+21 e_N, Newtonian", "CORRECT", "-"),
 ("1", "directional EFE, first firing", "prep_2026/aligned_firing/fire_aligned_n16.py:60-63,96", "lane A map at (x, e)", "e from Chae's published e_N (Newtonian)", "CORRECT", "-"),
 ("1", "directional EFE, WALLABY firing", "prep_2026/wallaby_firing/fire_wallaby.py:333-344; run_gext_237.py:41-48", "lane A map at (x, e)", "e_N from the 2M++/MCXC Newtonian sum (GextEstimator)", "CORRECT", "-"),
 ("1", "g_ext vectors", "gext_vectors_2026/src/gext_estimator.py:10,192", "Newtonian field-vector estimator, no nu or mu", "Newtonian sum of 2M++/MCXC sources", "CORRECT", "-"),
 ("1", "dipole mock", "prep_2026/dipole_mock/dipole_mock.py:17-36,106-127", "QUMOND closed form, point mass in a uniform field", "gNe Newtonian (Bilek 2024 convention)", "CORRECT", "-"),
 ("1", "l=1 BVP", "prep_2026/l1_bvp/l1_bvp.py:53,82-95", "Branch-B medium BVP; moduli run with the total |g| (mu_s is a shear modulus)", "Sun + total Galactic field 1.9-2.6 a0, AQUAL-class total", "CORRECT", "-"),
 ("1", "hunt h28 (Chae EFE on WALLABY)", "hunt_2026/h28_chae_efe_wallaby.py:29,95-96", "1D QUMOND nu((g_N+g_Ne)/a0)(g_N+g_Ne) - nu(e_N) g_Ne", "e_N from gext_wallaby_237.csv (Newtonian)", "CORRECT", "-"),
 ("1", "CFG514, CFG173 ('directional' by name)", "campaign_fresh_gravity/CFG514_directional_milky_way/cfg514_directional.py:91,159-170; campaign_fresh_gravity/CFG173_door11B_directional_flow/cfg173_directional_flow.py:116-122", "QUMOND phantom of MW baryons; a directional medium flow", "none (no external field)", "CORRECT", "-"),
 ("1", "09-03 Local Group dwarfs (hunt item 8; MW +0.64, M31 +0.29)", "hunt_2026/h8_h42_h96_dwarfs.py:53-54 (item 8), 90-91 (item 42); cited at hunt_2026/WHAT_THE_HUNT_TAUGHT.md:93-94", "quasi-Newtonian G_eff = nu(x_ext) G", "x_ext = sqrt(G M_host a0)/D / a0, the host's deep-MOND field (observed)", "DEFECT-Q", "MOVES: MW +0.641 -> +0.372 (alt +0.632 -> +0.352), M31 +0.294 -> +0.106 (alt +0.284 -> +0.086), all 46 +0.363 -> +0.284, centring Upsilon_V 23.8 -> 11.1 (alt 22.4 -> 9.9); 'item 8 does not close' holds. Item 42 simple-EFE DF2 14.9 -> 22.5, DF4 16.6 -> 25.2 km/s; check 42 holds"),
 ("1", "IC 1613 external-field lever", "rebuild_2026_10_22/FAILURES_LITERATURE_REVIEW_2026-10-28.md:34-41 (an estimate, no code)", "AQUAL suppression estimate", "LG 'total mass' field 0.015 a0, set against IC 1613's Newtonian 0.02", "FIXED", "closed by CZ1 Part D (Newtonian LG field 3.4e-4 / 2.8e-4 a0, E shift +0.00001 dex); confirmed: UX4's I4 AQUAL term with MOND fields 0.013-0.037 moves E by 0.002-0.015 dex (share 0.00-0.02)"),
 # ---------------- FIXED (CZ1/CZ2), not re-audited
 ("F", "KT15", "rebuild_2026_10_22/KT15_filtered_phantom_dsph/kt15.py:20,39", "KT dwarf form", "(200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 ("F", "KT16", "rebuild_2026_10_22/KT16_filtered_phantom_cassini/kt16.py:9,19", "Cassini quadrature", "eta = 2.32e-10/a0", "FIXED", "CZ1/CZ2"),
 ("F", "KT17", "rebuild_2026_10_22/KT17_mond_radius_filter/kt17.py:16,21", "Cassini and dwarf forms", "2.32e-10; (200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 ("F", "KT18, KT19, KT22, KT23", "rebuild_2026_10_22/KT18_*, KT19_*, KT22_*, KT23_*", "MW, SPARC, ladder rows", "no external field in nu", "FIXED", "CZ1/CZ2 scope; no external field (KT24 does not exist)"),
 ("F", "KT25", "rebuild_2026_10_22/KT25_eps_equals_kappa/kt25.py:16,21", "Cassini and dwarf forms", "2.32e-10; (200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 ("F", "KT26", "rebuild_2026_10_22/KT26_local_filter_rule/kt26.py:16,21,70,75", "Cassini and dwarf forms", "2.32e-10; (200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 ("F", "KT27", "rebuild_2026_10_22/KT27_local_rule_alt_grade/kt27.py:19,26", "Cassini and dwarf forms", "2.32e-10; (200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 ("F", "KT28", "rebuild_2026_10_22/KT28_tidal_filter_rule/kt28.py:24,31; kt28_mw.py:16,21", "Cassini and dwarf forms", "2.32e-10; (200 km/s)^2/D", "FIXED", "CZ1/CZ2"),
 # ---------------- beyond KT28
 ("K", "KT29", "rebuild_2026_10_22/KT29_tidal_rule_mw_full_tensor/kt29.py:16,21,23,37,47,73", "the KT Cassini and dwarf forms, carried beside the MW arm", "2.32e-10; (200 km/s)^2/D", "DEFECT-Q", "UNCHANGED: the frozen label comes from the MW cells, which carry no external field; the inherited dwarf eps rows beside it are CZ1's E1 rows once corrected"),
 ("K", "KT30", "rebuild_2026_10_22/KT30_tracefree_tidal_rule/kt30.py:26,40,85; kt30_mw.py:16,23,47,73", "the KT Cassini (T1) and dwarf (T2) forms, graded", "eta = 2.32e-10/a0; ge = (200 km/s)^2/D", "DEFECT-Q", "@KT30@"),
 ("K", "KT31, KT32", "rebuild_2026_10_22/KT31_tidal_rule_rz_solve, KT32_tidal_rule_rz_scatter", "MW (R, z) solves", "no external field", "CORRECT", "-"),
 # ---------------- 2. current record
 ("2", "REQUIREMENTS row 5 (dwarfs) / FG1 Dw", "rebuild_2026_10_22/FG1_final_grade/fg1_read.py:26,49,94; rebuild_2026_10_22/ND1_native_dwarfs/nd1_ceiling.py, nd1_ab.py, nd1_shapes.py", "plain nu(g_N); ND1 native halos (GE there is Newton's G)", "no external field", "CORRECT", "-"),
 ("2", "REQUIREMENTS row 6 (IC 1613): RF2, IN1, RT1, FD1", "rebuild_2026_10_22/RF2_ic1613_inclination_footing/rf2_ic1613.py:33-36; rebuild_2026_10_22/IN1_ic1613_inclination/in1_ic1613_inclination.py:37-41; rebuild_2026_10_22/RT1_lt_rotation_regrade/rt1_lt_rotation_regrade.py:70; rebuild_2026_10_22/FD1_field_dwarf_audit/fd1_field_dwarf_audit.py:71", "E = log g_obs - log(nu(g_N/a0) g_N)", "no external field", "CORRECT", "-"),
 ("2", "Local Group classes (PAPER67 line 77): LW1, X1, Z2", "rebuild_2026_10_22/LW1_law_scorecard/lw1_dwarfs.py:16,20-23,35; rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py:68-73,94-102,325-331; rebuild_2026_10_22/Z2_satellite_systematics/z2_satellite_systematics.py:62-76", "AQUAL (D10); LW1's 1D QUMOND row inverts g_e with mu first; X1's MM13 recipe uses mu(x_e)", "MOND field of host baryons into AQUAL; Newtonian gNe = mu(x) g_e into nu", "CORRECT", "-"),
 ("2", "D10 solver", "doors_push_2026_10_22/D10_native_Lstar/d10_solver.py:3-7,142-151", "AQUAL, mu = x/(1+x), background total x_e", "declared total", "CORRECT", "-"),
 ("2", "Solar System row (PAPER67 line 80): E2, read by M1", "doors_push_2026_10_22/E2_field_equation/e2_field_equation.py:43,154-159,186; aqual_axi.py:6,129,214-221; rebuild_2026_10_22/M1_trilemma/m1_trilemma.py:640-647", "AQUAL and QUMOND axisymmetric solves", "kinematic 1.9/2.2/2.6 a0 inverted to Newtonian y_e; AQUAL gets the total", "CORRECT", "-"),
 ("2", "Milky Way row (X5, RF1, UR3; LW1 MW)", "rebuild_2026_10_22/LW1_law_scorecard/lw1_mw.py:13-17", "nu(hypot(g_b, K_N)/a0)", "both Newtonian (no external field)", "CORRECT", "-"),
 # ---------------- DR4 pre-registration (read only)
 ("D", "DR4 frozen pipeline", "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py:39,92,186-201,281-283,470", "gamma(y) = 1 + (gamma_inf-1) y_extN/(y_extN+y); Route A eigenvalues ANISO_EIG", "y_extN = y_newt_from_obs(1.9 a0), the observed field inverted through the framework nu", "CORRECT", "-"),
 ("D", "DR4 banked target", "real_research/reviews/wb_dr4_prereg_framework_curve.py:53,60-98,138-142", "MG <nu(|y_int + y_ext,N|)>; MI per star nu(|g_ext,N + g_i,N|)", "y_ext,N = 1.4647, inverted from 1.9", "CORRECT", "-"),
 ("D", "DR4 Arm A in force (Amendment 10)", "prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py:45-55,173-177,293-297", "full AQUAL solve (primary) and QUMOND (fork)", "AQUAL background x_e = y nu(y) (total); QUMOND the inverted y_extN", "CORRECT", "-"),
 ("D", "DR4 Amendment 2 (derived EFE)", "prep_2026/gaia_dr4_prep/amendment2_derived_efe.py:8-21,50-77", "a = nu(|g|/a0) g, response eigenvalues at g_ext", "g_ext = 1.778e-10 / 2.078e-10 (observed) used as g; the text says the closure's argument is the total four-acceleration", "AMBIGUOUS", "NOT RERUN: DR4 folder is read only; superseded by Amendment 8's Route A eigenvalues at the inverted y_extN, which the pipeline carries"),
 ("D", "DR4 Amendment 1 gated row", "real_research/reviews/mi_wb_gate_fork_2026.py:56,90-102", "gamma_v = sqrt(1 + (nu(y_ext)-1) Re G), framework nu", "y_ext = (233 km/s)^2/8.2 kpc / a0 (observed); MI-named", "DEFECT-Q", "NOT RERUN: DR4 banked-target script, read only; Amendment 6 withdrew Amendment 1's basis"),
 ("D", "DR4 Amendment 1 cubic rise", "real_research/reviews/mi_wb_cubic_rise_2026.py:48,54,60; mi_wb_exponent_pipeline_2026.py:35,41,45", "gamma_v - 1 ~ (1/2)(nu(y_ext)-1)(omega_c^2/GM) s^3", "the same V^2/R; MI-named", "DEFECT-Q", "NOT RERUN: withdrawn with Amendment 1 (Amendment 6)"),
 # ---------------- 3. frozen grep, read by hand: DEFECT and AMBIGUOUS rows
 ("3", "hunt f09", "hunt_2026/f09_orbital_coherence_fork.py:52-53", "quasi-Newtonian nu_s(g_ext/a0)", "MW_VC^2/d (observed)", "DEFECT-Q", "NOT RERUN: corrected on record by hunt_2026/g05_dsph_prescription_fixed_and_expanded.py:263-271 (v3, Newtonian G M/D^2, -0.418 dex)"),
 ("3", "hunt h9 (Coma UDGs)", "hunt_2026/h9_h11_pressure_supported.py:49-52,63-67", "quasi-Newtonian nu_s(x_e) g_b", "G M_NFW(<r)/r^2 of Coma, M200 1.3e15 (total)", "DEFECT-Q", "NOT RERUN: corrected on record by hunt_2026/u02_qumond_efe_flux_theorem.out:68-85 (+1.195 -> +1.021 naive, +1.083 flux theorem, +0.942 baryon field; the kill still fires)"),
 ("3", "hunt g03, g03v", "hunt_2026/g03_anisotropy_correlation_test.py:118-119; g03v_adversarial_efe_branch_refutation.py:120,166", "quasi-Newtonian nu_s(g_ext/a0)", "MW_VC^2/d", "DEFECT-Q", P3),
 ("3", "hunt h47 item 47e (LMC-SMC)", "hunt_2026/h47_dwarf_pairs.py:74-77,722-723", "v = sqrt(nu_s(e_N)) v_Newton", "sqrt(G M_MW a0)/55 kpc (deep-MOND, 0.17 a0)", "DEFECT-Q", "NOT RERUN: side row; reading only: with the Newtonian 0.030 a0 the EFE speed 46 -> about 68 km/s, still below the isolated 75 and the observed 128, so 47e's statement holds"),
 ("3", "hunt k03, kernel-shape alpha and q-aniso", "hunt_2026/k03_widebinary_kernel_width.py:13,42,83; k_kernel-shape_alphawb.py:7,43; k_kernel-shape_qaniso.py:7,179", "Amendment 2's eigenvalue construction", "G_EXT 1.778e-10 / 2.078e-10 (observed) as g", "AMBIGUOUS", P3),
 ("3", "CFG331 R-efe", "campaign_fresh_gravity/CFG331_sluggs_centrals_environment/cfg331_environment.py:305,338-341", "1D QUMOND nu(|g_N+g_e|)(g_N+g_e) - nu(g_e) g_e", "g_e = nu(g_Ne/a0) g_Ne (MOND-boosted host)", "DEFECT-Q", "NOT RERUN: cannot flip; in this form a host field only lowers the boost, so the corrected R-efe offset sits between the K0 +0.224 and +0.295, and R-efe needs the excess to drop"),
 ("3", "cm14 (before cm14b)", "sonnet55_push/cold_mass/cm14_satellite_lensing.py:24-25", "nu(y + g_e) M_b", "NFW host field", "DEFECT-Q", "NOT RERUN: superseded by cm14b and CFG478, both rerun here"),
 ("3", "cm15 (SW01 rule on cluster satellites)", "sonnet55_push/cold_mass/cm15_sw01_rule_vs_satellites.py:1,17", "nu(sqrt(x^2+eta^2)) g_own", "eta = G M_NFW(<R)/R^2 / a0", "DEFECT-Q", P3),
 ("3", "cluster EFE channel", "prep_2026/cluster_efe_channel/mg_efe_zero.py:51,59-72", "d = 0.5 ln nu(g_ext/a0)", "NFW M200 1e15 total ('external MOND field')", "DEFECT-Q", P3),
 ("3", "EFE dS-Unruh paper figure data", "opus_48_extended_research/papers/efe_dsunruh_figdata.py:11-15 (paper EFE_dsunruh_paper.tex:159-162)", "nu(e), nu(e)(1+L_e), orbit average", "e = (233 km/s)^2/8.178 kpc / a0", "DEFECT-Q", SUP_WB),
 ("3", "opus wide-binary scripts", "opus_48_extended_research/reviews/wb_contamination_route4.py:41,50-55; wb_reconciliation_derivation.py:47,77; mi_vs_aqual_route2.py:42,75; widebinary_MI_MG_DR4_forecast_2026-06-20.py:24,47", "<nu(|y_ext+y_int|)>, 1D QUMOND", "Vc^2/R0 (2.15e-10); mi_vs_aqual MI-named", "DEFECT-Q", SUP_WB),
 ("3", "real_research wide-binary confrontations", "real_research/reviews/widebinary_chae2601_confront.py:39,56; widebinary_saadting_2603_confront.py:33,46,65; real_research/predictions/door6_wide_binaries_ultra.py:111,258-259", "1D QUMOND / nu(y_ext)", "Vc^2/R0, V_MW^2/R0", "DEFECT-Q", SUP_WB),
 ("3", "MI reviews (solar system, wide binaries, WEP)", "real_research/reviews/mi_alpha1_solar_system_2026.py:46,126-127; mi_microscope_wep_2026.py:77,267; mi_cassini_q2_omegac_2026.py:41-42,153; mi_eps_tot_mode_counting_verdict_2026.py:242-243; mi_q1_efe_order_count_2026.py:97,717; mi_q2_dc_or_orbital_2026.py:177; mi_quasistatic_efe_multipoles_2026.py:52,142; mi_wb_gext_kappa_route_2026.py:76,133; cmb_modinertia_oscillator.py:494-499; real_research/reviews/toe_law/mi_f4_widebinary_efe.py:20,28", "the framework nu (or nu_frame) at the Galactic field", "V^2/R, 1.8e-10, 1.778e-10, 2.078e-10 used as the Newtonian field; MI-named (A5)", "DEFECT-Q", P3),
 ("3", "other observed-field rows", "real_research/reviews/opt1_gates_2026.py:815-819; real_research/reviews/toe_law/agentM_milgrom2022_gauntlet.py:321,340; real_research/reviews/project_efe_check.py:36 (toy table, 'g_ext = 1.8 (MW)'); qwen_claude_field_theory/runs/claude/i001_efe_factorisation.py:256,541-549; qwen_claude_field_theory/closure_2026/route3_entropic_gravity_2026.py:376,382", "nu at the Galactic field; 1D QUMOND", "V_LSR^2/R_GC, 2.15e-10, 1.8 a0, 1.8e-10, V_sun^2/R_sun", "DEFECT-Q", P3),
 ("3", "fable SW-series and lanes", "fable_independent_2026/glm_moe_push/SW01b_envscalar_orthogonality.py:94,187-189; SW05_kepler_freeze.py:54,78,90; SW09_chain.py:151,286; fable_independent_2026/kappa_slot_2026/SW01_direction_blind_efe.py:37,58; fable_independent_2026/kappa_slot_2026/SW04_ppn_full.py:104; fable_independent_2026/L198_df2_external_field.py:40-41; fable_independent_2026/L233_predictions.py:92,101", "the SW01 rule nu(sqrt(x^2+eta^2)); nu(eta); L198 nu of a MOND-boosted field", "eta from V^2/R or 2.32e-10; L198 gext = nu(g_N/a0) g_N; L233 1.8e-10", "DEFECT-Q", P3),
 ("3", "DE02 decline law (generic eta)", "deepseek_push/DE02_framework_decline.py:4,29,145-150", "nu(sqrt(x^2+eta^2)) set against AQUAL's 1/mu(eta) at the same eta", "eta a generic grid, read as total in mu and as Newtonian in nu", "AMBIGUOUS", P3),
 ("3", "toy rows with a Galactic 1.8 a0", "qwen_claude_field_theory/theory_2026/york/elliptic_channel_signaling_theorem_2026.py:48-52", "nu_s((g_int+g_ext)/a0) derivative rows", "'wide binary in the Galaxy' g_ext 1.8 a0 (observed scale)", "DEFECT-Q", P3),
 ("3", "field passed in, not set in the file", "real_research/efe_clinch_framework.py:16; opus_48_extended_research/reviews/efe_clinch_framework_dsunruh.py:16; real_research/reviews/mi_efe_escape_and_ch23_withdrawn_2026.py:70; real_research/dark_sector_2026/L321_carrier_z0_retention_gate.py:85-89; hunt_2026/g06v_adversarial_external_field_baryon_budget.py:356", "1D QUMOND or nu(sqrt(g_N^2+g_e^2)) with g_ext a function argument", "value not resolved by reading the file", "AMBIGUOUS", P3),
 ("3", "L273, agentJJ", "fable_independent_2026/L273_direction_blind_reconciliation.py:16; real_research/reviews/toe_law/agentJJ_transient_fingerprint.py:287-288", "nu(eta_gal); 1D QUMOND", "field value not assigned in the file", "AMBIGUOUS", P3),
]
# hand-read CORRECT rows (one phrase each)
HAND_OK = [
 ("hunt_2026/h43_h44_ufd_m31_sigma.py:23,53,167", "Newtonian G M_host/D^2; flags h8's defect at lines 16-19"),
 ("hunt_2026/h93_outer_halo_globulars.py:22-27,182-195", "Newtonian g_ext_newton; flags h8's defect"),
 ("hunt_2026/g05_dsph_prescription_fixed_and_expanded.py:263-271", "v3 uses G M_host/D^2 (the fix of f09); v0-v2 keep V_c^2/D as the stated before-fix steps"),
 ("hunt_2026/u02_qumond_efe_flux_theorem.py", "re-grades h9 with the kernel-inverted and baryon fields"),
 ("hunt_2026/h34_h35_h38_milky_way.py:448-451,539", "nu slots take fitted or fixed e_N; the printed prior calls M31's deep-MOND field (0.017 a0) 'e_N' (Newtonian 3e-4), which no nu call uses"),
 ("hunt_2026/h37_lmc_bound.py:94", "M31's MOND pull inverted to e_N"), ("hunt_2026/h40_sednoid_perihelia.py:130", "Galactic field inverted to x_ext"),
 ("hunt_2026/h39_open_cluster_tails.py:91", "x_ext_newtonian"), ("hunt_2026/h41_wide_binary_eccentricity.py:44", "x_ext 1.7 = the Newtonian value of the Sun's field"),
 ("hunt_2026/h48_h69_binary_galaxies.py:49; h48_h69b_relative_isolation.py:51", "e_N 0.03 LSS (Newtonian)"), ("hunt_2026/k02_phantom_budget_s8_al.py:93-94", "Chae e_N"),
 ("hunt_2026/k03_dwarf_shape_laws.py:79-90", "MOND host field inverted before nu"), ("hunt_2026/f14_isolated_dwarf_msigma_law.py:67", "G M/D^2"),
 ("hunt_2026/g06_local_volume_groups_lambda_edge.py:617", "G M/D^2 + baryonic LSS"), ("hunt_2026/v_g06_dsph_shift_decomposition.py:75,90", "baryonic and total modes both computed, labelled"),
 ("campaign_fresh_gravity/CFG179_door11_merge_swirl/cfg179_s2_merge_numbers.py:268", "inverted (1.4647)"), ("campaign_fresh_gravity/CFG191_merge_referee/CFG191_s5_dr4_mapping.py:67", "inverted"),
 ("campaign_fresh_gravity/CFG333_one_ownership_rule/cfg333_one_rule.py:190", "G M_MW/R^2"), ("campaign_fresh_gravity/CFG820_stiffness_from_globulars/cfg820.py:14", "G M_MW/R^2"),
 ("campaign_fresh_gravity/CFG936_below_law_systems/cfg936.py:226,258,402", "G 0.6 L_K / D^2"), ("campaign_fresh_gravity/CFG946_option2_phantom_not_cold/cfg946.py:276-281", "G M_host/r^2"),
 ("campaign_fresh_gravity/CFG244_bound_fluid/CFG244_H_satellites.py:103", "G M_host/D^2"), ("campaign_fresh_gravity/CFG884_sextans_two_populations/cfg884.py:248", "G 6e10/D^2"),
 ("campaign_fresh_gravity/CFG212_budhies_efe_preflight/cfg212_budhies_preflight.py:88-92", "observed inverted"), ("campaign_fresh_gravity/CFG771_saddle_point/cfg771.py:104-105", "2.32e-10 inverted with the simple mu"),
 ("claude_goal_2026_11_03/CZ1, CZ2, CZ4", "the fix lanes; E0 rows reproduce the KT field by design; CZ4:112 inverts"),
 ("doors_push_2026_10_22/D8_Lstar_value/d8_lstar_value.py:110; E4_fitted_three/e4_fitted_three.py:216", "G M_MW/R^2"),
 ("nbody_2026/stage61_drain_reading_fork_2026.py:237; stage64_efe_two_body_exact_2026.py:93,150", "y_of_x inversion; AQUAL mu at the total"),
 ("prep_2026/mi_integrator/mi_integrator.py:945,993; VERIFY_independent.py:306,340; applications.py:388", "y_newt_from_obs"),
 ("qwen_claude_field_theory: audit3, g02c, route1_interpolation, gate0, gate3, g03g, g03i, df2_fixed_a0", "e_N inverted; AQUAL mu at the total"),
 ("real_research/reviews: aest_cassini_quadrupole_full, alldoors a2/d4/refute_a2, branchB laneA_family_scan, mi_kinetic_completion, toe_law agentD/agentH3, mi_route_a_*, mi_mg_arm_standing, mi_dwarf_efe_argument_test, mi_ngc1052_df2_efe, mi_route_a_cluster_residual_regimes, mi_dragged_frame_consolidation, tabby_exo_oort", "e_N or y_extN inverted from the observed field"),
 ("real_research/cross_thread_review_2026_09_26/XR27_efe_favouring.py:9,336-356", "graded law uses the band-passed Newtonian field; the h8 and FMM18 rows are reproduction controls, labelled"),
 ("rebuild_2026_10_22/CU1_gas_term_replication/cu1_core.py:17,103", "GE is Newton's G"), ("hunt_2026/f23, rebuild KT5, KT11, Z2 (taint hits)", "eN inverted; internal fields only"),
 ("mu (AQUAL) rows, all 43 A? files", "observed totals in mu, or totals built from Newtonian values; no DEFECT-A found"),
]
T = json.load(open(os.path.join(HERE, "cw3_triage.json"))); TT = {o["file"]: o for o in json.load(open(os.path.join(HERE, "cw3_taint.json")))}
kt30 = open(os.path.join(HERE, "kt30_class.txt")).read().strip() if os.path.exists(os.path.join(HERE, "kt30_class.txt")) else "pending"
HAND = [tuple(x.replace("@KT30@", kt30) for x in h) for h in HAND]
def paths(fl):
    out, d = [], ""
    for part in re.split(r"[;,]", fl):
        p = part.strip().split(":")[0].split(" ")[0].strip("`")
        if not p.endswith(".py"): continue
        if "/" in p: d = os.path.dirname(p) if p.count("/") >= 1 else d
        else: p = os.path.join(d, p) if d else p
        out.append(p)
    return out
defect_files = set(q for h in HAND for q in paths(h[2]))
flagged = [r for r in T["rows"] if r["cls"] in ("Q?", "N?", "A?") or (r["cls"] == "L?" and TT.get(r["file"], {}).get("hits"))]
hand_ok_auto = [r for r in flagged if r["file"] not in defect_files]
cnt = collections.Counter(h[5] for h in HAND)
byfile = collections.defaultdict(set)
for h in HAND:
    for q in (paths(h[2]) or [h[1]]): byfile[h[5]].add(q)
O = ["# CW3_TABLE: one row per audited file or lane", "",
     "κ = ½ FITTED; not theory closed. Labels and classes as frozen in `FROZEN_CRITERIA.md`; amendments A1-A6 in `AMENDMENTS.md`. File paths are from the repo root.", "",
     "## Hand-audited rows", "",
     "| § | lane | file:line | formulation | field used, source | label | verdict-change class |", "|---|---|---|---|---|---|---|"]
SEC = {"1": "1", "F": "1 (FIXED)", "K": "1 (after KT28)", "2": "2", "D": "DR4", "3": "3"}
E = lambda x: str(x).replace("|", "\\|")
for s, lane, fl, form, field, lab, vc in HAND:
    O.append(f"| {SEC[s]} | {E(lane)} | `{E(fl)}` | {E(form)} | {E(field)} | **{lab}** | {E(vc)} |")
O += ["", "## Read by hand, CORRECT (one phrase each)", "", "| file:line | why |", "|---|---|"]
for fl, why in HAND_OK: O.append(f"| `{E(fl)}` | {E(why)} |")
O += ["", f"## Flagged by the triage and read by hand: CORRECT ({len(hand_ok_auto)} files)", "", "Each was read at its ν/μ call and at the lines that set the field. The field is Newtonian (computed or inverted) in a ν slot, or total in a μ slot, or a generic grid value with no physical claim. The notes above give the reasons for the ones that needed one.", "", "| file:first line | triage class | label |", "|---|---|---|"]
for r in hand_ok_auto:
    ln = (r["efnu"] or r["efmu"] or r["obs"] or [1])[0]; O.append(f"| `{r['file']}:{ln}` | {r['cls']} | CORRECT (hand) |")
flagset = set(r["file"] for r in flagged)
mach = [r for r in T["rows"] if r["file"] not in flagset and r["file"] not in defect_files]
mc = collections.Counter()
O += ["", "## Machine triage (AMENDMENTS A3, A6), not read by hand", "",
      f"Frozen grep hits {T['n_hits']}; with a ν/μ call or a named interpolating function {T['n_audit']}. Every row below is labelled CORRECT by machine triage: no ν/μ argument carries an external-field name (CLEAR), or an observed literal exists but no taint path reaches a ν argument (L?, A6). Rows the triage flagged and that were read by hand appear above. A field that reaches ν through an unrecognised name passes as CORRECT here; that is the triage's stated limit.", "",
      "| file:first line | triage class | label |", "|---|---|---|"]
for r in mach:
    lab = "CORRECT (machine)"
    mc[lab] += 1; ln = (r["efnu"] or r["efmu"] or r["obs"] or [1])[0]
    O.append(f"| `{r['file']}:{ln}` | {r['cls']} | {lab} |")
summary = ["", "## Counts", "", "Hand-audited rows (a row can group files): " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())),
           f"Flagged files read by hand and CORRECT: {len(hand_ok_auto)}; flagged files inside the hand-audited rows: {len(defect_files & flagset)}.",
           "Files per label in the hand-audited rows: " + ", ".join(f"{k} {len(v)}" for k, v in sorted(byfile.items())) + "; DEFECT-A 0.", "Machine rows: " + ", ".join(f"{k} {v}" for k, v in sorted(mc.items()))]
O[4:4] = summary + [""]
open(os.path.join(HERE, "CW3_TABLE.md"), "w").write("\n".join(O) + "\n")
print("\n".join(summary)); print("defect/ambiguous files:", len(defect_files), "flagged:", len(flagset))
