#!/usr/bin/env python3
"""CJ1 audit: every frozen word quoted in SCORECARD.md must appear verbatim in the committed file it is cited from.

Reads cited files with `git show HEAD:<path>` (paths relative to the repository root). Text is compared after removing
markdown bold markers and collapsing whitespace, so line wraps do not matter. Also checks: each quoted word appears in
SCORECARD.md; every scorecard row has a check; the stated word counts match the table;
no home paths and no banned names in this folder's files; each file ends with the required line.
Exit 0 only if every check passes. Run: python3 -I -B cj1_audit.py
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      check=True).stdout.strip()
HERE = "closure_2026_11_13/CJ1_candidate_completion"
C13 = "closure_2026_11_13/"
C12 = "closure_2026_11_12/"
C11 = "closure_2026_11_11/"
C10 = "closure_2026_11_10/"
C09 = "closure_2026_11_09/"
TEX = "qwen_claude_field_theory/papers_2026/PAPER72_law_with_cold_dark_energy_counted_once_2026.tex"

# (scorecard row, committed path, quoted word)
CHECKS = [
    (1, C09 + "PD1_phantom_is_dust/RESULT.md", "PASS: rms 0.0563 (line 0.0660)"),
    (1, C13 + "JNT2_crossing_speed_joint/RESULT.md", "EQUAL TO THE LAW (0 above)"),
    (1, C13 + "JNT2R_blind_crossing_speed_joint/RESULT_BLIND.md", "175 / 175 by (a), L"),
    (2, TEX, "Solar System & pass, carried & PD1"),
    (3, "fable52_push/SHP1_cold_component_shape/RESULT.md", "THE LAW'S SHAPE ON ROTATION CURVES"),
    (4, C13 + "JNT1_regime_split_joint_on_data/RESULT.md", "NO VERDICT / JOINT COMPLETE ON POWERED ROWS [1.25, 2]"),
    (4, C13 + "JNT1R_blind_massive_spiral_regrade/RESULT_BLIND.md",
     "REFERENCE FAILS AT THE RECORD SHARE [L2 shape; L3 scatter], FRAGILE"),
    (4, C13 + "JNT1R_blind_massive_spiral_regrade/RESULT_BLIND.md", "THE LAW FITS, FRAGILE"),
    (4, C13 + "JNT1R_blind_massive_spiral_regrade/RESULT.md", "THE LAW FAILS [L2 shape], FRAGILE"),
    (5, C13 + "JNT2_crossing_speed_joint/RESULT.md", "JOINT FAILS ON G2 (coverage)"),
    (5, C13 + "JNT2R_blind_crossing_speed_joint/RESULT_BLIND.md", "JOINT FAILS ON G2 (coverage)"),
    (6, C12 + "SRJ3_reference_layout_disc_fit/RESULT.md", "NO VERDICT (no power) / NO VERDICT (no power)"),
    (6, C12 + "SRJ4_reference_layout_dark_fraction/RESULT.md", "NO VERDICT (no power) / NO VERDICT (no power)"),
    (7, C13 + "DSC1_joint_on_resolved_discs/RESULT.md", "JOINT'S STATEMENT HOLDS ON THE RESOLVED DISCS, FRAGILE"),
    (7, C13 + "DSC1_joint_on_resolved_discs/RESULT.md", "NO POWER (fewer than three discs above)"),
    (8, C13 + "DSC1_joint_on_resolved_discs/RESULT.md", "LAW FAILS BELOW, FRAGILE"),
    (7, C13 + "DSC1R_blind_resolved_discs_regrade/RESULT_BLIND.md", "NO POWER, FRAGILE"),
    (8, C13 + "DSC1R_blind_resolved_discs_regrade/RESULT_BLIND.md", "LAW HOLDS BELOW, FRAGILE"),
    (9, C13 + "ALP1_alpaka_discs_joint/RESULT.md", "NO POWER / NO POWER"),
    (9, C13 + "ALP1R_blind_alpaka_discs_joint/RESULT_BLIND.md", "NO VERDICT (TW-N and TW-D do not bite)"),
    (10, C12 + "U4L1_alma_limit_reading/RESULT.md", "NO LABEL"),
    (11, C10 + "SRH1_settled_radius_history/RESULT.md", "WINDOW EMPTY"),
    (11, C10 + "SRH1R_blind_lensing_regrade/RESULT.md", "NO VERDICT"),
    (11, C13 + "JNT2_crossing_speed_joint/RESULT.md", "cannot see f (SRH1R)"),
    (12, C09 + "KO2_kids_own_field_by_type/RESULT.md", "NO VERDICT for late types and NO VERDICT for early types"),
    (13, "fable52_push/ONE1_counted_once/RESULT.md", "KiDS host-free: PASSES / PASSES"),
    (14, C09 + "RB1_form_b_hot_systems/RESULT.md", "NOT FALSIFIED (ONE-SIDED)"),
    (14, C10 + "XCV1_xcop_nonhydrostatic_mass/RESULT.md", "NO VERDICT"),
    (14, C13 + "JNT2_crossing_speed_joint/RESULT.md", "TRIVIAL (all 7 above)"),
    (15, C09 + "PD1_phantom_is_dust/RESULT.md", "FAIL +0.16"),
    (15, C09 + "RB1_form_b_hot_systems/RESULT.md", "the two-sided amount gate stays FAIL as PD1 graded it"),
    (16, C09 + "RB1_form_b_hot_systems/RESULT.md", "NO VERDICT under the frozen KA-2"),
    (16, C12 + "SRJ1_settled_joint_clusters/RESULT.md", "JOINT FAILS ON CLUSTERS, FRAGILE (R500 aperture)"),
    (17, C13 + "JNT2_crossing_speed_joint/RESULT.md", "law in 19 / 20"),
    (17, C13 + "JNT2R_blind_crossing_speed_joint/RESULT_BLIND.md", "groups q at R500 (NO POWER)"),
    (18, C12 + "GO2_group_outskirts_desi_groups/RESULT.md", "NOT EVALUABLE [r_ta NOT REACHED]"),
    (18, C10 + "GO1_group_outskirts/RESULT.md", "NOT EVALUABLE"),
    (19, C09 + "RB1_form_b_hot_systems/RESULT.md", "CONSISTENT [STRIPPING-DEPENDENT]"),
    (20, TEX, "FAIL, about 3$\\sigma$ with systematics"),
    (20, "rebuild_2026_10_22/ZN4_cluster_resolution/README.md", "X-COP ONLY"),
    (20, "rebuild_2026_10_22/FR1_fair_share_retention/README.md", "NOT RETENTION"),
    (21, C10 + "FRZ1_forest_redistribution_at_z/RESULT.md", "FOREST ROW FAILS"),
    (21, C10 + "FZS1_forest_settled_radius/RESULT.md", "FOREST ROW FAILS, FRAGILE"),
    (21, C13 + "JNT2_crossing_speed_joint/RESULT.md", "TRIVIAL to f 2"),
    (21, C13 + "JNT2R_blind_crossing_speed_joint/RESULT_BLIND.md", "17.6 / 29.2 FAIL"),
    (22, C13 + "FRZ4_forest_flux_graded/RESULT.md", "FOREST ROW FAILS AT FLUX LEVEL"),
    (22, C13 + "FRZ4_forest_flux_graded/RESULT.md", "NO VERDICT (known answer e fails)"),
    (22, C12 + "SRF1_settled_radius_flux_window/RESULT.md", "NO VERDICT / NO VERDICT (canonical / alt)"),
    (22, C12 + "SRF1R_blind_settled_radius_flux_window/RESULT_BLIND.md", "As frozen: NO VERDICT / NO VERDICT"),
    (23, C09 + "CO1_form_b_cosmology_computed/RESULT.md", "ROWS HOLD / ROWS HOLD"),
    (23, C09 + "CO1_form_b_cosmology_computed/RESULT.md", "NO VERDICT / NO VERDICT"),
    (24, C10 + "HLF1_own_halo_list_forest/RESULT.md", "NO VERDICT / NO VERDICT (canonical / alt)"),
    (25, C09 + "CO2_form_b_amplitude_pinned/RESULT.md", "AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"),
    (25, C10 + "KL1_lensing_amplitude_survey_assumptions/RESULT.md", "As frozen: NO VERDICT / NO VERDICT."),
    (25, C10 + "BX1_fixed_amplitude_reference/RESULT.md", "NO VERDICT (canonical) / NO VERDICT (alt)"),
    (25, C12 + "LWB1R_blind_lensing_regrade/RESULT_BLIND.md", "AMPLITUDE CONSISTENT, FRAGILE"),
    (26, C12 + "AZ2_flat_a0_lya_ap/RESULT.md", "As frozen: NO VERDICT / NO VERDICT"),
    (26, C12 + "AZ2R_blind_flat_a0_regrade/RESULT_BLIND.md", "FLAT HOLDS / EXPANSION-MODEL DEPENDENT"),
    (27, C12 + "RAW1_halo_stars_direct/RESULT.md", "FAILS HOT, FRAGILE"),
    (27, C13 + "MWT1_hot_bin_assumptions/RESULT.md", "FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST"),
    (27, C13 + "MWT2_hot_bin_structure/RESULT.md", "NO POWER"),
    (27, C12 + "HOT1_hot_bin_localisation/RESULT.md", "CLUMPED"),
    (27, C12 + "LMC1_lmc_pull_on_halo_stars/RESULT.md", "NO LABEL"),
    (29, C12 + "NMB1_nimble_curves_vs_line/RESULT.md", "PASSES"),
    (29, C12 + "NIM2_curves_three_radii/RESULT.md", "FAILS LOW"),
    (29, C12 + "RG1_independent_regrade/RESULT.md", "REPRODUCED"),
    (30, C12 + "PLT1_outer_mass_vs_literature/RESULT.md", "PASSES, FRAGILE"),
    (30, C12 + "SAT1_satellite_directions/RESULT.md", "ANISOTROPY LOWERS IT, NOT ENOUGH"),
    (30, C12 + "EFC1_external_field_convention/RESULT.md", "CONVENTION-DEPENDENT"),
    (22, C13 + "FRZ5_forest_nuisance_refit/RESULT.md", "NO VERDICT (a twin does not bite)"),
    (22, C13 + "FRZ5_forest_nuisance_refit/RESULT.md", "FOREST ROW FAILS AFTER REFIT"),
    (28, C13 + "RRL1_halo_slope_from_rr_lyrae/RESULT.md", "MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]"),
    (31, C11 + "DW1_desi_dr2_mw_mass/RESULT.md", "9 of 12"),
    (32, C12 + "MWI1_inner_baryons/RESULT.md", "SUPPLIED BY 1 OF 5"),
    (33, C12 + "MWG1_hot_halo_gas/RESULT.md", "ROTATION CURVE NOT SUPPLIED"),
    (34, C12 + "RFX1_lmc_reflex_momentum_bound/RESULT.md", "REFLEX WITHIN THE BOUND, FRAGILE"),
    (35, C09 + "RB2_form_b_hosted_rows/RESULT.md", "B FAILS HIGH / B FAILS HIGH"),
    (35, C10 + "DG1_dwarf_gas_history/RESULT.md", "DOES NOT SURVIVE"),
    (35, C10 + "DSB1_dwarf_systematics_blind/RESULT.md", "lane NO POWER"),
    (35, "hy4_preview_push/CRACK-1_ufr_external_field/RESULT.md", "FAILS THE PAIR"),
    (36, C09 + "RB2_form_b_hosted_rows/RESULT.md", "B FAILS ON THE HOSTED ROWS"),
    (36, C10 + "NH2_ngc1052_host_mass/RESULT.md", "Label as frozen: NO VERDICT / NO VERDICT"),
    (36, C10 + "NH2_ngc1052_host_mass/RESULT.md", "TIDES CANNOT REACH"),
    (37, C09 + "RB2_form_b_hosted_rows/RESULT.md", "B CONSISTENT / B CONSISTENT"),
    (38, C12 + "DR4MAP_gaia_dr4_registry_map/DR4_MAP.md", "Governing for the adopted theory (wide binaries only)"),
    (39, C12 + "EUC1_eclipse_saturation_ceiling/RESULT.md", "NO VERDICT / NO VERDICT (canonical / alt)"),
    (39, C12 + "EUC13R_blind_population_gate_regrade/RESULT_BLIND.md", "NO VERDICT"),
    (39, C12 + "EUC15_image_arc_predicted_split/RESULT.md", "EARLY READING, NOT A GATE"),
    (39, C13 + "EUC16_better_arc_finder_source_redshifts/RESULT.md", "EUC1-F graded for the first time"),
    (40, C12 + "EUC4_wide_lenses/RESULT.md", "WIDE LENSES BREAK THE CEILING"),
    (40, C12 + "EUC4R_blind_regrade/RESULT.md", "WIDE LENSES BREAK THE CEILING"),
    (40, C12 + "EUC6_wide_lens_environment/RESULT.md", "WIDE LENSES SIT IN RICHER ENVIRONMENTS"),
    (40, C12 + "EUC6R_blind_regrade/RESULT.md", "WIDE LENSES SIT IN RICHER ENVIRONMENTS"),
    (40, C13 + "LNJ1_joint_switch_on_euclid_lenses/RESULT.md", "NO POWER, FRAGILE / NO POWER"),
    (41, C12 + "ESZ1_wide_lens_gas_pressure/RESULT.md", "ONLY A CUSP IS LEFT"),
    (41, C12 + "EXR1_wide_lens_xray_cusp/RESULT.md", "Frozen word: NOT EVALUABLE / NOT EVALUABLE"),
    (41, C12 + "EXR1R_blind_regrade/RESULT.md", "Frozen word: NOT EVALUABLE / NOT EVALUABLE"),
    (42, C12 + "KAP1_kappa_new_routes/RESULT.md", "KAPPA NOT DERIVED"),
    (42, C12 + "OUT4_kappa_window/RESULT.md", "KAPPA NOT DERIVED (FITTED)"),
    (43, C10 + "R541A_clock_matter_coupling/RESULT.md", "EXCLUDED / EXCLUDED"),
    (43, C10 + "R541B_early_symmetry_breaking/RESULT.md", "TRADES / TRADES"),
    (44, C13 + "JNT2_crossing_speed_joint/RESULT.md", "[1.25, 3] canonical and [1.25, 2] alt"),
    (44, C13 + "JNT2_crossing_speed_joint/RESULT.md",
     "window without the coverage line is [1.25, 2] in both builds on both footings"),
    (45, "fable52_push/FLD1_fold_reach/RESULT.md", "DOES NOT / DOES NOT"),
]
WORDS = ["PASSES TRIVIALLY", "FAILS ON COVERAGE ONLY", "EQUALS THE LAW", "NO POWER",
         "DEPENDS ON AN UNTESTED ASSUMPTION", "NOT GRADED FOR THIS FORM", "PASSES", "FAILS"]
END_LINE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."


def norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def committed(path):
    r = subprocess.run(["git", "show", "HEAD:" + path], cwd=ROOT, capture_output=True, text=True)
    return None if r.returncode != 0 else r.stdout


def main():
    ok_all = True
    n = 0
    lines = []

    def report(ok, msg):
        nonlocal ok_all, n
        n += 1
        ok_all &= ok
        lines.append(("PASS " if ok else "FAIL ") + msg)

    with open(os.path.join(ROOT, HERE, "SCORECARD.md"), encoding="utf-8") as fh:
        card_raw = fh.read()
    card = norm(card_raw)
    cache = {}
    for row, path, word in CHECKS:
        if path not in cache:
            txt = committed(path)
            cache[path] = None if txt is None else norm(txt)
        src = cache[path]
        in_src = src is not None and norm(word) in src
        in_card = norm(word) in card
        report(in_src and in_card, "row %d | %s | \"%s\" | in committed file: %s | in SCORECARD: %s"
               % (row, path, word, "yes" if in_src else ("NO" if src is not None else "FILE NOT COMMITTED"),
                  "yes" if in_card else "NO"))

    # table rows, coverage, counts
    rows = {}
    for ln in card_raw.splitlines():
        m = re.match(r"^\| (\d+) \|", ln)
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            rows[int(m.group(1))] = cells[5]
    report(sorted(rows) == list(range(1, len(rows) + 1)), "table rows numbered 1..%d without gaps" % len(rows))
    checked = {c[0] for c in CHECKS}
    missing = sorted(set(rows) - checked)
    report(not missing, "every table row has a check (missing: %s)" % (missing or "none"))
    for k, footing in ((0, "Canonical"), (1, "Alt")):
        counts = {w: 0 for w in WORDS}
        for row, cell in rows.items():
            parts = [p.strip() for p in cell.split(" / ")]
            w = parts[k] if len(parts) == 2 else parts[0]
            if w not in counts:
                report(False, "row %d: completed-form word '%s' not in the fixed list" % (row, w))
                continue
            counts[w] += 1
        m = re.search(r"^%s: (.*?) Total (\d+)\.$" % footing, card_raw, re.M)
        stated = {}
        if m:
            for part in m.group(1).rstrip(".").split(";"):
                part = part.strip().rstrip(".")
                mm = re.match(r"^(.*) (\d+)$", part)
                if mm:
                    stated[mm.group(1)] = int(mm.group(2))
        computed = {w: c for w, c in counts.items() if c}
        report(m is not None and stated == computed and int(m.group(2)) == len(rows),
               "%s counts from the table %s match the stated line" % (footing, computed))

    # folder hygiene
    for name in ("COMPLETED_FORM.md", "SCORECARD.md", "cj1_audit.py"):
        with open(os.path.join(ROOT, HERE, name), encoding="utf-8") as fh:
            t = fh.read()
        low = t.lower()
        bad = [s for s in ("/" + "users/", "cold " + "dark matter", "cdm" + "-like") if s in low]
        report(not bad, "%s: no home path and no banned name (found: %s)" % (name, bad or "none"))
        if name.endswith(".md"):
            report(t.rstrip().splitlines()[-1] == END_LINE, "%s ends with the required line" % name)

    for ln in lines:
        print(ln)
    passed = sum(1 for ln in lines if ln.startswith("PASS"))
    print("%d of %d checks pass" % (passed, n))
    print(END_LINE)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
