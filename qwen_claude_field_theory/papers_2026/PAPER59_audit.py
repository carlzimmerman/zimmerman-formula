#!/usr/bin/env python3
"""PAPER59 audit: the built PDF must be newer than the TeX; every quoted number must match the committed lane outputs
(covariant_push_2026_10_22/C1-C8 and doors_push_2026_10_22/D10, E6 *_results.json; otherwise the lane's .out, README, the
pre-DR4 note or the git record); every cited commit must exist and touch its lane; the two PENDING statements (native CMB,
native cosmic shear) must be true at build time (no C7 native-spectrum result committed; no CFG960 1024^3 verdict committed),
else this audit FAILS until the paper is updated; citations must match citations/REFERENCES.bib; no forbidden claim, local
path or personal name may appear.
Run: python3 PAPER59_audit.py (exit 0 only if all pass).  Read-only."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DP = os.path.join(ROOT, "doors_push_2026_10_22")
TEX = os.path.join(HERE, "PAPER59_covariant_screened_theory_2026.tex")
PDF = os.path.join(HERE, "PAPER59_covariant_screened_theory_2026.pdf")
ZJ = os.path.join(HERE, "PAPER59_covariant_screened_theory_2026.zenodo.json")
CV = os.path.join(ROOT, "covariant_push_2026_10_22")
F = 0
N = 0


def check(name, ok, msg=""):
    global F, N
    N += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    F += (not ok)


SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("ﬃ", "ffi"), ("−", "-"), ("–", "-"), ("—", "-"), ("’", "'"), ("‘", "'"),
                 (" ", " "), ("µ", "μ"), ("∆", "Δ"), ("ϕ", "φ"), ("∗", "*"), ("**", ""), ("\\|", "|")):
        t = t.replace(a, b)
    t = t.translate(SUB)
    t = re.sub(r"\s*×\s*", "x", t)
    t = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", t)
    t = re.sub(r"(?<=\w) (?=[,.;:)])", "", t)
    t = re.sub(r"\s*±\s*", " ± ", t)
    return re.sub(r"\s+", " ", t)


def dehyph(t):
    return re.sub(r"([a-z])- ([a-z])", r"\1\2", t)


def keephyph(t):
    return re.sub(r"([A-Za-z])- ([A-Za-z])", r"\1-\2", t)


def sci(x, d):
    """value -> how the PDF renders m\\times10^{e} after norm, e.g. 6.3355x107, 1.6x10-28"""
    m, e = f"{x:.{d}e}".split("e")
    return f"{m}x10{int(e)}"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=ROOT)


# ---------------------------------------------------------------- A. build
check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout).group(1))
check("A2 page count 4-10", 4 <= pages <= 10, f"{pages} pages")
raw = [norm(subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout) for m in (["-layout"], [], ["-raw"])]
flat = " ||| ".join(raw + [keephyph(x) for x in raw] + [dehyph(x) for x in raw])
low = flat.lower()
tex = open(TEX, encoding="utf-8").read()


def has(name, s):
    s = norm(s)
    check(name, s in flat, s)


def J(lane, fname):
    return json.load(open(os.path.join(DP, lane, fname)))


def get(d, *keys):
    for k in keys:
        d = d[k]
    return d


def num(name, value_str, ctx):
    """value_str is formatted from a committed JSON value; ctx (with {}) is the PDF wording around it"""
    s = norm(ctx.format(value_str))
    check(name, s in flat, s)


def txt(lane, fname):
    return norm(open(os.path.join(DP, lane, fname), encoding="utf-8").read())


def rd(name, lane, fname, s, pdf_s=None):
    """s must be in the lane file AND (s, or pdf_s) in the PDF"""
    s, p = norm(s), norm(pdf_s or s)
    check(name, s in txt(lane, fname) and p in flat, f"{lane}/{fname}: '{s}'" + (f" / PDF '{p}'" if pdf_s else ""))


def outline(lane, fname):
    t = open(os.path.join(DP, lane, fname), encoding="utf-8").read()
    m = re.findall(r"COMPLETE: (\d+)/(\d+) checks PASS", t)
    return f"{m[-1][0]}/{m[-1][1]}" if m else None



f2 = lambda x: f"{x:.2f}"
def CJ(lane, fname):
    return json.load(open(os.path.join(CV, lane, fname)))
def ctxt(lane, fname):
    return norm(open(os.path.join(CV, lane, fname), encoding="utf-8").read())
def crd(name, lane, fname, s, pdf_s=None):
    s, p = norm(s), norm(pdf_s or s)
    check(name, s in ctxt(lane, fname) and p in flat, f"{lane}/{fname}: '{s}'" + (f" / PDF '{p}'" if pdf_s else ""))
def cout(lane, fname):
    m = re.findall(r"COMPLETE: (\d+)/(\d+) checks PASS", open(os.path.join(CV, lane, fname), encoding="utf-8").read())
    return f"{m[-1][0]}/{m[-1][1]}" if m else None

# ---------------------------------------------------------------- B. source document and settings
th = git("show", "5d7308f3a2:covariant_push_2026_10_22/THEORY_V3_DRAFT.md").stdout
check("B THEORY_V3_DRAFT committed at 5d7308f3a2, cited", "The screened theory, v3" in th and "5d7308f3a2" in flat)
check("B draft names the stiffness term and eta = 0", "−(γ_L/2)(D·P)²" in th and "η = 0" in th)
has("B footings", "(9.36x10-11 and 1.13x10-10 m s-2")
has("B kappa fitted, not closed", "is fitted; the theory is not closed")

# ---------------------------------------------------------------- C. lane table: checks and commits
COV = {  # lane: (out file, checks in table, verdict in README, commits)
    "C1_aest_embedding": ("c1_aest_embedding.out", "8/8", "EMBEDS WITH EXTRA TERM", ["d9a9a17f4e", "6502ef90a9"]),
    "C2_aest_cosmology": ("c2_aest_cosmology.out", "9/9", "COMPUTED", ["ac4b30ff62", "2dd388643a", "5e93769089"]),
    "C3_scale_map": ("c3_scale_map.out", "9/11", "SCOPED NO-GO", ["c16ef33ae5", "fd7196584c", "6dba29d773"]),
    "C4_khronon_parent": ("c4_khronon_parent.out", "8/8", "EMBEDS WITH EXTRA TERM", ["b0ea16ecf1", "5f4f845554"]),
    "C5_health": ("c5_health.out", "7/10", "CONDITIONALLY HEALTHY", ["f002ce909a", "f3e7d4d661"]),
    "C6_literal_cassini": ("c6_literal_cassini.out", "7/8", "UNDECIDED", ["1b2ced55a4", "ae428dc252"]),
    "C7_aest_class": ("c7_validate.out", "7/7", "RUNNABLE NOW", ["b0ced915c8"]),
    "C8_instantaneous": ("c8_instantaneous.out", "8/8", "WELL-POSED + UNCONSTRAINED", ["f2399aaf5e", "aa113a5e96"]),
}
for lane, (out, chk, verdict, commits) in COV.items():
    check(f"C {lane} checks {chk} (.out)", cout(lane, out) == chk, f"{cout(lane, out)}")
    check(f"C {lane} verdict '{verdict}' (README)", verdict in ctxt(lane, "README.md") and verdict in flat)
    for h in commits:
        files = git("show", "--name-only", "--format=", h).stdout
        check(f"C {lane} commit {h} touches lane, cited", f"covariant_push_2026_10_22/{lane}/" in files and h in flat)
DOORS = {"D10_native_Lstar": ("d10_native_lstar.out", "10/10", ["e3333cb274", "ecec1ce9e7", "3ac0573063"]),
         "E6_native_fret": ("e6_native_fret.out", "5/5", ["c42925d9dc", "5c0669a33d", "0bea588820"])}
for lane, (out, chk, commits) in DOORS.items():
    check(f"C {lane} checks {chk} (.out)", outline(lane, out) == chk and f"{chk} & " in tex)
    check(f"C {lane} CRISP FINDING (README)", "CRISP FINDING" in txt(lane, "README.md"))
    for h in commits:
        check(f"C {lane} commit {h} touches lane, cited", f"doors_push_2026_10_22/{lane}/" in git("show", "--name-only", "--format=", h).stdout and h in flat)
for h, path in (("ffb14e40bc", "CLARIFICATION_2026-10-22_ADDENDUM_E.md"), ("92fa9f9471", "CFG942"), ("3d82af0a7e", "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md"),
                ("f72bef68ea", "CFG960_sctm_engine/AMENDMENT_A6")):
    check(f"C record commit {h} ({path}) exists, cited", path in git("show", "--name-only", "--format=", h).stdout and h in flat)

# ---------------------------------------------------------------- D. the action (C1, C3, C4, C5)
c4 = CJ("C4_khronon_parent", "c4_khronon_parent_results.json")
num("D C4 curl of the auxiliary (JSON)", f"{c4['K4']['curl_over_grad']:.3f}", "= {} on a two-mass test")
pr = c4["K5"]["planet_ratio_to_bound_Jx"]
num("D C4 J_x planet ratios (JSON)", f"{sci(min(pr.values()), 2)}-{sci(max(pr.values()), 2)}", "full a0, {} times")
aq = c4["K5"]["AQUAL_Q2_over_Hees_min_by_row"]
num("D C4 turn-off J AQUAL min (JSON)", f"{min(v for k, v in aq.items() if k.startswith('canonical')):.2f}x(canonical) and {min(v for k, v in aq.items() if k.startswith('alt')):.2f}x(alternative)", "at least {}")
yt = c4["K8"]["yt_khronon"]
ck7 = c4["checks"][7] if isinstance(c4["checks"], list) else c4["checks"]["7"]
check("D C4 Khronon y_t 33.94 / 23.70 / 33.98 (JSON)", f"{yt['canonical_quotedLambda']:.2f}" == "33.94" and f"{yt['kappa_half_32pi']:.2f}" == "33.98" and "alt=23.6962" in ck7["value"])
has("D C4 y_t in PDF", "33.94 (canonical), 23.70 (alternative) or 33.98")
crd("D C4 J_x outside BS class (README)", "C4_khronon_parent", "README.md", "lies **outside BS's admissible class**".replace("**", ""), "outside Blanchet and Skordis's admissible class")
crd("D C4 read via WebFetch, not on disk (README)", "C4_khronon_parent", "README.md", "They are **not verified on disk**".replace("**", ""), "not verified on disk")
crd("D C1 gamma_L identically zero in AeST (README)", "C1_aest_embedding", "README.md", "is **identically zero** in AeST".replace("**", ""), "identically zero in AeST")
c5 = CJ("C5_health", "c5_health_results.json")
ss = c5["H7"]["solar_system_beta0"]
num("D C5 eta>0 rates (JSON)", f"{ss['canonical']['growth_rate_per_yr']} /yr (canonical) and {ss['alt']['growth_rate_per_yr']} /yr", "rate is {}")
check("D C5 boundary beta* (JSON)", c5["H7"]["beta_star_bisected"] == "1.4870736e-19" and "β = 1.48707x10-19" in flat)

# ---------------------------------------------------------------- E. health, well-posedness (C5, C8)
crd("E C5 tensor modes at c (README)", "C5_health", "README.md", "Only the 2 tensor modes propagate, at c", "only the two tensor modes propagate, at c")
crd("E C5 three frozen fails (README)", "C5_health", "README.md", "Checks: 7/10 PASS, exit 1 (three frozen FAILs kept)", "7/10, exit 1")
c8 = CJ("C8_instantaneous", "c8_instantaneous_results.json")
num("E C8 signal at 24 pc (JSON)", sci(c8["signal_illustration"]["L24"], 1), "1 km away by {} m s-2")
num("E C8 pulsars (JSON)", sci(c8["K7"]["worst_ratio"], 1), "at most {} of the double pulsar")
num("E C8 alpha2 (JSON)", sci(c8["K8"]["L24"]["ratio_vs_2.4e-7"], 1), "of {} of the bound")
dv = max(c8["K9"]["canonical_Earth_surface_g"]["dv_over_c"], c8["K9"]["alt_Earth_surface_g"]["dv_over_c"])
num("E C8 GW (JSON)", sci(dv, 1), "∆v/c ≤ {}".replace("∆", "Δ"))
crd("E C8 criterion B satisfied (README)", "C8_instantaneous", "README.md", "Criterion B (global time, nothing backward in τ, no closed signal loops): satisfied", "the single-global-time criterion holds")
crd("E C8 infinite volume OPEN (README)", "C8_instantaneous", "README.md", "The theorem on infinite volume is **OPEN**".replace("**", ""), "the infinite-volume theorem")

# ---------------------------------------------------------------- F. parameters
d10 = J("D10_native_Lstar", "d10_native_lstar_results.json")
v10 = d10["verdict"]
num("F D10 central floor (JSON)", f"{v10['canonical']['central']:.2f} pc (canonical) / {v10['alt']['central']:.2f} pc", "L⋆,95 = {}")
num("F D10 abstract floor (JSON)", f"{v10['canonical']['central']:.2f} / {v10['alt']['central']:.2f} pc", "set L⋆ ≥ {}")
num("F D10 band (JSON)", f"{v10['canonical']['band'][0]:.2f}-{v10['canonical']['band'][1]:.2f} / {v10['alt']['band'][0]:.2f}-{v10['alt']['band'][1]:.2f} pc", "spans {}")
check("F D10 straddles 20 pc (JSON)", v10["canonical"]["window"] == v10["alt"]["window"] == "STRADDLES the 20 pc edge" and "straddles 20 pc" in flat)
c2 = CJ("C2_aest_cosmology", "c2_aest_cosmology_results.json")
check("F C2 BBN bound 0.9611 (JSON)", "0.9611" in c2["K4"]["cases"] and "Gcosmo/GN > 0.9611" in flat)
c2b = CJ("C2_aest_cosmology", "c2b_native_cmb_results.json")
num("F C2 Planck-lite sigma (JSON)", f"{c2b['P5']['sigma_g']:.3f}", "gives σ = {}")
num("F C2 K_B bound (JSON)", f"{c2b['P2']['KB_max']}", "KB < {}")
has("F kappa values (CFG493, E4 via PAPER58)", "κΛ = 0.417 ± 0.095 (CFG493); 0.414 ± 0.094")
crd("F dust abundance an initial condition (C4 README)", "C4_khronon_parent", "README.md", "I₀ is an integration constant, so Ω_K is FITTED".replace("₀", "0").replace("_K", "_K"), "nothing in the action fixes it")

# ---------------------------------------------------------------- G. tests
c6 = CJ("C6_literal_cassini", "c6_literal_cassini_results.json")
R1 = c6["R1_physical"]
check("G C6 all 24 cells pass Hees and Park (JSON)", len(R1) == 24 and all(v["hees"] and v["park"] for v in R1.values()) and "All 24 cells" in flat)
q24 = [v["Q2"] for k, v in R1.items() if "|24|" in k]; q90 = [v["Q2"] for k, v in R1.items() if "|90|" in k]
num("G C6 Q2 at 24 pc (JSON)", f"{min(q24) * 1e34:.2f}-{max(q24) * 1e34:.2f}x10-34", "Q2 = {} s-2")
num("G C6 Q2 at 90 pc (JSON)", f"{min(q90) * 1e36:.2f}-{max(q90) * 1e36:.2f}x10-36", "at 90 pc {}")
mg = c6["R1_margin"]
num("G C6 margin (JSON)", f"{sci(mg['Hees_min'], 1)} to {sci(mg['Hees_max'], 1)}", "Hees line is {}")
num("G C6 abstract margin (JSON)", f"{sci(mg['Hees_min'], 1)} to {sci(mg['Hees_max'], 1)}", "cells, by {}")
rt = [v["ratio_to_D7d"] for v in R1.values()]
num("G C6 10-19% lower than D7d (JSON)", f"{round(100 * (1 - max(rt)))}-{round(100 * (1 - min(rt)))}%", "lowers Q2 by {}")
num("G C6 frozen C2 float cancellation (JSON)", sci(c6["C2"]["isolated_rF0_vs_rF1_rel"], 1), "fails at {} against")
crd("G C6 frozen UNDECIDED (README)", "C6_literal_cassini", "README.md", "By the frozen verdict rule: UNDECIDED", "The frozen rule reads UNDECIDED")
crd("G C6 planets (README)", "C6_literal_cassini", "README.md", "Mars 0.173, Saturn 0.035 and Earth 0.028", "Mars is at 0.173 of its bound, Saturn 0.035 and Earth 0.028")
cells = d10["band_cells"]
dq = [v["dchi2_AQUAL"] for v in cells.values()]
num("G D10 AQUAL excluded in 18 cells (JSON)", f"{len(dq)} cells (Δχ2 = {min(dq):.1f}-{max(dq):.1f})", "excluded in all {}")
check("G D10 no finite L* beats Newton (JSON)", not v10["canonical"]["Newton_excluded_any_cell"] and v10["canonical"]["AQUAL_excluded_all_cells"] and "no finite L⋆ beats Newton" in flat)
e6 = J("E6_native_fret", "e6_native_fret_results.json")["summary"]["canonical"]
num("G E6 z_req (JSON)", f"{e6['z_req_median']:.2f}", "Median zreq = {}")
num("G E6 nu_req (JSON)", f"{e6['nu_req_F1'][0]:.2f}σ", "an ordinary {} fluctuation")
num("G E6 L_min (JSON)", f"{e6['Lmin_cons_median'][0]:.2f}", "median {} times the present baryons")
num("G E6 q_chem (JSON)", f"{e6['qchem_F1_-0.5|W2'][0]:.3f}", "need is {} of the supply")
num("G E6 6 of 36 (JSON)", f"{len(e6['chem_over_central'])} of {e6['n_chem']}", "{} tested systems")
has("G E3 gap (PAPER58 E3)", "+0.89 ± 0.13 dex above the screened prediction")
e3 = json.load(open(os.path.join(DP, "E3_dwarf_excess", "e3_dwarf_excess_results.json")))["A_above_screened_diag"]["canonical|L*24"]
check("G E3 gap from JSON", f"+{e3['median_Delta']:.2f} ± {e3['sd']:.2f}" == "+0.89 ± 0.13")
d4 = json.dumps(json.load(open(os.path.join(DP, "D4_alma_status", "d4_alma_status_results.json")))["R7_quoted"])
check("G D4 ALMA S/N 0.04-0.58 (JSON cells)", "S/N 0.04" in d4 and "S/N 0.58" in d4 and "S/N 0.04-0.58" in flat)

# ---------------------------------------------------------------- H. sealed predictions
note = open(os.path.join(ROOT, "prep_2026", "gaia_dr4_prep", "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md"), encoding="utf-8").read()
check("H DR4 rule A3 in the note", "## AMENDMENT A3 (2026-10-22, pre-data): OWNER DECISION on the σ_sys rule" in note and "Use (b) as the primary" in note and "(b) primary, (a), (e), (g2) must agree" in flat)
wb = c6["R3_wide_binary"]
num("H C6 gamma_v-1 24/50/90 (JSON)", " / ".join(sci(max(wb[f"canonical|{L}"]["gamma_minus_1"]), 1) for L in (24, 50, 90)), "γv - 1 = {} at")
e2 = json.load(open(os.path.join(DP, "E2_field_equation", "e2_field_equation_results.json")))["R2"]
num("H E2 AQUAL law-first (JSON)", f"{e2['canonical|PREREG_primary']['gamma_AQUAL_anch']:.3f} (canonical) / {e2['alt|PREREG_primary']['gamma_AQUAL_anch']:.3f}", "(AQUAL): {}")
num("H abstract 1.17 (JSON)", f"{e2['canonical|PREREG_primary']['gamma_AQUAL_anch']:.2f}", "γv ≈ {} for the unscreened")
dd = json.load(open(os.path.join(DP, "D2_wide_binary_fork", "d2_sigma_sys_defs_results.json")))["defs"]["canonical"]
bkey = [k for k in dd if k.startswith("b ")][0]
zb = [dd[bkey][c]["z"] for c in ("primary|mock", "primary|DR3-cal", "alt_gext|mock", "alt_gext|DR3-cal")]
num("H DR4 expected power under (b) (JSON)", f"{min(zb):.2f}-{max(zb):.2f}σ canonical", "{}")
rd("H ALMA dates (D4 README)", "D4_alma_status", "README.md", "Public **2026-11-06**".replace("**", ""), "public 2026-11-06")
rd("H ALMA GS4 date", "D4_alma_status", "README.md", "Public **2026-11-28**".replace("**", ""), "GS4 (2026-11-28)")


# ---------------------------------------------------------------- R. rebuild lanes (F1-H3) and the v3/v4 restructure
RB = os.path.join(ROOT, "rebuild_2026_10_22")
def RJ(lane, fname):
    return json.load(open(os.path.join(RB, lane, fname)))
def rtxt(lane, fname="README.md"):
    return norm(open(os.path.join(RB, lane, fname), encoding="utf-8").read())
def rout(lane, fname):
    m = re.findall(r"COMPLETE: (\d+)/(\d+) checks PASS", open(os.path.join(RB, lane, fname), encoding="utf-8").read())
    return f"{m[-1][0]}/{m[-1][1]}" if m else None
REB = {"F1_cluster_cores": ("f1_cluster_cores.out", "6/6", "REAL FAILURE", ["9fd5aee16e", "f1803b0256"]),
       "F2_outer_lensing": ("f2_outer_lensing.out", "9/9", "UNDECIDABLE", ["e9816b47d2", "7c8c3d5302"]),
       "F3_growth_audit": ("f3_growth_audit.out", "9/9", "BELONGS TO THE SETTLING RULES ONLY", ["0bef684eea", "059766caa5"]),
       "G1_smooth_cap": ("g1_smooth_cap.out", "7/7", "ARTEFACT", ["9921a5172a", "a048e6d468"]),
       "G2_preinfall_retention": ("g2_preinfall_retention.out", "4/6", "FAILS on native inputs", ["92716d0148", "b3fbb9ed9d", "3cdcf3b4c5"]),
       "H1_aest_F": ("h1_aest_f.out", "6/6", "NONE IN THE FAMILY", ["a4d76f492e", "1654b84f78"]),
       "H2_aest_clusters": ("h2_aest_clusters.out", "6/6", "CANNOT", ["364a56c250", "5160a89939", "385f61a14c"]),
       "H3_jeans_control": ("h3_jeans_control.out", "4/5", "CLAIM FAILS", ["04355110c4", "6b905cb6d8"])}
for lane, (out, chk, verdict, commits) in REB.items():
    check(f"R {lane} checks {chk} (.out), in table", rout(lane, out) == chk and f"& {chk} &" in tex, f"{rout(lane, out)}")
    check(f"R {lane} verdict '{verdict}' (README)", norm(verdict) in rtxt(lane))
    for h in commits:
        check(f"R {lane} commit {h} touches lane, cited", f"rebuild_2026_10_22/{lane}/" in git("show", "--name-only", "--format=", h).stdout and h in flat)
th2 = git("show", "8bcafea2fa:covariant_push_2026_10_22/THEORY_V3_DRAFT.md").stdout
check("R THEORY draft section 1b (v4) at 8bcafea2fa, cited", "## 1b. A better-surviving candidate" in th2 and "8bcafea2fa" in flat)
f1 = RJ("F1_cluster_cores", "f1_cluster_cores_results.json")
check("R F1 verdict REAL FAILURE (JSON)", f1["verdict"] == "REAL FAILURE")
rows = f1["rows"]
pc = [rows[f"PRIMARY {h}"]["canonical"]["MID"][0] for h in ("h0672", "h0686")]; pa = [rows[f"PRIMARY {h}"]["alt"]["MID"][0] for h in ("h0672", "h0686")]
zc = [f1["Z_primary"][h]["canonical"] for h in ("h0672", "h0686")]; za = [f1["Z_primary"][h]["alt"] for h in ("h0672", "h0686")]
num("R F1 primary canonical (JSON)", f"{min(pc):.2f}-{max(pc):.2f} (canonical, Z = +{min(zc):.1f} to +{max(zc):.1f})", "AMID = {}")
num("R F1 primary alt (JSON)", f"{min(pa):.2f}-{max(pa):.2f} (alternative, Z = +{min(za):.1f} to +{max(za):.1f})", "and {}")
bc = [rows[f"A1 PRIMARY {h} boost clipped at 1"]["canonical"]["MID"][0] for h in ("h0672", "h0686")]; ba = [rows[f"A1 PRIMARY {h} boost clipped at 1"]["alt"]["MID"][0] for h in ("h0672", "h0686")]
num("R F1 boost-fixed (JSON)", f"{min(bc):.2f}-{max(bc):.2f} / {min(ba):.2f}-{max(ba):.2f}", "(post-result) {}")
num("R F1 abstract range (JSON)", f"{min(pc):.2f}-{max(bc):.2f} (canonical) and {min(pa):.2f}-{max(ba):.2f} (alternative)", "sit {} times above")
fv = f1["favourable"]
fc = [fv[h]["canonical"]["A"]["MID"][0] for h in ("h0672", "h0686")]; fa = [fv[h]["alt"]["A"]["MID"][0] for h in ("h0672", "h0686")]
num("R F1 favourable corner (JSON)", f"{min(fc):.2f}-{max(fc):.2f} (canonical) and {min(fa):.2f}-{max(fa):.2f} (alternative)", "still {}")
check("R F1 326 clusters (JSON K3)", "N 326" in f1["checks"]["K3"]["value"] and "(326 clusters" in flat)
check("R F1 levers <= 4% (README)", "Native h moves A_MID by 1–4 %".replace("–", "-") in rtxt("F1_cluster_cores") and "by at most 4%" in flat)
h2 = RJ("H2_aest_clusters", "h2_aest_clusters_results.json")
cellbest = {}
for k_, v_ in h2["A1_min_chi2"].items():
    c_ = k_.split("|", 1)[1]; cellbest[c_] = min(v_, cellbest.get(c_, 1e9))
mc = list(cellbest.values())
check("R H2 four cells (JSON)", len(mc) == 4)
num("R H2 best profile chi2 (JSON)", f"{min(mc):.1f}-{max(mc):.1f}", "profile χ2 is {}")
check("R H2 law alone 27.3-41.8 and pass 11.07 (README)", "The law alone gives 27.3–41.8".replace("–", "-") in rtxt("H2_aest_clusters") and "11.07" in rtxt("H2_aest_clusters")
      and "against 27.3-41.8 for the law alone and a pass line of 11.07" in flat)
f2 = RJ("F2_outer_lensing", "f2_outer_lensing_results.json")
ta = f2["trackA"]["canonical"]
num("R F2 record dchi2 (JSON)", f"+{f2['K0']['canonical']['all']['dchi2']:.1f}", "∆χ2 = {} came".replace("∆", "Δ"))
num("R F2 edge removal (JSON)", f"{ta['L0_record_Dder']['A_O2']:.2f} to {ta['L1_no_edge_B']['A_O2']:.2f}", "falls from {} of the data")
num("R F2 weakest field (JSON)", f"{ta['L5_plus_EFE_noclu=T_central']['A_O2']:.2f}", "an amplitude of {}")
num("R F2 isolation shift (JSON)", f"{f2['trackB']['canonical']['zero']['diff_out']['d']:.2f}", "moves by {} ±")
check("R F2 y_e <~ 3e-5 and 8.6 sigma (README)", "B21's sample allows only y_e ≲ 3e-5".replace("y_e", "y_e") in rtxt("F2_outer_lensing").replace("ye", "y_e") or "3e-5" in rtxt("F2_outer_lensing"))
has("R F2 8.6 sigma in PDF", "(8.6σ)")
f3 = RJ("F3_growth_audit", "f3_growth_audit_results.json")
check("R F3 J'(0) = -1 (JSON K1)", "J'(0) = -1" in f3["checks"]["K1"]["value"] and "J ′ (0) = -1" in " ||| ".join(raw))
w = f3["K5"]["windows"]
mins = [w[k]["mu_min_hMpc"] for k in w if k.startswith("bsk2")]; gaps = [w[k]["gap_factor"] for k in w]
num("R F3 mu_K window (JSON)", f"{min(mins):.0f}-{max(mins):.0f} h/Mpc", "at least {}")
num("R F3 BS cap (JSON)", f"{f3['K5']['mu_max_hMpc_BS24_Eq39']:.1f} h/Mpc", "caps it at {}")
num("R F3 gap (JSON)", f"{min(gaps):.0f}-{max(gaps):.0f}x", "a gap of {}")
num("R F3 abstract gap (JSON)", f"{min(gaps):.0f}-{max(gaps):.0f}x", "(a gap of {})")
sr = [v["sigma8_ratio"] for k, v in f3["K4"]["BS24_Eq39_edge_100kpc"].items() if isinstance(v, dict) and "sigma8_ratio" in v]
num("R F3 sigma8 inside allowed range (JSON)", f"{min(sr):.2f}-{max(sr):.2f}", "only {} of the dust limit")
num("R F3 CFG596 reproduced (JSON)", f"+{f3['K0']['dchi2']:.2f}", "exactly ({})")
k3 = f3["K3"]
num("R F3 S8 (JSON)", f"{k3['A_c2b_refit']['0.3']['S8_pred']:.3f} / {k3['B_cfg886_bg']['0.3']['S8_pred']:.3f}", "S8 = {} against")
num("R F3 KiDS S8 (JSON)", f"{k3['A_c2b_refit']['0.3']['S8_data_lin']:.3f} ± {k3['A_c2b_refit']['0.3']['S8_data_sigma']:.3f} / {k3['B_cfg886_bg']['0.3']['S8_data_lin']:.3f} ± {k3['B_cfg886_bg']['0.3']['S8_data_sigma']:.3f}", "({})")
check("R F3 both CONSISTENT (JSON)", k3["A_c2b_refit"]["0.3"]["cls"] == k3["B_cfg886_bg"]["0.3"]["cls"] == "CONSISTENT")
g1 = RJ("G1_smooth_cap", "g1_smooth_cap_results.json")
check("R G1 512^3 excess 0.163 (JSON) and 0.040/0.077 coarser grids (README)", f"{g1['K1']['425_R3_can_512']['maxdev']:.3f}" == "0.163"
      and "0.040 (128³), 0.077 (256³)" in open(os.path.join(RB, "G1_smooth_cap", "README.md"), encoding="utf-8").read() and "0.040 / 0.077 / 0.163" in flat)
g2 = RJ("G2_preinfall_retention", "g2_preinfall_retention_results.json")["verdict"]
num("R G2 offset (JSON)", f"+{g2['canonical']['primary_CHEMcons']['O']:.2f}", "offset stays {} ±")
num("R G2 offset alt (JSON)", f"+{g2['alt']['primary_CHEMcons']['O']:.2f}", "/ {} ± 0.15 (alternative)")
check("R G2 overshoots 8 (README)", "It overshoots **8** systems".replace("**", "") in rtxt("G2_preinfall_retention") and "overshoots 8 systems" in flat)
h1 = RJ("H1_aest_F", "h1_aest_f_results.json")["SPARC"]
zcn = [h1["canonical"][m]["z_vs_canonical"] for m in ("SZ-simple", "SZ-exp", "SZ-sharp", "SZ-inf")]; zal = [h1["alt"][m]["z_vs_canonical"] for m in ("SZ-simple", "SZ-exp", "SZ-sharp", "SZ-inf")]
num("R H1 SZ interpolants lose (JSON)", f"z = {max(zcn):.2f} to {min(zcn):.2f} (canonical) and {max(zal):.2f} to {min(zal):.2f}", "SPARC at {}")
check("R H1 BBN lambda_s >= 24.7 (C2b JSON + README)", f"{c2b['P2']['lambda_s_min']:.1f}" == "24.7" and "BBN needs λ_s ≥ 24.7" in open(os.path.join(RB, "H1_aest_F", "README.md"), encoding="utf-8").read() and "λs ≥ 24.7" in flat)
h3 = RJ("H3_jeans_control", "h3_jeans_control_results.json")
num("R H3 bounded rate (JSON)", f"{h3['T4']['I=2e-7|gL']['max_Gamma2_over_4piGrho']:.5f}", "(maximum {} of it)")
check("R H3 band end and contact term (README)", "242.75 μ" in open(os.path.join(RB, "H3_jeans_control", "README.md"), encoding="utf-8").read() and "2.3e4 × Newton at" in open(os.path.join(RB, "H3_jeans_control", "README.md"), encoding="utf-8").read()
      and "kc ≈ 243 µ".replace("µ", "μ") in flat.replace("µ", "μ") and "2.3x104 times Newton" in flat)
check("R H3 criterion flags ordinary dust (README)", "Criterion (i) is mis-specified" in rtxt("H3_jeans_control") and "flags ordinary self-gravitating Newtonian dust" in flat)
check("R abstract: clusters fail, v4 health linear only", "Clusters fail, in both forms" in flat and "at linear order only" in flat and "REAL FAILURE" in flat)
check("R v4 not established", "v4 is the better-surviving candidate; it is not established" in flat)

# ---------------------------------------------------------------- P. pending statements must be true at build time
c7log = git("log", "--format=%h %s", "b0ced915c8..HEAD", "--", "covariant_push_2026_10_22/C7_aest_class").stdout
c7files = os.listdir(os.path.join(CV, "C7_aest_class"))
check("P native CMB pending: no C7 commit after milestone 4", c7log.strip() == "", c7log.strip()[:200])
check("P native CMB pending: no native-spectrum/chi2 result file in C7", not any(re.search(r"native|step_?n|chi2|spectr", f, re.I) for f in c7files), str(c7files))
crd("P C7 'No native spectrum has been confronted' (README)", "C7_aest_class", "README.md", "No native spectrum has been confronted with data yet", "No native spectrum has been run or confronted with data")
cv = validate = CJ("C7_aest_class", "c7_validate_results.json")
check("P C7 validation 7/7 at 2.2e-6 (README + .out)", cout("C7_aest_class", "c7_validate.out") == "7/7" and "to 2.2×10⁻⁶" in open(os.path.join(CV, "C7_aest_class", "README.md"), encoding="utf-8").read() and "to 2.2x10-6" in flat)
c960 = git("log", "--format=%h %s", "2ccd47be97..HEAD", "--", "campaign_fresh_gravity/CFG960_sctm_engine").stdout
check("P cosmic shear pending: no CFG960 commit after the A6 engine", c960.strip() == "", c960.strip()[:200])
vfiles = [f for f in git("ls-files", "campaign_fresh_gravity/CFG960_sctm_engine").stdout.split() if re.search(r"(SC1x|SC2x|1024).*(verdict|result|score)", f, re.I)]
check("P cosmic shear pending: no SC1x/SC2x/1024 verdict file tracked", vfiles == [], str(vfiles))
LED = open(os.path.join(ROOT, "campaign_fresh_gravity", "LEDGER.md"), encoding="utf-8").read().splitlines()
check("P no CFG960 ledger row with a 1024^3 verdict (the pre-registration's pass line excepted)", not any(l.startswith("| CFG960") and re.search(r"KiDS (CONSISTENT|INCONSISTENT)|VERDICT: (PASS|FAIL)", l.replace("pass iff both footings are KiDS CONSISTENT", "")) for l in LED))
check("P CFG596 +68.7 (README)", "Δχ²(F − S0) = +68.7" in open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG596_lean_pm_1024", "README.md"), encoding="utf-8").read() and "∆χ2 = +68.7".replace("∆", "Δ") in flat)
check("P pending stated in plain text, no % PENDING marker", "% PENDING" not in tex and "Native CMB: pending" in flat and "Native cosmic shear: pending" in flat)
crd("P a0 absent at linear order (C2 README)", "C2_aest_cosmology", "README.md", "a0 cannot enter the background or the linear equations", "the CMB cannot test the galactic law")

# ---------------------------------------------------------------- O. citations and metadata
CIT = os.path.join(ROOT, "citations")
bib = open(os.path.join(CIT, "REFERENCES.bib"), encoding="utf-8").read()
def bibentry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
    return m.group(1) if m else ""
e = bibentry("Blanchet2024")
check("O Blanchet & Skordis 2024 (bib)", "2404.06584" in e and "{Blanchet}, Luc and {Skordis}, Constantinos" in e and "pages = {040}" in e and "number = {11}" in e
      and "L. Blanchet, C. Skordis, JCAP 11 (2024) 040 (arXiv:2404.06584)" in flat)
e = bibentry("Blanchet2025c")
check("O Blanchet & Skordis 2025 (bib)", "2507.00912" in e and "L. Blanchet, C. Skordis, arXiv:2507.00912 (2025)" in flat)
e = bibentry("Skordis2021")
check("O Skordis & Zlosnik 2021 (bib)", "2007.00082" in e and "161302" in e and "127" in e and "PRL 127, 161302 (2021) (arXiv:2007.00082)" in flat)
check("O SZ21 source on disk (C2 provenance)", "New Relativistic Theory for Modified Newtonian Dynamics" in ctxt("C2_aest_cosmology", "PROVENANCE.md"))
e = bibentry("Hees2014"); check("O Hees 2014 (bib)", "102002" in e and "PRD 89, 102002 (2014)" in flat)
e = bibentry("Park2026"); check("O Park 2026 (bib)", "024066" in e and "PRD 114, 024066 (2026)" in flat)
z = json.load(open(ZJ))["metadata"]
ids = {r["identifier"] for r in z["related_identifiers"]}
check("O related identifiers (PAPER58 v1.1, PAPER49 v1.2, PAPER57)", {"10.5281/zenodo.23579379", "10.5281/zenodo.23533323", "10.5281/zenodo.23532885"} <= ids)
check("O never 23532894", "23532894" not in json.dumps(z) and "23532894" not in tex)
check("O zenodo: working paper, CC-BY, fitted, not closed, pending", z["publication_type"] == "workingpaper" and z["license"] == "cc-by-4.0" and "fitted" in z["description"]
      and "not closed" in z["description"] and "pending" in z["description"].lower())
for s in ("PAPER58 v1.1 (doi:10.5281/zenodo.23579379)", "PAPER57 (doi:10.5281/zenodo.23532885)", "PAPER49 v1.2 (doi:10.5281/zenodo.23533323)"):
    has(f"O companion '{s[:20]}'", s)

# ---------------------------------------------------------------- Q. honesty, forbidden, names
for s in ("fitted", "the theory is not closed", "not peer reviewed", "never pooled", "AI-assisted", "Anthropic's Claude", "not a particle", "POSTULATED",
          "Not a UV completion", "Criterion A (no influence faster than light) is violated", "The dwarf supply is conditional", "The owner's programme"):
    has(f"Q honesty '{s}'", s)
zl = z["description"].lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "breakthrough",
            "κ is derived", "kappa is derived", "l★ is derived", "/users/", "gmail", "dark matter particle", "dark-matter particle"):
    check(f"Q forbidden '{bad}' absent", bad not in low and bad not in tex.lower() and bad not in zl)
check("Q no 'derived' applied to kappa or L*", not re.search(r"(κ|kappa|L⋆|Lstar)[^.]{0,30}\bis derived", low))
check("Q no home path in TeX", "/Users/" not in tex and "~/" not in tex)
gu = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split()
check("Q no personal name (repo user) in PDF, TeX or zenodo description", all(w.lower() not in low and w.lower() not in tex.lower() and w.lower() not in zl for w in gu if len(w) >= 3), f"{len(gu)} name parts checked")

print(f"\nPAPER59 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
