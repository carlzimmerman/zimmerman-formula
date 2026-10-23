#!/usr/bin/env python3
"""PAPER60 audit: the built PDF must be newer than the TeX; every quoted number must match the committed lane outputs
(rebuild_2026_10_22/ P3, P4, S1-S4, T1, U1, M1, Q6, Q7, H4, I1, F1, F3; covariant_push_2026_10_22/ C6, C7, C8;
doors_push_2026_10_22/ D10, E2: *_results.json, else the lane's .out or README); every cited commit must exist and touch
its lane; the two seal hashes are recomputed from the sealed files; the PENDING statement (no L1 production result) must
be true at build time, else this audit FAILS until the paper is updated; citations must match citations/REFERENCES.bib;
no forbidden claim, local path or personal name may appear.
Run: python3 PAPER60_audit.py (exit 0 only if all pass).
     python3 PAPER60_audit.py --mutate (perturbs the last digit of every JSON-formatted number; exit 0 only if every
     such check then FAILS, i.e. each number check is live).  Read-only."""
import hashlib, json, os, re, subprocess, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RB = os.path.join(ROOT, "rebuild_2026_10_22")
CV = os.path.join(ROOT, "covariant_push_2026_10_22")
DP = os.path.join(ROOT, "doors_push_2026_10_22")
TEX = os.path.join(HERE, "PAPER60_scope_of_the_screened_theory_2026.tex")
PDF = os.path.join(HERE, "PAPER60_scope_of_the_screened_theory_2026.pdf")
ZJ = os.path.join(HERE, "PAPER60_scope_of_the_screened_theory_2026.zenodo.json")
F = 0
N = 0
NUM = []  # (name, caught) for the mutate mode


def check(name, ok, msg=""):
    global F, N
    N += 1
    if not MUT:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    F += (not ok)


SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("ﬃ", "ffi"), ("−", "-"), ("–", "-"), ("—", "-"), ("’", "'"), ("‘", "'"),
                 (" ", " "), ("µ", "μ"), ("∆", "Δ"), ("ϕ", "φ"), ("∗", "*"), ("**", ""), ("\\|", "|"), ("⋆", "★"), ("ϵ", "ε")):
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
    """value -> how the PDF renders m\\times10^{e} after norm, e.g. 4.8x107, 2.7x10-28"""
    m, e = f"{x:.{d}e}".split("e")
    return f"{m}x10{int(e)}"


def bump(s):
    """change the last digit of s (mutation)"""
    for i in range(len(s) - 1, -1, -1):
        if s[i].isdigit():
            return s[:i] + str((int(s[i]) + 1) % 10) + s[i + 1:]
    return s + "9"


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


def num(name, value_str, ctx):
    """value_str is formatted from a committed JSON value; ctx (with {}) is the PDF wording around it"""
    if MUT:
        s = norm(ctx.format(bump(value_str)))
        NUM.append((name, s not in flat))
        return
    s = norm(ctx.format(value_str))
    check(name, s in flat, s)


def JS(base, lane, fname):
    return json.load(open(os.path.join(base, lane, fname)))


def TX(base, lane, fname="README.md"):
    return norm(open(os.path.join(base, lane, fname), encoding="utf-8").read())


def rd(name, base, lane, fname, s, pdf_s=None):
    """s must be in the lane file AND (s, or pdf_s) in the PDF"""
    s, p = norm(s), norm(pdf_s or s)
    check(name, s in TX(base, lane, fname) and p in flat, f"{lane}/{fname}: '{s}'" + (f" / PDF '{p}'" if pdf_s else ""))


def outline(base, lane, fname):
    m = re.findall(r"COMPLETE: (\d+)/(\d+) checks PASS", open(os.path.join(base, lane, fname), encoding="utf-8").read())
    return f"{m[-1][0]}/{m[-1][1]}" if m else None


f2 = lambda x: f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
pm = lambda x: f"{x:+.2f}"

# ---------------------------------------------------------------- B. source document, board and settings
th = git("show", "45bd132464:covariant_push_2026_10_22/THEORY_V3_DRAFT.md").stdout
check("B THEORY_V3_DRAFT at 45bd132464 has the S4 and H4 rows, cited", "SCOPED NO-GO for every allowed μ_K" in th and "ILL-POSED" in th and "45bd132464" in flat)
board = git("show", "fc50a03878:explainers/make_status_board.py").stdout
check("B board at fc50a03878 (v3 only, tidal dwarfs green via U1), cited", "VERIFIED_GREEN" in board and "pass (U1: v3's own dynamics)" in board and "fc50a03878" in flat)
has("B footings", "(9.36x10-11 and 1.13x10-10 m s-2")
has("B kappa fitted, not closed", "is fitted; the theory is not closed")
has("B never pooled", "never pooled")

# ---------------------------------------------------------------- C. lane table: checks, verdicts and commits
LANES = {  # lane: (out file, checks, README verdict substring, PDF table verdict, commits)
    "P3_v3_strong_field": ("p3_v3_strong_field.out", "17/18", "PASS (estimate)", "PASS (five tiles, two scoped)", ["f28b8c6a92", "2b067f2813"]),
    "P4_v3_galaxy_tiles": ("p4_v3_galaxy_tiles.out", "11/11", "Verdict: CRISP FINDING", "CRISP FINDING", ["6c5e6161b9", "6c0249a8bc"]),
    "S1_v3_hosted_small": ("s1_v3_hosted_small.out", "10/10", "FAIL, ROBUST", "both FAIL", ["25c5861b57", "2b6bb658a1"]),
    "S2_v3_lowg_lensing": ("s2_v3_lowg_lensing.out", "8/9", "## Verdicts", "both CONDITIONAL", ["c94150c05d", "0a3db18162"]),
    "S3_v3_mw_seals": ("s3_v3_mw_seals.out", "28/31", "## Verdict: CRISP FINDING", "CRISP FINDING", ["8f6c6587e1", "a2e4a36598"]),
    "S4_v3_muK_clusters": ("s4_v3_muk_clusters.out", "8/8", "## Verdict: SCOPED NO-GO (R6)", "SCOPED NO-GO", ["f167979b09", "0ef14fdd9a"]),
    "T1_efe_strength": ("t1_efe_strength.out", "10/11", "FOOTING SPLIT, and FRAGILE on both footings", "FOOTING SPLIT", ["0fbdb17c87", "31e3c85bf6"]),
    "U1_v3_dust_content": ("u1_v3_dust_content.out", "15/16", "## Verdict: CRISP FINDING", "CRISP FINDING", ["edb372c22d", "54ee83e54e"]),
    "M1_trilemma": ("m1_trilemma.out", "11/11", "NO-GO (linear growth, theorem for a stated class)", "NO-GO", ["3298c74815", "836cc3661f"]),
    "Q6_v3_class": ("q6_derive.out", "19/19", "## Verdict: CRISP FINDING", "CRISP FINDING", ["386ab3c2bb", "ed5894d6e1"]),
    "Q7_bs25_cosmology": ("q7_source.out", "11/11", "(B): BS25's sector fixes BBN only; linear growth still fails.", "(B) BBN ONLY", ["6dac2d6486", "142d9d8ccd"]),
    "H4_v3_saddle_stability": ("h4_v3_saddle_stability.out", "13/14", "ILL-POSED.", "ILL-POSED", ["b8860b6666", "58bf38dcb3"]),
    "I1_gammaL_causality": ("i1_gammal_causality.out", "9/9", "ILL-POSED (where the aether twists)", "ILL-POSED", ["d5e8ba9842", "81af28477c"]),
}
for lane, (out, chk, rv, pv, commits) in LANES.items():
    tag = lane.split("_")[0]
    check(f"C {tag} checks {chk} (.out), in table", outline(RB, lane, out) == chk and re.search(rf"\n{tag} &[^\n]*& {re.escape(chk)}", tex) is not None, f"{outline(RB, lane, out)}")
    check(f"C {tag} verdict (README) and table", norm(rv) in TX(RB, lane) and re.search(rf"\n{tag} &[^\n]*& {re.escape(pv)}", tex) is not None, rv)
    for h in commits:
        files = git("show", "--name-only", "--format=", h).stdout
        check(f"C {tag} commit {h} touches lane, cited", f"rebuild_2026_10_22/{lane}/" in files and h in flat)
check("C S4 frozen rule UNDECIDED, A1 CANNOT (.out)", "VERDICT (frozen rule): UNDECIDED" in open(os.path.join(RB, "S4_v3_muK_clusters", "s4_v3_muk_clusters.out")).read()
      and "VERDICT (AMENDMENT A1 gates): CANNOT" in open(os.path.join(RB, "S4_v3_muK_clusters", "s4_v3_muk_clusters.out")).read() and "the frozen rule reads UNDECIDED" in flat)
check("C Q6 validation 8/12, native 6/6 (.out)", outline(RB, "Q6_v3_class", "q6_validate.out") == "8/12" and outline(RB, "Q6_v3_class", "q6_native.out") == "6/6" and "validation 8/12" in flat and "native 6/6" in flat)
q7v = re.findall(r"COMPLETE: (\d+)/(\d+)", open(os.path.join(RB, "Q7_bs25_cosmology", "q7_validate.out")).read())[-1]
q7n = re.findall(r"COMPLETE: (\d+)/(\d+)", open(os.path.join(RB, "Q7_bs25_cosmology", "q7_native.out")).read())[-1]
check("C Q7 validation 12/14, native 6/7 (.out)", q7v == ("12", "14") and q7n == ("6", "7") and "validation 12/14; native 6/7" in flat)

# ---------------------------------------------------------------- D. what passes (Table 2)
p4 = JS(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")["tiles"]
mk = p4["T2"]["rows"]["REST|nu1"]
num("D P4 MeerKAT a0 (JSON)", f"{sci(mk['a0'], 2)} against SPARC's {sci(mk['a0_sparc'], 2)}", "{}")
num("D P4 MeerKAT offset (JSON)", f"{mk['dlog_M_minus_S']:+.3f}", "with the same recipe: {} dex")
num("D P4 MeerKAT offset, abstract (JSON)", f"{mk['dlog_M_minus_S']:+.3f}", "sits {} dex from SPARC's")
g3 = p4["T3"]["footings"]
num("D P4 groups isolated (JSON)", f"{g3['canonical']['v3_isolated']['mean']:+.3f} / {g3['alt']['v3_isolated']['mean']:+.3f}", "{} dex from the law")
num("D P4 groups EFE Z (JSON)", f"{g3['canonical']['EFE_sensitivity']['ge=0.03']['Z']:.2f}", "(Z = {})")
u1 = JS(RB, "U1_v3_dust_content", "u1_v3_dust_content_results.json")["numbers"]
tdg = u1["N5"]["tdg"]["canonical"]
num("D U1 TDGs (JSON)", f"{tdg['TDG_B0']['rbar']:+.3f} ± {tdg['TDG_B0']['se']:.3f}", "{} dex")
num("D U1 DF2/DF4 (JSON)", f"{tdg['DF_B0']['r'][0]:+.2f} / {tdg['DF_B0']['r'][1]:+.2f}", "DF2/DF4 {} in ln")
c6 = JS(CV, "C6_literal_cassini", "c6_literal_cassini_results.json")
R1 = c6["R1_physical"]
check("D C6 all 24 cells pass Hees and Park (JSON)", len(R1) == 24 and all(v["hees"] and v["park"] for v in R1.values()) and "all 24 cells pass Hees and Park" in flat)
mg = c6["R1_margin"]
num("D C6 margin (JSON)", f"{sci(mg['Hees_min'], 1)} to {sci(mg['Hees_max'], 1)}", "by {}")
rd("D C6 frozen UNDECIDED (README)", CV, "C6_literal_cassini", "README.md", "By the frozen verdict rule: UNDECIDED", "the frozen rule reads UNDECIDED on one rounding check")
rd("D C6 Mars (README)", CV, "C6_literal_cassini", "README.md", "Mars 0.173", "Mars at 0.173 of its bound")
d10 = JS(DP, "D10_native_Lstar", "d10_native_lstar_results.json")
v10 = d10["verdict"]
num("D D10 floor (JSON)", f"{v10['canonical']['central']:.2f} / {v10['alt']['central']:.2f}", "L★ ≥ {} pc")
dq = [v["dchi2_AQUAL"] for v in d10["band_cells"].values()]
num("D D10 cells (JSON)", f"{len(dq)}", "excluded in all {} cells")
check("D D10 unscreened excluded in every cell (JSON)", v10["canonical"]["AQUAL_excluded_all_cells"])
c8 = JS(CV, "C8_instantaneous", "c8_instantaneous_results.json")
dv = max(c8["K9"]["canonical_Earth_surface_g"]["dv_over_c"], c8["K9"]["alt_Earth_surface_g"]["dv_over_c"])
num("D C8 GW (JSON)", sci(dv, 1), "(Δv/c ≤ {})")
num("D C8 pulsars (JSON)", sci(c8["K7"]["worst_ratio"], 1), "at most {} of the double pulsar")
p3 = JS(RB, "P3_v3_strong_field", "p3_v3_strong_field_results.json")
ws = p3["worst_shifts"]
num("D P3 shape shifts (JSON)", sci(max(ws["r_isco"][0], ws["r_ph"][0], ws["shadow_local"][0]), 1), "shape shifts ≤ {}")
num("D P3 ringdown (JSON)", sci(ws["f_qnm"][0], 1), "ringdown ≤ {}")
num("D P3 neutron stars, 1.4 Msun and maximum mass (JSON)", sci(max(abs(v["dlnR"]) for v in p3["NS"].values()), 1), "|ΔR/R| ≤ {}")
num("D P3 neutron stars, 1.4 Msun only (JSON, disclosed)", sci(max(abs(v["dlnR"]) for k, v in p3["NS"].items() if k.startswith("1.4|")), 1), "draft's {} is the 1.4")
check("D P3 all five verdicts PASS (JSON)", sorted(k for k in p3["verdicts"] if re.match(r"V[1-5]_", k)) == ["V1_black_holes", "V2_ringdown", "V3_neutron_stars", "V4_strong_coupling", "V5_strong_field_leaf"]
      and all(p3["verdicts"][k] == "PASS" for k in p3["verdicts"] if re.match(r"V[1-5]_", k)))
rd("D P3 regular holes need an infalling khronon (README)", RB, "P3_v3_strong_field", "README.md", "infalling", "regular holes need an infalling khronon")
fp = p4["T1"]["footings"]
num("D P4 RAR rms (JSON)", f"{fp['canonical']['L24']['rms']:.3f} / {fp['alt']['L24']['rms']:.3f}", "rms {} dex")
num("D P4 median Upsilon (JSON)", f"{fp['canonical']['L24']['U_median']:.2f} / {fp['alt']['L24']['U_median']:.2f}", "median Υ {}")
num("D P4 acceptable fraction (JSON)", f"{round(100 * fp['canonical']['L24']['frac_p_ok'])}-{round(100 * fp['alt']['L24']['frac_p_ok'])}%", "({} of galaxies acceptable)")
check("D P4 chi2 line fails in every cell (JSON)", all(v is False or v == "FAIL" for v in (p4["T1"]["chi2_line"].values() if isinstance(p4["T1"]["chi2_line"], dict) else [p4["T1"]["chi2_line"]])), str(p4["T1"]["chi2_line"])[:120])
num("D P4 EFE solved for (JSON)", f"{p4['T1']['n_env']}", "external field solved for {}")
s2 = JS(RB, "S2_v3_lowg_lensing", "s2_v3_lowg_lensing_results.json")["cells_central"]
num("D S2 blue at the primary field (JSON)", f"{s2['canonical|R0|noclu|blue']['A']:.2f} / {s2['alt|R0|noclu|blue']['A']:.2f}", "data/v3 {} at the primary field")
num("D S2 red inventory (JSON)", f"{s2['canonical|R0|zero|red']['A']:.2f} / {s2['alt|R0|zero|red']['A']:.2f}", "inventory alone {} short")
num("D S2 red with posits (JSON)", f"{s2['canonical|R2|noclu|red']['A']:.2f} / {s2['alt|R2|noclu|red']['A']:.2f}", "short; {} with the record's")
check("D S2 board's 0.80 is the alt zero-field cell (JSON)", f"{s2['alt|R0|zero|blue']['A']:.2f}" == "0.80" and "0.80 is the alternative footing at zero external field" in flat)
e4 = p3["verdicts"]["numbers"]["E4_worst"]
num("D P3 strong coupling loop factor (JSON)", sci(e4[0], 1), "worst loop factor {} at")
check("D P3 strong coupling at Eot-Wash 38.6 um (JSON)", "Eot-Wash (38.6 um)" in e4[1] and "(38.6 μm)" in flat)
rd("D P3 margin 1.7 in k (README)", RB, "P3_v3_strong_field", "README.md", "a factor 1.7 in k", "a margin of only 1.7 in k")
s3b = JS(RB, "S3_v3_mw_seals", "s3_partB_kappa_results.json")["steps"]["A_aqual_disc"]
num("D S3 kappa (JSON)", f"{s3b['canonical']['kappa']:.3f} ± {s3b['canonical']['kappa_err']:.3f} / {s3b['alt']['kappa']:.3f} ± {s3b['alt']['kappa_err']:.3f}", "{}: consistent")
check("D S3 kappa verdict (JSON)", s3b["canonical"]["verdict"] == "CONSISTENT BUT NOT DISCRIMINATING" and "not discriminating" in flat)
E4c = p3["E4"]
num("D P3 pair speed Solar System (JSON)", sci(E4c["Eot-Wash (38.6 um)|canonical|20pc"]["c_pi"], 0).replace("1x10", "10"), "(about {}")
num("D P3 pair speed NS (JSON)", f"{E4c['NS surface|canonical|20pc']['c_pi']:.2f}", "{}c at a neutron-star surface")
num("D P3 metric coupling (JSON)", sci(p3["verdicts"]["numbers"]["mixing_eps_max"], 1), "at most {}, so")
rd("D P3 corrects 'only tensor modes' (README)", RB, "P3_v3_strong_field", "README.md", "only tensor modes propagate", "only the tensor modes propagate")
check("D P4 MeerKAT double rounding (JSON vs board)", f"{mk['dlog_M_minus_S']:.3f}" == "0.032" and f"{round(mk['dlog_M_minus_S'], 4):.3f}" in ("0.033", "0.032") and "+0.033 dex, line 0.15" in board and "not the board's +0.033" in flat)

# ---------------------------------------------------------------- E. galaxy-scale failures
t4 = p4["T4"]
B1m = t4["models"]["B1_McMillan17"]
num("E P4 MW K_z (JSON)", f"{B1m['canonical']['F0|L24']['K_R0']:.1f} / {B1m['alt']['F0|L24']['K_R0']:.1f}", "Kz = {} against")
num("E P4 MW chi2 (JSON)", f"{B1m['canonical']['F0|L24']['chi2_kz']:.0f} / {B1m['alt']['F0|L24']['chi2_kz']:.0f}", "(χ2 = {} against a line of")
num("E P4 MW line (JSON)", f"{t4['LINE_chi2_0p99']:.1f}", "a line of {})")
check("E P4 MW data 66.4 +- 2.2 (JSON) and four baryon models", t4["data"]["K_R0_data"].startswith("66.4 +- 2.2") and len(t4["models"]) == 4 and "against 66.4 ± 2.2" in flat and "all four baryon models" in flat)
check("E P4 MW tile FAIL (JSON)", p4["T4"]["class"] == "FAIL" and p4["T5"]["class"] == "FAIL")
s3a = JS(RB, "S3_v3_mw_seals", "s3_partA_mw_results.json")
aq = s3a["steps"]["AQ_gamma0"]
num("E S3 law slope (JSON)", f"{aq['canonical']['cells']['Ou24']['slope_census']:.3f} / {aq['alt']['cells']['Ou24']['slope_census']:.3f}", "slope is {} against")
num("E S3 data slope (JSON)", f"{aq['canonical']['cells']['Ou24']['slope_data']:.3f}", "the data's {}")
num("E S3 Z (JSON)", f"{aq['canonical']['combined']['primary']['Z']:.2f} / {aq['alt']['combined']['primary']['Z']:.2f}", "Z = {}, worse")
num("E S3 record Z (JSON)", f"{s3a['step0_old']['canonical|RMv']['primary']['Z']:.2f} / {s3a['step0_old']['alt|RMv']['primary']['Z']:.2f}", "the record's {}")
num("E S3 abstract Z (JSON)", f"{aq['canonical']['combined']['primary']['Z']:.2f} / {aq['alt']['combined']['primary']['Z']:.2f}", "excluded (Z = {})")
num("E U1 T1 equilibria (JSON)", f"{u1['N1']['counts'][0]:,}", "({} equilibria")
num("E U1 T1 max ratio (JSON)", f"{u1['N1']['max_ratio']['frozen']:.3f}", "maximum ratio {})")
rd("E U1 T3 (README)", RB, "U1_v3_dust_content", "README.md", "Held dust is weightless in its host (theorem T3)", "held dust is weightless in a static host")
num("E P4 static TDGs (JSON)", f"{p4['T5']['footings']['canonical']['L24']['T']['rbar']:.2f} / {p4['T5']['footings']['alt']['L24']['T']['rbar']:.2f}", "had them {} dex below v3")
sat = u1["N5"]["satellites"]
num("E U1 satellites (JSON)", f"{sat['canonical']['stats']['B0'][0]:+.2f} / {sat['alt']['stats']['B0'][0]:+.2f}", "satellites fail structurally: {}")
num("E U1 satellites abstract (JSON)", f"{sat['canonical']['stats']['B0'][0]:+.2f} / {sat['alt']['stats']['B0'][0]:+.2f}", "Dwarf satellites ({} dex)")
num("E U1 isolated AQUAL (JSON)", f"{sat['canonical']['stats']['iso_law'][0]:+.2f} / {sat['alt']['stats']['iso_law'][0]:+.2f}", "would leave {})")
s1 = JS(RB, "S1_v3_hosted_small", "s1_v3_hosted_small_results.json")
sk = lambda f_: s1["satellites"][f"{f_}|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]["Delta"]
num("E S1 satellites at the floor (JSON)", f"{sk('canonical'):+.2f} / {sk('alt'):+.2f}", "the gap is {} dex at the")
sc = json.load(open(os.path.join(RB, "T1_efe_strength", "t1_stage_satcoma.json")))["SAT"]
num("E T1 satellites at eps=0 (JSON)", f"{sc['canonical']['curves']['primary_EW']['Delta'][0]:+.2f} / {sc['alt']['curves']['primary_EW']['Delta'][0]:+.2f}", "still sit {} dex high")
t1 = JS(RB, "T1_efe_strength", "t1_efe_strength_results.json")
cmb = t1["combinations"]
num("E T1 GOF p (JSON)", f"{cmb['canonical']['V (primary)']['p_PG']:.3f} / {cmb['alt']['V (primary)']['p_PG']:.3f}", "goodness-of-fit p = {}")
cs = t1["curves_summary"]
num("E T1 Coma eps (JSON)", f"{cs['canonical']['COMA']['interval95'][-1][-1] if isinstance(cs['canonical']['COMA']['interval95'][0], list) else cs['canonical']['COMA']['interval95'][1]:.2f} / "
    f"{cs['alt']['COMA']['interval95'][-1][-1] if isinstance(cs['alt']['COMA']['interval95'][0], list) else cs['alt']['COMA']['interval95'][1]:.2f}", "Coma wants ε ≤ {} of")
lo = lambda iv: (iv[0][0] if isinstance(iv[0], list) else iv[0])
num("E T1 P2 eps (JSON)", f"{lo(cs['canonical']['LENS-P2']['interval95']):.2f} / {lo(cs['alt']['LENS-P2']['interval95']):.2f}", "lensing wants ε ≥ {})")
check("E T1 class FOOTING SPLIT (JSON)", t1["verdict"]["lane"] == "FOOTING SPLIT")
cm = u1["N5"]["coma"]["canonical"]["B0"]
num("E U1 Coma (JSON)", f"{cm['dex']:+.2f} dex (z = {cm['z_sys']:.1f})", "galaxies fail: {}")
num("E U1 Coma abstract (JSON)", f"{cm['dex']:+.2f}", "galaxies ({} dex)")
ck = lambda f_: s1["coma"][f"{f_}|S4 v3 dmean L*floor E-W"]["meanE_dex"]
num("E S1 Coma static (JSON)", f"{ck('canonical'):+.2f} / {ck('alt'):+.2f}", "; {} dex in the static host field")
n6 = u1["N6"]
num("E U1 MW v_c bound (JSON)", f"{n6['canonical']['vc_R0_bound']:.1f} / {n6['alt']['vc_R0_bound']:.1f}", "at most {} km s-1")
num("E U1 MW v_c data (JSON)", f"{n6['canonical']['vc_Eilers_R0']:.1f} ± {n6['canonical']['e_vc_Eilers']:.1f}", "against {}")
rd("E U1 what would have to change (README)", RB, "U1_v3_dust_content", "README.md", "The dust coupling (T3)", "what would have to change is the dust coupling")

# ---------------------------------------------------------------- F. clusters (F1, H2, S4)
f1 = JS(RB, "F1_cluster_cores", "f1_cluster_cores_results.json")
rows = f1["rows"]
pc = [rows[f"PRIMARY {h}"]["canonical"]["MID"][0] for h in ("h0672", "h0686")]; pa = [rows[f"PRIMARY {h}"]["alt"]["MID"][0] for h in ("h0672", "h0686")]
bc = [rows[f"A1 PRIMARY {h} boost clipped at 1"]["canonical"]["MID"][0] for h in ("h0672", "h0686")]; ba = [rows[f"A1 PRIMARY {h} boost clipped at 1"]["alt"]["MID"][0] for h in ("h0672", "h0686")]
num("F F1 range (JSON)", f"{min(pc):.2f}-{max(bc):.2f} / {min(pa):.2f}-{max(ba):.2f}", "cores (0.3-1 Mpc) sit {} times")
num("F F1 abstract range (JSON)", f"{min(pc):.2f}-{max(bc):.2f} (canonical) / {min(pa):.2f}-{max(ba):.2f} (alternative)", "The cores sit {} times above")
check("F F1 326 clusters, REAL FAILURE (JSON)", "N 326" in f1["checks"]["K3"]["value"] and f1["verdict"] == "REAL FAILURE" and "F1, 326 clusters" in flat)
check("F F1 levers <= 4% (README)", "Native h moves A_MID by 1-4 %" in TX(RB, "F1_cluster_cores") and "by at most 4%" in flat)
s4 = JS(RB, "S4_v3_muK_clusters", "s4_v3_muk_clusters_results.json")
nscan = sum(len(v) for v in s4["scan"].values())
num("F S4 cells (JSON)", f"0 of {nscan:,}", "{} cells pass")
num("F S4 cells abstract (JSON)", f"0 of {nscan:,}", "fixes no cluster cell ({})")
check("F S4 no single cell, CANNOT on both footings (JSON)", s4["single_cells_passing"] == [] and s4["knob_passes"] == [] and s4["verdict_per_footing"] == {"canonical": "CANNOT", "alt": "CANNOT"})
check("F S4 identity with H2 to 0.0058 (JSON)", "0.0058" in s4["checks"]["K2"]["value"] and "reproduced to 0.0058" in flat)
W = s4["why"]
gm = {f_: min(W[k]["min_chi2"] for k in W if k.endswith("|" + f_)) for f_ in ("canonical", "alt")}
num("F S4 best chi2 on the grid (JSON)", f"{gm['canonical']:.1f} / {gm['alt']:.1f}", "anywhere on the grid is {} against")
rd("F S4 pass line 11.07 (README)", RB, "S4_v3_muK_clusters", "README.md", "χ² ≤ 11.07", "against a pass line of 11.07")
rd("F S4 README 'law's own 33.0' (disclosed)", RB, "S4_v3_muK_clusters", "README.md", "the law's own: 27.5 alt, 33.0 canonical", "the law's own 33.0")
law = s4["law"]["h0672|canonical"]["P3"]["MID"][0]
check("F S4 mu_K <= 0.03 untouched (JSON: MID moves < 0.5%)", abs(W["0.03|h0672|canonical"]["A_MID_D0"][0] / law - 1) < 0.005 and "For μK ≤ 0.03 Mpc-1 the clusters are untouched" in flat)
check("F S4 about 1% at 0.1 (JSON)", 0.005 < abs(W["0.1|h0672|canonical"]["A_MID_D0"][0] / law - 1) < 0.02 and "cluster cores move by about 1%" in flat)
num("F S4 galaxy lensing at 0.1 (JSON)", f"+{s4['galaxy']['0.1|canonical|0.0']['dchi2_zero_vs_law']:.1f} / +{s4['galaxy']['0.1|alt|0.0']['dchi2_zero_vs_law']:.1f}", "(Δχ2 = {})")
rd("F S4 guard fails for every mu_K >= 0.1 (README)", RB, "S4_v3_muK_clusters", "README.md", "The isolated-galaxy guard fails for every μ_K ≥ 0.1 Mpc⁻¹", "the galaxy guard fails for every μK ≥ 0.1 Mpc-1")
num("F S4 psi zeros at 0.1 (JSON)", f"{s4['galaxy_profiles']['0.1|canonical']['first_zero_psi_Mpc'][1]:.2f} Mpc around a galaxy and {s4['cluster_profiles']['0.1|h0672|canonical']['first_zero_psi_Mpc_median']:.2f}", "is at {} Mpc around")
rd("F S4 M^1/6 ordering (README)", RB, "S4_v3_muK_clusters", "README.md", "∝ M^{1/6}", "the onset scales as M1/6")
num("F S4 A_MID at 1, 3.333, 10 /Mpc (JSON)", " / ".join(f"{W[f'{m}|h0672|canonical']['A_MID_D0'][0]:.2f}" for m in ("1.0", "3.333", "10.0")), "MID amplitude becomes {} (canonical)")
nd = [s4["neg_dust_fraction"][f"{m}|h0672|canonical"]["median_Delta0"] for m in ("0.3", "0.5", "0.7", "1.0")]
num("F S4 negative dust (JSON)", f"{round(100 * min(nd))}-{round(100 * max(nd))}%", "negative over {} of the cluster volume")
rd("F S4 allowed range 10 /Mpc (README)", RB, "S4_v3_muK_clusters", "README.md", "allows μ_K up to 10 Mpc⁻¹, which is 14.8 h/Mpc", "μK ≤ 14.8 h/Mpc (10 Mpc-1)")
rd("F S4 Jeans-unstable branch (README)", RB, "S4_v3_muK_clusters", "README.md", "This is the Jeans-unstable branch, not a prediction", "static branch Jeans-unstable")
check("F M2 lesson in the draft at 45bd132464", "anything attached to every mass element acts like a halo on small systems; the cluster component must have its own scale between galaxies and clusters" in th
      and "anything attached to every mass element acts like a halo on small systems" in flat)
h2 = JS(RB, "H2_aest_clusters", "h2_aest_clusters_results.json")
check("F H2 verdict CANNOT (README)", "CANNOT" in TX(RB, "H2_aest_clusters") and "wrong radial shape (H2)" in flat)

# ---------------------------------------------------------------- G. growth and the early universe (F3, M1, Q6, Q7)
m1 = JS(RB, "M1_trilemma", "m1_trilemma_results.json")
check("G M1 kernel (JSON)", m1["R1b_i"]["s"].replace(" ", "") == "(-f_0*k**2+mu**2)/(-f_0*k**2+k**2+mu**2)" and "s(k;f0) = (μ2 - f0k2)/((1 - f0)k2 + μ2)".replace(" ", "") in flat.replace(" ", ""))
r3 = m1["R1b_iii"]
num("G M1 ratio J_x (JSON)", f"{r3['ratios']['f0=0|ai=0.001']:.3f} for Jx ({r3['ratios']['f0=1|ai=0.001']:.3f}", "σ8/σ8,dust = {} for J")
num("G M1 abstract 0.391 (JSON)", f"{r3['ratios']['f0=0|ai=0.001']:.3f}", "at the cap v3 reaches {} of")
num("G M1 cap (JSON)", f"{r3['mu_cap_hMpc']:.1f}", "cap at {} h/Mpc")
num("G M1 J'(0)=0 window (JSON)", f"{r3['mu_min_f0_1_ai1em3']:.0f} h/Mpc for J ′ (0) = 0 ({r3['gap_factor']:.1f} times", "and {}, M1)")
check("G M1 411 is the J'(0)=0 (f0 = 1) window (JSON)", r3["F3_reference"]["K5_mu_min_jeans"] == r3["mu_min_f0_1_ai1em3"] and "J'(0) = 0 needs 411" in flat.replace("J ′ (0)", "J'(0)") or "that figure is for J ′ (0) = 0" in flat)
check("G draft's M1 row gives 411 as v3's requirement (disclosed)", "Reaching σ₈ ≈ 0.95 needs μ_K ≥ 411 h/Mpc, 27.8× the BS cap" in th and "The draft's M1 row gives 411 h/Mpc (27.8x) as v3's requirement" in flat)
check("G M1 Jeans scale K''(1)/2 (JSON)", "K''(1)/2" in m1["checks"]["M2"]["value"] if isinstance(m1["checks"], dict) else any("K''(1)/2" in str(c) for c in m1["checks"]))
f3 = JS(RB, "F3_growth_audit", "f3_growth_audit_results.json")
w = f3["K5"]["windows"]
num("G F3 J_x window (JSON)", f"{w['bsk2_ai0.001']['mu_min_hMpc']:.0f}-{w['bsk2_ai0.0001']['mu_min_hMpc']:.0f} h/Mpc for Jx", "needs μK ≥ {} (ai")
num("G F3 J_x gap (JSON)", f"{w['bsk2_ai0.001']['gap_factor']:.0f}-{w['bsk2_ai0.0001']['gap_factor']:.0f} times the cap, F3", "10-4; {})")
num("G F3 abstract window (JSON)", f"{w['bsk2_ai0.001']['mu_min_hMpc']:.0f}-{w['bsk2_ai0.0001']['mu_min_hMpc']:.0f} h/Mpc, {w['bsk2_ai0.001']['gap_factor']:.0f}-{w['bsk2_ai0.0001']['gap_factor']:.0f} times", "needs μK ≥ {} the cap")
rd("G F3 double-counts (README)", RB, "F3_growth_audit", "README.md", "makes the dust double-count in galaxies", "the dust forms galaxy halos and double-counts against the law")
q6 = JS(RB, "Q6_v3_class", "q6_native_results.json")
num("G Q6 sigma8 at the cap (JSON)", f"{q6['fixed']['LOB_14.8']['sigma8']:.3f} at the cap (RB = {q6['fixed']['LOB_14.8']['R_B']:.3f}", "σ8 = {}, against")
num("G Q6 R_B at 2542 (JSON)", f"{float(re.search(r'R_B\(2542\) = ([0-9.]+)', q6['stepC']['mu_min_B_text']).group(1)):.2f}", "reaches only RB = {}.")
num("G Q6 fits (JSON)", f"+{q6['fits']['LOB_14.8']['dchi2_vs_LCDM']:,.0f} (not converged) down to +{q6['fits']['LOB_2542']['dchi2_vs_LCDM']:.1f}", "Δχ2 = {} over")
num("G Q6 stiff z (JSON)", f"{q6['stepB']['rows']['14.8']['z_stiff_equals_radiation']:.0f} at the cap and before {sci(q6['stepB']['rows']['2542']['z_stiff_equals_radiation'], 1)}", "before z = {} at 2542")
num("G Q6 BBN mu_K (JSON)", f"{sci(q6['stepB']['mu_K_BBN_hMpc'], 2)} h/Mpc, {sci(q6['stepB']['gap_over_BS_cap'], 2)}", "BBN needs μK ≥ {} times the cap")
rd("G Q6 not converged (README)", RB, "Q6_v3_class", "README.md", "not converged", "its +13,891 fit is not converged")
q7 = JS(RB, "Q7_bs25_cosmology", "q7_native_results.json")
rb7 = [q7["fixed"][k]["R_B"] for k in ("P1", "P2", "C1", "C30")]
num("G Q7 R_B (JSON)", f"{min(rb7):.2f}-{max(rb7):.2f}", "growth stays at RB = {}, Planck")
num("G Q7 R_B in table (JSON)", f"{min(rb7):.2f}-{max(rb7):.2f}", "growth (RB {})")
fin = [q7["fits"][k]["dchi2_vs_LCDM"] for k in ("P1", "P2", "C30")]
check("G Q7 one fit not converged (C1 inf) (JSON)", q7["fits"]["C1"]["dchi2_vs_LCDM"] == float("inf") and "one parameter set does not converge" in flat)
num("G Q7 fits (JSON)", f"+{min(fin):.0f} to +{max(fin):.0f}", "Planck lite Δχ2 = {}. Their")
dn = q7["stepB"]["rows"]
num("G Q7 dNeff (JSON)", f"{sci(dn['C30']['dNeff_equiv_1MeV'], 1)} / {sci(dn['P2']['dNeff_equiv_1MeV'], 1)} at λD = {dn['C30']['lambda_D']:.0f} / {dn['P2']['lambda_D']:.0f}", "1 MeV {}, against")
check("G Q7 lambda_D 30 and 1 sets share their dNeff (JSON)", abs(dn["P1"]["dNeff_equiv_1MeV"] / dn["C30"]["dNeff_equiv_1MeV"] - 1) < 1e-6 and abs(dn["C1"]["dNeff_equiv_1MeV"] / dn["P2"]["dNeff_equiv_1MeV"] - 1) < 1e-5)
num("G Q7 quadratic K dNeff (JSON)", sci(q7["stepB"]["K0c"]["dNeff_14.8"], 1), "against {} for the quadratic K")
num("G Q7 lambda_D 95 (JSON)", sci(q7["scans"]["cap"]["lambda_D_95"], 1), "λD ≈ {} restores")
num("G Q7 P(k) at 1 h/Mpc (JSON)", f"{q7['fits']['CAP@l95']['Pk_over_LCDM_bestfits']['1']:.2f}", "1 h/Mpc at {} of ΛCDM")
rd("G Q7 BS ran no Boltzmann code (README)", RB, "Q7_bs25_cosmology", "README.md", "BS ran no Boltzmann code.", "they ran no Boltzmann code")
rd("G Q7 BS25 is arXiv:2507.00912 (README)", RB, "Q7_bs25_cosmology", "README.md", "BS25 (arXiv:2507.00912)", "arXiv:2507.00912 (2025)")

# ---------------------------------------------------------------- H. saddles (H4, I1, C7, M1 screening routes)
h4 = JS(RB, "H4_v3_saddle_stability", "h4_v3_saddle_stability_results.json")
check("H H4 overall ILL-POSED (JSON)", h4["overall"] == "ILL-POSED")
rd("H H4 growth rate (README)", RB, "H4_v3_saddle_stability", "README.md", "Γ = L★ k √(2πG|ρ_τ|)", "the growth rate Γ = L★k")
ef = h4["efolds"]
nb = [v["median"]["N_bounded"] for v in ef.values()]
num("H H4 bounded without gamma_L (JSON)", f"{min(nb):.3f}-{max(nb):.2f}", "grows by only {} e-folds")
l1 = [v["median"]["lambda1_pc"] for v in ef.values()]
num("H H4 lambda_1 (JSON)", f"{min(l1):.1f}-{max(l1):.0f}", "Wavelengths below {} pc")
na = [v["median"]["N_1AU"] for v in ef.values()]
num("H H4 1 AU e-folds (JSON)", f"{sci(min(na), 1)} to {sci(max(na), 1)}", "grows by {} e-folds")
check("H H4 README's 0.9-6.7e7 differs (disclosed)", "at λ = 1 AU it is 0.9-6.7x10⁷" in TX(RB, "H4_v3_saddle_stability") and "growth as 0.9-6.7x107 e-folds" in flat)
c3v = h4["checks"]["C3"]["value"] if isinstance(h4["checks"], dict) else [c for c in h4["checks"] if c.get("id") == "C3"][0]["value"]
m_ = re.search(r"min D\.P = ([0-9.e+-]+) Msun/pc\^3", c3v)
num("H H4 Solar System D.P (JSON)", f"{float(m_.group(1)):.3f}", "keeps D · P ≥ {}")
i1 = JS(RB, "I1_gammaL_causality", "i1_gammal_causality_results.json")
lg = i1["K7"]["summary_ranges"]["dt_gal_loop_s"]
num("H I1 loops (JSON)", f"{lg[0] * 1e3:.0f} ms to {lg[1]:.1f} s", "close loops in time, by {} around")
c7 = JS(CV, "C7_aest_class", "c7_native_results.json")
num("H C7 v4 runaway (JSON)", sci(c7["fixed_caption"]["v4_KB0.01_mu1"]["Pk_over_LCDM"]["10"], 1), "up to {} at k = 10")
check("H C7 runaway result commit 64b0fdc9b4 touches C7", "covariant_push_2026_10_22/C7_aest_class/" in git("show", "--name-only", "--format=", "64b0fdc9b4").stdout)
sp = m1["R2a"]["canonical"]["sparc_cost"]
num("H M1 galileon SPARC cost (JSON)", f"{-sp['cubic']['median_dlog_g']:.2f} / {-sp['quartic']['median_dlog_g']:.2f}", "cost SPARC {} dex")
rc = m1["verdicts"]["R2_candidates"]
check("H M1 screening routes (JSON)", rc["R2b3 ambient density"] == "NO-GO (CONDITIONAL)" and rc["R2b4 curvature (R = b3; Weyl ghost)"] == "NO-GO (health)"
      and rc["R2a galileons (L3/L4/L5)"] == "NO-GO" and rc["R2b1 potential/thin-shell"] == "NO-GO"
      and "density keying is a conditional no-go" in flat and "Weyl keying carries an Ostrogradsky ghost" in flat)
rd("H M1 Ostrogradsky (README)", RB, "M1_trilemma", "README.md", "Ostrogradsky", "Ostrogradsky ghost")

# ---------------------------------------------------------------- I. repairs table: E2
e2 = TX(DP, "E2_field_equation")
check("I E2 unscreened Cassini 2.44-5.19x (README)", "2.44-4.59x" in e2 and "2.85-5.19x" in e2 and "Cassini, by 2.44-5.19x" in flat)

# ---------------------------------------------------------------- J. sealed predictions
wb = c6["R3_wide_binary"]
num("J C6 gamma_v-1 at 24 pc (JSON)", sci(max(wb["canonical|24"]["gamma_minus_1"]), 1), "γv - 1 = {} at L★ = 24 pc")
e2j = JS(DP, "E2_field_equation", "e2_field_equation_results.json")["R2"]
num("J E2 unscreened gamma (JSON)", f"{e2j['canonical|PREREG_primary']['gamma_AQUAL_anch']:.2f}", "γv ≈ {} for the unscreened")
for fn, h, cm_ in (("SEALED_V3_MW_DR4.json", "15b7e6ff", "ec0c57d236"), ("SEALED_V3_ALMA_AQUAL.json", "b5d65a5e", "90f4d517d6")):
    sha = hashlib.sha256(open(os.path.join(RB, "S3_v3_mw_seals", fn), "rb").read()).hexdigest()
    check(f"J {fn} sha256 {h} recomputed, commit {cm_} adds it, cited", sha.startswith(h) and fn in git("show", "--name-only", "--format=", cm_).stdout and f"sha256 {h}" in flat and cm_ in flat)
seal = json.load(open(os.path.join(RB, "S3_v3_mw_seals", "SEALED_V3_MW_DR4.json")))["v3"]["canonical"]["1.000000"]["P6_asymmetry_A"]
num("J S3 P6 asymmetry (JSON)", " / ".join(f"{100 * seal[r]:.1f}" for r in ("R20", "R30", "R60")), "circular speed, {}% at 20")
check("J ALMA addendum F commit f6f0ba66a4 exists, cited", "ADDENDUM_F" in git("show", "--name-only", "--format=", "f6f0ba66a4").stdout.upper() and "f6f0ba66a4" in flat)
check("J ALMA dates (D4 README)", "2026-11-06" in TX(DP, "D4_alma_status") and "2026-11-28" in TX(DP, "D4_alma_status") and "U4 (2026-11-06) and GS4 (2026-11-28)" in flat)

# ---------------------------------------------------------------- P. pending statements must be true at build time
L1D = "rebuild_2026_10_22/L1_khronon_pm"
tracked = git("ls-files", L1D).stdout.split()
prod = [f for f in tracked if re.search(r"(A5_|A6_|N384|N256|ladder|production|_verdict)", f, re.I)]
check("P L1 pending: no production result file tracked", prod == [], str(prod))
l1log = git("log", "--format=%h %s", "0a43187bea..HEAD", "--", L1D).stdout
check("P L1 pending: no L1 commit after the A7 pre-flight", l1log.strip() == "", l1log.strip()[:200])
rd("P L1 indicative run is not a verdict (README)", RB, "L1_khronon_pm", "README.md", "not a verdict", "labelled not a verdict")
led = open(os.path.join(ROOT, "campaign_fresh_gravity", "LEDGER.md"), encoding="utf-8").read()
check("P radiative stability still grey (STALE tile S(...)) on the board", re.search(r'\n    S\(\d+, "Radiative stability \(G12\)"', board) is not None
      and "Radiative stability stays grey" in board and "radiative stability, is still grey" in flat)
check("P CFG960 scored canonical only, retired engine (LEDGER)", "CFG960 canonical FAILS" in led and "SC2x (alt) NOT RUN" in led and "tests the retired SCT-M settling engine, not the current best theory v3" in led
      and "scored canonical only and tests that engine, not v3" in flat)

# ---------------------------------------------------------------- O. citations and metadata
bib = open(os.path.join(ROOT, "citations", "REFERENCES.bib"), encoding="utf-8").read()


def bibentry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
    return m.group(1) if m else ""


e = bibentry("Blanchet2024")
check("O Blanchet & Skordis 2024 (bib)", "2404.06584" in e and "pages = {040}" in e and "L. Blanchet, C. Skordis, JCAP 11 (2024) 040 (arXiv:2404.06584)" in flat)
check("O Blanchet & Skordis 2025 (bib)", "2507.00912" in bibentry("Blanchet2025c") and "L. Blanchet, C. Skordis, arXiv:2507.00912 (2025)" in flat)
e = bibentry("Skordis2021")
check("O Skordis & Zlosnik 2021 (bib)", "2007.00082" in e and "161302" in e and "PRL 127, 161302 (2021) (arXiv:2007.00082)" in flat)
check("O Hees 2014 (bib)", "102002" in bibentry("Hees2014") and "PRD 89, 102002 (2014)" in flat)
check("O Park 2026 (bib)", "024066" in bibentry("Park2026") and "PRD 114, 024066 (2026)" in flat)
z = json.load(open(ZJ))["metadata"]
ids = {r["identifier"] for r in z["related_identifiers"]}
check("O related identifiers (PAPER59, PAPER58 v1.1)", {"10.5281/zenodo.23585319", "10.5281/zenodo.23579379"} <= ids)
check("O never 23532894", "23532894" not in json.dumps(z) and "23532894" not in tex)
check("O zenodo: working paper, CC-BY, fitted, not closed, pending", z["publication_type"] == "workingpaper" and z["license"] == "cc-by-4.0" and "fitted" in z["description"]
      and "not closed" in z["description"] and "pending" in z["description"].lower())
for s in ("PAPER59 (doi:10.5281/zenodo.23585319)", "PAPER58 v1.1 (doi:10.5281/zenodo.23579379)"):
    has(f"O companion '{s[:20]}'", s)

# ---------------------------------------------------------------- Q. honesty, forbidden, names
for s in ("fitted", "the theory is not closed", "not peer reviewed", "never pooled", "AI-assisted", "Anthropic's Claude", "not a particle", "POSTULATED",
          "Not a UV completion", "Not evidence for the framework", "The owner's programme", "No particle species is added", "not a cluster theory, not a cosmology"):
    has(f"Q honesty '{s}'", s)
zl = z["description"].lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "breakthrough",
            "κ is derived", "kappa is derived", "l★ is derived", "/users/", "gmail", "dark matter particle", "dark-matter particle"):
    check(f"Q forbidden '{bad}' absent", bad not in low and bad not in tex.lower() and bad not in zl)
check("Q no 'derived' applied to kappa or L*", not re.search(r"(κ|kappa|L★|Lstar)[^.]{0,30}\bis derived", low))
check("Q no home path in TeX", "/Users/" not in tex and "~/" not in tex)
gu = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split()
check("Q no personal name (repo user) in PDF, TeX or zenodo description", all(x.lower() not in low and x.lower() not in tex.lower() and x.lower() not in zl for x in gu if len(x) >= 3), f"{len(gu)} name parts checked")

if MUT:
    missed = [n for n, caught in NUM if not caught]
    for n in missed:
        print(f"  [NOT CAUGHT] {n}")
    print(f"\nPAPER60 audit --mutate: {len(NUM) - len(missed)}/{len(NUM)} perturbed number checks FAIL as required")
    sys.exit(1 if missed else 0)
print(f"\nPAPER60 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
