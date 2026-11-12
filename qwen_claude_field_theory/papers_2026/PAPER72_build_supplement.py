#!/usr/bin/env python3
"""Build PAPER72's supplement: every committed file of the lanes the paper cites (KO2, RB1, RB2, CO1, CO2, PD1, PD2, the owner's decision and the re-run record
under closure_2026_11_09/; HE1, ONE1, TPA1, SCS1, FB1, KO3F under fable52_push/), as one zip, with a manifest.
Version 1.1 adds the lanes of 2026-11-10: SCS2, SCS3, MK1, MK2, COL1, FLD1, REL1, SHP1 under fable52_push/ (with MK1's and MK2's Lean
files, which sit in fable_independent_2026/lean_2026/) and the fable52_push/ README that records what its lead checked; TK1, AKD1, LFS1,
CLS1, KL1, KL1R, DG1, NH2, XCV1, GO1 under closure_2026_11_10/, beside the notes THEORY_ASSEMBLED_2026-11-10.md and
MEDIUM_DESIGN_2026-11-10.md (with MEDIUM_DESIGN_check.py and its output) and the re-run record RERUNS_2026-11-10.md; and the single
result file of each older lane that Section 7's survey of media quotes (M5, PH1, IJ1, HF1, TM1 under rebuild_2026_10_22/; QX28, FA3,
WM1) with the owner's retirement record of 2026-11-01; DCN1 (the disc-centre null) under fable52_push/; the note R541 (why 5.41;
not a graded lane) and its lanes R541A to R541E under closure_2026_11_10/; and X38's README, which states route E. BX1 is included.
Version 1.2 adds every lane folded into its Section 8 (closure_2026_11_10/ to closure_2026_11_12/, fable52_push/, hy4_preview_push/,
hy4_push/, toe_2026_11_10/) and the audit files A1 to A4 of reviews/hy4_codex_audit_2026_11_12/.
The shared checkout has diverged from origin (PD1 and PD2 are committed on origin only), so each lane path is taken from whichever
of HEAD and origin/main last committed to it; the manifest records the ref and commit for each. Untracked files are not included
and are listed (unless the same path is committed on the chosen ref); a tracked file modified in the working tree stops the build. Deterministic for given commits (fixed entry dates).
Run: python3 PAPER72_build_supplement.py   (from anywhere inside the repository)
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import hashlib, io, json, os, subprocess, sys, tarfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ZIP = os.path.join(HERE, "PAPER72_supplement_lanes_2026.zip")
MAN = os.path.join(HERE, "PAPER72_supplement_manifest.json")
PATHS = [
 "closure_2026_11_09/KO2_kids_own_field_by_type",
 "closure_2026_11_09/RB1_form_b_hot_systems",
 "closure_2026_11_09/RB2_form_b_hosted_rows",
 "closure_2026_11_09/PD1_phantom_is_dust",
 "closure_2026_11_09/PD2_sheet_captured_phantom_dust",
 "closure_2026_11_09/CO1_form_b_cosmology_computed",
 "closure_2026_11_09/CO2_form_b_amplitude_pinned",
 "closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md",
 "closure_2026_11_09/RERUNS_2026-11-09.md",
 "fable52_push/HE1_held_out_envelope",
 "fable52_push/ONE1_counted_once",
 "fable52_push/TPA1_two_phase_action",
 "fable52_push/SCS1_static_clock_coupled_stability",
 "fable52_push/FB1_form_b_from_the_action",
 "fable52_push/KO3F_spec_veto_power_forecast",
 # version 1.1
 "fable52_push/README.md",
 "fable52_push/SCS2_static_clock_stability_discs",
 "fable52_push/SCS3_external_field_stability",
 "fable52_push/MK1_one_dust_constant",
 "fable52_push/MK2_exponential_dust_term",
 "fable52_push/COL1_clock_collapse",
 "fable52_push/FLD1_fold_reach",
 "fable52_push/REL1_relative_acceleration",
 "fable52_push/SHP1_cold_component_shape",
 "fable_independent_2026/lean_2026/MK1.lean",
 "fable_independent_2026/lean_2026/MK1_MUTATE.lean",
 "fable_independent_2026/lean_2026/MK2.lean",
 "fable_independent_2026/lean_2026/MK2_MUTATE.lean",
 "closure_2026_11_10/TK1_expansion_keyed_dust",
 "closure_2026_11_10/AKD1_acceleration_keyed_dust",
 "closure_2026_11_10/LFS1_leafwise_flux_supply",
 "closure_2026_11_10/CLS1_cluster_state_in_action",
 "closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions",
 "closure_2026_11_10/KL1R_blind_legacy_regrade",
 "closure_2026_11_10/DG1_dwarf_gas_history",
 "closure_2026_11_10/NH2_ngc1052_host_mass",
 "closure_2026_11_10/XCV1_xcop_nonhydrostatic_mass",
 "closure_2026_11_10/GO1_group_outskirts",
 "closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md",
 "closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md",
 "closure_2026_11_10/MEDIUM_DESIGN_check.py",
 "closure_2026_11_10/MEDIUM_DESIGN_check.out",
 "closure_2026_11_10/RERUNS_2026-11-10.md",
 # version 1.1: the older lanes quoted by Section 7's survey of media (their result files only) and the owner's retirement record
 "rebuild_2026_10_22/M5_equilibrium_law/README.md",
 "rebuild_2026_10_22/PH1_two_phase_cold_energy/README.md",
 "rebuild_2026_10_22/IJ1_isothermal_jeans_halos/README.md",
 "rebuild_2026_10_22/HF1_hybrid_fermion/README.md",
 "rebuild_2026_10_22/TM1_tethered_medium/README.md",
 "closure_2026_11_06/QX28_superfluid_two_phase/README.md",
 "closure_2026_11_07/FA3_nonlocal_action_search/RESULT.md",
 "closure_2026_11_09/WM1_warm_component_law_baryons/RESULT.md",
 "rebuild_2026_10_22/OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md",
 # version 1.1, round 2: the disc-centre lane, the note on the 5.41 and its five lanes, and X38's statement of route E
 "fable52_push/DCN1_disc_centre_null",
 "closure_2026_11_10/R541_why_the_cold_share",
 "closure_2026_11_10/R541A_clock_matter_coupling",
 "closure_2026_11_10/R541B_early_symmetry_breaking",
 "closure_2026_11_10/R541C_made_in_inflation",
 "closure_2026_11_10/R541D_baryon_current_cogenesis",
 "closure_2026_11_10/R541E_b_minus_l_variant",
 "closure_2026_11_10/BX1_fixed_amplitude_reference",
 "closure_2026_11_10/DSB1_dwarf_systematics_blind",
 "closure_2026_11_10/PAR1_parent_action_spec",
 "closure_2026_11_10/WV1_wave_dust_split_charge",
 "closure_2026_11_10/SMF1_smooth_frame_parent",
 "rebuild_2026_10_22/X38_a0_surface_density_halos/README.md",
 # version 1.2: every lane folded in after version 1.1, and the four audit files Section 8 quotes
 "closure_2026_11_10/CLS2_what_the_cluster_mass_is",
 "closure_2026_11_10/EDG1_held_edge_layer",
 "closure_2026_11_10/EFN1_external_field_nonlinear",
 "closure_2026_11_10/FRZ1_forest_redistribution_at_z",
 "closure_2026_11_10/FRZ1R_blind_forest_regrade",
 "closure_2026_11_10/FRZ2_forest_a0_of_z",
 "closure_2026_11_10/FZS1_forest_settled_radius",
 "closure_2026_11_10/HLF1_own_halo_list_forest",
 "closure_2026_11_10/SET1_irreversible_settling",
 "closure_2026_11_10/SRH1_settled_radius_history",
 "closure_2026_11_10/SRH1R_blind_lensing_regrade",
 "closure_2026_11_10/VSH1_viscous_shock_settling",
 "closure_2026_11_11/DW1_desi_dr2_mw_mass",
 "closure_2026_11_11/FINAL-12_lean_background",
 "closure_2026_11_11/FINAL15_formation",
 "closure_2026_11_11/FINAL16_kappa_real",
 "closure_2026_11_11/FINAL18_kappa_fold",
 "closure_2026_11_11/FINAL2_epoch",
 "closure_2026_11_11/FINAL4_growth_history",
 "closure_2026_11_11/FINAL6_kappa_formation",
 "closure_2026_11_11/VCC1_sourced_charge_current",
 "closure_2026_11_12/AZ2_flat_a0_lya_ap",
 "closure_2026_11_12/AZ2R_blind_flat_a0_regrade",
 "closure_2026_11_12/CLOSE2_par1_branch_union",
 "closure_2026_11_12/EUC1_eclipse_saturation_ceiling",
 "closure_2026_11_12/EUC2_desi_source_hunt",
 "closure_2026_11_12/EUC4_wide_lenses",
 "closure_2026_11_12/EUC4R_blind_regrade",
 "closure_2026_11_12/EUC5_dynamical_boost",
 "closure_2026_11_12/FINAL7F_formation_reading",
 "closure_2026_11_12/GO2_group_outskirts_desi_groups",
 "closure_2026_11_12/LWB1_lensing_amplitude_crosscheck",
 "closure_2026_11_12/LWB1R_blind_lensing_regrade",
 "closure_2026_11_12/MWG1_hot_halo_gas",
 "closure_2026_11_12/MWJ1_milky_way_joint_window",
 "closure_2026_11_12/NMB1_nimble_curves_vs_line",
 "closure_2026_11_12/OUT4_kappa_window",
 "closure_2026_11_12/PLT1_outer_mass_vs_literature",
 "closure_2026_11_12/U4L1_alma_limit_reading",
 "fable52_push/A0Z1_chi_sector_grade",
 "fable52_push/FRM1_formation_theory",
 "fable52_push/NBC1_neutral_baryon_contact",
 "fable52_push/PIK1_pi_gated_dust",
 "hy4_preview_push/CLOSE-1_DT2",
 "hy4_preview_push/CRACK-1_ufr_external_field",
 "hy4_preview_push/ELA1_elastic_medium",
 "hy4_preview_push/FINAL-1_THEORY_ASSEMBLY",
 "hy4_preview_push/FINAL-7_what_it_is",
 "hy4_preview_push/FINAL-10_lean_stress",
 "hy4_preview_push/FINAL-11_lean_budget",
 "hy4_preview_push/FINAL-14_lean_amount",
 "hy4_preview_push/FINAL-17_kappa_A",
 "hy4_preview_push/FINAL-19_kappa_C",
 "hy4_preview_push/FINAL5_measurement",
 "hy4_preview_push/HY4-1_GAS1_hot_gas_census",
 "hy4_preview_push/OUT-2_kappa_ratelock",
 "hy4_preview_push/OUT3_cosmic_share_fold",
 "hy4_preview_push/OUT3_scale_free_boundary",
 "hy4_preview_push/OUT5_bootstrap_carrier",
 "hy4_push/HY4-2_STR1_anisotropic_stress_lensing",
 "toe_2026_11_10/AKS1_acceleration_keyed_sink",
 "toe_2026_11_10/VSJ1_viscous_shock_joint",
 "toe_2026_11_10/TOE0_gate_battery",
 "toe_2026_11_10/QG1_quantum_health_of_A",
 "toe_2026_11_10/HZ1_uv_completion",
 "toe_2026_11_10/NPJ1_nonperturbative_J",
 "toe_2026_11_10/LSF1_lifshitz_fermion_superfluid",
 "reviews/hy4_codex_audit_2026_11_12/A1_kappa_and_amount.md",
 "reviews/hy4_codex_audit_2026_11_12/A2_medium_and_joint.md",
 "reviews/hy4_codex_audit_2026_11_12/A3_data_and_repairs.md",
 "reviews/hy4_codex_audit_2026_11_12/A4_paper_ledger_lean.md",
]
REFS = ("HEAD", "origin/main")
def git(*a, check=True):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=check).stdout.strip()
def gitb(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, check=True).stdout
dirty = [l for l in git("status", "--porcelain", "--", *PATHS).splitlines() if not l.startswith("??")]
if dirty:
    sys.exit("REFUSING: tracked lane files have uncommitted changes:\n" + "\n".join(dirty))
untracked = sorted(l[3:] for l in git("status", "--porcelain", "--untracked-files=all", "--", *PATHS).splitlines() if l.startswith("??"))
chosen = {}
for p in PATHS:
    best = None
    for ref in REFS:
        c = git("log", "-1", "--format=%ct %H", ref, "--", p, check=False)
        if c and git("ls-tree", "-r", "--name-only", ref, "--", p):
            t, h = c.split()
            if best is None or int(t) > best[0]: best = (int(t), ref, h)
    if best is None:
        sys.exit(f"REFUSING: {p} is committed on neither HEAD nor origin/main")
    chosen[p] = dict(ref=best[1], ref_commit=git("rev-parse", best[1]), last_commit=best[2])
files = {}
for p, c in chosen.items():
    tf = tarfile.open(fileobj=io.BytesIO(gitb("archive", "--format=tar", c["ref"], "--", p)))
    for m in tf.getmembers():
        if m.isfile(): files[m.name] = tf.extractfile(m).read()
names = sorted(files)
bad = [n for n in names if n.startswith("/") or "/Users/" in n]
if bad: sys.exit(f"REFUSING: absolute paths in the archive: {bad[:3]}")
for n in names:                                  # no personal paths inside text files
    if n.endswith((".md", ".py", ".txt", ".out", ".json", ".lean", ".sh")) and b"/Users/" in files[n]:
        sys.exit(f"REFUSING: a home path appears inside {n}")
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        zi = zipfile.ZipInfo(n, date_time=(2026, 11, 9, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        z.writestr(zi, files[n])
untracked = [u for u in untracked if u not in files]   # present in the archive from origin/main
blob = open(ZIP, "rb").read()
lanes = sorted({n.split("/")[1] for n in names if n.count("/") >= 2})
man = dict(paper="PAPER72", git_head=git("rev-parse", "HEAD"), origin_main=git("rev-parse", "origin/main"), sources=chosen,
           count=len(names), zip_bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), lanes=lanes,
           lean=sorted(n for n in names if n.endswith(".lean")), untracked_not_included=untracked, files=names)
json.dump(man, open(MAN, "w"), indent=1)
print(f"supplement: {man['count']} files, {man['zip_bytes'] / 1e6:.2f} MB, sha256 {man['sha256'][:16]}, "
      f"HEAD {man['git_head'][:10]}, origin {man['origin_main'][:10]}")
for p, c in chosen.items(): print(f"  {p}: {c['ref']} (last commit {c['last_commit'][:10]})")
print("lanes:", ", ".join(lanes))
if untracked: print(f"untracked, not included ({len(untracked)}):", ", ".join(untracked))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
