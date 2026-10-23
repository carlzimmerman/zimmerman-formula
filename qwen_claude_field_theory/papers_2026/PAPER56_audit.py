#!/usr/bin/env python3
"""PAPER56 audit: the built PDF must be newer than the TeX and 4-8 pages long (the deposit version adds NC2x and CFG929, 7 pages; the
v1.1 correction box an 8th, which is accepted); every quoted number must match the committed lane
outputs (JSON first; LEDGER row or lane README text where the number lives only there); the honesty phrases and post-hoc
disclosures must be present; the in-progress statements must still be true; no forbidden claim or local path may appear.
v1.1 (2026-10-23, section V): the dated correction box (lane CFG963, attribution of the native shear pass) must exist above the
abstract on page 1; no unqualified "matched control" may remain (TeX outside the box, PDF, Zenodo description) other than the one
quotation of v1.0 and "feedback-matched"; the v1.0 sentences that presented -10.08 / -9.39 as the framework's lead must be gone and
every changed sentence marked "Correction v1.1"; every CFG963 number must match its results JSON (attribution and reuse/A1); the
credited commits must exist; the Zenodo metadata must be v1.1, lead with the correction, mark isNewVersionOf 10.5281/zenodo.23532875,
and keep v1.0's other fields. The v1.1 box re-paginates the note, so the PDF text is now read with each page-number footer removed
at page breaks (two v1.0 phrases, unchanged in the TeX, fell across a break), and Table 1's float placement is [b] instead of [t]
(at [t] the table landed inside an unchanged v1.0 sentence); no check string was loosened.
Run: python3 PAPER56_audit.py (exit 0 only if all pass).  Read-only: it opens committed files and the PDF, nothing else."""
import json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.normpath(os.path.join(HERE, "..", "..", "campaign_fresh_gravity"))
TEX = os.path.join(HERE, "PAPER56_pressure_supported_excess_2026.tex")
PDF = os.path.join(HERE, "PAPER56_pressure_supported_excess_2026.pdf")
F = 0
N = 0


def check(name, ok, msg=""):
    global F, N
    N += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    F += (not ok)


def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("−", "-"), ("–", "-"), ("—", "-"), ("’", "'"), ("×", "x"), (" ", " ")):
        t = t.replace(a, b)
    t = re.sub(r"([a-z])-\s+([a-z])", r"\1-\2", t)  # explicit hyphens broken across lines
    t = re.sub(r"\s*±\s*", " ± ", t)
    t = re.sub(r"\s*→\s*", " → ", t)
    return re.sub(r"\s+", " ", t)


J = lambda p: json.load(open(os.path.join(CFG, p)))
LEDGER = open(os.path.join(CFG, "LEDGER.md"), encoding="utf-8").read().splitlines()


def row(lane):
    hits = [l for l in LEDGER if l.startswith(f"| {lane} |")]
    return norm(hits[0]) if hits else ""


def readme(path):
    return norm(open(os.path.join(CFG, path), encoding="utf-8").read())


# ---------------------------------------------------------------- A. build
check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout).group(1))
check("A2 page count 4-8 (8 accepted for v1.1's correction box)", 4 <= pages <= 8, f"{pages} pages")
# two extractions of the same PDF: layout mode (running text) and reading-order mode (keeps table cells contiguous)
FOOT = re.compile(r"\n[ \t]*\d{1,2}[ \t]*\n*\f")   # v1.1: drop the page-number footer at each page break, so a sentence split by a break still matches
raw = [norm(FOOT.sub("\n", subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout)) for m in (["-layout"], [])]
flat = " ||| ".join(raw)
tex = open(TEX, encoding="utf-8").read()


def has(name, s):
    check(name, s in flat, s)


def led(name, lane, s, pdf_s=None):
    """number/phrase s must be in the lane's LEDGER row AND (s, or its PDF wording pdf_s) in the PDF"""
    r = row(lane)
    check(name, bool(r) and s in r and (pdf_s or s) in flat, f"{lane}: '{s}'" + (f" / PDF '{pdf_s}'" if pdf_s else "") + ("" if r else " (no LEDGER row)"))


def rd(name, path, s, pdf_s=None):
    """number/phrase must be in the lane README AND in the PDF"""
    check(name, s in readme(path) and (pdf_s or s) in flat, f"{path.split('/')[0]}: '{s}'")


f2 = lambda x: f"{x:.2f}"

# ---------------------------------------------------------------- B. native-input shear rerun (CFG654 A2)
n1 = J("CFG654_independent_inputs/cfg654_native_results_NC1x.json")
k, d = n1["surveys"]["KiDS"], n1["surveys"]["DES"]
for tag, s in (("KiDS", k), ("DES", d)):
    has(f"B {tag} chi2 control", f2(s["chi2_S0"])); has(f"B {tag} chi2 framework", f2(s["chi2_F"]))
    has(f"B {tag} dchi2", f2(s["dchi2"]))
    rv = list(s["robust"].values()); has(f"B {tag} robustness range", f"{max(rv):.2f} to {min(rv):.2f}")
    has(f"B {tag} points", f"{s['N_kept']}")
check("B KiDS class CONSISTENT", k["class"] == "CONSISTENT" and "CONSISTENT" in flat)
check("B DES class NOT DIAGNOSTIC", d["class"] == "NOT DIAGNOSTIC" and "NOT DIAGNOSTIC" in flat)
check("B verdict PASS (shear side, canonical)", n1["verdict"].startswith("PASS") and n1["foot"] == "canonical")
b0 = n1["benchmark"]["z0"]["at"]; has("B power ratios z=0", f"{b0['0.3']:.3f}, {b0['0.5']:.3f} and {b0['1.0']:.3f}")
out909 = open(os.path.join(CFG, "CFG909_shear_score_lcdm_input_sensitivity/cfg909_NC1x.out"), encoding="utf-8").read()
m = re.search(r"AS_SCORED\s*\] canonical KiDS: N 108; chi2 S0 ([\d.]+) \(p ([\d.]+)\), F ([\d.]+) \(p ([\d.]+)\)", out909)
check("B p-values parsed from CFG909 K1 reproduction", bool(m))
if m:
    has("B p framework", f"p = {m.group(4)}"); has("B p control", f"(p = {m.group(2)})")
led("B inherited T1x absolute chi2", "CFG654-A2", "136.6")
led("B A2 reading HOLDS", "CFG654-A2", "HOLDS")
# ---- NC2x (CFG654 A3, alt footing, native inputs) landed 2026-10-21: every number from its JSON, the K1 p-value from CFG909
n2 = J("CFG654_independent_inputs/cfg654_native_results_NC2x.json")
k2, d2 = n2["surveys"]["KiDS"], n2["surveys"]["DES"]
check("B NC2x is the alt footing on native inputs vs NCS0", n2["foot"] == "alt" and n2["inputs"] == "native_cmb" and n2["jobs"] == ["NC2x", "NCS0"])
for tag, s in (("KiDS", k2), ("DES", d2)):
    has(f"B NC2x {tag} chi2 framework", f2(s["chi2_F"])); has(f"B NC2x {tag} dchi2", f2(s["dchi2"]))
    check(f"B NC2x {tag} shares the control chi2 of NC1x", abs(s["chi2_S0"] - n1["surveys"][tag]["chi2_S0"]) < 1e-9)
    rv = list(s["robust"].values()); has(f"B NC2x {tag} robustness range", f"{max(rv):.2f} to {min(rv):.2f}")
check("B NC2x KiDS and DES both CONSISTENT", k2["class"] == d2["class"] == "CONSISTENT")
has("B abstract quotes both KiDS dchi2", f"{f2(k['dchi2'])} canonical, {f2(k2['dchi2'])} alternative")
has("B abstract quotes NC2x DES", f"also CONSISTENT ({f2(d2['dchi2'])})")
check("B NC2x verdict PASS (shear side, alt)", n2["verdict"].startswith("PASS"))
mu1 = J("CFG654_independent_inputs/cfg654_native_results_NC1x_MUTATE.json")["surveys"]
mu2 = J("CFG654_independent_inputs/cfg654_native_results_NC2x_MUTATE.json")["surveys"]
check("B mutation control bites for both runs (NZ1)", all(m_[s_]["NZ1"] for m_ in (mu1, mu2) for s_ in ("KiDS", "DES")))
check("B DES T-OWN: diagnostic for NC2x only", mu2["DES"]["T_OWN"] and not mu1["DES"]["T_OWN"])
has("B DES T-OWN NC2x", f"reaches {mu2['DES']['T_OWN_chi2']:.2f} there"); has("B DES T-OWN NC1x", f"against {mu1['DES']['T_OWN_chi2']:.2f} on the canonical")
b2 = n2["benchmark"]["z0"]["at"]; has("B NC2x power ratios z=0", f"{b2['0.3']:.3f}, {b2['0.5']:.3f} and {b2['1.0']:.3f} for NC2x")
m2 = re.search(r"AS_SCORED\s*\] alt\s+KiDS: N 108; chi2 S0 ([\d.]+) \(p ([\d.]+)\), F ([\d.]+) \(p ([\d.]+)\)",
               open(os.path.join(CFG, "CFG909_shear_score_lcdm_input_sensitivity/cfg909_NC2x.out"), encoding="utf-8").read())
check("B NC2x p-value parsed from CFG909's K1 reproduction (alt)", bool(m2) and abs(float(m2.group(3)) - k2["chi2_F"]) < 0.006)
if m2:
    has("B NC2x p framework", f"145.38 (p = {m2.group(4)})")
led("B A3 reading HOLDS", "CFG654-A3", "HOLDS"); led("B A3 KiDS dchi2", "CFG654-A3", "-9.39")
led("B A3 DES CONSISTENT", "CFG654-A3", "DES Y3 Δχ² -2.15 → CONSISTENT", "CONSISTENT ($-2.15$)".replace("$", ""))
led("B A3 both footings", "CFG654-A3", "passes on BOTH footings with native inputs", "now holds on both footings")
rd("B A3 inherited-IC condition lifted on both", "CFG654_independent_inputs/README.md", "the inherited-IC condition is lifted on both", "inherited-input condition is lifted on both")
led("B A3 engine has no established physical parent", "CFG654-A3", "no established physical parent", "no established physical parent")
has("B PAPER57 pointer", "PAPER57"); has("B pass is a computational result", "computational result of that engine")
check("B no stale 'running' statement about NC2x", "is running" not in flat and "still running" not in flat)
rd("B run-plan deviation disclosed", "CFG654_independent_inputs/README.md", "2 GB below the frozen", "below the frozen start rule")

# ---------------------------------------------------------------- C. CFG909 amplitude caveat
c9 = J("CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC1x.json")
g = c9["grid"]; has("C Om grid", f"{min(g):.4f}-{max(g):.4f}")
dk = lambda v: c9["variants"][v]["results"]["canonical"]["KiDS"]["cfg"]["main"]["dchi2"]
has("C dchi2 at Om 0.2806", f2(dk("OM_0.2806"))); has("C dchi2 at Om 0.3308", f2(dk("OM_0.3308")))
has("C own covariance", f2(dk("CV1_OWN")))
check("C class ROBUST", c9["lane_class"] == "ROBUST" and "ROBUST" in flat)
led("C power deficit 3-6%", "CFG909", "3-6% power deficit")
# CFG909's NC2x rescore (2026-10-21; output complete: LANE CLASS line, K1-K4 pass, MUTATE bites)
o9 = open(os.path.join(CFG, "CFG909_shear_score_lcdm_input_sensitivity/cfg909_NC2x.out"), encoding="utf-8").read()
check("C NC2x rescore complete (LANE CLASS ROBUST, K1-K4 pass)", "LANE CLASS (KiDS, class-weighted variants): ROBUST; flips: none" in o9
      and "controls: K1_pass True, K2_pass True, K3_pass True, K4_pass True" in o9)
m9 = open(os.path.join(CFG, "CFG909_shear_score_lcdm_input_sensitivity/cfg909_NC2x_MUTATE.out"), encoding="utf-8").read()
check("C NC2x rescore MUTATE bites", "all bite = True" in m9)
c92 = J("CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC2x.json")
check("C NC2x same Om grid and class ROBUST", c92["grid"] == c9["grid"] and c92["lane_class"] == "ROBUST" and c92["flips"] == [])
dk2 = lambda v: c92["variants"][v]["results"]["alt"]["KiDS"]["cfg"]["main"]["dchi2"]
om2 = [dk2(v) for v in ("OM_0.2806", "OM_0.2976", "OM_0.3085", "OM_0.3138", "OM_0.3308")]
check("C NC2x KiDS CONSISTENT in every Om variant", all(c92["variants"][v]["results"]["alt"]["KiDS"]["class"] == "CONSISTENT"
      for v in ("OM_0.2806", "OM_0.2976", "OM_0.3085", "OM_0.3138", "OM_0.3308")))
has("C NC2x dchi2 range over Om", f"from {f2(max(om2))} to {f2(min(om2))}"); has("C NC2x own covariance", f"{f2(dk2('CV1_OWN'))} with the framework's own covariance")
led("C NC2x LEDGER class ROBUST", "CFG909-NC2x", "LANE CLASS ROBUST, no flips", "the class is also ROBUST")
led("C NC2x LEDGER Om range", "CFG909-NC2x", "-2.93 to -14.69", "from -2.93 to -14.69")
led("C NC2x LEDGER own covariance", "CFG909-NC2x", "framework's own covariance -2.81", "-2.81 with the framework's own covariance")
led("C NC2x LEDGER MUTATE bites", "CFG909-NC2x", "MUTATE bites", "its mutation control bites")
tt = open(os.path.join(CFG, "CFG909_shear_score_lcdm_input_sensitivity/cfg909_T.out"), encoding="utf-8").read()
mt = {f: re.search(rf"AS_SCORED\s*\] {f}\s+KiDS: N (\d+); chi2 S0 [\d.]+ \(p [\d.]+\), F ([\d.]+) \(p ([\d.]+)\)", tt) for f in ("canonical", "alt")}
check("C inherited T1x/T2x absolute chi2 parsed", all(mt.values()))
if all(mt.values()):
    has("C inherited T1x/T2x chi2", f"{float(mt['canonical'].group(2)):.1f} for T1x and {float(mt['alt'].group(2)):.1f} for T2x on {mt['alt'].group(1)} points")
    has("C inherited p-values", f"p = {mt['canonical'].group(3)} and {mt['alt'].group(3)}")

# ---------------------------------------------------------------- D. CFG917 CMB lensing
a1 = J("CFG917_cmb_lensing_gate/cfg917_A1_classes.json")["pairs"]
for p in ("NC1x", "T1x", "T2x", "NC2x"):
    q = a1[p]
    has(f"D {p} part A dA", f"{q['partA_dA']:.4f}"); check(f"D {p} part A SAFE", q["partA_label"] == "SAFE")
    has(f"D {p} dchi2", f"{q['dchi2']:.3f}"); has(f"D {p} chi2 F", f"{q['chi2_F']:.3f}"); has(f"D {p} chi2 S0", f"{q['chi2_S0']:.3f}")
    check(f"D {p} frozen NOT DIAGNOSTIC / A1 CONSISTENT / gate PASS",
          q["class_frozen"] == "NOT DIAGNOSTIC" and q["class_A1"] == "CONSISTENT" and q["gate_A1"] == "PASS")
mr = max(abs(v) for p in ("NC1x", "T1x", "T2x", "NC2x") for v in a1[p]["robust"].values())
check("D NC2x scored blind: CFG917 criteria frozen before any NC2x output", "before any NC2x output" in row("CFG917") and "NC2x was scored blind" in flat)
check("D all four SAFE / CONSISTENT stated", "All four are SAFE" in flat and "all four pairs are CONSISTENT" in flat)
check("D every robustness member |dchi2| < 1.6", mr < 1.6 and "below 1.6" in flat, f"max {mr:.3f}")
p1 = J("CFG917_cmb_lensing_gate/cfg917_T1x_MUTATE.json")["M3_context"]["primary"]["dchi2"]; has("D KiDS-excluded candidate", f"+{p1:.2f}")
rd("D Part A 2sigma", "CFG917_cmb_lensing_gate/README.md", "2σ = 0.056")
rd("D KiDS dchi2 of excluded candidate", "CFG917_cmb_lensing_gate/README.md", "+68.7")
rd("D 70% super-box signal", "CFG917_cmb_lensing_gate/README.md", "About 70%", "About 70%")
rd("D PR4 amplitude error", "CFG917_cmb_lensing_gate/README.md", "2.4%")
check("D A1 disclosed as post hoc", "post-hoc amendment (A1)" in flat and "rests on A1" in flat)

# ---------------------------------------------------------------- E. CFG927 sealed forecast
t27 = J("CFG927_cmb_lensing_forecast/cfg927_forecast_table.json")
pr = ("T1x", "T2x", "NC1x")
for model in ("ACT-DR6-like", "SO-baseline-like", "S4-like", "CV-limited"):
    for L in ("400", "1000", "2000", "3000"):
        v = [t27["pairs"][p]["cells"][model][L]["dchi2"] for p in pr]
        s = f"{min(v):.2f}-{max(v):.2f}" if max(v) < 100 else f"{min(v):.0f}-{max(v):.0f}"
        has(f"E {model} L<={L}", s)
cell = lambda p, m, L: t27["pairs"][p]["cells"][m][L]
check("E ACT-like blind to L 3000 (all < 9)", all(cell(p, "ACT-DR6-like", L)["dchi2"] < 9 for p in pr for L in ("400", "763", "1000", "2000", "3000")))
s4 = [cell(p, "S4-like", "1000")["dchi2"] for p in pr]; has("E S4 L<=1000 rounded", f"({int(min(s4))}-{int(max(s4))})")
check("E S4 robust at L<=1000", all(cell(p, "S4-like", "1000")["robust"] for p in pr))
so = [cell(p, "SO-baseline-like", "2000")["dchi2"] for p in pr]; has("E SO L<=2000 rounded", f"({int(min(so))}-{int(max(so))})")
l9 = [t27["pairs"][p]["L_9"]["S4-like"] for p in pr]
check("E S4 L_9 near 700", all(x is not None and 650 <= float(x) <= 750 for x in l9) and "L ≈ 700" in flat, f"{l9}")
has("E excluded candidate ACT L<=763", f2(cell("P1", "ACT-DR6-like", "763")["dchi2"]))
an = t27["noise_anchors_K7"]; has("E noise anchors", f"{an['Planck-like-anchor']['ratio']:.2f} and {an['ACT-DR6-like']['ratio']:.2f}")
led("E z>1 continuation share", "CFG927", "45-78%")
led("E sealed forecast", "CFG927", "SEALED FORECAST", "sealed a Fisher forecast")

# ---------------------------------------------------------------- F. CFG919 pattern
r19 = J("CFG919_pressure_support_selector/cfg919_results.json")
for cls in ("DW", "CL", "LS", "LD", "SS", "SL"):
    for foot in ("canonical", "alt"):
        c = r19["byfoot"][foot]["V0"]["class_summary"][cls]
        has(f"F {cls} {foot} excess", f"{c['dex']:+.3f} ± {c['se'] / math.log(10):.3f}")
    fv = r19["byfoot"]["canonical"]["V0"]["class_summary"][cls]["f"]; has(f"F {cls} f_P", f"{fv:.3f}".rstrip("0").rstrip(".") if fv < 0.5 else f"{fv:.1f}")
v0 = r19["byfoot"]["canonical"]["V0"]
has("F ordering T", f"T = {v0['T']:+.3f}"); has("F n>2 vs n<2 dE", f"{v0['W']['W1']['dE']:+.2f}"); has("F n>2 vs n<2 z", f"z = {v0['W']['W1']['z']:+.1f}")
f1c, f1a = v0["F"]["F1"], r19["byfoot"]["alt"]["V0"]["F"]["F1"]
has("F F1 chi2 canonical", f"{f1c['chi2']:.1f} for {f1c['dof']}"); has("F F1 chi2 alt", f"{f1a['chi2']:.1f} on the alternative")
check("F F1 p < 1e-6 both footings", f1c["p"] < 1e-6 and f1a["p"] < 1e-6 and "p < 10" in flat)
check("F class SELECTOR CONTRADICTED, FRAGILE", r19["overall"] == "SELECTOR CONTRADICTED" and r19["overall_frozen"] == "SELECTOR CONTRADICTED"
      and r19["robustness"] == "FRAGILE" and "SELECTOR CONTRADICTED" in flat and "FRAGILE" in flat)
rd("F permutation p", "CFG919_pressure_support_selector/README.md", "permutation p = 0.002")
led("F dwarfs 3-5x lenses", "CFG919", "3-5x the n>2 lenses", "3-5 times the spheroidal")
led("F floor 0.10 dex", "CFG919", "floor 0.10 dex", "floor to 0.10")
led("F CFG914 no common ordering, all ten variants", "CFG914", "all 10 variants", "all ten variants")

# ---------------------------------------------------------------- G. CFG922 cluster cores
r22 = J("CFG922_cluster_core_baryon_recheck/cfg922_results_A1.json")["results"]
C, A = r22["eRASS1|s|canonical"], r22["eRASS1|s|alt"]
has("G A_MID baseline", f"{C['baseline_f020']['MID'][0]:.2f} canonical, {A['baseline_f020']['MID'][0]:.2f} alternative")
has("G lambda", f"{C['U_lambda_conc_on_gascyl']['A1']['value']:.2f} (canonical) or {A['U_lambda_conc_on_gascyl']['A1']['value']:.2f}")
has("G stars", f"{C['1a_stars_k_on_Sup']['A1']['value']:.1f} / {A['1a_stars_k_on_Sup']['A1']['value']:.1f}")
has("G hot gas", f"{C['2a_gas_m_whole']['A1']['value']:.2f} / {A['2a_gas_m_whole']['A1']['value']:.2f}")
has("G hot gas upper end", f"{C['2a_gas_m_whole']['upper']:.2f}")
has("G corner MID", f"{C['corner']['MID'][0]:.2f} / {A['corner']['MID'][0]:.2f}")
o22 = J("CFG922_cluster_core_baryon_recheck/cfg922_results_A1.json")["overall"]
zc, za = o22["per_footing_nu_s"]["eRASS1|s|canonical"]["corner_Z_MID"], o22["per_footing_nu_s"]["eRASS1|s|alt"]["corner_Z_MID"]
has("G corner Z", f"Z = {zc:+.1f} / {za:+.1f}")
kk = [o22["per_footing_nu_s"][f"eRASS1|s|{f}"][x] for f in ("canonical", "alt") for x in ("k_ICL", "k_H2")]
has("G ICL/H2 need", f"{int(min(kk))}-{round(max(kk))}")
check("G EXCESS STANDS both kernels", o22["nu_s"] == "EXCESS STANDS" and o22["nu_mono"] == "EXCESS STANDS" and "EXCESS STANDS" in flat)
led("G 318 clusters", "CFG922", "eRASS1 318", "318 eRASS1"); led("G 68 matches", "CFG922", "68 eRASS1", "68 cross-matched")
has("G 318 in PDF", "318 eRASS1"); has("G 68 in PDF", "68 cross-matched")

# ---------------------------------------------------------------- H. CFG921 five selectors
r21 = J("CFG921_excess_selector_posits/cfg921_results.json")
check("H trials factor 5", r21["trials"]["N_T"] == 5 and "trials factor of 5" in flat)
check("H all five FAIL, no survivor", r21["survivors"] == [] and all(r21["classes"][p]["overall"] == "FAILS" for p in ("P1", "P2", "P3", "P4", "P5")))
fz = lambda f, P, k_: r21["byfoot"][f]["V0"][P]["facts"][k_]["min_abs_z"]
has("H P2 clusters", f"z = -{fz('canonical', 'P2', 'F5'):.1f} / -{fz('alt', 'P2', 'F5'):.1f}")
has("H P2 red lenses", f"(-{fz('canonical', 'P2', 'F1'):.1f} / -{fz('alt', 'P2', 'F1'):.1f})")
has("H P4 clusters", f"(-{fz('canonical', 'P4', 'F5'):.1f} / -{fz('alt', 'P4', 'F5'):.1f})")
p4 = fz("canonical", "P4", "F1"); check("H P4 red-lens miss below trials bar", p4 < r21["trials"]["z_TF"] and f"{p4:.1f}σ" in flat, f"{p4:.2f} < {r21['trials']['z_TF']:.2f}")
led("H P5 ~40x short", "CFG921", "~40x short", "about 40 times too small"); led("H scale-free 1.25x", "CFG921", "1.25x"); led("H velocity selectors >~100x", "CFG921", "100x")

# ---------------------------------------------------------------- I. dwarf environment and clump lanes
r74 = J("CFG874_isolated_dwarfs_pooled/cfg874_results.json")["canonical"]["primary"]
has("I CFG874 E", f"{r74['E']:+.3f} ± {r74['se_E']:.3f}"); has("I CFG874 c", f"{r74['c']:+.3f} ± {r74['se_c']:.3f}")
check("I CFG874 11 isolated, UNDECIDED", r74["N_I"] == 11 and r74["cls"] == "UNDECIDED" and "all 11 isolated" in flat)
r75 = J("CFG875_host_distance_trend/cfg875_results.json")
has("I CFG875 k", f"{r75['canonical']['primary']['k']:+.3f} ± {r75['canonical']['primary']['se_k']:.3f}")
check("I CFG875 UNDECIDED both", r75["canonical"]["primary"]["cls"] == r75["alt"]["primary"]["cls"] == "UNDECIDED")
led("I CFG860 NOT GAS", "CFG860", "NOT GAS")
r80 = J("CFG880_clump_sigma_universality/cfg880_results.json")
pc, pa = r80["canonical"]["primary"], r80["alt"]["primary"]
has("I CFG880 s_int", f"{pc['s_hat']:.3f} (95%: {pc['s95'][0]:.3f}-{pc['s95'][1]:.3f}"); has("I CFG880 alt s_int", f"also gives {pa['s_hat']:.3f}")
has("I CFG880 per-dwarf factor", f"x{math.exp(pc['s_hat']):.2f} per dwarf")
check("I CFG880 NOT UNIVERSAL both", pc["cls"] == pa["cls"] == "NOT UNIVERSAL")
led("I CFG880 six variants", "CFG880", "All six variants NOT UNIVERSAL", "all six variants")
led("I CFG888 baryons only", "CFG888", "BARYONS ONLY", "source is the baryons"); led("I CFG888 no self-gravity", "CFG888", "NO SELF-GRAVITY", "no self-gravity")
led("I CFG888 adds a parameter", "CFG888", "ADDS A PARAMETER", "adds a parameter")
led("I CFG889 half-life", "CFG889", "105-148 Myr/α", "105-148"); led("I CFG889 inconclusive as frozen", "CFG889", "INCONCLUSIVE as frozen", "inconclusive as frozen")
led("I CFG913 42 forms", "CFG913", "42 pre-declared"); led("I CFG913 infeasible", "CFG913", "INFEASIBLE", "No single local mobility law")
led("I CFG915 contradicted under both", "CFG915", "CONTRADICTED under both")
led("I CFG916 x4.32", "CFG916", "4.32"); led("I CFG916 capped capture", "CFG916", "capped capture", "capped-capture")

# ---------------------------------------------------------------- J. dwarf-route conditions
r20 = J("CFG920_dwarf_baryon_loss_chemistry/cfg920_results.json")
has("J CFG920 median required loss", f"{r20['summary']['canonical']['median']['-0.5|W1']['M_req']:.2f} (canonical) or {r20['summary']['alt']['median']['-0.5|W1']['M_req']:.2f}")
cn = r20["summary"]["canonical"]["counts"]
has("J CFG920 per-dwarf counts", f"{cn['COMPATIBLE']} compatible, {cn['UNDERDETERMINED']} underdetermined, {cn['CONTRADICTED']} contradicted")
check("J CFG920 20 tested, UNDERDETERMINED", len(r20["tested"]) == 20 and r20["overall"] == "UNDERDETERMINED" and "the 20 dwarfs" in flat)
led("J CFG923 trigger window", "CFG923", "4.9-12.7 Gyr", "4.9-12.7"); led("J CFG923 overall UNDERDETERMINED", "CFG923", "OVERALL UNDERDETERMINED", "UNDERDETERMINED overall")
led("J CFG918 bound envelope excluded", "CFG918", "BOUND ENVELOPE EXCLUDED", "bound outer envelope is excluded"); led("J CFG918 escaping receiver", "CFG918", "escaping receiver remains")

# ---------------------------------------------------------------- K. small reframings
r25 = J("CFG925_small_reframings_A/cfg925_results.json")
has("K R1 canonical", f"{r25['observed_dex']['canonical']['F0']:+.3f} → {r25['R1']['canonical']['corners']['J0|A1']['F0_jeans_dex']:+.3f}")
has("K R1 alt", f"{r25['observed_dex']['alt']['F0']:+.3f} → {r25['R1']['alt']['corners']['J0|A1']['F0_jeans_dex']:+.3f}")
has("K R1 radial corner", f"{r25['R1']['canonical']['corners']['J1|A1']['grade']['dabs_dex']['F0']:.3f}")
e1 = r25["R3"]["canonical"]["corners"]["E1|nom"]
has("K R3 satellites", f"{e1['sat_mean_shift_dex']:+.2f}"); has("K R3 dwarf class", f"→ {e1['grade']['res_dex']['F0']:+.3f}")
check("K CFG925 classes", r25["classes"]["R1|canonical"] == r25["classes"]["R1|alt"] == "NO EFFECT"
      and all(r25["classes"][x] == "WORSENS" for x in ("R2|canonical", "R2|alt", "R2B|canonical", "R2B|alt", "R3|canonical", "R3|alt")))
led("K R2 range", "CFG925", "0.1-1.8 dex", "0.1-1.8")
r26 = J("CFG926_small_reframings_B/cfg926_results.json")
for foot in ("canonical", "alt"):
    t = r26["R5"]["byfoot"][foot]["target_F1"]
    has(f"K R5 {foot}", f"{t['obs'] / math.log(10):+.3f} → {t['res'] / math.log(10):+.3f}"); check(f"K R5 {foot} RESOLVES", t["label"] == "RESOLVES")
sc = r26["R5"]["byfoot"]["canonical"]["split_cells"]; has("K R5 split", f"{sc['before']:.2f} → {sc['after']:.2f}")
hz = r26["R4"]["canonical"]["H(z)"]["targets"]
has("K R4 rival dwarfs", f"{hz['F0']['pred']:+.2f} against {hz['F0']['obs']:+.2f}"); has("K R4 rival clusters", f"{100 * hz['F5']['removed_frac']:.0f}%")
md = r26["R4"]["canonical"]["M-DEC"]["targets"]["F0"]["pred"]; has("K R4 DE-tracking wrong sign", f"about {abs(md) / math.log(10):.2f} dex below the law")
check("K R4 flat NO EFFECT, rival PARTIAL", r26["summary"]["canonical"]["R4"]["FLAT"] == "NO EFFECT" and r26["summary"]["canonical"]["R4"]["H(z)"].startswith("PARTIAL"))
led("K R6", "CFG926", "-0.004 ln", "-0.004 (ln)"); led("K R6 full", "CFG926", "-0.023 ln", "-0.023")
led("K R5 49%", "CFG926", "49%"); led("K R5 45%", "CFG926", "45%")
check("K R4 reported as evidence, not rescue", "evidence about" in flat and "as a rescue" in flat)  # the phrase straddles a page break

# ---------------------------------------------------------------- L. in-progress statements and disclosures
# CFG928 landed while this note was written: its result is reported, so check it against its JSON and LEDGER row
r28 = J("CFG928_posit_regrade_imf/cfg928_results.json")
check("L CFG928 LEDGER row exists and is reported", bool(row("CFG928")) and "A conditional re-grade (CFG928)" in flat)
check("L CFG928 trials factor 20", r28["trials"]["N_T"] == 20 and "trials factor 20" in flat)
cl28 = {q: r28["classes"][q]["per_footing"] for q in r28["classes"]}
check("L CFG928 P2 SURVIVES (galaxy-scale) both, P4 UNDERDETERMINED, P1/P3/P5 FAIL",
      all(v == "SURVIVES (galaxy-scale)" for v in cl28["P2"].values()) and all(v == "UNDERDETERMINED" for v in cl28["P4"].values())
      and all(v == "FAILS" for q in ("P1", "P3", "P5") for v in cl28[q].values()) and "SURVIVES on the galaxy-scale facts" in flat)
check("L CFG928 P2 FRAGILE and C1-dependent (canonical)", r28["classes"]["P2"]["fragile"] and r28["classes"]["P2"]["c1_dependent"]
      and all(x.startswith("canonical") for x in r28["classes"]["P2"]["c1_dependent_by"]) and "FRAGILE" in flat)
sn = r28["sealed_numbers"]
has("L CFG928 v_2", f"= {sn['P2|canonical']['theta']:.2f} / {sn['P2|alt']['theta']:.2f} km/s")
has("L CFG928 clusters z", f"z = -{sn['P2|canonical']['clusters']['F5_min_abs_z']:.1f} / -{sn['P2|alt']['clusters']['F5_min_abs_z']:.1f}")
has("L CFG928 cluster supply", f"x{sn['P2|canonical']['clusters']['supply_g_factor']:.2f} / x{sn['P2|alt']['clusters']['supply_g_factor']:.2f}")
led("L CFG928 best of 20", "CFG928", "best of 20", "best of 20 posit-framings")
led("L CFG928 needs +0.123 correction", "CFG928", "+0.123", "+0.123")
led("L CFG928 sealed UDG prediction", "CFG928", "Sealed prediction (P2)", "is sealed")
# CFG929 landed after the first draft: its result is reported, checked against its JSON and LEDGER row
r29 = J("CFG929_cluster_core_reframings/cfg929_results.json")
s29 = r29["summary"]
check("L CFG929 classes: a/b/c NO EFFECT, d BREAKS SOMETHING", s29["a"].startswith("NO EFFECT") and s29["b"] == s29["c"] == "NO EFFECT"
      and s29["d"] == "BREAKS SOMETHING" and "BREAKS SOMETHING" in flat and "(CFG929)" in flat)
fr = [r29["results"]["a"]["rows"][f"nu_beta_best|{f}"]["cls"]["f_rem"] for f in ("canonical", "alt")]
has("L CFG929 best removal", f"{100 * fr[0]:.1f}% / {100 * fr[1]:.1f}%")
led("L CFG929 none resolves", "CFG929", "none resolves it", "None resolves it")
led("L CFG929 real mass the law does not supply", "CFG929", "real mass the law does not supply", "real mass that the law does not supply")
led("L CFG929 MUTATE leg disclosed", "CFG929", "post-hoc Md-b holds", "a post-hoc replacement leg holds")
check("L no stale CFG929 in-progress statement", "no ledger results yet" not in flat and "In progress" not in flat)
for lane in ("CFG917 A1", "CFG919 A1", "CFG921 A1", "CFG925 A1", "CFG926 A1", "CFG914 A1", "CFG918 A1", "CFG922 A1"):
    has(f"L disclosure {lane}", lane)
for lane, s in (("CFG917", "A1 187f895aa POST HOC"), ("CFG919", "POST HOC"), ("CFG921", "POST HOC"), ("CFG925", "POST HOC"), ("CFG926", "POST HOC")):
    check(f"L LEDGER marks {lane} amendment post hoc", s in row(lane))
rd("L footings", "CFG919_pressure_support_selector/README.md", "9.3603e-11 / 1.1312e-10", "9.36")
has("L footing alt in PDF", "1.13")

# ---------------------------------------------------------------- N. citations (deposit-prep pass, 2026-10-21)
# Journal references verified against the publisher DOI records (Crossref; Wolf+10 volume/page from its arXiv journal-ref):
#   Asgari+21 10.1051/0004-6361/202039070; Giblin+21 10.1051/0004-6361/202038850; Amon+22 10.1103/PhysRevD.105.023514;
#   Secco+22 10.1103/PhysRevD.105.023515; Carron+22 10.1088/1475-7516/2022/09/039; Planck 2018 VI 10.1051/0004-6361/201833910;
#   Planck 2018 VIII 10.1051/0004-6361/201833886; Brouwer+21 10.1051/0004-6361/202040108; SPARC 10.3847/0004-6256/152/6/157;
#   Weisz+14 10.1088/0004-637X/789/2/147; Pace 2025 (LVD) 10.33232/001c.144859; Bulbul+24 10.1051/0004-6361/202348264;
#   Cavagnolo+09 10.1088/0067-0049/182/1/12; Ettori+19 10.1051/0004-6361/201833323; Cappellari+13 10.1093/mnras/stt562, stt644;
#   Auger+09 10.1088/0004-637X/705/2/1099; Wolf+10 10.1111/j.1365-2966.2010.16753.x; Chabrier 03 10.1086/376392; CAMB 10.1086/309179.
#   PAPER55 = 10.5281/zenodo.23482936 (public Zenodo record).
for s in ("M. Asgari et al., A&A 645, A104 (2021)", "B. Giblin et al., A&A 645, A105 (2021)", "A. Amon et al., PRD 105, 023514 (2022)",
          "L. F. Secco et al., PRD 105, 023515 (2022)", "JCAP 09 (2022) 039", "A&A 641, A6 and A8 (2020)", "M. M. Brouwer et al., A&A 650, A113 (2021)",
          "AJ 152, 157 (2016)", "D. R. Weisz et al., ApJ 789, 147 (2014)", "A. B. Pace, Open J. Astrophys. 8 (2025)", "E. Bulbul et al., A&A 685, A106 (2024)",
          "K. W. Cavagnolo et al., ApJS 182, 12 (2009)", "S. Ettori et al., A&A 621, A39 (2019)", "MNRAS 432, 1709 and 1862 (2013)",
          "M. W. Auger et al., ApJ 705, 1099 (2009)", "J. Wolf et al., MNRAS 406, 1220 (2010)", "G. Chabrier, PASP 115, 763 (2003)",
          "ApJ 538, 473 (2000) (CAMB)", "PAPER55, doi:10.5281/zenodo.23482936"):
    has(f"N citation '{s[:44]}'", s)
check("N KiDS-1000 SOM-gold shear is what the cluster stacks use (CFG686/687)", "KiDS-1000 SOM-gold" in readme("CFG686_cluster_shear_vs_law/FROZEN_CRITERIA.md")
      and "KiDS-1000 SOM-gold" in readme("CFG687_erass1_shear_stack/FROZEN_CRITERIA.md"))

# ---------------------------------------------------------------- M. honesty phrases, forbidden claims, paths
for s in ("fitted", "the theory is not closed", "not peer reviewed", "conditional", "never pooled", "post-hoc", "not a preference",
          "not established", "AI-assisted", "Anthropic's Claude"):
    has(f"M honesty '{s}'", s)
low = flat.lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework",
            "breakthrough", "/users/", "gmail", "dark matter particle"):
    check(f"M forbidden '{bad}' absent", bad not in low)
check("M no home path in TeX", "/Users/" not in tex and "~/" not in tex)

# ---------------------------------------------------------------- V. v1.1 correction (2026-10-23): CFG963, attribution of the native shear pass
C63 = "CFG963_shear_attribution"
r63 = J(f"{C63}/cfg963_attrib_results.json")          # frozen-criteria scoring (f2354ed22)
u63 = J(f"{C63}/cfg963_reuse_results.json")           # amendment A1 items (CFG646 bracket R3, K2-K4)
p1 = norm(subprocess.run(["pdftotext", "-f", "1", "-l", "1", PDF, "-"], capture_output=True, text=True, check=True).stdout)
BOX0 = "\\noindent\\fbox{\\parbox{"
BOXT = "\\textbf{Correction (v1.1, 2026-10-23).}"
ib, ia, ic = tex.find(BOX0), tex.find("\\begin{abstract}"), tex.find("\\end{center}")
check("V1 correction box in the TeX, dated, between the title block and the abstract", 0 <= ic < ib < tex.find(BOXT) < ia and tex.count(BOXT) == 1)
box_end = tex.find("\n\n\\begin{abstract}")
box = tex[ib:box_end] if 0 <= ib < box_end else ""
check("V1 correction box closes before the abstract", box.rstrip().endswith("}}") and "Consequences." in box)
check("V1 correction box on PDF page 1, dated", "Correction (v1.1, 2026-10-23)." in p1 and "Consequences." in p1 and "M3-CARRIED on both footings" in p1)
has("V2 header v1.1 dated 2026-10-23", "Working note, v1.1, 2026-10-23 (correction of v1.0 of 2026-10-21; see the box below)")
check("V2 v1.0 header gone", "Working note, 2026-10-21, v1.0" not in flat and "2026-10-21, v1.0." not in tex)
# --- no unqualified "matched control": outside the box only "feedback-matched"; inside it, one quotation of v1.0
outside = tex if not box else tex[:ib] + tex[box_end:]
MC = re.compile(r"matched\s+(?:Poisson\s+)?control", re.I)
def mc_hits(text, quote):
    """(unqualified, quoted) starts of 'matched (Poisson) control'; 'feedback-matched' is qualified, a quotation of v1.0 is quoted"""
    un, qu = [], []
    for m_ in MC.finditer(text):
        pre = text[:m_.start()]
        if pre.endswith("feedback-"):
            continue
        (qu if pre.endswith(quote) else un).append(m_.start())
    return un, qu
un, qu = mc_hits(outside, "``")
check("V3 TeX outside the box: no 'matched control' except 'feedback-matched'", not un and not qu, f"{len(un)} unqualified, {len(qu)} quoted")
un, qu = mc_hits(box, "``")
check("V3 TeX inside the box: 'matched control' only as the one quotation of v1.0", bool(box) and not un and len(qu) == 1, f"{len(un)} unqualified, {len(qu)} quoted")
for i_, mode in enumerate(("layout", "reading-order")):
    un = [s_ for s_ in mc_hits(raw[i_], "“")[0] if not raw[i_][:s_].endswith('"')]
    qu = mc_hits(raw[i_], "“")[1]
    check(f"V3 PDF ({mode}): no unqualified 'matched control'; one quotation of v1.0", not un and len(qu) == 1, f"{len(un)} unqualified, {len(qu)} quoted")
check("V3 'matched in initial conditions only' in the box, the abstract, section 1 and the disclosures",
      len(re.findall(r"matched in initial conditions only", outside)) == 3 and "NCS0 is matched in initial conditions only.}" in box
      and len(re.findall(r"matched in initial conditions only", flat)) >= 8)   # 4 places x 2 extractions
# --- the v1.0 sentences that presented -10.08 / -9.39 as the framework's lead or preference are gone
for s in ("against its matched control on both footings", "The size of the lead is set mainly by the lensing amplitude",
          "The framework beats its control by suppressing small-scale power", "so the pass is a computational result of that engine",
          "Four caveats limit what this means", "is the same pipeline on the same initial conditions with plain Poisson gravity"):
    check(f"V4 v1.0 sentence gone from TeX and PDF: '{s[:50]}'", s not in tex and norm(s) not in flat)
# --- every changed sentence is present and marked "Correction v1.1"
MK = "(Correction v1.1)"
for s in ("which is matched in initial conditions only and has no gas expulsion (∆χ2 = -10.08 canonical, -9.39 alternative; Correction v1.1)",
          "KiDS cannot tell the capped cold sector from plain gravity plus gas expulsion, and the result shows that the capped cold sector does not "
          "overproduce structure, not a preference for the law " + MK,
          "On the alternative footing DES Y3 is diagnostic and also CONSISTENT (-2.15), but plain gravity with the expulsion gives -2.17 " + MK,
          "Shear ∆χ2 sizes are set mainly by the lensing amplitude, and no arm fits well in absolute terms " + MK,
          "The engine that produces the pass has no established physical parent (PAPER57); per CFG963 that is not load-bearing for the shear result " + MK,
          "The control, NCS0, is the same pipeline with every module off (plain Poisson gravity) on the same initial conditions; it has no a0 , so it "
          "serves both footings, but it is matched in initial conditions only: it applies no gas expulsion, while NC1x and NC2x include the census gas "
          "expulsion M3 (CFG963; Correction v1.1)",
          "Five caveats limit what this means; the first is new in v1.1 " + MK,
          "The lead over NCS0 is carried by gas expulsion " + MK,
          "The CONSISTENT class holds against this fair control too, but KiDS cannot tell the capped cold sector from plain gravity plus gas expulsion",
          "CFG963 traces the deficit to the gas expulsion: the M3 transfer alone is", "at the same k " + MK,
          "The framework beats NCS0 by suppressing small-scale power, and the suppression is the gas expulsion's: plain gravity with the same expulsion reaches",
          "as good a fit or slightly better " + MK,
          "Per CFG963 the missing parent is not load-bearing for the shear result: any parent that clusters like plain dust on",
          "and expels the census gas would pass " + MK,
          "Against plain gravity with the same gas expulsion it is also CONSISTENT", "the pass shows only that the capped cold sector does not overproduce "
          "structure (CFG963; Correction v1.1)",
          "Also not established: any shear preference for the law over plain gravity with gas expulsion (CFG963; Correction v1.1)",
          "v1.1 corrects the reading of the native shear result: NCS0 is matched in initial conditions only, and the lead over it is carried by the census "
          "gas expulsion (CFG963, a diagnostic attribution reported only; its CFG646 bracket comes from amendment A1, written after the frozen result was seen)",
          "for v1.1, CFG963"):
    has(f"V5 changed text '{s[:56]}'", s)
check("V5 13 'Correction v1.1' markers outside the box, none left unmatched", outside.count("Correction v1.1") == 13
      and len(re.findall(r"Correction v1\.1", raw[1])) == 14, f"TeX {outside.count('Correction v1.1')}, PDF {len(re.findall(r'Correction v1.1', raw[1]))}")
check("V5 Table 1 float at [b] (v1.1 re-pagination; caption and rows unchanged)", "\\begin{table}[b]" in tex and "\\begin{table}[t]" not in tex
      and "Table 1: Six small reframings of the pressure-supported excess." in flat)
# --- wording from CFG963's LEDGER row and README
L63 = row("CFG963")
for s, pdf_s in (("M3-CARRIED on both footings", None), ("matched in ICs only", "matched in initial conditions only"),
                 ("KiDS cannot tell the framework's capped cold sector from plain gravity + the same gas expulsion",
                  "KiDS cannot tell the framework's capped cold sector from plain gravity plus gas expulsion"),
                 ("the capped cold sector does not overproduce", "the capped cold sector does not overproduce structure"),
                 ("not a preference for the law", None), ("The engine-parent problem is not load-bearing for this result", "missing parent is not load-bearing for this result"),
                 ("+68.7", "excluded at +68.7 (CFG596)"), ("A1 64718930a committed alone before its numbers", "64718930a, committed alone before its numbers")):
    check(f"V6 LEDGER CFG963 '{s[:48]}' (and the PDF)", bool(L63) and s in L63 and (pdf_s or s) in flat)
R63 = f"{C63}/README.md"
for s, pdf_s in (("CFG596's uncapped engine gave +68.7", "the uncapped settling engine was excluded at +68.7"),
                 ("DIAGNOSTIC attribution, reported only", "diagnostic attribution, reported only"),
                 ("This lane changes how that pass is read, not its class", "it changes how the result reads, not any frozen class"),
                 ("clusters like plain dust", None), ("and expels the census gas would pass", None),
                 ("The decisive 1024³ control NCS0+M3 is designed but not run", "is designed but not run"),
                 ("Before amendment A1, the frozen result", "after the frozen result was seen")):
    rd(f"V6 README CFG963 '{s[:48]}'", R63, s, pdf_s)
crit = readme(f"{C63}/FROZEN_CRITERIA.md")
check("V6 noise scale |d| >= 4 is the frozen 'KiDS can tell' rule; M3-CARRIED needs f >= 0.70 and |d| <= 3", "Only if |d| ≥ 4 (the CFG592 TENSION scale)" in crit
      and "**M3-CARRIED** if f ≥ 0.70 AND |d| ≤ 3" in crit and "< 4 noise scale" in flat and "< 4 against the fair control" in flat)
# --- numbers: every CFG963 number in the note is read from its results JSON
at = r63["attribution"]; pr = r63["pairs"]
kid = lambda p: pr[p]["surveys"]["KiDS"]
bt = lambda f_, t_: at[f_]["by_transfer"][t_]
r3 = u63["R3_attribution"]
check("V7 CFG963 controls exact: K (stored NC1x / NC2x vs NCS0), A1 K2-K4; not a mutation run; the note says reported only",
      r63["K_pass"] and r63["K_max_abs_diff"] == 0 and u63["K2_pass"] and u63["K34_pass"] and r63["mutate"] is False and u63["mutate"] is False
      and abs(kid("K_NC1x_vs_NCS0")["dchi2"] - n1["surveys"]["KiDS"]["dchi2"]) < 1e-9 and abs(kid("K_NC2x_vs_NCS0")["dchi2"] - n2["surveys"]["KiDS"]["dchi2"]) < 1e-9
      and "CFG963 is a diagnostic attribution, reported only" in flat)
check("V7 stored leads -10.08 / -9.39 quoted in the box (JSON)", f"framework's {f2(at['canonical']['dchi2_framework_vs_NCS0'])} / {f2(at['alt']['dchi2_framework_vs_NCS0'])}" in flat)
ex = [r63["m3_expelled_mass_frac"][r_][z_] for r_ in ("NC1x", "NC2x") for z_ in ("z0", "z0.5", "z1")]
check("V7 M3 re-places 3.2-3.7% of all mass at z = 0-1, NC1x and NC2x (JSON)", f"{100 * min(ex):.1f}-{100 * max(ex):.1f}" == "3.2-3.7"
      and f"re-places {100 * min(ex):.1f}-{100 * max(ex):.1f}% of all mass at z = 0-1" in flat, f"{min(ex):.4f}..{max(ex):.4f}")
m3 = {t_: kid(f"S0+M3[{t_}]_canonical_vs_NCS0")["dchi2"] for t_ in ("M3-1024", "M3-256", "M3-alone-256")}
check("V7 one surrogate serves both footings (canonical = alt pair, every bracket; R3 too)", all(kid(f"S0+M3[{t_}]_alt_vs_NCS0")["dchi2"] == m3[t_] for t_ in m3)
      and r3["canonical"]["dchi2_S0M3_vs_NCS0"] == r3["alt"]["dchi2_S0M3_vs_NCS0"] and "(a surrogate: NCS0 times the M3 transfer" in flat)
check("V7 plain gravity + M3 vs NCS0 -11.87 (JSON), box and abstract", f2(m3["M3-1024"]) == "-11.87" and f"{f2(m3['M3-1024'])} against NCS0 on KiDS-1000" in flat
      and f"census gas expulsion scores {f2(m3['M3-1024'])} against NCS0" in flat)
fc, fa = bt("canonical", "M3-1024")["f"], bt("alt", "M3-1024")["f"]
has("V7 f = 118% canonical / 126% alt (JSON)", f"{100 * fc:.0f}% (canonical) and {100 * fa:.0f}% (alternative)")
has("V7 brackets 256^3 / M3 alone / CFG646 (JSON, R3 from A1)", f"give {f2(m3['M3-256'])}, {f2(m3['M3-alone-256'])} and {f2(r3['canonical']['dchi2_S0M3_vs_NCS0'])}")
d1, d2_ = bt("canonical", "M3-1024")["dchi2_framework_vs_S0M3"], bt("alt", "M3-1024")["dchi2_framework_vs_S0M3"]
has("V7 NC1x / NC2x vs the feedback-matched control +1.78 / +2.47 (JSON), box", f"NC1x scores {d1:+.2f} and NC2x {d2_:+.2f}")
check("V7 +1.78 / +2.47 in the abstract and section 4 (JSON)", f"framework scores {d1:+.2f} / {d2_:+.2f} against it, within noise" in flat
      and f"also CONSISTENT ({d1:+.2f} / {d2_:+.2f})" in flat and f"NC1x scores {d1:+.2f} and NC2x {d2_:+.2f}, within noise" in flat)
db = {f_: [bt(f_, t_)["dchi2_framework_vs_S0M3"] for t_ in ("M3-256", "M3-alone-256")] + [r3[f_]["dchi2_framework_vs_S0M3"]] for f_ in ("canonical", "alt")}
has("V7 bracket ranges of d (JSON)", f"(brackets {min(db['canonical']):+.2f} to {max(db['canonical']):+.2f} and {min(db['alt']):+.2f} to {max(db['alt']):+.2f})")
alld = [d1, d2_] + db["canonical"] + db["alt"]
check("V7 every d within |d| < 4, KiDS never distinguishes, M3-CARRIED in every bracket and both footings (JSON)",
      all(abs(v) < 4 for v in alld) and all(not bt(f_, t_)["KiDS_distinguishes"] and bt(f_, t_)["attribution"] == "M3-CARRIED"
      for f_ in ("canonical", "alt") for t_ in ("M3-1024", "M3-256", "M3-alone-256")) and all(at[f_]["class_primary"] == "M3-CARRIED" for f_ in at)
      and all(r3[f_]["attribution"] == "M3-CARRIED" for f_ in r3) and "M3-CARRIED on both footings and in every bracket" in flat, f"max |d| {max(map(abs, alld)):.2f}")
m12 = at["canonical"]["M12"]["M12-1024"]["dchi2_S0M12_vs_NCS0"]
check("V7 M1+M2 alone vs NCS0 +2.66 (JSON), box and section 1", m12 == at["alt"]["M12"]["M12-1024"]["dchi2_S0M12_vs_NCS0"]
      and f"(M1+M2) alone score {m12:+.2f} against NCS0" in flat and f"rules alone cost {m12:+.2f} against NCS0" in flat)
cl = (at["canonical"]["closure"], at["alt"]["closure"])
check("V7 closure -10.21 / -9.51, to within 0.13, PASS (JSON)", all(c_["PASS"] for c_ in cl)
      and f"to within {max(abs(c_['diff']) for c_ in cl):.2f} ({f2(cl[0]['dchi2'])} / {f2(cl[1]['dchi2'])})" in flat)
dz = pr["S0+M3[M3-1024]_canonical_vs_NCS0"]["surveys"]["DES"]["dchi2"]
dd = [pr[f"{r_}_vs_S0+M3[M3-1024]"]["surveys"]["DES"] for r_ in ("NC1x", "NC2x")]
check("V7 DES: plain gravity + M3 -2.17 vs NCS0; framework +0.27 / +0.43 vs it, NOT DIAGNOSTIC (JSON)", all(x["class"] == "NOT DIAGNOSTIC" for x in dd)
      and f"plain gravity plus M3 gives {f2(dz)} against NCS0, and the framework {dd[0]['dchi2']:+.2f} / {dd[1]['dchi2']:+.2f} against it (NOT DIAGNOSTIC)" in flat
      and f"plain gravity with the expulsion gives {f2(dz)}" in flat)
s3 = kid("S0+M3[M3-1024]_canonical_vs_NCS0")
check("V7 plain gravity + M3 absolute fit 142.89 on 108 points (JSON)", s3["N_kept"] == 108 and f"reaches {f2(s3['chi2_F'])} on {s3['N_kept']} points" in flat
      and f"= {f2(s3['chi2_F'])}, as good a fit or slightly better" in flat and s3["chi2_F"] < min(n1["surveys"]["KiDS"]["chi2_F"], n2["surveys"]["KiDS"]["chi2_F"]))
tm = r63["transfers"]["M3-1024"]["z0"]
has("V7 M3 transfer at k = 0.3 / 0.5 / 1, z = 0 (JSON)", f"the M3 transfer alone is {tm['0.3']:.3f}, {tm['0.5']:.3f} and {tm['1.0']:.3f} at the same k")
# --- credits: the lane's commits exist and are what the note says they are
def gsub(c):
    r_ = subprocess.run(["git", "log", "-1", "--format=%s", c], capture_output=True, text=True, cwd=HERE)
    return r_.stdout.strip() if r_.returncode == 0 else ""
for c, key, s in (("d3b18181c", "CFG963 FROZEN_CRITERIA", "frozen criteria d3b18181c"), ("f2354ed22", "CFG963 scoring under the frozen criteria", "frozen scoring f2354ed22"),
                  ("64718930a", "CFG963 AMENDMENT A1", "amendment A1 64718930a"), ("e96c21a87", "CFG963 amendment A1 results", "results e96c21a87")):
    check(f"V8 commit {c} exists ({key}) and is credited in the PDF", key in gsub(c) and s in flat)
check("V8 the JSONs name the same criteria and amendment commits", r63["criteria"] == "FROZEN_CRITERIA.md (d3b18181c)" and u63["amendment"] == "AMENDMENT_A1_2026-10-23.md (64718930a)"
      and "CFG963" in L63 and L63.rstrip(" |").endswith("e96c21a87") and "Source: the repository lane CFG963 (frozen criteria d3b18181c" in flat)
# --- Zenodo metadata for the new version
ZJ = os.path.join(HERE, "PAPER56_pressure_supported_excess_2026.zenodo.json")
zj = json.load(open(ZJ, encoding="utf-8"))["metadata"]
z0 = json.loads(subprocess.run(["git", "show", "ee866f4bc2:qwen_claude_field_theory/papers_2026/PAPER56_pressure_supported_excess_2026.zenodo.json"],
                               cwd=HERE, capture_output=True, text=True, check=True).stdout)["metadata"]
zd = re.sub(r"<[^>]+>", "", zj["description"])
check("V9 Zenodo version 1.1", zj["version"] == "1.1" and z0["version"] == "1.0")
check("V9 Zenodo description leads with 'Correction (v1.1, 2026-10-23):'", zd.startswith("Correction (v1.1, 2026-10-23):") and "version 1.1 (2026-10-23; v1.0 2026-10-21)" in zd)
check("V9 Zenodo isNewVersionOf 10.5281/zenodo.23532875", {"identifier": "10.5281/zenodo.23532875", "relation": "isNewVersionOf", "scheme": "doi"} in zj["related_identifiers"])
check("V9 Zenodo keeps v1.0's other fields and every v1.0 related identifier", all(zj[k_] == z0[k_] for k_ in z0 if k_ not in ("version", "description", "related_identifiers"))
      and set(zj) == set(z0) and all(r_ in zj["related_identifiers"] for r_ in z0["related_identifiers"]) and len(zj["related_identifiers"]) == len(z0["related_identifiers"]) + 1)
un, qu = mc_hits(zd, "'")
check("V9 Zenodo description: no unqualified 'matched control'; one quotation of v1.0", not un and len(qu) == 1 and "matched in initial conditions only" in zd, f"{len(un)} unqualified, {len(qu)} quoted")
check("V9 Zenodo: v1.0 lead wording gone", all(s not in zd for s in ("The size of the lead is amplitude-driven", "against its matched Poisson control",
      "(companion note PAPER57): the pass is a computational result")))
check("V9 Zenodo numbers match CFG963 JSON", f"Delta chi^2 = {f2(m3['M3-1024'])} against NCS0" in zd and f"{d1:+.2f} (canonical) / {d2_:+.2f} (alternative)" in zd
      and f"framework scores {d1:+.2f} / {d2_:+.2f}" in zd and f"rules alone score {m12:+.2f}" in zd and f"re-places {100 * min(ex):.1f}-{100 * max(ex):.1f}% of all mass" in zd
      and f"plain gravity with the expulsion gives {f2(dz)}" in zd and "excluded at +68.7" in zd and "M3-CARRIED on both footings" in zd
      and all(c in zd for c in ("d3b18181c", "f2354ed22", "64718930a", "e96c21a87")) and "(Delta chi^2 -10.08 canonical, -9.39 alternative)" in zd)
check("V9 Zenodo honesty kept, nothing forbidden", "kappa = 1/2 is fitted; the theory is not closed" in zd and "A CONSISTENT class is not a preference" in zd
      and "not a preference for the law" in zd and not any(b_ in zd.lower() for b_ in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "/users/", "gmail")))

print(f"\nPAPER56 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
