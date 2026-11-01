#!/usr/bin/env python3
"""Every number in REQUIREMENTS_LIST.md and FOREST_KILL_AUDIT.md is read from a file on record. This checks that each literal is there.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I check_requirements.py      (REQ_MUTATE=1 twin: one literal changed, must exit 1)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); Q = os.path.dirname(RB)
MUT = os.environ.get("REQ_MUTATE", "0") == "1"
P = "qwen_claude_field_theory/closure_2026/condensate_pincer_2026/"
L = [
    ("rebuild_2026_10_22/FG1_final_grade/x62_x43copy_law_a2.out", "rms 0.0541, median U 0.52, line PASS"),
    ("rebuild_2026_10_22/FG1_final_grade/x62_x43copy_law_a2.out", "median U 0.44, line FAIL"),
    ("rebuild_2026_10_22/ND1_native_dwarfs/README.md", "0.0682 / 0.0694"),
    ("rebuild_2026_10_22/ND1_native_dwarfs/README.md", "+0.138 / +0.132"),
    ("rebuild_2026_10_22/ND1_native_dwarfs/README.md", "−0.173 ± 0.064"),
    ("rebuild_2026_10_22/ND1_native_dwarfs/README.md", "| −0.025 |"),
    ("rebuild_2026_10_22/ND1_native_dwarfs/README.md", "−0.474 (−6.3)"),
    ("rebuild_2026_10_22/HS1_hsb_lsb_residual_slope/README.md", "**−0.016**"),
    ("rebuild_2026_10_22/HS1_hsb_lsb_residual_slope/README.md", "±0.061"),
    ("rebuild_2026_10_22/ARGON_BRIEF_2026-11-01_LATE.md", "Υ 0.75/0.76"),
    ("rebuild_2026_10_22/ARGON_BRIEF_2026-11-01_LATE.md", "1.20, 1.18, 0.90, 0.57"),
    ("rebuild_2026_10_22/ARGON_BRIEF_2026-11-01_LATE.md", "Υ ≥ 0.50 means tilt ≥ +0.32"),
    ("rebuild_2026_10_22/ARGON_BRIEF_2026-11-01_LATE.md", "≤ 0.15 means Υ ≤ 0.32"),
    ("rebuild_2026_10_22/RM2_mass_falling_response/README.md", "Six of 75 cells"),
    ("rebuild_2026_10_22/RM2_mass_falling_response/README.md", "f_hi 0 or 0.2"),
    ("rebuild_2026_10_22/RM2_mass_falling_response/README.md", "12 of 15"),
    ("rebuild_2026_10_22/LC1_live_contraction/README.md", "f_Q 0.872 [0.54, 1.07]"),
    ("rebuild_2026_10_22/LC1_live_contraction/README.md", "R_live 2.154"),
    ("rebuild_2026_10_22/RG1_native_n_regrade/README.md", "**0 of 5**"),
    ("rebuild_2026_10_22/RG1_native_n_regrade/README.md", "+0.758 (+6.63)"),
    ("rebuild_2026_10_22/RF2_ic1613_inclination_footing/README.md", "−0.5928"),
    ("rebuild_2026_10_22/X5_mw_joint_baryons/README.md", "+4.7 to +6.6σ"),
    ("rebuild_2026_10_22/RF1_mw_halo_free_baryons/README.md", "canonical OS1 0 of 625 cells"),
    ("rebuild_2026_10_22/UR3_direct_weighing/README.md", "about 4e10 M☉"),
    ("rebuild_2026_10_22/KN1_kids_native_halos/README.md", "+366.0"),
    ("rebuild_2026_10_22/BL1_blue_lens_halo_mass/README.md", "1.053 ± 0.095"),
    ("rebuild_2026_10_22/BL1_blue_lens_halo_mass/README.md", "1.649 ± 0.083"),
    ("rebuild_2026_10_22/BL1_blue_lens_halo_mass/README.md", "0.878"),
    ("rebuild_2026_10_22/BL1_blue_lens_halo_mass/README.md", "1.313"),
    ("campaign_fresh_gravity/CFG687_erass1_shear_stack/README.md", "1.91 ± 0.12"),
    ("campaign_fresh_gravity/CFG687_erass1_shear_stack/README.md", "1.01 ± 0.09"),
    ("campaign_fresh_gravity/CFG687_erass1_shear_stack/README.md", "s = 0.90 ± 0.21"),
    ("campaign_fresh_gravity/CFG687_erass1_shear_stack/README.md", "s = 0.47"),
    ("rebuild_2026_10_22/RF5_growth_native_yardstick/README.md", "z_on ∈ [3e4, 1e6]"),
    ("rebuild_2026_10_22/X56_law_floor_structure/README.md", "**0.47**"),
    ("rebuild_2026_10_22/X56_law_floor_structure/README.md", "G-OUT-all OVER (−2.38)"),
    ("rebuild_2026_10_22/X56_law_floor_structure/README.md", "G-OUT-M3 UNDER (+2.23)"),
    ("rebuild_2026_10_22/THEORY_STATEMENT_2026-10-26.md", "retain/exclude/retain is non-monotone in mass"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/README.md", "1.22–1.80"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/README.md", "below 0.96"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/INVENTORY_2026-11-01.md", "M3 +2.39 / +2.10"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/INVENTORY_2026-11-01.md", "X62 environment: nothing passes at any c_f"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/INVENTORY_2026-11-01.md", "G-IN-all 2.10/2.99 (−0.49), G-IN-Mall 2.47/3.04 (−0.50)"),
    ("rebuild_2026_10_22/SL2_inverse_core_ratio/INVENTORY_2026-11-01.md", "G-MID-T3 2.27/1.68 (+2.17)"),
    ("rebuild_2026_10_22/BOLTZ1_covariant_closure/README.md", "forest 424.0/327"),
    ("rebuild_2026_10_22/P1D4_m6_native_3d_forest/README.md", "1864.2/690"),
    ("rebuild_2026_10_22/NU1_cluster_gap_sources/README.md", "Z −6.9 to −7.8"),
    ("STANDING.md", "the 5–11 eV sterile-fermion corner dies on the forest"),
    (P + "mond_sheet_nbody_forest_gate_2026.out", "falls 1000-5000x short"),
    (P + "mond_sheet_nbody_forest_gate_2026.py", "dark component smooth (it contributes to H(a) only)"),
    (P + "mond_sheet_nbody_forest_gate_2026.py", "OM_DM = 0.1200/h**2"),
    (P + "mond_sheet_nbody_forest_gate_2026.py", "(0.811/math.sqrt"),
    (P + "mond_sheet_nbody_forest_gate_2026.out", "these are not the hybrid's large scales"),
    (P + "ballistic_survivor_window_2026.out", "dead if thermal (N_eff)"),
    (P + "ballistic_survivor_window_2026.out", "overproduces massive clusters"),
    (P + "dark_sector_debug_2026.out", "FAIL: forest, sheet N-body + Hubble floor"),
]
if MUT:
    L[0] = (L[0][0], "rms 0.0999, median U 0.52, line PASS")
bad = []
for f, s in L:
    txt = open(os.path.join(Q, f), encoding="utf-8").read()
    if s not in txt:
        bad.append((f, s)); print("MISSING", f, repr(s))
# ZN4's key is read from its JSON, not a README
zn = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_results.json")))["runs"]["f* 0.034, gas +0.005"]["cells"]["h0672"]["G-OUT-M3"]
ok = abs(zn["meas"] - 1.56) < 0.005 and abs(zn["pred"] - 1.04) < 0.005 and abs(zn["Z"] - 4.41) < 0.005
if not ok:
    bad.append(("zn4_results.json", str(zn))); print("MISMATCH ZN4", zn)
print(f"{len(L) + 1 - len(bad)} of {len(L) + 1} literals found" + (" [MUTATE]" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(1 if bad else 0)
