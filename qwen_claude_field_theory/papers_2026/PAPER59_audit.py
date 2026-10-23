#!/usr/bin/env python3
"""PAPER59 audit (v1.1): the built PDF must be newer than the TeX; every quoted number must match the committed lane outputs
(covariant_push_2026_10_22/C1-C8 and doors_push_2026_10_22/D10, E6 *_results.json; otherwise the lane's .out, README, the
pre-DR4 note or the git record); every cited commit must exist and touch its lane; v1.0's two PENDING items are checked as
resolved (C7 milestone 5; CFG960 SC1x scored on the retired engine) and v1.1's one PENDING statement (L1 nonlinear production,
no result) must be true at build time (no L1 commit after the A6 implementation 28c65bc28d; no production output tracked),
else this audit FAILS until the paper is updated; section V checks every number added in v1.1 against the theory draft at
45bd132464 and the lane README by file:line; citations must match citations/REFERENCES.bib; no forbidden claim, local
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
has("B kappa FITTED, not closed", "FITTED; the theory is not closed")
check("B kappa = 1/2 FITTED written in TeX (header, abstract, setting)", tex.count("$\\kappa=\\tfrac12$ FITTED") >= 3, str(tex.count("$\\kappa=\\tfrac12$ FITTED")))
DRAFT = "covariant_push_2026_10_22/THEORY_V3_DRAFT.md"
th3 = git("show", "45bd132464:" + DRAFT).stdout
check("B v1.1 source: THEORY_V3_DRAFT at 45bd132464 equals the working file and is its last commit, cited",
      th3 == open(os.path.join(ROOT, DRAFT), encoding="utf-8").read() and git("log", "-1", "--format=%h", "--abbrev=10", "--", DRAFT).stdout.strip() == "45bd132464"
      and "commit 45bd132464 for v1.1" in flat)

# ---------------------------------------------------------------- C. lane table: checks and commits
COV = {  # lane: (out file, checks in table, verdict in README, commits)
    "C1_aest_embedding": ("c1_aest_embedding.out", "8/8", "EMBEDS WITH EXTRA TERM", ["d9a9a17f4e", "6502ef90a9"]),
    "C2_aest_cosmology": ("c2_aest_cosmology.out", "9/9", "COMPUTED", ["ac4b30ff62", "2dd388643a", "5e93769089"]),
    "C3_scale_map": ("c3_scale_map.out", "9/11", "SCOPED NO-GO", ["c16ef33ae5", "fd7196584c", "6dba29d773"]),
    "C4_khronon_parent": ("c4_khronon_parent.out", "8/8", "EMBEDS WITH EXTRA TERM", ["b0ea16ecf1", "5f4f845554"]),
    "C5_health": ("c5_health.out", "7/10", "CONDITIONALLY HEALTHY", ["f002ce909a", "f3e7d4d661"]),
    "C6_literal_cassini": ("c6_literal_cassini.out", "7/8", "UNDECIDED", ["1b2ced55a4", "ae428dc252"]),
    "C7_aest_class": ("c7_native.out", "7/7", "CRISP FINDING", ["b0ced915c8", "64b0fdc9b4"]),
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
                ("f72bef68ea", "CFG960_sctm_engine/AMENDMENT_A6"), ("f6f0ba66a4", "CLARIFICATION_2026-10-23_ADDENDUM_F.md")):
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
num("R F2 weakest field (JSON)", f"{ta['L5_plus_EFE_noclu=T_central']['A_O2']:.2f}", "the amplitude (data over model) is {}")
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
check("R v1.1: v4 no longer the better-surviving candidate (I1, C7)", "v1.0 called v4 the better-surviving candidate; with I1 and C7 neither form is a complete, healthy theory" in flat
      and "v4 is the better-surviving candidate; it is not established" not in flat)

# ---------------------------------------------------------------- P. v1.0's pending items resolved; v1.1's L1 statement must be true at build time
c7m5 = git("show", "--name-only", "--format=%s", "64b0fdc9b4").stdout
check("P C7 milestone 5 (64b0fdc9b4) touches C7, cited", "covariant_push_2026_10_22/C7_aest_class/" in c7m5 and "milestone 5" in c7m5 and "64b0fdc9b4" in flat)
crd("P C7 README L5: v4 runs away", "C7_aest_class", "README.md", "Every BBN-compatible small-K_B configuration runs away at linear order", "v4 runs away on FRW for the dust shape tried")
c7r = open(os.path.join(CV, "C7_aest_class", "README.md"), encoding="utf-8").read().splitlines()
check("P C7 validation 7/7 (.out) and 2.2e-6 (README L102), milestone 4 cited", cout("C7_aest_class", "c7_validate.out") == "7/7" and "TT 2.2e-6" in c7r[101]
      and "to 2.2x10-6" in flat and "b0ced915c8" in flat, "covariant_push_2026_10_22/C7_aest_class/README.md:102")
has("P native CMB stated as no longer pending", "Native CMB: no longer pending")
LED = open(os.path.join(ROOT, "campaign_fresh_gravity", "LEDGER.md"), encoding="utf-8").read().splitlines()
r960 = [(i + 1, l) for i, l in enumerate(LED) if l.startswith("| CFG960-SC1x-RESULT+STOP")]
check("P CFG960 SC1x scored as frozen (ledger row): KiDS EXCLUDED +47.28, retired engine, SC2x not run", len(r960) == 1 and "KiDS EXCLUDED, dchi2 +47.28" in r960[0][1]
      and "retired SCT-M settling engine, not the current best theory v3" in r960[0][1] and "SC2x (alt) NOT RUN" in r960[0][1]
      and "KiDS EXCLUDED, Δχ2 = +47.28" in flat and "It tests the record's retired settling engine, not v3" in flat, f"campaign_fresh_gravity/LEDGER.md:{r960[0][0] if r960 else '?'}")
c960 = git("log", "--format=%h %s", "cfbd4ecf4b..HEAD", "--", "campaign_fresh_gravity/CFG960_sctm_engine").stdout
check("P CFG960 status current: no CFG960 commit after the SC1x score outputs (cfbd4ecf4b)", c960.strip() == "", c960.strip()[:200])
l1log = [s for s in git("log", "--format=%h %s", "28c65bc28d..HEAD", "--", "rebuild_2026_10_22/L1_khronon_pm").stdout.splitlines() if s.strip()]
l1bad = [s[:120] for s in l1log if re.search(r"(?<!PRE-)RESULT\b|SCORED|VERDICT|production (run|result)", s, re.I) and not re.search(r"PRE-RESULT", s)]
check("P L1 pending: every L1 commit after its A6 implementation (28c65bc28d) is pre-result (no production result)", l1bad == [],
      f"{len(l1log)} later commits, none a result" if not l1bad else str(l1bad))
l1f = [f for f in git("ls-files", "rebuild_2026_10_22/L1_khronon_pm").stdout.split() if re.search(r"prod|512|384|256", f, re.I)]
check("P L1 pending: no production output tracked", l1f == [], str(l1f))
l1r = open(os.path.join(ROOT, "rebuild_2026_10_22", "L1_khronon_pm", "README.md"), encoding="utf-8").read().splitlines()
check("P L1 README L470: only the frozen production cells decide", "Only the frozen 512³ cells decide those." in l1r[469], "rebuild_2026_10_22/L1_khronon_pm/README.md:470")
has("P L1 stated as in progress, no result", "Its production runs are in progress; no result is given here")
check("P CFG596 +68.7 (README)", "Δχ²(F − S0) = +68.7" in open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG596_lean_pm_1024", "README.md"), encoding="utf-8").read() and "∆χ2 = +68.7".replace("∆", "Δ") in flat)
check("P no % PENDING marker in the TeX", "% PENDING" not in tex)
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
check("O zenodo version 1.1, v1.0 DOI cited in TeX and description", z["version"] == "1.1" and "doi:10.5281/zenodo.23585319" in flat and "doi:10.5281/zenodo.23585319" in z["description"])
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

# ---------------------------------------------------------------- V. v1.1: every added number vs the draft row and the lane README (file:line)
D = DRAFT
def RB_(lane):
    return f"rebuild_2026_10_22/{lane}/README.md"
C7R = "covariant_push_2026_10_22/C7_aest_class/README.md"
_lines = {}
def LN(path, n):
    if path not in _lines:
        _lines[path] = open(os.path.join(ROOT, path), encoding="utf-8").read().splitlines()
    return norm(_lines[path][n - 1].replace("**", ""))
def v(name, pdf_s, *srcs):
    """each (path, line, s): s must be on that line of that file; pdf_s must be in the PDF"""
    bad = [f"{pth}:{n}" for pth, n, s in srcs if norm(s.replace("**", "")) not in LN(pth, n)]
    ok_pdf = norm(pdf_s) in flat
    check("V " + name, not bad and ok_pdf, "; ".join(f"{pth}:{n}" for pth, n, _ in srcs) + ("" if ok_pdf else f" | PDF missing '{norm(pdf_s)}'") + (f" | not on line: {bad}" if bad else ""))

# M1 erratum
v("M1 sigma8 ratio at the cap 0.391 vs 0.121", "0.391 against 0.121", (D, 75, "σ₈ at the cap 0.391 vs 0.121"), (RB_("M1_trilemma"), 7, "is 0.121 for J′(0) = 0, against 0.391 for J_x"))
v("M1 411 h/Mpc, 27.8x the cap", "411 h/Mpc, 27.8", (D, 75, "μ_K ≥ 411 h/Mpc, 27.8× the BS cap"), (RB_("M1_trilemma"), 7, "μ_K ≥ 411 h/Mpc, 27.8× the cap"))
v("M1 kernel s(k; f0) and both -> 1", "Both tend to 1 as k", (D, 75, "s(k; f₀) = (μ² − f₀k²)/((1−f₀)k² + μ²)"), (RB_("M1_trilemma"), 59, "s(k; f₀) = (μ² − f₀k²)/((1−f₀)k² + μ²)"))
v("M1 late Jeans scale = mu_K", "late Jeans scale is μK", (D, 75, "late Jeans scale = K″(1)/2"), (RB_("M1_trilemma"), 16, "Jeans scale, which equals the galactic static mass μ_K for every K analytic at Q = 1"))
v("M1 T2 planets >= 0.96 a0", "at least 0.96 a", (D, 75, "planets ≥ 0.96 a₀"), (RB_("M1_trilemma"), 8, "≥ 0.96 a₀"))
v("M1 erratum supersedes J'(0) = -1 statements", "That cause is wrong", (D, 75, "Every statement in this draft, F3's README, the board and PAPER59 that blames J′(0) = −1 is superseded by this row"), (RB_("M1_trilemma"), 15, "The linear failure is not caused by J′(0) = −1"))
# Q6
v("Q6 no radiation era", "Literal v3 has no radiation era", (D, 79, "Literal v3 has no radiation era"), (RB_("Q6_v3_class"), 5, "Literal v3 has no radiation era"))
v("Q6 z 1854 to 3.2e5", "before z = 1854 (μK = 14.8 h/Mpc) up to 3.2x105", (D, 79, "It beats radiation before z = 1854 (μ_K 14.8 h/Mpc) up to 3.2×10⁵ (2542)"), (RB_("Q6_v3_class"), 7, "before z = 1854–3.2×10⁵"))
v("Q6 BBN mu_K >= 1.84e8 (abstract and body)", "BBN needs μK ≥ 1.84x108 h/Mpc", (D, 79, "needs μ_K ≥ 1.84×10⁸ h/Mpc"), (RB_("Q6_v3_class"), 10, "needs μ_K ≥ 1.84×10⁸ h/Mpc"))
v("Q6 1.2e7 x the cap", "1.2x107 times the cap", (D, 79, "1.2×10⁷ × the BS cap"), (RB_("Q6_v3_class"), 118, "a factor of 1.2×10⁷"))
v("Q6 sigma8 0.061, R_B 0.073", "σ8 = 0.061", (D, 79, "σ₈ = 0.061 (R_B 0.073, against F3's ODE 0.391)"), (RB_("Q6_v3_class"), 15, "σ₈ is 0.061: R_B = σ₈/σ₈(dust) = 0.073"))
v("Q6 R_B 0.073 vs ODE 0.391 (PDF)", "= 0.073, against F3's ODE 0.391", (D, 79, "R_B 0.073, against F3's ODE 0.391"), (RB_("Q6_v3_class"), 16, "F3's ODE gave 0.391"))
v("Q6 5% growth needs mu_K > 2542", "5% growth needs μK > 2542 h/Mpc", (D, 79, "5 % growth needs μ_K > 2542"), (RB_("Q6_v3_class"), 18, "> 2542 h/Mpc"))
v("Q6 plik-lite +13891 (not converged) to +18.7", "from +13891 (not converged) down to +18.7", (D, 79, "+13891 down to +18.7 over μ_K 14.8–2542"), (RB_("Q6_v3_class"), 22, "+13 891 (not converged)"), (RB_("Q6_v3_class"), 25, "2542: +18.7"))
# Q7
v("Q7 fixes BBN only (abstract)", "BS25's DBI K fixes BBN only", (D, 84, "fixes BBN only; linear growth still fails"), (RB_("Q7_bs25_cosmology"), 3, "BS25's sector fixes BBN only; linear growth still fails"))
v("Q7 dN_eff 4e-6 to 7e-6 vs 7.7e13", "against 7.7x1013 for the quadratic", (D, 84, "ΔN_eff,equiv 4e-6 – 7e-6 at 1 MeV vs 7.7e13 for the quadratic K"), (RB_("Q7_bs25_cosmology"), 17, "is 4.3e-6 (λ_D = 30) and 7.2e-6 (λ_D = 1). The quadratic K gives 7.7e13"))
v("Q7 dN_eff range in PDF", "4x10-6-7x10-6 at 1 MeV", (D, 84, "4e-6 – 7e-6 at 1 MeV"))
v("Q7 R_B 0.26-0.32", "RB = 0.26-0.32", (D, 84, "R_B = σ₈/σ₈,dust 0.26–0.32"), (RB_("Q7_bs25_cosmology"), 23, "P1: 0.259"), (RB_("Q7_bs25_cosmology"), 24, "P2: 0.324"))
v("Q7 plik-lite +350 to +748", "plik-lite ∆χ2 is +350 to +748".replace("∆", "Δ"), (D, 84, "plik-lite Δχ² vs ΛCDM +350 to +748"), (RB_("Q7_bs25_cosmology"), 29, "Δχ² +350"), (RB_("Q7_bs25_cosmology"), 30, "Δχ² +748"))
v("Q7 BS ran no Boltzmann code", "Blanchet and Skordis ran no Boltzmann code", (D, 84, "BS ran no Boltzmann code"), (RB_("Q7_bs25_cosmology"), 11, "BS ran no Boltzmann code."))
v("Q7 large lambda_D leaves P(1 h/Mpc) at 0.33", "1 h/Mpc at 0.33 of ΛCDM", (D, 84, "leaves P(k) at 1 h/Mpc at 0.33 of ΛCDM"), (RB_("Q7_bs25_cosmology"), 51, "P(k) at 1 / 3 / 10 h/Mpc is 0.33"))
# C7 milestone 5 (v4 on FRW)
v("C7 v4 runaway 1e2-1e41 by k <= 10", "102-1041 by k ≤ 10 h/Mpc", (D, 72, "P/P_ΛCDM 10²–10⁴¹ by k ≤ 10 h/Mpc"), (C7R, 7, "10²–10⁴¹ by k ≤ 10 h/Mpc"))
v("C7 dust shape Cosh, Q0 = 0.1", "(Cosh, Q0 = 0.1 Mpc-1)", (D, 72, "(Cosh, Q₀ = 0.1 Mpc⁻¹)"), (C7R, 219, "(Cosh, Q₀ = 0.1, s = 0.1) is POSTULATED"))
v("C7 tachyonic pair before z ~ 78", "before z ≈ 78", (D, 72, "Likely a tachyonic vector pair before z ≈ 78"), (C7R, 202, "z_c ≈ 71–78 for Q₀ = 0.1 Mpc⁻¹"))
v("C7 untested escape Q0 >~ 30", "Q0 ≳ 30 Mpc-1", (D, 72, "Q₀ ≳ 30 Mpc⁻¹"), (C7R, 207, "Q₀ ≳ 30 Mpc⁻¹"))
v("C7 not numerical", "gauge- and tolerance-stable, so not numerical", (D, 72, "gauge- and tolerance-stable, so not numerical"), (C7R, 9, "not a numerical artefact"))
# H4
v("H4 ILL-POSED where rho_tau < 0", "v3 is ill-posed wherever the khronon density is negative", (D, 86, "ILL-POSED."), (RB_("H4_v3_saddle_stability"), 3, "ILL-POSED"))
v("H4 gamma_L makes it unbounded", "It is the γL screening term that makes it unbounded", (D, 86, "it is the γ_L screening term that makes it unbounded"), (RB_("H4_v3_saddle_stability"), 11, "γ_L is what makes it unbounded"))
v("H4 without gamma_L 0.006-0.20 e-folds", "only 0.006-0.20 e-folds", (D, 86, "0.006–0.20 e-folds"), (RB_("H4_v3_saddle_stability"), 12, "0.006–0.20 e-folds"))
v("H4 MW-M31 ~290 kpc", "about 290 kpc across", (D, 86, "MW–M31 ~290 kpc"), (RB_("H4_v3_saddle_stability"), 30, "V^⅓ 290 kpc"))
v("H4 LMC-MW 12 kpc", "LMC-Milky Way, 12 kpc", (D, 86, "LMC–MW 12 kpc"), (RB_("H4_v3_saddle_stability"), 31, "12 kpc region"))
v("H4 wavelengths below 4-330 pc", "below about 4-330 pc grow", (D, 86, "wavelengths below ~4–330 pc grow by > 1 e-fold"), (RB_("H4_v3_saddle_stability"), 22, "λ₁ ≈ 4–330 pc"))
v("H4 Solar System healthy, D.P >= 0.045", "≥ +0.045 M", (D, 86, "D·P ≥ +0.045 M☉/pc³"), (RB_("H4_v3_saddle_stability"), 20, "at least 0.045 M☉/pc³"))
v("H4 + I1: both forms ill-posed somewhere", "makes both covariant forms ill-posed somewhere", (D, 86, "the γ_L screening operator makes both covariant forms ill-posed somewhere"))
v("H4 C8 WELL-POSED stands for the leaf problem only", "C8's WELL-POSED verdict stands for the leaf (P, lapse) problem only", (RB_("H4_v3_saddle_stability"), 181, "C8's WELL-POSED verdict stands for the leaf (P, lapse) problem only"))
# I1
v("I1 v4 ill-posed where the aether twists", "v4 is ill-posed wherever the aether twists", (D, 37, "v4 is ILL-POSED wherever the aether twists"), (RB_("I1_gammaL_causality"), 3, "ILL-POSED (where the aether twists)"))
v("I1 loop gains 4 ms-3.9 s", "4 ms-3.9 s around the Galaxy", (D, 37, "illustrative loop gains 4 ms–3.9 s around the Galaxy"), (RB_("I1_gammaL_causality"), 81, "4 ms – 3.9 s"))
v("I1 Ostrogradsky ghost", "adds an Ostrogradsky ghost", (D, 37, "adds an Ostrogradsky ghost"), (RB_("I1_gammaL_causality"), 17, "brings an Ostrogradsky ghost"))
# P3
v("P3 PASS on all five, two scoped", "PASS on all five, two scoped", (D, 81, "PASS on all five, two scoped"))
v("P3 shadow/ISCO <= 2.9e-11", "at most 2.9x10-11", (D, 81, "shadow/ISCO/photon-sphere shifts ≤ 2.9e-11"), (RB_("P3_v3_strong_field"), 7, "moves by at most 2.9e-11"))
v("P3 ringdown <= 2.8e-11", "at most 2.8x10-11", (D, 81, "Ringdown shifts ≤ 2.8e-11"), (RB_("P3_v3_strong_field"), 8, "at most 2.8e-11"))
v("P3 NS dR/R <= 2.7e-28", "dR/R ≤ 2.7x10-28", (D, 81, "Neutron stars dR/R ≤ 2.7e-28"), (RB_("P3_v3_strong_field"), 9, "dR/R at 1.4 Msun is at most 2.7e-28"))
v("P3 loop factor 1.3e-3 at Eot-Wash 38.6 um, L* 90 pc", "1.3x10-3 at Eöt-Wash (38.6", (D, 81, "worst loop factor 1.3e-3 at Eöt-Wash 38.6 μm (L★ 90 pc)"), (RB_("P3_v3_strong_field"), 10, "eps = 1.3e-3, for Eot-Wash (38.6 um) at L* = 90 pc"))
v("P3 lab strong-coupling 3.5-7 um", "3.5-7 μm", (D, 81, "3.5–7 μm"), (RB_("P3_v3_strong_field"), 10, "3.5-7 um"))
v("P3 margin 1.7 in k", "margin of only 1.7 in k", (D, 81, "a margin of only 1.7× in k"), (RB_("P3_v3_strong_field"), 102, "a factor 1.7 in k"))
v("P3 pair speeds 1e-4 c, 0.44 c", "0.44 c at a neutron-star surface", (D, 81, "~1e-4 c in the Solar System, 0.44 c at a neutron-star surface"), (RB_("P3_v3_strong_field"), 58, "1.0e-4"), (RB_("P3_v3_strong_field"), 61, "0.44"))
v("P3 metric coupling <= 2.4e-9", "at most at 2.4x10-9", (D, 81, "metric coupling ≤ 2.4e-9"), (RB_("P3_v3_strong_field"), 64, "at most 2.4e-9"))
# P4
v("P4 SPARC rms 0.054 / 0.054 dex", "rms 0.054 / 0.054 dex", (D, 80, "rms 0.054 / 0.054 dex"), (RB_("P4_v3_galaxy_tiles"), 16, "rms 0.054 / 0.054 dex"))
v("P4 median Upsilon 0.52 / 0.44", "median Υ 0.52 / 0.44", (D, 80, "median Υ 0.52 / 0.44 (alt below the 0.50–0.80 window)"), (RB_("P4_v3_galaxy_tiles"), 16, "median Υ 0.52 / 0.44"))
v("P4 frozen window 0.50-0.80", "0.50-0.80 window", (D, 80, "0.50–0.80 window"), (RB_("P4_v3_galaxy_tiles"), 31, "below the frozen window of 0.50–0.80"))
v("P4 chi2 line 63-64%", "(63-64% of galaxies acceptable)", (D, 80, "(63–64 % of galaxies acceptable"), (RB_("P4_v3_galaxy_tiles"), 38, "Only 63–64 % of galaxies"))
v("P4 MeerKAT +0.033 dex", "+0.033 dex against SPARC's same recipe", (D, 80, "MeerKAT local a₀ PASS (+0.033 dex vs SPARC, same recipe)"), (RB_("P4_v3_galaxy_tiles"), 17, "+0.033 dex"))
v("P4 groups +0.010 / -0.010 dex", "(+0.010 / -0.010 dex)", (D, 80, "(+0.010 / −0.010 dex, no supply rule)"), (RB_("P4_v3_galaxy_tiles"), 18, "+0.010 / −0.010 dex"))
v("P4 groups ABOVE LAW at 0.03 a0 (Z 4.7)", "ABOVE LAW at ge = 0.03 a0 (Z 4.7)", (D, 80, "ABOVE LAW at g_e = 0.03 a₀ (Z 4.7)"), (RB_("P4_v3_galaxy_tiles"), 74, "At g_e = 0.03 a₀ they sit at +0.151 / +0.143 dex (Z 4.7 / 4.5, ABOVE LAW)"))
v("P4 MW K_z 92.3 / 96.9 vs 66.4 +- 2.2", "92.3 / 96.9 against 66.4 ± 2.2", (D, 80, "K_z,1.1 92.3 / 96.9 vs 66.4 ± 2.2"), (RB_("P4_v3_galaxy_tiles"), 19, "92.3 / 96.9 against 66.4 ± 2.2"))
v("P4 MW chi2 178 / 251 vs 67.5", "178 / 251 against a line of 67.5", (D, 80, "χ² 178 / 251 vs 67.5"), (RB_("P4_v3_galaxy_tiles"), 19, "χ² 178 / 251 against a line of 67.5"))
v("P4 TDGs -0.59 / -0.62 dex, DF2/DF4 -1.66 / -1.74 ln", "-0.59 / -0.62 dex and -1.66 / -1.74 (ln)", (D, 80, "−0.59 / −0.62 dex and −1.66 / −1.74 ln below v3"), (RB_("P4_v3_galaxy_tiles"), 20, "−0.59 / −0.62 dex (TDGs) and −1.66 / −1.74 ln (DF2/DF4)"))
# S1
v("S1 satellites +1.33 / +1.30 dex at the L* floor", "+1.33 / +1.30 dex above v3 at the L", (D, 77, "+1.33 / +1.30 dex above v3 at the L★ floor"), (RB_("S1_v3_hosted_small"), 7, "+1.33 / +1.30 dex at L★ floor"))
v("S1 +1.72 / +1.68 at 90 pc", "(+1.72 / +1.68 at 90 pc)", (D, 77, "+1.72 / +1.68 at 90 pc"), (RB_("S1_v3_hosted_small"), 40, "+1.715 ± 0.138 | +1.681"))
v("S1 EFE costs +0.58 dex", "costs +0.58 dex", (D, 77, "the EFE costs +0.58 dex"), (RB_("S1_v3_hosted_small"), 7, "adds +0.58 / +0.57 dex"))
v("S1 Coma UDGs +1.12 / +1.08 dex at z +4.3-4.7", "+1.12 / +1.08 dex at zsys +4.3 to +4.7", (D, 77, "+1.12 / +1.08 dex at z +4.3–4.7"), (RB_("S1_v3_hosted_small"), 8, "z_sys +4.3 / +4.1 at dmean, +4.7 / +4.5 at dproj"), (RB_("S1_v3_hosted_small"), 8, "+1.12 dex above v3"))
# U1
v("U1 T1 14,373 equilibria, ratio 0.666", "(14,373 equilibria; largest ratio 0.666)", (D, 85, "14,373 equilibria, max ratio 0.666"), (RB_("U1_v3_dust_content"), 8, "14,373 equilibria"), (RB_("U1_v3_dust_content"), 9, "the largest ratio is 0.666"))
v("U1 satellites +2.00 / +1.99 dex STRUCTURAL", "satellites +2.00 / +1.99 dex, STRUCTURAL", (D, 85, "satellites +2.00 / +1.99 dex STRUCTURAL"), (RB_("U1_v3_dust_content"), 133, "+2.00 ± 0.08 / +1.99 ± 0.07"))
v("U1 abstract +2.00 / +1.99 dex", "Satellites then sit +2.00 / +1.99 dex and Coma's UDGs +1.41 dex above v3: STRUCTURAL", (D, 85, "Coma UDGs +1.41 dex, z 5.4 STRUCTURAL"))
v("U1 Coma +1.41 dex, z 5.4", "+1.41 dex (zsys 5.4)", (D, 85, "Coma UDGs +1.41 dex, z 5.4 STRUCTURAL"), (RB_("U1_v3_dust_content"), 134, "+1.41 dex, z_sys 5.4"))
v("U1 TDGs +0.055 +- 0.114 NATIVE PASS", "(+0.055 ± 0.114 dex)", (D, 85, "TDGs (+0.055 ± 0.114 dex) and DF2/DF4 NATIVE PASS"), (RB_("U1_v3_dust_content"), 135, "+0.055 ± 0.114"))
v("U1 DF2/DF4 NATIVE pass", "DF2/DF4 a NATIVE PASS", (D, 85, "DF2/DF4 NATIVE PASS"), (RB_("U1_v3_dust_content"), 136, "NATIVE pass"))
v("U1 MW v_c(R0) <= 216 / 221 vs 229 +- 4.6", "≤ 216 / 221 km/s in every branch, against 229 ± 4.6", (D, 85, "MW v_c(R₀) ≤ 216 / 221 vs 229 ± 4.6"), (RB_("U1_v3_dust_content"), 138, "≤ 215.6 / 220.6 km/s in every branch vs Eilers 229.1 ± 4.6"))
v("U1 field galaxies V_rel <= 1.8 km/s", "(relative speed at most 1.8 km/s)", (D, 85, "linear V_rel ≤ 1.8 km/s"), (RB_("U1_v3_dust_content"), 175, "σ_rel ≤ 1.8 km/s"))
v("U1 UMa 12.6-14.4 sigma", "(12.6-14.4σ per galaxy)", (D, 85, "12.6–14.4σ per galaxy"), (RB_("U1_v3_dust_content"), 169, "(12.6 / 13.4σ)"), (RB_("U1_v3_dust_content"), 172, "(13.6 / 14.4σ)"))
v("U1 MW K_z STRUCTURAL / history-dependent", "STRUCTURAL in the literal theory and history-dependent for multi-stream dust", (D, 85, "MW K_z STRUCTURAL in the literal theory (multi-stream hot round dust: history-dependent)"), (RB_("U1_v3_dust_content"), 16, "MW K_z is STRUCTURAL in literal v3 and HISTORY-DEPENDENT for multi-stream dust"))
v("U1 what would have to change", "What would have to change: the dust coupling (and J)", (D, 85, "What would have to change: the dust coupling (and J)"))
# T1
v("T1 FOOTING SPLIT, FRAGILE", "FOOTING SPLIT, FRAGILE", (D, 83, "FOOTING SPLIT, FRAGILE"), (RB_("T1_efe_strength"), 10, "FOOTING SPLIT, and FRAGILE on both footings"))
v("T1 eps-hat 0.02, 95% [0, 0.26]", "= 0.02, 95% interval [0, 0.26]", (D, 83, "ε̂ 0.02, 95 % [0, 0.26]"), (RB_("T1_efe_strength"), 11, "ε̂ = 0.02, 95 % interval [0, 0.26]"))
v("T1 alt dchi2 7.96 < 9", "7.96 against a line of 9", (D, 83, "Δχ² 7.96 < 9"), (RB_("T1_efe_strength"), 12, "Δχ² 7.96, under the frozen line of 9"))
v("T1 p = 0.023 / 0.014", "p = 0.023 / 0.014", (D, 83, "p = 0.023 / 0.014"), (RB_("T1_efe_strength"), 18, "p = 0.023 / 0.014"))
v("T1 Coma eps <= 0.21 / 0.24", "≤ 0.21 / 0.24", (D, 83, "ε ≤ 0.21 / 0.24"), (RB_("T1_efe_strength"), 16, "ε ≤ 0.21 / 0.24"))
v("T1 P2 eps >= 0.67 / 0.81", "≥ 0.67 / 0.81", (D, 83, "ε ≥ 0.67 / 0.81"), (RB_("T1_efe_strength"), 16, "ε ≥ 0.67 / 0.81"))
v("T1 satellites +0.91 / +0.89 dex at eps = 0", "+0.91 / +0.89 dex above", (D, 83, "+0.91 / +0.89 dex"), (RB_("T1_efe_strength"), 47, "+0.91 / +0.89 dex"))
v("T1 residual slope +0.76 +- 0.26", "(slope +0.76 ± 0.26 at", (D, 83, "+0.76 ± 0.26 at ε = 0"), (RB_("T1_efe_strength"), 50, "+0.76 ± 0.26 dex per dex at ε = 0"))
v("T1 globular floor 21.7 -> 28.4 pc", "rise from 21.7 to 28.4 pc", (D, 83, "L★_95 21.7 → 28.4 pc at ε = 0"), (RB_("T1_efe_strength"), 60, "28.42 / 29.25 pc at ε = 0"))
# S2
v("S2 blue 0.88 / 0.80 (2.9 sigma)", "0.88 (canonical, PASS but fragile) / 0.80 (alternative, 2.9σ short)", (D, 76, "Blue: data/v3 0.88 (canonical, PASS-fragile) / 0.80 (alt, 2.9σ short)"), (RB_("S2_v3_lowg_lensing"), 21, "0.802 ± 0.067 between (−2.9σ)"))
v("S2 red inventory 1.31 / 1.20", "1.31 / 1.20 short", (D, 76, "inventory alone 1.31 / 1.20 short"), (RB_("S2_v3_lowg_lensing"), 22, "1.313 ± 0.063 / 1.200 ± 0.058 short"))
v("S2 red with CFG667 + IMF 1.02 / 0.93", "1.02 / 0.93, consistent", (D, 76, "1.02 / 0.93, consistent"), (RB_("S2_v3_lowg_lensing"), 24, "1.023 ± 0.049 / 0.935 ± 0.045 consistent"))
# P2
v("P2 2,251 lenses", "2,251 GAMA", (D, 78, "2,251 GAMA host-vetoed lenses"), (RB_("P2_spec_isolated_lensing"), 5, "N = 2,251"))
v("P2 separation 0.87 / 0.96 sigma", "only 0.87σ / 0.96σ", (D, 78, "by only 0.9σ"), (RB_("P2_spec_isolated_lensing"), 41, "S = 0.87σ (canonical) / 0.96σ (alt)"))
v("P2 22,000-26,500 needed", "about 22,000-26,500 are needed", (D, 78, "~22,000–26,500 needed"), (RB_("P2_spec_isolated_lensing"), 6, "N ≈ 26,500 (canonical) / 22,000 (alt)"))
v("P2 2.8-3.0 sigma below zero-field", "2.8-3.0σ below zero-field v3", (D, 78, "The data sit 2.8–3.0σ BELOW zero-field v3"), (RB_("P2_spec_isolated_lensing"), 13, "(canonical, 2.8σ)"), (RB_("P2_spec_isolated_lensing"), 14, "(alt, 3.0σ)"))
v("P2 catalogue field y_e ~ 6.6e-5", "6.6x10-5", (D, 78, "y_e ≈ 6.6e-5"), (RB_("P2_spec_isolated_lensing"), 17, "Median y_e for the S3 lenses: 6.6e-5"))
v("P2 F2 tolerance 3e-5 does not survive", "does not survive spectroscopic isolation", (D, 78, "F2's 'tolerates only y_e ≲ 3e-5' does not survive spectroscopic isolation"), (RB_("P2_spec_isolated_lensing"), 11, "y_e ≲ 3e-5"))
# S3
v("S3 MW slope -0.126 / -0.114 vs -0.325", "-0.126 / -0.114 against the data's -0.325", (D, 82, "law slope −0.126 / −0.114 vs data −0.325"), (RB_("S3_v3_mw_seals"), 5, "is −0.126"), (RB_("S3_v3_mw_seals"), 6, "(canonical) / −0.114 (alt) on Ou+24. The data slope is −0.325"))
v("S3 Z -4.37 / -4.62 (abstract and body)", "Z = -4.37 / -4.62", (D, 82, "Z −4.37 / −4.62"), (RB_("S3_v3_mw_seals"), 6, "Z −4.37 / −4.62"))
v("S3 record round rule -3.63 / -3.90", "(-3.63 / -3.90)", (D, 82, "worse than the record's −3.63 / −3.90"), (RB_("S3_v3_mw_seals"), 7, "RM-v gave Z −3.63 / −3.90"))
v("S3 15-27.5 kpc", "at 15-27.5 kpc", (RB_("S3_v3_mw_seals"), 5, "v3's 15–27.5 kpc slope"))
v("S3 kappa 0.499 +- 0.116 / 0.413 +- 0.096", "κΛ = 0.499 ± 0.116 and κcrit = 0.413 ± 0.096", (D, 82, "κ_Λ 0.499 ± 0.116, κ_crit 0.413 ± 0.096"), (RB_("S3_v3_mw_seals"), 9, "0.499 ± 0.116"), (RB_("S3_v3_mw_seals"), 10, "0.413 ± 0.096"))
v("S3 1/2 at 0.01 / 0.82 sigma", "at 0.01σ and 0.82σ", (D, 82, "(½ at 0.01σ / 0.82σ)"), (RB_("S3_v3_mw_seals"), 9, "(½ at 0.01σ)"), (RB_("S3_v3_mw_seals"), 10, "(½ at 0.82σ)"))
v("S3 CONSISTENT, NOT DISCRIMINATING", "CONSISTENT, NOT DISCRIMINATING", (D, 82, "κ CONSISTENT, NOT DISCRIMINATING"), (RB_("S3_v3_mw_seals"), 10, "CONSISTENT BUT NOT DISCRIMINATING"))
v("S3 ring-singularity record error", "ring-singularity noise", (D, 82, "CFG493's v2_disc has ring-singularity noise"))
v("S3 DR4 MW seal 15b7e6ff", "SEALED_V3_MW_DR4.json (sha256 15b7e6ff", (D, 82, "SEALED_V3_MW_DR4.json` (sha256 15b7e6ff"), (RB_("S3_v3_mw_seals"), 17, "15b7e6ffb0a340248e111d83a4dd214492f0f2e3b2294e5ff23d6542da3b6160"))
v("S3 ALMA seal b5d65a5e", "SEALED_V3_ALMA_AQUAL.json (sha256 b5d65a5e", (D, 82, "SEALED_V3_ALMA_AQUAL.json` (sha256 b5d65a5e"), (RB_("S3_v3_mw_seals"), 24, "b5d65a5e17bbce21c3ca2f3cd748169fe736e9b86281ff1329449176e1a8c11d"))
v("S3 P6 asymmetry 3.0 / 5.2 / 8.2% at 20 / 30 / 60 kpc", "3.0 / 5.2 / 8.2% at 20 / 30 / 60 kpc", (D, 82, "3.0 / 5.2 / 8.2 % at 20 / 30 / 60 kpc"), (RB_("S3_v3_mw_seals"), 21, "1.8 / 3.0 / 4.1 / 5.2 / 8.2 % at R = 15 / 20 / 25 / 30 / 60 kpc"))
v("S3 GS4 +0.03 to +0.05 dex", "+0.03 to +0.05 dex more", (D, 82, "GS4 +0.03–0.05 dex in V²_bar"), (RB_("S3_v3_mw_seals"), 26, "+0.03 to +0.05 dex more"))
# S4
v("S4 SCOPED NO-GO", "SCOPED NO-GO.", (D, 87, "Clusters: SCOPED NO-GO for every allowed μ_K"), (RB_("S4_v3_muK_clusters"), 3, "SCOPED NO-GO (R6)"))
v("S4 0 of 1,804", "(0 of 1,804)", (D, 87, "0 of 1,804 (μ_K, Δ) cells pass even one cluster cell"), (RB_("S4_v3_muK_clusters"), 9, "0 of 1,804 cell-rows"))
v("S4 best chi2 33.0 / 27.5 vs 11.07", "33.0 / 27.5 against 11.07", (D, 87, "the law's own 33.0 / 27.5 vs 11.07"), (RB_("S4_v3_muK_clusters"), 58, "33.0 / 27.5"))
v("S4 H2 identity to 0.0058", "(reproduced to 0.0058)", (D, 87, "(reproduced to 0.0058)"), (RB_("S4_v3_muK_clusters"), 38, "to 0.0058"))
v("S4 mu_K <= 0.1 unchanged to 1-2%", "unchanged to 1-2%", (D, 87, "μ_K ≤ 0.1 Mpc⁻¹ leaves clusters unchanged to 1–2 %"))
v("S4 A_MID 1.33 / -3.84 / -9.86", "AMID = 1.33 / -3.84 / -9.86", (D, 87, "A_MID 1.33 / −3.84 / −9.86"), (RB_("S4_v3_muK_clusters"), 63, "1.33 / −1.31 / 211"), (RB_("S4_v3_muK_clusters"), 65, "−3.84 / 14.4 / 344"), (RB_("S4_v3_muK_clusters"), 67, "−9.86 / 21.7 / 218"))
v("S4 outer lensing +110 at 0.1 /Mpc", "+110 already at 0.1 Mpc-1", (D, 87, "outer lensing Δχ² +110 already at 0.1 Mpc⁻¹"), (RB_("S4_v3_muK_clusters"), 94, "274 (+110)"))
v("S4 negative dust 46-89%", "46-89% of the cluster volume", (D, 87, "negative absolute dust over 46–89 % of the cluster volume for μ_K ≥ 0.3"), (RB_("S4_v3_muK_clusters"), 148, "0.66 / 0.89 / 0.78 / 0.46 at μ_K = 0.3 / 0.5 / 0.7 / 1"))
# P1
v("P1 need-to-supply 0.463 / 0.445", "0.463 / 0.445", (D, 74, "0.46 (canonical) / 0.45 (alt)"), (RB_("P1_dwarf_chemistry"), 6, "Median q = L_req / L_MDF = 0.463"), (RB_("P1_dwarf_chemistry"), 6, "0.445"))
v("P1 10 systems too narrow", "(10 systems too narrow)", (D, 74, "(10 systems too narrow"), (RB_("P1_dwarf_chemistry"), 11, "10 systems are too narrow"))
v("P1 not robust at 2 sigma: 1.12 / 1.08", "median 1.12 / 1.08 with every width", (D, 74, "the median is 1.12 / 1.08"), (RB_("P1_dwarf_chemistry"), 23, "the median q is 1.12 canonical / 1.08"))
v("P1 pre-enrichment raises the supply", "pre-enrichment raises the supply", (D, 74, "Pre-enrichment raises the supply"), (RB_("P1_dwarf_chemistry"), 19, "Pre-enrichment raises L; it does not lower it."))
# J1, K1, M2
v("J1 FAILS, not in either action", "a potential-depth selector, which neither action contains (J1)", (D, 70, "FAILS.** Not in either action"), (RB_("J1_potential_selector"), 3, "FAILS, on both footings. It is not in the action"))
v("K1 FAILS for every closure", "a braneworld Weyl term, for every closure (K1)", (D, 71, "FAILS** for every closure on both footings"), (RB_("K1_braneworld_weyl"), 7, "FAILS (frozen rule), on both footings, for every closure"))
v("M2 FAILS; screening never reaches clusters", "which never reaches cluster scales (M2)", (D, 73, "L★ screening never touches cluster scales"), (RB_("M2_cluster_compact"), 7, "FAILS (frozen rule), on both footings"))
# disclosures (checks from README, file:line)
v("D P3 17/18", "P3 scores 17/18", (RB_("P3_v3_strong_field"), 13, "Checks: 17/18 PASS, exit 1"))
v("D H4 13/14", "H4 scores 13/14", (RB_("H4_v3_saddle_stability"), 41, "Checks: 13/14 PASS, exit 1"))
v("D U1 15/16", "U1 scores 15/16", (RB_("U1_v3_dust_content"), 25, "15/16 PASS"))
v("D S3 28/31", "S3 scores 28/31", (RB_("S3_v3_mw_seals"), 34, "28/31 checks PASS"))
v("D S4 frozen UNDECIDED, CANNOT under A1", "its CANNOT is under amendment A1, written after test runs and before production", (RB_("S4_v3_muK_clusters"), 5, "UNDECIDED, because the frozen K5 and K7 lines fail"), (RB_("S4_v3_muK_clusters"), 6, "written after test runs and before production"))
v("D Q6 frozen V2/V3/V5 failed, A3 post-result", "Q6's frozen V2, V3 and V5 validation gates failed", (RB_("Q6_v3_class"), 97, "The frozen V2, V3 and V5 gates FAILED. The native numbers rest on the post-result gates of AMENDMENT A3."))
v("D L1 KB frozen FAILED", "L1's frozen KB check failed", (RB_("L1_khronon_pm"), 6, "KB as frozen FAILED"))
v("D C7 A4 post-result", "C7's amendment A4 is post-result", (C7R, 156, "A4 (post-result)"))

# table 2: verdict on the draft row, row in the TeX, and the draft commit added that lane's row
T2 = {"M1": ("0eeb77c747", 75, "ERRATUM (M1"), "Q6": ("c7cc6f9e61", 79, "Literal v3 has no radiation era"), "Q7": ("428e689b49", 84, "fixes BBN only"),
      "C7": ("0d39e739a6", 72, "v4 RUNS AWAY on FRW"), "H4": ("9fe0dcb5b5", 86, "ILL-POSED"), "I1": ("1b5444fb47", 37, "v4 is ILL-POSED wherever the aether twists"),
      "P3": ("c9f7f1cc09", 81, "PASS on all five, two scoped"), "P4": ("433e29eb85", 80, "SPARC RAR CONDITIONAL"), "S1": ("244f4468f6", 77, "both FAIL"),
      "U1": ("428e689b49", 85, "NATIVE PASS"), "T1": ("dc6d6a3e1e", 83, "FOOTING SPLIT, FRAGILE"), "S2": ("bc441b4656", 76, "both CONDITIONAL"),
      "P2": ("244f4468f6", 78, "UNDECIDABLE (N too small)"), "S3": ("52286e05ee", 82, "SHAPE EXCLUDED"), "S4": ("45bd132464", 87, "SCOPED NO-GO"),
      "P1": ("7602bc3238", 74, "SUPPLY CONFIRMED for the median, not robust at 2σ"), "J1": ("a410688c53", 70, "FAILS"), "K1": ("52360cde46", 71, "FAILS"), "M2": ("0944553f40", 73, "FAILS")}
for lane, (h, ln, verdict) in T2.items():
    added = [l for l in git("show", "--format=", h, "--", DRAFT).stdout.splitlines() if l.startswith("+") and re.search(r"\b" + lane + r"\b", l)]
    row = [l for l in tex.splitlines() if l.startswith(lane + " & ") and l.rstrip("\\\\").endswith(h)]
    check(f"T2 {lane}: draft {DRAFT}:{ln} has '{verdict}'; commit {h} adds the row; TeX row cites it",
          norm(verdict) in LN(DRAFT, ln) and bool(added) and len(row) == 1 and row[0].rstrip("\\\\").endswith(h), f"{DRAFT}:{ln}")
l1row = [l for l in tex.splitlines() if l.startswith("L1 & ")]
check("T2 L1 row: production in progress (no result)", len(l1row) == 1 and "production in progress (no result)" in l1row[0])

# plain statements required in the abstract and conclusions
for s in ("The covariant candidate v3 is ill-posed wherever the khronon density is negative", "v3 also fails several structural tests",
          "What the data require of any successor is a cold component that binds in hosted systems and in clusters, and grows like dust",
          "The covariant candidate is ill-posed at saddles", "v3 fails several structural tests",
          "What the data require of any successor: a cold component that binds in hosted systems and in clusters, and grows like dust",
          "No result here is evidence for the framework over its rivals", "Changes in v1.1 (2026-10-23)", "Erratum M1"):
    has(f"S plain statement '{s[:50]}'", s)
check("S erratum: J'(0) = -1 no longer given as the cause", "so the Newtonian term vanishes on FRW, and" not in flat and "its free function has J" not in flat)

print(f"\nPAPER59 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
