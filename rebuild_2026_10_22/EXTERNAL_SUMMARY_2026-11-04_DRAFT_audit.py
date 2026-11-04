#!/usr/bin/env python3
"""Audit of EXTERNAL_SUMMARY_2026-11-04_DRAFT.md (lane FN5): each quoted number appears in the summary and in the committed file named
beside it; the scorecard matches FG1; naming and wording rules; no local paths; the draft marker.
Run: python3 EXTERNAL_SUMMARY_2026-11-04_DRAFT_audit.py (exit 0 only if all pass). --mutate changes one digit of each source literal and
perturbs the recomputed count; exit 0 only if at least 80 % of literals and the recomputation then fail.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, ".."))
MD = open(os.path.join(HERE, "EXTERNAL_SUMMARY_2026-11-04_DRAFT.md"), encoding="utf-8").read()
Q = "rebuild_2026_10_22/"; C = "campaign_fresh_gravity/"; P = "qwen_claude_field_theory/papers_2026/"
FG1 = Q + "FG1_final_grade/README.md"; REQ = Q + "REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md"; LED = Q + "CLOSING_LEDGER_2026-11-01_DRAFT.md"; LW = Q + "LW1_law_scorecard/README.md"
UL1 = Q + "UL1_measured_upsilon_test/README.md"; HS1 = Q + "HS1_hsb_lsb_residual_slope/README.md"; OD1 = Q + "OD1_old_disc_ruler/README.md"; C687 = C + "CFG687_erass1_shear_stack/README.md"; C689 = C + "CFG689_native_ruler_bao/README.md"
KF = "real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out"; KCL = C + "CFG894_kappa_campaign_ledger/"; K03 = "kappa_closure/k03_half_vs_two_pi_precision.out"
FR = Q + "FR1_fair_share_retention/README.md"; F3 = Q + "FR3_retention_independent/README.md"; LM = Q + "LM1_law_missing_mass_map/README.md"; GM = Q + "GM1_gas_tied_missing_mass/README.md"; AR = Q + "AR1_action_response/README.md"
LE = Q + "LE1_lensing_estimator_audit/"; W6 = "cw_lanes_2026_11_04/CW6_lensing_measured_gas/"; W1 = "cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/"; Z5 = "claude_goal_2026_11_03/CZ5_local_rule_3d_regrade/"
AX = Q + "AX1_action_for_law/"; CP = Q + "C6P_cassini_high_precision/"; HF = Q + "HF1_hybrid_fermion/"; VW = Q + "VW1_velocity_window/"; N1 = Q + "AN1_aest_nonlinear_dust/"; N2 = Q + "AN2_aest_3d_fold/"
A3 = Q + "AS3_ppn_and_khronon_scalar/README.md"; V3 = "covariant_push_2026_10_22/THEORY_V3_DRAFT.md"; CG = Q + "CG1_a0_certificate/README.md"; U3 = Q + "UX3_cluster_gas_term/README.md"; CU = Q + "CU1_gas_term_replication/README.md"
B = Q + "BK2_dimensional_law_search/"; BF = Q + "BF1_exhaustive_law_search/"; AT = Q + "AT1_a0z_tracking_decision/at1.out"; FK = Q + "REQUIREMENTS_2026-11-01/FOREST_KILL_AUDIT.md"
# (fragment in the summary, file, literal in that file)
L = [
 # header and section 1
 ("PAPER67 v1.0, DOI 10.5281/zenodo.23883741", P + "PAPER67_galaxy_law_and_what_it_leaves_2026.zenodo.json", "\"doi\": \"10.5281/zenodo.23883741\""), ("it waits on one running search", B + "README.md", "## Unfinished, running"),
 ("canonical 9.3603e-11", Q + "THEORY_STATEMENT_2026-10-26.md", "9.3603"), ("alternative 1.1312e-10", Q + "THEORY_STATEMENT_2026-10-26.md", "1.1312"),
 ("Δχ² 5.34 against 63.90", KF, "1.0421   0.9680     5.34     2.31     0.53"), ("Δχ² 5.34 against 63.90", KF, "0.9361   0.8696    63.90     7.99     1.82"),
 ("Of 550 derivation or selection attempts", KCL + "kappa_campaign_lee.out", "derivation/selection attempts 550"), ("exactly c/√(Gρ), that no field equation on record supplies (KC1)", KCL + "KAPPA_CLOSURE_2026-11-03.md", "length exactly c/sqrt(G rho). No field equation in the record does that."),
 ("Telling ½ from 0.461 needs a₀ to 2.8 %", K03, "kappa = sqrt(8 pi/3)/(2 pi) = 0.4607"), ("Telling ½ from 0.461 needs a₀ to 2.8 %", K03, "P1: 3 sigma separation needs sigma(a0)/a0 <= 2.8%"), ("floor is 9.47 %", K03, "corpus BTFR floor 9.47%"),
 # section 1 table
 ("0.0541, 0.52 (alt 0.44, under the 0.50-0.80 line)", FG1, "U 0.52/0.52, rms 0.0541/0.0541"), ("0.0541, 0.52 (alt 0.44, under the 0.50-0.80 line)", FG1, "U 0.44/0.44, rms 0.0537/0.0537"), ("0.0541, 0.52 (alt 0.44, under the 0.50-0.80 line)", UL1, "The 0.50-0.80 line isn't moved"),
 ("passes 1 in-prior cell (LW1)", LW, "form R PASS, 1 in-prior cell"), ("no smoothing-length rule survives the 3D field (CZ5)", Z5 + "README.md", "No filter form on record survives"),
 ("| Tilt with speed | +0.02 |", FG1, "+0.02/+0.02"), ("E −0.593, Z −7.9", FG1, "E -0.593 (Z -7.9)"), ("| LITTLE THINGS, median E | −0.025 |", FG1, "-0.025/-0.025"),
 ("Z up to +5.22, +6.76 with the external field", FG1, "MW ultra-faint +5.22"), ("Z up to +5.22, +6.76 with the external field", LW, "+1.30 (+6.76)"), ("AQUAL predicts −0.76 per dex (LW1)", LW, "predicts -0.76"),
 ("| 63 groups | Z +0.31 |", FG1, "Z +0.31"), ("Stellar masses, 60-150 km/s", UL1, "the 60-150 excess"), ("Υ 0.62, 0.65 against GSWLC 0.277, 0.304", UL1, "| law canonical | 0.62 | 0.65 |"), ("Υ 0.62, 0.65 against GSWLC 0.277, 0.304", UL1, "| GSWLC (W1 chain) | 0.277 | 0.304 |"),
 ("−0.016 ± 0.061, flat", HS1, "**−0.016**"), ("−0.016 ± 0.061, flat", HS1, "**±0.061"), ("A 1.91 ± 0.12 at 0.5-1.2 Mpc", C687, "**1.91 ± 0.12**"), ("A 1.91 ± 0.12 at 0.5-1.2 Mpc", REQ, "A 1.91 ± 0.12 at 0.5–1.2 Mpc"),
 ("10 of 15, G-OUT-M3 +4.76, joint p 3e-8 (LW1)", LW, "10 of 15 at both f*"), ("10 of 15, G-OUT-M3 +4.76, joint p 3e-8 (LW1)", LW, "+4.76, +4.26"), ("10 of 15, G-OUT-M3 +4.76, joint p 3e-8 (LW1)", LW, "65.0, 3e-8"),
 ("M_HSE / M_law 2.93, +0.467 dex (LW1)", LW, "**2.93** | 2.72"), ("M_HSE / M_law 2.93, +0.467 dex (LW1)", LW, "+0.467, 0.476"), ("2.23 with 0.12 dex off M_HSE", LW, "factors 2.23, 2.06"),
 ("data +0.0887 dex above the law inside 0.3 Mpc", LE + "le1_real.out", "mean log10(Y/model) +0.0887 +- 0.0132  z +6.69"), ("data +0.0887 dex above the law inside 0.3 Mpc", LE + "README.md", "R ≤ 0.3 Mpc"),
 ("under every estimator on record (LE1)", LE + "le1_verdict.out", "law single swaps crossing |Z| <= 2: {\"canonical\": [], \"alt\": []}"), ("the measured kSZ gas doesn't close it (CW6)", W6 + "cw6_verdict.out", "P1    GAP UNCHANGED"),
 ("round rule r 1.239 against 0.90-1.10 (LW1)", LW, "r 1.239"), ("round rule r 1.239 against 0.90-1.10 (LW1)", FG1, "neither in 0.90-1.10"), ("slope 0.47 against 0.90 ± 0.21", C687, "s = 0.90 ± 0.21"), ("slope 0.47 against 0.90 ± 0.21", C687, "the law's s = 0.47 and Newton's 0.84"),
 ("Cassini Q₂ fails by 2.44-4.59 × the 2σ line", P + "PAPER58_doors_push_2026.tex", "2.44--4.59$\\times$"), ("no unscreened action class passes (AX1)", AX + "README.md", "NO UNSCREENED ACTION GIVES THE LAW AND PASSES THE SOLAR SYSTEM"),
 ("from about 1.24 to 1.88 (OD1, NOT SEPARATED)", OD1, "median 1.24"), ("from about 1.24 to 1.88 (OD1, NOT SEPARATED)", OD1, "median 1.88"), ("from about 1.24 to 1.88 (OD1, NOT SEPARATED)", OD1, "NOT SEPARATED [JEANS-DEPENDENT]"),
 # section 2
 ("289 match, 6 close, 0 disagree of 295", LED, "295 items, 289 MATCH, 6"), ("289 match, 6 close, 0 disagree of 295", LED, "289 MATCH, 6 CLOSE, 0 DISAGREE"), ("retired the sector on 2026-11-01", Q + "OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md", "# Owner decision, 2026-11-01: route E's cold sector is retired"),
 ("T ≈ 10^12.3 M☉", Q + "OWNER_DECISION_2026-11-01_T_ONLY.md", "near 10^12.3 M☉"), ("HM1 printed NO VERDICT as frozen", Q + "HM1_honest_model/README.md", "NO VERDICT AS FROZEN"), ("moves no key by over 0.001", LED, "moves no key by over 0.001"),
 ("at +0.111 dex the native rule reaches 15 of 15", LED, "+0.111 ZN4 reaches 15 of 15"), ("against a measured +0.005 ± 0.017", LED, "+0.005 ± 0.017"), ("each candidate still fails at least two lines on each reading run (DA1)", Q + "DA1_definition_audit/README.md", "VERDICT MOVES, PARTLY AUDITED"),
 # section 3
 ("Spirals at 150-250 km/s", LED, "**Spirals, 150–250 km/s.**"), ("f_Q 0.872 [0.54, 1.07] (LC1)", REQ, "f_Q 0.872 [0.54, 1.07]"), ("0.946 [0.78, 1.08]", LED, "PZ1 0.946 [0.78, 1.08]"), ("f_B 0.753 [0.729, 0.777]", LED, "f_B 0.753 [0.729, 0.777]"),
 ("f 1.019 (DR8, one mass, isolated)", Q + "DR8_pressure_core_response/README.md", "| 1.019 [0.965, 1.134] |"), ("net f about 0-0.2", LED, "needs net f about 0–0.2"), ("six of 75 cells, three fitted numbers", REQ, "six of 75 cells"),
 ("G-OUT-M3 reads 1.56 against 1.04, Z +4.41", REQ, "G-OUT-M3 1.56 against 1.04, Z +4.41"), ("about +3.0 to +3.5 with systematics", FG1, "Z_tot +3.03 to +3.51"), ("3-11 % of +21 to +27 %", LED, "3–11 % against +21 to +27 %"),
 ("takes keys from 12 to 10 and X-COP from pass to fail (HM1)", Q + "HM1_honest_model/README.md", "keys 12 to 10, X-COP from pass to fail"),
 ("from 12 to 14 of 15 keys with X-COP passing", FR, "| 12, 12 |"), ("G-OUT-M3 +3.48, +3.09", FR, "**+3.48, +3.09**"), ("NOT RETENTION, by one cell", FR, "NOT RETENTION"),
 ("0.216 dex below that line, −4.4σ", F3, "**-0.216 (-4.4 sigma)**"), ("4 of 15, G-OUT-M3 −2.54", F3, "4 of 15 keys"), ("4 of 15, G-OUT-M3 −2.54", F3, "**-2.54, -2.70**"),
 ("near 8 × the gas at 0.2-0.5 R500 and 5 × at 0.5-1 R500", LM, "near 8 times at 0.2-0.5 R500 and 5 times at 0.5-1 R500"), ("picked from 31 looks", LM, "31 looks"), ("about 1.7 × higher", GM, "about 1.7 times higher"), ("GM1's label is NOT", GM, "**NOT**"),
 ("Density term: SPARC BREAKS", LED, "SPARC BREAKS"), ("Phase-space cap: BITES, FAILS", LED, "BITES, FAILS"), ("Barotropic halo: MOVES, FAILS", LED, "MOVES, FAILS"), ("Fresh hunt, 19 routes", LED, "fresh hunt, 19 routes"), ("Derived T: LOCATED, NOT DERIVED", LED, "T LOCATED, NOT DERIVED"),
 ("c_s² < 0 at all 14 grid z_on", Q + "BOLTZ1_covariant_closure/README.md", "at all 14 grid z_on"), ("Υ 0.45/0.46 against Blumenthal's 0.36/0.37", AR, "| **0.45/0.46** | 0.0652 | **+0.22/+0.23**"), ("Υ 0.45/0.46 against Blumenthal's 0.36/0.37", AR, "| Blumenthal, MONO-INV | 0.36/0.37 |"),
 ("tilt +0.22/+0.23", AR, "**+0.22/+0.23**"), ("(2.8e-5 against 1e-6)", AR, "preds 2.8e-5, line 1e-6"), ("MOVES AND FAILS", AR, "**Label: MOVES AND FAILS"),
 # section 4 table and text
 ("| 0.0541 | 0.0682 / 0.0694 |", REQ, "0.0682 / 0.0694"), ("| −0.016 | −0.173 |", REQ, "−0.173 ± 0.064"), ("| 0.52, alt 0.44 | 0.75, running 1.20 to 0.57 |", REQ, "running 1.20 down to 0.57"), ("needs f ≤ 0.2, measured 0.872", REQ, "f_Q 0.872 [0.54, 1.07]"),
 ("ultra-faints still +5.08 (UX4)", Q + "UX4_dwarf_failures/README.md", "**0.03**, Z +5.08"), ("filters don't lift them (CZ5)", Z5 + "cz5.out", "plain3 17/24, R2 17/24"), ("+0.138; 0 of 5 classes", REQ, "+0.138 / +0.132; **0 of 5**"), ("| −0.593 | −0.474 |", REQ, "−0.474 (−6.3)"),
 ("INFEASIBLE in AQUAL and QUMOND", LW, "**INFEASIBLE**, 0 cells"), ("INFEASIBLE in AQUAL and QUMOND", Q + "UX5_mw_stellar_mass/README.md", "K_z FAILURE SURVIVES"), ("asks 4e10 M☉ inside R₀", REQ, "about 4e10 M☉"),
 ("0.09 dex short inside 0.3 Mpc (LE1, CW6)", LE + "le1_real.out", "+0.0887 +- 0.0132"), ("Δχ² +366.0", Q + "KN1_kids_native_halos/README.md", "**+366.0**"), ("| A 1.91 | G-IN −0.49, G-MID +2.17 |", REQ, "G-IN −0.49, −0.50; G-MID-T3 +2.17"),
 ("G-OUT-M3 +4.76; slope 0.47 against 0.90 | G-OUT-M3 +4.41", REQ, "G-OUT-M3 1.56 against 1.04, Z +4.41"), ("z_on in [3e4, 1e6]", Q + "RF5_growth_native_yardstick/README.md", "z_on ∈ [3e4, 1e6]"), ("unscreened classes fail Q₂ (AX1)", AX + "README.md", "Every class whose static limit is AQUAL or QUMOND with g²/(g + a0) fails Cassini Q2"),
 ("about 0.8 of native on SPARC to 1.22-1.80 on clusters", REQ, "about 0.8 of native on SPARC"), ("about 0.8 of native on SPARC to 1.22-1.80 on clusters", REQ, "1.22–1.80"),
 ("A 5-11 eV fermion", FK, "5–11 eV"), ("its forest kill isn't on the current footing", FK, "falls 1000–5000 × short"), ("lifted the rule for one experiment lane only, which adopts nothing", HF + "README.md", "The owner's lift of the no-particle rule covers this lane only; running it adopts nothing."),
 ("fails the early universe at 5 of 6 masses", HF + "README.md", "FAILS GATE 1 AT 5 OF 6 m, 1 UNDETERMINED"), ("best plik 1432.4 at 11.8 eV", HF + "hf1_g1.out", "11.8  0.13119  1.012  0.694  0.322   1432.4"), ("with the sixth unconverged", HF + "hf1_g1.out", "UNDETERMINED (unconverged)"),
 ("X-COP (+0.159)", HF + "hf1_g23_RUN.out", "X-COP canonical: all mean +0.159 rms 0.251 FAIL"), ("the keys (3 of 15)", HF + "hf1_g23_RUN.out", "Keys canonical, f* 0.034, gas +0.005: 3 of 15"), ("the groups (Z −5.90) (HF1)", HF + "hf1_g23_RUN.out", "groups Z -5.90 BELOW LAW"),
 ("at most 2-4 km/s today", VW + "vw1_b.out", "S-S_min 22.3 conv True PASS"), ("at most 2-4 km/s today", VW + "vw1_b.out", "S-S_min 91.8 conv True FAIL ['S']"), ("between 6.72 and 14.9", VW + "vw1_a2.out", "v0 6.72 km/s; FAIL"), ("between 6.72 and 14.9", VW + "vw1_a2.out", "v0 14.92 km/s; PASS"),
 ("rests on the Υ floor of 0.50 (VW1)", VW + "README.md", "resting on the Υ floor of 0.50"),
 # covariant attempts
 ("recorded with α₁ = −2(K_B + 2)", "STANDING.md", "α₁ = −2(K_B+2)"), ("α₁ = α₂ = 0 at G = G̃ (AS3)", A3, "alpha_1 = alpha_2 = 0, for every K_B"), ("loses the law for moving systems", A3, "v9 then loses the law for moving systems"),
 ("μ_K ≤ 14.8 h/Mpc sits 24-172 × below", V3, "μ_K ≤ 14.8 h/Mpc"), ("μ_K ≤ 14.8 h/Mpc sits 24-172 × below", V3, "gap of 24–172×"), ("ill-posed where the aether twists", V3, "v4 is ILL-POSED wherever the aether twists"), ("runs away on FRW", V3, "v4 RUNS AWAY on FRW"),
 ("1.69-5.18 × the 2σ bound", AX + "v3s/ax1_v3s.out", "canonical|law            QUMOND [1.694,"), ("1.69-5.18 × the 2σ bound", AX + "v3s/ax1_v3s.out", "AQUAL(E2) [2.859, 3.898, 4.464, 5.181]"),
 ("fail on gravitational waves, BIMOND's on a source read only in part", AX + "README.md", "die on GW propagation"), ("fail on gravitational waves, BIMOND's on a source read only in part", AX + "README.md", "their argument was not read"),
 ("cleanly once a high-precision rerun cleared its one failed check (C6P)", CP + "c6p_cassini_hp.out", "CHECKS 9/9 PASS"), ("cleanly once a high-precision rerun cleared its one failed check (C6P)", CP + "c6p_cassini_hp.out", "LABELS: canonical PASS; alt PASS"),
 ("at least 4.8e7 inside the bound", CP + "c6p_cassini_hp.out", "Hees margin >= 4.849e+07"), ("a₀ enters by hand in every class", AX + "README.md", "**by hand in every class.**"), ("v3s's verdict stands", CP + "README.md", "The 10-24 v3s verdict stands"),
 # section 5
 ("public 2026-11-06 02:42:31 UTC", LED, "2026-11-06 02:42:31 UTC"), ("PAPER66 v1.4, DOI 10.5281/zenodo.23958256", P + "PAPER66_v1.4.zenodo.json", "\"doi\": \"10.5281/zenodo.23958256\""), ("2026-11-28 by earlier metadata", LED, "2026-11-28 by earlier metadata"),
 ("at or below 0.51σ", Q + "EXTERNAL_BRIEF_OUTLINE_2026-11-01.md", "every n = 1 vs n = 2 pair at or below 0.51σ"), ("its own test beyond 50 kAU", "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md", "~50 kAU in a contamination-controlled sample"),
 ("γ_∞ 1.149 (alt 1.208)", W1 + "cw1.out", "PQ    gamma_inf 1.1494 (spread 0.0269)"), ("γ_∞ 1.149 (alt 1.208)", W1 + "cw1.out", "PQ    gamma_inf 1.2081 (spread 0.0067)"),
 ("a₀ point at z ≈ 2.5 to about 0.10 dex", C689, "one clean deep-MOND a0 point at z ≈ 2.5"), ("a₀ point at z ≈ 2.5 to about 0.10 dex", C689, "≈ 0.10 dex"), ("reaches 0.4-0.5 dex", C689, "best 0.4–0.5 dex"),
 ("under 0.055-0.084 dex (AT1)", AT, "1.0   0.2272   0.0068   0.0511   0.0546"), ("under 0.055-0.084 dex (AT1)", AT, "2.33  0.4534   0.0061   0.1246   0.0843"),
 # section 6
 ("5.51 bits at 5 %, FDR-DEAD", CG, "5.51 bits at 5 %, under its 10 bit line. FDR-DEAD"), ("at SPARC's 16.6 % precision 92.7 %", CG, "| 16.6 % | 0.927 |"), ("at SPARC's 16.6 % precision 92.7 %", CG, "92.7 % of scrambled scalars get a decomposition as simple"),
 ("reaches 14 of 15 keys on canonical, 10 on alt", U3, "canonical keys from 10 to 14 of 15"), ("reaches 14 of 15 keys on canonical, 10 on alt", U3, "alt reads 10"), ("with no k giving 15 (UX3, CU1)", CU, "so no k passes all 15"), ("dead on the Bullet (UX6)", Q + "UX6_gas_term_bullet/README.md", "All seven readings read DEAD"),
 ("13.3 × the ceiling (alt 18.1)", Z5 + "cz5.out", "[canonical] Cassini 13.3 x ceiling (FAIL)"), ("13.3 × the ceiling (alt 18.1)", Z5 + "cz5.out", "[alt] Cassini 18.11 x ceiling (FAIL)"), ("at the saddle where the Sun's and the Galaxy's pulls cancel (CZ5)", Z5 + "README.md", "the Sun's pull and the Galaxy's cancel at a saddle"),
 ("Fixed widths fail Cassini or the planets", W1 + "cw1.out", "K3 [canonical] HALF: Cassini 1.179 x ceiling (CZ2 1.179)"), ("Fixed widths fail Cassini or the planets", "claude_goal_2026_11_03/CZ3_planet_precession_filters/cz3.out", "LABEL [canonical] HALF FAILS PLANETS: Mars, Saturn"),
 ("tidal rules fail the Milky Way once the vertical tide is in", Q + "KT32_tidal_rule_rz_scatter/kt32.out", "LABEL [canonical] rule F: FAILS MW"), ("tidal rules fail the Milky Way once the vertical tide is in", Q + "KT32_tidal_rule_rz_scatter/kt32.out", "LABEL [alt] rule TF: FAILS MW"),
 ("+0.0887 dex (alt +0.0500)", LE + "le1_real.out", "mean log10(Y/model) +0.0500 +- 0.0132  z +3.78"), ("mostly at 200-500 kpc", W6 + "README.md", "The gas sits mostly at 200-500 kpc."), ("4.87σ above the law (CW6)", W6 + "cw6_b21c.out", "red A 1.3060 +- 0.0628 (short, z +4.87"),
 ("(+0.003 dex)", Q + "NP1_nonparametric_rule/np1_real.out", "X +0.003/0.035 P"), ("the 96-row acceptance list rejects it in every cell", Q + "NP1_nonparametric_rule/np1_real.out", "L3 canonical Stage 3: REJECTED"), ("the 96-row acceptance list rejects it in every cell", Q + "RQ3_acceptance_v2/README.md", "Counts over 96 rows"),
 ("it still fails IC 1613 and the Υ rows (NP2)", Q + "NP2_admissible_rule/np2_real_L3.out", "| IN HULL (IC1613 1.000)"), ("No non-local variable on record resolves those rows (NV1, NV2)", Q + "NV1_nonlocal_variable/nv1_real.out", "LANE canonical: NO SINGLE NON-LOCAL VARIABLE ON RECORD RESOLVES"), ("No non-local variable on record resolves those rows (NV1, NV2)", Q + "NV2_external_field_xcop_lenses/nv2_real.out", "LANE alt: NO SINGLE NON-LOCAL VARIABLE ON RECORD RESOLVES"),
 ("7.5e11 expressions, read NO HIT", BF + "README.md", "| **L4 real** (A1, gates unchanged) | 7.5e11 | 17,692 | **0** |"), ("7.5e11 expressions, read NO HIT", BF + "bf1_read_real_L4.out", "Stage 1 distinct 0; gate 3 0; gate 4 0"), ("as their scrambled control does (BF1)", BF + "README.md", "| L4 scrambled control | 7.5e11 | 1,283 | 0 |"),
 ("reads NO HIT at level L1", B + "bk2_read_L1_canonical_real.out", "'train_line': 0, 'train_err': 0"), ("1.01 and 1.02 against the real 1.08 and 1.07 (BK2)", B + "bk2_read_L1_canonical_control.out", "Zl 1.01 cass False X +0.003,0.101"), ("1.01 and 1.02 against the real 1.08 and 1.07 (BK2)", B + "bk2_read_L1_alt_control.out", "Zl 1.02 cass True X -0.003,0.102"),
 ("1.01 and 1.02 against the real 1.08 and 1.07 (BK2)", B + "bk2_read_L1_canonical_real.out", "Zl 1.08 cass True X +0.008,0.104"), ("1.01 and 1.02 against the real 1.08 and 1.07 (BK2)", B + "bk2_read_L1_alt_real.out", "Zl 1.07 cass True X +0.012,0.097"), ("its level L2 is still running", B + "README.md", "## Unfinished, running"),
 ("passes the early universe in 5 of 10 cells (DF2)", Q + "DF2_dark_fluid_requirement/df2.out", "P label: DENSITY KEY PASSES GATE 1 AT ['P_G1.667_s30', 'P_G1.667_s100', 'P_G1.000_s30', 'P_G1.000_s100', 'P_G0.667_s30']"), ("passes the early universe in 5 of 10 cells (DF2)", Q + "DF2_dark_fluid_requirement/README.md", "five of ten barotrope cells"),
 ("none of those passes discs, clusters or the Bullet (DF3)", Q + "DF3_fluid_next_gates/df3g.out", "NO GATE; 4 of the other four cells read the same"), ("doesn't collapse on any one variable (RS1)", Q + "RS1_required_source/README.md", "The required source doesn't collapse on any one variable"),
 ("from 1e-25 eV up and fails the keys, 1 of 15 (WF1)", Q + "WF1_wave_pressure_field/wf1_g1.out", "FIT S-Smin 17.1 plik 584.4 s8 0.721 wf 0.1199 conv True PASS"), ("from 1e-25 eV up and fails the keys, 1 of 15 (WF1)", Q + "WF1_wave_pressure_field/wf1_RUN_m1e-25_s1.out", "Keys canonical, f* 0.034, gas +0.005: 1 of 15"),
 ("withdrew its first headline after a centre-cell error", N1 + "README.md", "This lane's headline and fold table don't stand."), ("61 of 68 rows fold first, 5 never collapse, 2 oscillate, none settles", N1 + "README_V3.md", "61 of 68 rows fold first, 5 never collapse, 2 reach z = 0 oscillating; none settles"),
 ("A 3D engine (AN2) reads NO VERDICT too", N2 + "README.md", "# AN2_aest_3d_fold: NO VERDICT, numbers only."), ("5-16 % before AN1's sphere (SG, P160)", N2 + "diag_a2/SHAPE_GRID_RESULT.md", "B 4.44 (−15.9 %)"), ("5-16 % before AN1's sphere (SG, P160)", N2 + "diag_a2/SHAPE_GRID_RESULT.md", "A 4.46 vs 4.701 (−5.1 %)"),
 ("a₁ = 1.59 ± 0.10 in units of 1e-10 m/s², 95 % intervals", "data_assembly/arxiv_tables/musedark_II_III/musedarkIII_stated_results_NOT_A_TABLE.csv", "1.59,0.10,0.10,95% CI (stated)"), ("not measured galaxy values", KCL + "KAPPA_CLOSURE_2026-11-03.md", "not measured galaxy a₀ values"),
]
F = 0; n = 0; caught = 0
def rd(f):
    return open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read()
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i] in "0123456789": return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "!"
for frag, f, lit in L:
    n += 1
    if MUT:
        caught += bump(lit) not in rd(f) or frag not in MD
        continue
    a = frag in MD; b = lit in rd(f)
    if not (a and b): F += 1; print(f"  FAIL {'MD ' if not a else ''}{'SRC ' if not b else ''}{frag!r} | {f} | {lit!r}")
def an1(want):  # AN1 v3 label counts recomputed from its row file
    rows = rd(N1 + "an1_v3_rows.out").splitlines()
    return [sum(1 for r in rows if f" {lab} " in r) for lab in ("FOLD FIRST", "NO COLLAPSE", "OSCILLATING")] + [len(rows)] == want
if MUT:
    cc = not an1([62, 5, 2, 68])
    print(f"MUTATE: {caught} of {n} perturbed literals not found; recomputed AN1 count with a perturbed expectation fails: {cc}")
    for frag, f, lit in L:
        if bump(lit) in rd(f) and frag in MD: print("  survivor", repr(lit), f)
    sys.exit(0 if caught >= 0.8 * n and cc else 1)
n += 1
if not an1([61, 5, 2, 68]): F += 1; print("  FAIL recomputed AN1 counts")
# scorecard against FG1's verdict table and the ledger's fail lists (the same rows as PAPER67's Table 2)
rows = {"C1 native collapse rule": "PFFPFPFFFFF", "C2 C1 + Blumenthal response": "FFFPFFF-FP-", "C3 basin split at T ≈ 10^12.3 M☉": "PPPPFPPPF-F", "C4 law alone (X, DM from LW1)": "PPPPFFPFFFF", "C5 native + measured response (HM1)": "FFFFFFFFPPF"}
names = ["S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC"]; fg = rd(FG1)
led = {"C1": "Tl, LT, K, Ln, Dw, MW, DM, IC", "C2": "S, Tl, LT, K, X, Ln, MW", "C3": "K, MW, IC"}
for k, v in rows.items():
    n += 1
    m = re.search(r"^\| " + re.escape(k) + r" \|(.*)\|\s*$", MD, flags=re.M)
    got = "".join("-" if c.strip() == "–" else c.strip() for c in m.group(1).split("|")) if m else ""
    fails = ", ".join(a for a, c in zip(names, got) if c == "F")
    if got != v or (k[:2] in led and (fails != led[k[:2]] or fails not in fg)): F += 1; print("  FAIL scorecard", k, got, fails)
# naming and wording rules
low = MD.lower()
for bad in ("/users/", "carl", "zimmerman", "kappa derived", "κ derived", "measured flat", "cdm-like"):
    n += 1
    if bad in low: F += 1; print("  FAIL found", bad)
n += 1
if len(re.findall(r"theory closed", low)) != len(re.findall(r"not theory closed", low)): F += 1; print("  FAIL 'theory closed' outside 'not theory closed'")
n += 1
if len(re.findall(r"data favour", low)) != len(re.findall(r"nothing here says the data favour", low)): F += 1; print("  FAIL 'data favour' outside the disclaimer")
n += 1
if len(re.findall(r"cold dark matter", low)) != len(re.findall(r"linear behaviour of cold dark matter", low)): F += 1; print("  FAIL naming: cold dark matter")
for need in ("**draft for the owner to read; not sent.**", "κ = ½ is fitted", "not theory closed", "nothing here says the data favour this framework", "never proposed as a particle", "limbach, psaltis and özel", "not a no-go theorem", "adopts nothing"):
    n += 1
    if need not in low: F += 1; print("  FAIL missing", need)
print(f"{n - F} of {n} checks pass"); print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(1 if F else 0)
