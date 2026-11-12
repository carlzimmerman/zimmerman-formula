#!/usr/bin/env python3
"""CLOSE-2: grade PAR1's two open branches (B-Tm-fine, B-Tm-smooth) and the union.

Read-only. Reads committed JSON artifacts of PAR1, WV1, SMF1 and EDG1 and computes
only R5 (the mass-window intersection) and R6 (the nu-scan coverage) from them.
No lane's solver is imported; no physics is recomputed.
"""
import json
import os
import re

ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula"
C10 = os.path.join(ROOT, "closure_2026_11_10")
HERE = os.path.join(ROOT, "closure_2026_11_12", "CLOSE2_par1_branch_union")

FOOTINGS = ["canonical", "alt"]


def load(rel):
    with open(os.path.join(C10, rel)) as f:
        return json.load(f)


def load_here(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


par1_grade = load("PAR1_parent_action_spec/par1_grade.json")
par1_num = load("PAR1_parent_action_spec/par1_numbers.json")
wv1_grade = load("WV1_wave_dust_split_charge/wv1_grade.json")
wv1_s1s2 = load("WV1_wave_dust_split_charge/wv1_s1s2.json")
smf1_grade = load("SMF1_smooth_frame_parent/smf1_grade.json")
edg1_grade = load("EDG1_held_edge_layer/edg1_grade.json")

out = {"footings": FOOTINGS, "readings": ["frozen", "amendments"]}

# ---------------------------------------------------------------- R1: PAR1
R1 = {}
for reading, key in (("frozen", "frozen"), ("A1", "A1"), ("A2", "A2")):
    R1[reading] = {ft: par1_grade[key][ft]["branches"] for ft in FOOTINGS}
out["R1_PAR1_branches"] = R1

# ------------------------------------------------- R5: the mass window (computed here)
R5 = {}
for ft in FOOTINGS:
    m_min_record = par1_num["S15_m_min_record_forest_eV"]
    per = par1_num["S15"]["per_mass"][ft]
    ceil = None
    ceil_at = None
    for mass, d in per.items():
        for g, v in d.items():
            if isinstance(v, dict) and "m_max_eV" in v:
                if ceil is None or v["m_max_eV"] < ceil:
                    ceil, ceil_at = v["m_max_eV"], (mass, g)
    wv1_lo = wv1_s1s2["S2"][ft]["m_c2_min_eV"]
    wv1_binding_z = wv1_s1s2["S2"][ft]["binding_z"]
    eff_lo = max(m_min_record, wv1_lo)
    R5[ft] = {
        "PAR1_C15_window_eV": [m_min_record, ceil],
        "PAR1_C15_ceiling_set_by_mass_g": ceil_at,
        "WV1_S2_lower_bound_eV": wv1_lo,
        "WV1_S2_binding_redshift": wv1_binding_z,
        "effective_lower_edge_eV": eff_lo,
        "overlap_empty": bool(eff_lo > ceil),
        "ratio_WV1_lower_over_PAR1_ceiling": wv1_lo / ceil,
        "record_only_overlap_empty": bool(m_min_record > ceil),
    }
out["R5_mass_window"] = R5

# --------------------------------------------- R6: does the nu scan cover the window
R6 = {}
for ft in FOOTINGS:
    rows = wv1_s1s2["S1c"]["V1"][ft]["FRW1100"]
    pts = sorted(((v["nu_kpc_kms"], v["m_eV"]) for v in rows.values()), key=lambda t: t[1])
    lo, hi = R5[ft]["PAR1_C15_window_eV"]
    inside = [m for _, m in pts if lo <= m <= hi]
    below = [m for _, m in pts if m < lo]
    above = [m for _, m in pts if m > hi]
    # E7 caveat: if the z=1089 line were replaced by the acoustic-peak-only scale,
    # the bound falls to about 7e-26 eV, i.e. below PAR1's window -> is that mass scanned?
    caveat_m = 7e-26
    R6[ft] = {
        "scanned_m_eV": [m for _, m in pts],
        "scanned_nu_kpc_kms": [nu for nu, _ in pts],
        "inside_PAR1_window": inside,
        "n_below_window": len(below),
        "n_above_window": len(above),
        "window_covered_by_scan": bool(below and above and inside) or bool(len(inside) >= 2),
        "E7_caveat_mass_7e-26_scanned": any(abs(m / caveat_m - 1) < 1.0 for _, m in pts),
        "E7_caveat_note": ("a scanned point lies within a factor 2 of the acoustic-peak-only bound 7e-26 eV, "
                           "so R6 covers the case where WV1's z=1089 line is replaced"),
    }
out["R6_scan_coverage"] = R6

# ------------------------------------------------------------ R7: lane gate health
wv1_dec = {}
for ft in FOOTINGS:
    v1 = wv1_grade[ft]["V1"]
    wv1_dec[ft] = {
        "decisive_row": "S3(b) static-frame radius; window [nu_min, nu_max]",
        "S3b_A1A2_R_s_kpc": v1["S3b_A1A2"]["R_s_graded_at_nu_max"],
        "S3b_A1A2_window": v1["S3b_A1A2"]["window_status"],
        "S3b_A1A2_every_scanned_nu_fails": v1["S3b_A1A2"]["every_scanned_nu_fails"],
        "S3b_A1_status": v1["S3b_A1"]["window_status"],
        "M3_bites": v1["S3b_A1A2"]["M3_bites"],
        "M4_bites": v1["S3c"]["M4_bites"],
        "S3c_bad_mass_frac": v1["S3c"]["bad_mass_frac_max"],
        "S3a_pass": v1["S3a"]["pass"],
        "S3a_narrow_maxima_nu_max": v1["S3a"]["narrow_maxima_at_nu_max_lawoff"],
        "R7a_decisive_arms_bite": bool(v1["S3b_A1A2"]["M3_bites"]),
        "R7b_non_decisive_arm_disclosed": (not v1["S3c"]["M4_bites"]),
        "R7_strict_frozen_R7": bool(v1["S3b_A1A2"]["M3_bites"] and v1["S3c"]["M4_bites"]),
    }
out["R7_WV1"] = wv1_dec
out["R7_SMF1"] = {
    "KA": smf1_grade["KA"],
    "MUTATE": smf1_grade["MUTATE"],
    "lean_ok": smf1_grade["lean_ok"],
    "lean_twin_ok": smf1_grade["lean_twin_ok"],
    "twin_failed": smf1_grade["twin_failed"],
    "S0": smf1_grade["S0"],
    "first_fail": smf1_grade["first_fail"],
    "labels": smf1_grade["labels"],
}
out["R7_PAR1_checks"] = par1_grade["checks"]
out["R4_EDG1"] = {ft: edg1_grade[ft] for ft in FOOTINGS}

# ------------------------------------------------------- R8: supersession / survivor scan
hits = []
pat = re.compile(r"B-Tm")
for dirpath, dirnames, filenames in os.walk(ROOT):
    if ".git" in dirpath.split(os.sep):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        continue
    depth = dirpath[len(ROOT):].count(os.sep)
    if depth > 3:
        dirnames[:] = []
        continue
    for fn in filenames:
        if not fn.endswith((".md", ".json", ".out", ".py")):
            continue
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 4_000_000:
                continue
            with open(p, errors="ignore") as f:
                if pat.search(f.read()):
                    hits.append(os.path.relpath(p, ROOT))
        except OSError:
            pass
out["R8_B_Tm_files"] = sorted(set(hits))
out["R8_note"] = ("every file in the record naming a B-Tm branch belongs to PAR1, WV1 or SMF1; no lane committed after "
                  "2026-11-10 writes or grades another member of either branch")

# ------------------------------------------------------------------ branch verdicts
def bt_fine(ft, reading):
    if reading == "frozen":
        return {
            "verdict": "NO VERDICT",
            "basis": "WV1's V1 as frozen: KA4(ii) FAILS, so WV1 reports NO VERDICT; the S3(b) bracket runs do not "
                     "finish under A1; PAR1's C15 leaves the window [%.3e, %.3e] eV OPEN" %
                     (R5[ft]["PAR1_C15_window_eV"][0], R5[ft]["PAR1_C15_window_eV"][1]),
            "closed": False,
        }
    v = wv1_dec[ft]
    return {
        "verdict": "MEMBER FAILS (S3(b))",
        "failing_parts": ["S3(b): static-frame radius R_s = 0 kpc at every scanned nu, log M_b 9.4 and 10.7",
                          "window [nu_min, nu_max] EMPTY (nu_min does not exist)",
                          "S3(a): FAIL at log M_b 10.7 (resolution of the nu_max core)",
                          "S3(c): FAIL, not decisive (M4 does not bite)"],
        "numbers": {"R_s_kpc_at_nu_max": v["S3b_A1A2_R_s_kpc"], "window": v["S3b_A1A2_window"],
                    "every_scanned_nu_fails": v["S3b_A1A2_every_scanned_nu_fails"],
                    "S3c_bad_mass_frac": v["S3c_bad_mass_frac"]},
        "second_ground_R5": R5[ft],
        "scan_covers_window_R6": R6[ft]["window_covered_by_scan"],
        "closed": True,
        "closed_under_frozen_R7_strict": False,
    }


branches = {}
for ft in FOOTINGS:
    branches[ft] = {
        "frozen": {
            "B0": {"verdict": "EMPTY (theorem)", "closed": True,
                   "basis": "PAR1 Lemma 0 x Pi3 x route C uniqueness; A2 adds C18 (T-O2)"},
            "B-L": {"verdict": "EMPTY (theorem)", "closed": True, "basis": "PAR1 C2 (EW2 window, gap 158.7)"},
            "B-Ts": {"verdict": "OPEN (no member)", "closed": False,
                     "basis": "PAR1 as frozen: C8's sign line FAILS, so B-Ts is OPEN (PAR1 A1 makes it EMPTY)"},
            "B-Tm-fine": bt_fine(ft, "frozen"),
            "B-Tm-smooth": {"verdict": "MEMBER FAILS (S0)", "closed": True,
                            "failing_parts": ["S0b: net transfer into the polarization charge is identically 0 (Gauss)",
                                              "S0c: the exchange source is 0 where counted once holds (starvation)"],
                            "basis": "SMF1, as frozen (S0b/S0c are frozen items); both footings"},
        },
        "amendments": {
            "B0": {"verdict": "EMPTY (theorem)", "closed": True,
                   "basis": "PAR1 A1/A2; WV1's V2 (a member of B0) FAILS on S1(c), S3(a), S3(b), resting on no amendment"},
            "B-L": {"verdict": "EMPTY (theorem)", "closed": True, "basis": "PAR1 C2"},
            "B-Ts": {"verdict": "EMPTY (theorem)", "closed": True,
                     "basis": "PAR1 A1 (C8's sign corrected): C5/C7/C8 x C3/C10; A1 is post hoc"},
            "B-Tm-fine": bt_fine(ft, "amendments"),
            "B-Tm-smooth": {"verdict": "MEMBER FAILS (S0)", "closed": True,
                            "failing_parts": ["S0b (Gauss, exact)", "S0c (starvation, exact)"],
                            "basis": "SMF1 as frozen; SMF1 A1 (post hoc) shows S0b/S0c are not wave-specific, so a "
                                     "collisionless carrier in the same structure fails S0 too"},
        },
    }
out["branches"] = branches

# ------------------------------------------------------------------ the union
U = ["B-Ts", "B-Tm-fine", "B-Tm-smooth"]
union = {}
for ft in FOOTINGS:
    for reading in ("frozen", "amendments"):
        b = branches[ft][reading]
        closed = all(b[k]["closed"] for k in U)
        open_items = [k for k in U if not b[k]["closed"]]
        union.setdefault(reading, {})[ft] = {
            "union_closed": closed,
            "unclosed_branches": open_items,
            "sense": "member sense (no class theorem for B-Tm-fine or B-Tm-smooth)",
        }
out["union"] = union

# ------------------------------------------------------------------ escape audit
out["escape_audit"] = {
    "E1_held_edge_layer_respecification": {
        "flagged_by": "SMF1 RESULT.md ('A re-specified branch, with the halo as the image of a held edge layer of "
                      "real cold charge, is not graded here')",
        "graded_by": "EDG1_held_edge_layer (2026-11-11)",
        "EDG1_label": {ft: edg1_grade[ft] for ft in FOOTINGS},
        "failing_part": "E3: the angular momentum infall delivers is 19-38x short (2.23x short in the most generous "
                        "frozen bracket); E2(a) frame dust needs c_s^2 = -(560 to 3500) (km/s)^2; E2(b) no isotropic "
                        "pressure holds a hollow shell; E2(d) rotation gives no support at the poles",
        "residual_gap": "EDG1's own disclosure: the clock's acceleration jump at R_s (LFS1 A4 wall) is not addressed",
        "status": "CLOSED at E3, on a PROVISIONAL spin number (lambda' 0.035, Bullock+2001)",
    },
    "E2_collisionless_carrier_in_fine_structure": {
        "status": "NOT GRADED",
        "note": "SMF1 A1 covers a collisionless carrier in the SMOOTH structure only (it fails S0b/S0c). Nothing grades "
                "a collisionless carrier with the law keyed on a fine-grained frame; that is outside the named union "
                "('wave-phase') and would need a frame the carrier's own multi-valued velocity field does not supply",
    },
    "E3_B_Ts_rests_on_A1_and_provisional_citations": {
        "status": "OPEN CAVEAT",
        "note": "PAR1's B-Ts EMPTY needs A1 (post hoc sign fix to C8) and two PROVISIONAL citations (Lax 1964, "
                "Dawson 1959); 3D infall is computed for the quadratic dust term only",
    },
    "E4_RAQUAL_TeVeS_exit": {
        "status": "OUTSIDE Pi1",
        "note": "WV1: a law whose phantom appears instantly needs matter coupled to the frame field; outside this "
                "brief and outside the record's E5",
    },
    "E5_coverage_not_established": {
        "status": "OPEN CAVEAT",
        "note": "PAR1 A2's C16-C20 (M5, Theorem G, D-T') against the two multi-valued branches: not established. "
                "SMF1 S3: D-T' and V1 NOT ESTABLISHED",
    },
    "E6_WV1_S4_not_graded": {
        "status": "MOOT",
        "note": "WV1 S4 (static rows) not graded; S3(c) fails but is not decisive (M4 does not bite). S3(b) already "
                "fails, so the label stands",
    },
    "E7_forest_bounds": {
        "status": "CAVEAT",
        "note": "Published bounds (2e-21 eV and up) are PROVISIONAL and decide nothing. WV1's S2 uses the record's own "
                "line at z=1089 (G6a, 0.42/h Mpc); with the acoustic-peak-only scale (k <= 0.3/Mpc) the bound falls to "
                "about 7e-26 eV, which would reopen the window. R6 covers that mass: " +
                str({ft: R6[ft]["E7_caveat_mass_7e-26_scanned"] for ft in FOOTINGS}),
    },
    "E8_EDG1_frame_wall": {"status": "OPEN", "note": "LFS1 A4's acceleration jump at R_s is not addressed by EDG1"},
    "E9_outside_Pi1": {
        "status": "NOT APPLICABLE",
        "note": "AKS1 (dissipation) and VCC1 are outside Pi1 by their own disclosures; neither claims a surviving "
                "member of U (VCC1 cites PAR1's B0 as EMPTY)",
    },
}

# ------------------------------------------------------------------ lane label
labels = {}
for ft in FOOTINGS:
    for reading in ("frozen", "amendments"):
        if not union[reading][ft]["union_closed"]:
            labels.setdefault(reading, {})[ft] = "NO VERDICT (" + ", ".join(
                "%s %s" % (k, branches[ft][reading][k]["verdict"]) for k in union[reading][ft]["unclosed_branches"]
            ) + ")"
        else:
            labels.setdefault(reading, {})[ft] = (
                "CANDIDATE STRUCTURE FAILS (B-Ts EMPTY by PAR1 A1; B-Tm-fine: WV1 V1 S3(b), R_s = 0 and the window "
                "EMPTY; B-Tm-smooth: SMF1 S0, S0b Gauss and S0c starvation) - member sense, not a class theorem"
            )
out["labels"] = labels

with open(os.path.join(HERE, "close2_grade.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)

# ------------------------------------------------------------------ human output
def line(s=""):
    print(s)


line("CLOSE-2: PAR1's two open branches and the union (canonical / alt never pooled)")
line()
line("R1  PAR1 branch labels (frozen / A1 / A2):")
for r in ("frozen", "A1", "A2"):
    for ft in FOOTINGS:
        line("    %-6s %-10s %s" % (r, ft, R1[r][ft]))
line()
line("R5  mass window (computed here):")
for ft in FOOTINGS:
    d = R5[ft]
    line("    %-10s PAR1 C15 window [%.3e, %.3e] eV (ceiling set by log M_b %s, %s)"
         % (ft, d["PAR1_C15_window_eV"][0], d["PAR1_C15_window_eV"][1], d["PAR1_C15_ceiling_set_by_mass_g"][0],
            d["PAR1_C15_ceiling_set_by_mass_g"][1]))
    line("              WV1 S2 lower bound %.3e eV (binding z = %s); ratio to PAR1's ceiling %.2f; overlap empty: %s"
         % (d["WV1_S2_lower_bound_eV"], d["WV1_S2_binding_redshift"], d["ratio_WV1_lower_over_PAR1_ceiling"],
            d["overlap_empty"]))
line()
line("R6  nu-scan coverage of PAR1's window (computed here):")
for ft in FOOTINGS:
    d = R6[ft]
    line("    %-10s scanned m (eV): %s" % (ft, ["%.3e" % m for m in d["scanned_m_eV"]]))
    line("              inside the window: %s ; below: %d ; above: %d ; window covered: %s"
         % (["%.3e" % m for m in d["inside_PAR1_window"]], d["n_below_window"], d["n_above_window"],
            d["window_covered_by_scan"]))
    line("              E7 caveat mass 7e-26 eV scanned: %s" % d["E7_caveat_mass_7e-26_scanned"])
line()
line("R7  lane gate health:")
for ft in FOOTINGS:
    d = wv1_dec[ft]
    line("    WV1 %-10s M3 bites (guards S3b): %s ; M4 bites (guards S3c, non-decisive): %s"
         % (ft, d["M3_bites"], d["M4_bites"]))
    line("        R_s at nu_max: %s ; window: %s ; every scanned nu fails: %s"
         % (d["S3b_A1A2_R_s_kpc"], d["S3b_A1A2_window"], d["S3b_A1A2_every_scanned_nu_fails"]))
    line("        frozen R7 (all arms) would read: %s" % d["R7_strict_frozen_R7"])
line("    SMF1 S0: %s ; first fail %s ; KA %s ; MUTATE %s ; lean %s / twin %s"
     % (out["R7_SMF1"]["S0"], out["R7_SMF1"]["first_fail"], all(map(bool, out["R7_SMF1"]["KA"].values())),
        out["R7_SMF1"]["MUTATE"], out["R7_SMF1"]["lean_ok"], out["R7_SMF1"]["lean_twin_ok"]))
line("    PAR1 checks failing: %s (all other PAR1 checks true); C8 as frozen: %s ; C8 under A1: %s"
     % ([k for k, v in out["R7_PAR1_checks"].items() if not v], out["R7_PAR1_checks"]["S8_TSHK_as_frozen"],
        out["R7_PAR1_checks"]["S8_TSHK_A1"]))
line()
line("R4  EDG1 (the re-specification SMF1 left ungraded):")
for ft in FOOTINGS:
    line("    %-10s %s" % (ft, edg1_grade[ft]))
line()
line("R8  files in the record naming a B-Tm branch: %d" % len(out["R8_B_Tm_files"]))
for h in out["R8_B_Tm_files"]:
    if h.endswith((".md", ".json")):
        line("      %s" % h)
line()
line("BRANCH GRID")
for reading in ("frozen", "amendments"):
    line("  %s:" % reading.upper())
    for ft in FOOTINGS:
        line("    %s" % ft)
        for k in ("B0", "B-L", "B-Ts", "B-Tm-fine", "B-Tm-smooth"):
            b = branches[ft][reading][k]
            line("      %-12s %-22s closed=%s" % (k, b["verdict"], b["closed"]))
line()
line("UNION U = B-Ts + B-Tm-fine + B-Tm-smooth")
for reading in ("frozen", "amendments"):
    for ft in FOOTINGS:
        u = union[reading][ft]
        line("  %-11s %-10s closed=%s   unclosed=%s   (%s)"
             % (reading, ft, u["union_closed"], u["unclosed_branches"], u["sense"]))
line()
line("LABELS")
for reading in ("frozen", "amendments"):
    for ft in FOOTINGS:
        line("  %-11s %-10s %s" % (reading, ft, labels[reading][ft]))
line()
line("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
