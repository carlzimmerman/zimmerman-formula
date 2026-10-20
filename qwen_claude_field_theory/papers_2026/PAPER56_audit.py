#!/usr/bin/env python3
"""PAPER56 audit: the built PDF must be newer than the TeX and 4-6 pages long; every quoted number must match the committed lane
outputs (JSON first; LEDGER row or lane README text where the number lives only there); the honesty phrases and post-hoc
disclosures must be present; the in-progress statements must still be true; no forbidden claim or local path may appear.
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
check("A2 page count 4-6", 4 <= pages <= 6, f"{pages} pages")
# two extractions of the same PDF: layout mode (running text) and reading-order mode (keeps table cells contiguous)
flat = " ||| ".join(norm(subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout) for m in (["-layout"], []))
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
check("B NC2x still running (no NC2x result file)", not os.path.exists(os.path.join(CFG, "CFG654_independent_inputs/cfg654_native_results_NC2x.json"))
      and "is running" in flat)

# ---------------------------------------------------------------- C. CFG909 amplitude caveat
c9 = J("CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC1x.json")
g = c9["grid"]; has("C Om grid", f"{min(g):.4f}-{max(g):.4f}")
dk = lambda v: c9["variants"][v]["results"]["canonical"]["KiDS"]["cfg"]["main"]["dchi2"]
has("C dchi2 at Om 0.2806", f2(dk("OM_0.2806"))); has("C dchi2 at Om 0.3308", f2(dk("OM_0.3308")))
has("C own covariance", f2(dk("CV1_OWN")))
check("C class ROBUST", c9["lane_class"] == "ROBUST" and "ROBUST" in flat)
led("C power deficit 3-6%", "CFG909", "3-6% power deficit")

# ---------------------------------------------------------------- D. CFG917 CMB lensing
a1 = J("CFG917_cmb_lensing_gate/cfg917_A1_classes.json")["pairs"]
for p in ("NC1x", "T1x", "T2x"):
    q = a1[p]
    has(f"D {p} part A dA", f"{q['partA_dA']:.4f}"); check(f"D {p} part A SAFE", q["partA_label"] == "SAFE")
    has(f"D {p} dchi2", f"{q['dchi2']:.3f}"); has(f"D {p} chi2 F", f"{q['chi2_F']:.3f}"); has(f"D {p} chi2 S0", f"{q['chi2_S0']:.3f}")
    check(f"D {p} frozen NOT DIAGNOSTIC / A1 CONSISTENT / gate PASS",
          q["class_frozen"] == "NOT DIAGNOSTIC" and q["class_A1"] == "CONSISTENT" and q["gate_A1"] == "PASS")
mr = max(abs(v) for p in ("NC1x", "T1x", "T2x") for v in a1[p]["robust"].values())
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
check("L CFG929 still in progress (criteria only, no LEDGER result row)", row("CFG929") == ""
      and sorted(os.listdir(os.path.join(CFG, "CFG929_cluster_core_reframings"))) == ["FROZEN_CRITERIA.md"] and "no ledger results yet" in flat)
for lane in ("CFG917 A1", "CFG919 A1", "CFG921 A1", "CFG925 A1", "CFG926 A1", "CFG914 A1", "CFG918 A1", "CFG922 A1"):
    has(f"L disclosure {lane}", lane)
for lane, s in (("CFG917", "A1 187f895aa POST HOC"), ("CFG919", "POST HOC"), ("CFG921", "POST HOC"), ("CFG925", "POST HOC"), ("CFG926", "POST HOC")):
    check(f"L LEDGER marks {lane} amendment post hoc", s in row(lane))
rd("L footings", "CFG919_pressure_support_selector/README.md", "9.3603e-11 / 1.1312e-10", "9.36")
has("L footing alt in PDF", "1.13")

# ---------------------------------------------------------------- M. honesty phrases, forbidden claims, paths
for s in ("fitted", "the theory is not closed", "not peer reviewed", "conditional", "never pooled", "post-hoc", "not a preference",
          "not established", "AI-assisted", "Anthropic's Claude"):
    has(f"M honesty '{s}'", s)
low = flat.lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework",
            "breakthrough", "/users/", "gmail", "dark matter particle"):
    check(f"M forbidden '{bad}' absent", bad not in low)
check("M no home path in TeX", "/Users/" not in tex and "~/" not in tex)

print(f"\nPAPER56 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
