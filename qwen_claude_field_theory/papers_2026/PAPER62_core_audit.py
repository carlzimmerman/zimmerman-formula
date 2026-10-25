#!/usr/bin/env python3
"""PAPER62 core-note audit: the built PDF must be newer than the TeX and the figure; every quoted number must match the committed
lane outputs (rebuild_2026_10_22/ P4, U1, X11, X13, X20_hosted_dwarf_disequilibrium, X22, X24, X25, X30, X34, X36, EM1,
X38-X44, MAP1: *_results.json, else the lane's .out or README; covariant_push_2026_10_22/ C6, C8 and
V3S_FINAL_VERDICT_2026-10-24.md; rebuild_2026_10_22/COLD_SECTOR_SPEC_2026-10-24.md); every cited commit must exist and
touch its lane; the figure is regenerated in memory from MAP1's JSON and its counts checked; the PENDING statement (no L1
production result) must be true at build time; citations must match citations/REFERENCES.bib where present; naming
rules (cold dark energy; CDM only as LambdaCDM), no forbidden claim, local path or personal name.
Run: python3 PAPER62_core_audit.py (exit 0 only if all pass).
     python3 PAPER62_core_audit.py --mutate (perturbs the last digit of every JSON- or .out-formatted number; exit 0 only if
     every such check then FAILS, i.e. each number check is live).  Read-only."""
import json, math, os, re, subprocess, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RB = os.path.join(ROOT, "rebuild_2026_10_22")
CV = os.path.join(ROOT, "covariant_push_2026_10_22")
STEM = "PAPER62_galaxy_law_sets_the_core_2026"
TEX = os.path.join(HERE, STEM + ".tex")
PDF = os.path.join(HERE, STEM + ".pdf")
ZJ = os.path.join(HERE, STEM + ".zenodo.json")
FIGPY = os.path.join(HERE, "PAPER62_fig_river.py")
FIGPDF = os.path.join(HERE, "PAPER62_fig_river.pdf")
F = 0
N = 0
NUM = []


def check(name, ok, msg=""):
    global F, N
    N += 1
    if not MUT:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    F += (not ok)


SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("ﬃ", "ffi"), ("−", "-"), ("–", "-"), ("—", "-"), ("’", "'"), ("‘", "'"),
                 (" ", " "), ("µ", "μ"), ("∆", "Δ"), ("ϕ", "φ"), ("∗", "*"), ("**", ""), ("\\|", "|"), ("⋆", "★"), ("ϵ", "ε"), ("“", '"'), ("”", '"')):
        t = t.replace(a, b)
    t = t.translate(SUB)
    t = re.sub(r"\s*×\s*", "x", t)
    t = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", t)
    t = re.sub(r"(?<=\w) (?=[,.;:)])", "", t)
    t = re.sub(r"\s*±\s*", " ± ", t)
    t = re.sub(r"\s*=\s*", " = ", t)
    return re.sub(r"\s+", " ", t)


def dehyph(t):
    return re.sub(r"([a-z])- ([a-z])", r"\1\2", t)


def keephyph(t):
    return re.sub(r"([A-Za-z])- ([A-Za-z])", r"\1-\2", t)


def sci(x, d):
    m, e = f"{x:.{d}e}".split("e")
    return f"{m}x10{int(e)}"


def bump(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isdigit():
            return s[:i] + str((int(s[i]) + 1) % 10) + s[i + 1:]
    return s + "9"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=ROOT)


# ---------------------------------------------------------------- A. build
check("A1 PDF newer than TeX and figure", os.path.getmtime(PDF) >= os.path.getmtime(TEX) and os.path.getmtime(PDF) >= os.path.getmtime(FIGPDF))
check("A1b figure newer than its script", os.path.getmtime(FIGPDF) >= os.path.getmtime(FIGPY))
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
    """value_str is formatted from a committed JSON / .out value; ctx (with {}) is the PDF wording around it"""
    if MUT:
        s = norm(ctx.format(bump(value_str)))
        NUM.append((name, s not in flat))
        return
    s = norm(ctx.format(value_str))
    check(name, s in flat, s)


def JS(lane, fname, base=RB):
    return json.load(open(os.path.join(base, lane, fname)))


def TX(path):
    return norm(open(path, encoding="utf-8").read())


VERD = os.path.join(CV, "V3S_FINAL_VERDICT_2026-10-24.md")
SPEC = os.path.join(RB, "COLD_SECTOR_SPEC_2026-10-24.md")


def rd(name, path, s, pdf_s=None):
    """s must be in the source file AND (s, or pdf_s) in the PDF"""
    s, p = norm(s), norm(pdf_s or s)
    check(name, s in TX(path) and p in flat, f"{os.path.basename(os.path.dirname(path))}/{os.path.basename(path)}: '{s}'" + (f" / PDF '{p}'" if pdf_s else ""))


def readme(lane):
    return os.path.join(RB, lane, "README.md")


def outtxt(lane, fname):
    return open(os.path.join(RB, lane, fname), encoding="utf-8").read()


f1 = lambda x: f"{x:.1f}"
f2 = lambda x: f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
f4 = lambda x: f"{x:.4f}"
p2 = lambda x: f"{x:+.2f}"

# ---------------------------------------------------------------- B. rules and naming
has("B footings (abstract)", "(9.36x10-11 and 1.13x10-10 m s-2, never pooled)")
has("B footings (exact)", "canonical a0 = 9.3603x10-11, alternative 1.1312x10-10 m s-2, never pooled")
has("B kappa fitted, not closed", "is fitted; the theory is not closed")
has("B naming defined once", "Cold dark energy is the cold, clumping (w ≈ 0) component that the data require beyond the law")
has("B naming: not matter, not a particle", "It is not matter and not a particle")
has("B LambdaCDM is the rival", "ΛCDM is the name of the external rival model")
check("B 'CDM' only as LambdaCDM in TeX", re.findall(r"CDM", tex) and all(tex[m.start() - 9:m.start()] == "$\\Lambda$" for m in re.finditer(r"CDM", tex)),
      f"{len(re.findall('CDM', tex))} occurrences")
check("B 'CDM' only as LambdaCDM in PDF", all(flat[m.start() - 1] == "Λ" for m in re.finditer(r"CDM", flat)))
for bad in ("cold dark matter", "cdm-like"):
    check(f"B forbidden '{bad}' absent", bad not in low and bad not in tex.lower())
rd("B naming matches the owner's (spec)", SPEC, "the cold component is called _cold dark energy_", "Cold dark energy is the cold, clumping")

# ---------------------------------------------------------------- C. the galaxy law (P4, U1, C6, C8, verdict)
p4 = JS("P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")["tiles"]
fp = p4["T1"]["footings"]
num("C P4 RAR rms (JSON)", f"{fp['canonical']['L24']['rms']:.3f} / {fp['alt']['L24']['rms']:.3f}", "rms {} dex, one Υ per galaxy")
num("C P4 RAR rms abstract (JSON)", f"{fp['canonical']['L24']['rms']:.3f}", "relation (rms {} dex)")
num("C P4 median Upsilon (JSON)", f"{fp['canonical']['L24']['U_median']:.2f} / {fp['alt']['L24']['U_median']:.2f}", "(median {}); the")
mk = p4["T2"]["rows"]["REST|nu1"]
num("C P4 MeerKAT (JSON)", f"{mk['dlog_M_minus_S']:+.3f}", "{} dex from SPARC's, same recipe")
g3 = p4["T3"]["footings"]
num("C P4 groups (JSON)", f"{g3['canonical']['v3_isolated']['mean']:+.3f} / {g3['alt']['v3_isolated']['mean']:+.3f}", "{} dex from the law on baryons")
u1 = JS("U1_v3_dust_content", "u1_v3_dust_content_results.json")["numbers"]
tdg = u1["N5"]["tdg"]["canonical"]
num("C U1 TDGs (JSON)", f"{tdg['TDG_B0']['rbar']:+.3f} ± {tdg['TDG_B0']['se']:.3f}", "{} dex: Newtonian")
c6 = JS("C6_literal_cassini", "c6_literal_cassini_results.json", CV)
R1 = c6["R1_physical"]
check("C C6 all 24 cells pass (JSON)", len(R1) == 24 and all(v["hees"] and v["park"] for v in R1.values()) and "all 24 Cassini cells pass" in flat)
mg = c6["R1_margin"]
num("C C6 margin (JSON)", f"{sci(mg['Hees_min'], 1)} to {sci(mg['Hees_max'], 1)}", "pass, by {}")
c8 = JS("C8_instantaneous", "c8_instantaneous_results.json", CV)
num("C C8 pulsars (JSON)", sci(c8["K7"]["worst_ratio"], 1), "at most {} of the double pulsar")
rd("C v3s constraint algebra 3 DOF (verdict)", VERD, "closes with 3 DOF; switched stiffness well-posed and statics unchanged", "closes with 3 degrees of freedom")
rd("C v3s fails as gravity+cosmology (verdict)", VERD, "As a theory of gravity and cosmology, v3s fails", "As a theory of gravity and cosmology, v3s fails")
rd("C the one mechanism (verdict)", VERD, "v3s has one cold field, and kinematics fix it to be the field that carries the law")

# ---------------------------------------------------------------- D. beyond galaxies
x11 = JS("X11_cross_shear_diagnosis", "x11_analysis_results.json")["Z_MID"]
x13 = JS("X13_source_size_test", "x13_analysis_results.json")["Z_MID_corr"]
num("D X11 Z_MID all-source range (JSON)", f"{min(x11.values()):.1f}-{max(x11.values()):.1f}", "significance is Z {} (X11)")
num("D X13 Z_MID corrected range (JSON)", f"{min(v['Z'] for v in x13.values()):.1f}-{max(v['Z'] for v in x13.values()):.1f}", "selection it is Z {},")
num("D abstract cluster Z range (JSON)", f"{min(v['Z'] for v in x13.values()):.1f}-{max(x11.values()):.1f}", "Cluster cores sit above it at Z {}")
check("D X11/X13 class REAL (JSON)", JS("X11_cross_shear_diagnosis", "x11_analysis_results.json")["Z_MID_class"] == "REAL"
      and JS("X13_source_size_test", "x13_analysis_results.json")["Z_MID_corr_class"] == "REAL" and "still real by X7's rule" in flat)
rd("D cores 1.5-1.7x (verdict)", VERD, "1.5–1.7 × the law in 0.3–1 Mpc", "the cores sit 1.5-1.7 times above the law")
rd("D X21 baryons short x4-7 (verdict)", VERD, "generous omitted baryons fall short ×4–7", "Known baryons fall short by a factor 4-7")
x20 = JS("X20_hosted_dwarf_disequilibrium", "x20_hosted_dwarf_disequilibrium_results.json")["footings"]
num("D X20 tau<=0.1 extra (JSON)", f"{x20['canonical']['T2']['0.1']['median']:+.2f} / {x20['alt']['T2']['0.1']['median']:+.2f}", "still sits {} dex high")
num("D X20 tau<=0.1 Z (JSON)", f"{x20['canonical']['T2']['0.1']['Z']:.1f} / {x20['alt']['T2']['0.1']['Z']:.1f}", "dex high, Z = {} (X20")
check("D X20 label EXTRA both (JSON)", x20["canonical"]["T2"]["0.1"]["label"] == "EXTRA" and x20["alt"]["T2"]["0.1"]["label"] == "EXTRA")
x24 = JS("X24_dwarf_velocity_floor", "x24_dwarf_velocity_floor_results.json")["footings"]
num("D X24 c0 (JSON)", f"{x24['canonical']['B']['c0']:.1f} / {x24['alt']['B']['c0']:.1f}", "c0 = {} km s-1 calibrated")
num("D X24 chi2 canonical (JSON)", f"{x24['canonical']['B']['chi2_H_law']:.0f} to {x24['canonical']['B']['chi2_H_floor']:.0f}", "χ2 from {} (canonical)")
num("D X24 chi2 alt (JSON)", f"{x24['alt']['B']['chi2_H_law']:.0f} to {x24['alt']['B']['chi2_H_floor']:.0f}", "and {} (alternative)")
rd("D X24 being hosted adds nothing (README)", readme("X24_dwarf_velocity_floor"), "Being hosted adds nothing.", "Being hosted adds nothing")
x25 = JS("X25_dwarf_pericentre_tides", "x25_dwarf_pericentre_tides_results.json")["footings"]
num("D X25 weak-stress extra (JSON)", f"{x25['canonical']['W']['0.1']['median']:+.2f} / {x25['alt']['W']['0.1']['median']:+.2f}", "still sit {} dex high")
num("D X25 Z (JSON)", f"{x25['canonical']['W']['0.1']['Z']:.1f} / {x25['alt']['W']['0.1']['Z']:.1f}", "Z = {} (X25)")
rd("D X25 floor not in action (README)", readme("X25_floor_from_action"), "WRONG SIGN", "The floor is not in the action")
x22 = JS("X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")
num("D X22 lambda_hm (JSON)", f"{x22['step1']['alpha_NF']['lambda_hm_Mpc_h']:.2f}", "λhm ≈ {} Mpc/h")
num("D X22 M_hm (JSON)", sci(x22["step1"]["alpha_NF"]["M_hm_Msun"], 1), "(Mhm ≈ {} M⊙)")
num("D X22 capture (JSON)", f"{x22['step3A']['canonical']['alpha_NF']['captured_T2_min_p16_p50_p84_max'][2]:.2f}", "median capture {} of the fair share")
x34 = JS("X34_recombination_release", "x34_recombination_release_results.json")
s8l = x34["S0"]["sigma8_LCDM"]
num("D X34 sigma8 at z_on 1100/1500 (JSON)", f"{x34['Q1']['R1']['1100']['sigma8'] / s8l:.3f} / {x34['Q1']['R1']['1500']['sigma8'] / s8l:.3f}", "(σ8 at {} of")
rd("D X34 dust by 5e4 (README)", readme("X34_recombination_release"), "It must already exist and cluster by z ≈ 5e4", "It must already be dust-like by z ≈ 5x104 (X34)")
rd("D X30 OUTER predicted (verdict)", VERD, "predicted 1.42–2.26 against measured", "OUTER band is 1.42-2.26 against measured")
rd("D X30 OUTER measured (verdict)", VERD, "measured 0.66–0.72", "0.72 ± 0.14 / 0.66 ± 0.13 (X30)")
rd("D X30 measured band (spec)", SPEC, "measured 1.42–2.26 vs measured 0.72 ± 0.14 / 0.66 ± 0.13".replace("measured 1.42", "predicted 1.42"), "0.72 ± 0.14 / 0.66 ± 0.13")
rd("D X32 tracer (verdict)", VERD, "survives (f_ret 0.80–1.02) and lands on the galaxies", "(fret 0.80-1.02) and lands on the galaxies")
rd("D behaves like the cold component (verdict)", VERD, "behaves like the cold component of ΛCDM", "behaves like the cold component of ΛCDM")

# ---------------------------------------------------------------- E. doors (Table 2)
rd("E X19 (README)", readme("X19_selector_rank_test"), "NO LOW-DIMENSIONAL SELECTOR", "no single catalogue variable or axis-aligned pair")
rd("E X31 Spearman (verdict)", VERD, "F does not order them (Spearman +0.10)", "does not order the classes (Spearman +0.10)")
rd("E X31 verdict (README)", readme("X31_feedback_energy_selector"), "FEEDBACK FAILS", "the heavy clusters that need extra have the lowest F")
rd("E X23 A_MID (verdict)", VERD, "A_MID 7.5–10.7 against the measured 1.0–2.2", "AMID 7.5-10.7 against 1.0-2.2")
rd("E X23 graded dwarfs (README)", readme("X23_late_heating_graded"), "E_pred ≤ 8e-4 dex", "hosted dwarfs get ≤ 8x10-4 dex against +0.21 to +0.64")
rd("E X23 graded observed (README)", readme("X23_late_heating_graded"), "+0.21 to +0.64", "+0.21 to +0.64")
rd("E X24b epsilon (verdict)", VERD, "The forest gives ε ≤ 2.41e-6. SPARC needs ε ≥ 7.65e-6 / 8.59e-6", "ε ≤ 2.41x10-6, SPARC needs ≥ 7.65x10-6 / 8.59x10-6")
rd("E X26 sheet points (verdict)", VERD, "a thin sheet survives (45 / 37 grid points", "at 45 / 37 grid points")
rd("E X35 UNDECIDED, rho_tau = 0 (verdict)", VERD, "gives ρ_τ ≡ 0", "(ρτ ≡ 0)")
rd("E X35 README verdict", readme("X35_a0_tracks_ede"), "UNDECIDED", "UNDECIDED; v3s has nothing")
rd("E X34 reduces (spec)", SPEC, "either reduce to ordinary dust-like clumping", "reduces to ordinary dust-like clumping")
x37 = TX(readme("X37_orbit_conversion"))
check("E X37 OUTER 1.67 vs 0.72, Z -6.7, slope -0.29 (README)", "| OUTER all-KT | 0.72 ± 0.14 | 1.67 | -6.7 | OVER |" in x37 and "WRONG SIGN" in x37
      and "OUTER 1.67 against 0.72 ± 0.14 (Z = -6.7)" in flat and "of the wrong sign" in flat)
rd("E X37 general statement (verdict)", VERD, "any depletion rule keyed to orbits, density, temperature or time removes cold dark energy from cluster centres first",
   "any depletion rule keyed to orbits, density, temperature or time removes cold dark energy from cluster centres first")

# ---------------------------------------------------------------- F. route E (EM1, X36)
em = JS("EM1_emergent_dust_law", "em1_emergent_results.json")["rows"]["A_c2b_refit"]["R1"]
num("F EM1 rms (JSON)", f"{em['rms']:.4f}", "give rms {} but")
num("F EM1 Upsilon (JSON)", f"{em['U_median']:.2f}", "median Υ {}, below")
check("F EM1 R1 class FAIL (JSON)", em["class"] == "FAIL")
up = JS("EM1_emergent_dust_law", "em1_emergent_results_UPS05.json")
num("F EM1 UPS05 (JSON)", f"{up['rows']['A_c2b_refit']['R1']['rms']:.4f} against the law's {up['law']['canonical']['rms']:.4f} / {up['law']['alt']['rms']:.4f}", "model gives {}")
x36 = JS("X36_efe_discriminator", "x36_efe_results.json")
sc, sa = x36["slopes"]["canonical|C_U0|S_L"], x36["slopes"]["alt|C_U0|S_L"]
num("F X36 measured slope (JSON)", f"{sc['s_obs']:.3f} ± {sc['sd_obs']:.3f} / {sa['s_obs']:.3f} ± {sa['sd_obs']:.3f}", "slope {}")
num("F X36 law z (JSON)", f"{sc['models']['a']['z']:.2f} / {sa['models']['a']['z']:.2f}", "almost none of it (Z = {})")
num("F X36 route E z (JSON)", f"{sc['models']['b']['z']:.2f} / {sa['models']['b']['z']:.2f}", "reaches part of it (Z = {})")
num("F X36 power (JSON)", f"{sc['P']:.2f} / {sa['P']:.2f}", "differ by only {} of the")
check("F X36 verdict NOT DIAGNOSTIC (JSON)", "NOT DIAGNOSTIC" in str(x36["verdict"]) and "NOT DIAGNOSTIC" in flat)
rd("F X36 DR4 both Newton (README)", readme("X36_efe_discriminator"), "Both readings predict Newton", "both readings predict Newtonian binaries")
has("F stated plainly", "no test in the record yet distinguishes a fundamental law from a law that emerges from cold dark energy around baryons")

# ---------------------------------------------------------------- G. core surface density (X38-X44)
x38 = JS("X38_a0_surface_density_halos", "x38_sd_halos_results.json")
S = x38["Sigma_Msun_pc2"]
num("G Sigma_a0 (JSON)", f"{S['canonical']:.1f} / {S['alt']:.1f}", "a0/(2πG), i.e. {}")
num("G Sigma_a0 abstract (JSON)", f"{S['canonical']:.1f} / {S['alt']:.1f}", "a0/(2πG) ({}")
rd("G verdict rounds to 107 / 129 (disclosed)", VERD, "107 / 129 M☉/pc²", "the JSON gives 106.9 / 129.2")
o38 = outtxt("X38_a0_surface_density_halos", "x38_sd_halos.out")
r38 = [float(x) for x in re.findall(r"SPARC \[A_c2b_refit\] EM1 relation \(a 11.18, b 0.9\): rms ([0-9.]+)", o38)]
u38 = [float(x) for x in re.findall(r"SPARC \[A_c2b_refit\] EM1 relation \(a 11.18, b 0.9\): rms [0-9.]+, median U ([0-9.]+)", o38)]
num("G X38 SPARC rms (.out)", f"{r38[0]:.4f} / {r38[1]:.4f}", "sensible Υ: rms {}")
num("G X38 SPARC Upsilon (.out)", f"{u38[0]:.2f} / {u38[1]:.2f}", "rms 0.0795 / 0.0729, median Υ {}. The")
cc = {f: x38["footings"][f]["clusters"]["cells"]["h0672"] for f in ("canonical", "alt")}
num("G X38 OUTER all-KT Z (JSON)", f"{cc['canonical']['G-OUT-all']['Z']:+.2f} / {cc['alt']['G-OUT-all']['Z']:+.2f}", "(all-KT Z = {})")
num("G X38 MID T3 Z (JSON)", f"{cc['canonical']['G-MID-T3']['Z']:+.2f} / {cc['alt']['G-MID-T3']['Z']:+.2f}", "MID T3 Z = {}, MID")
num("G X38 MID slope Z (JSON)", f"{cc['canonical']['G-MID-b']['Z']:+.2f} / {cc['alt']['G-MID-b']['Z']:+.2f}", "with KT {}, and")
num("G X38 MGAS T3 OUTER Z (JSON)", f"{cc['canonical']['G-OUT-M3']['Z']:+.2f} / {cc['alt']['G-OUT-M3']['Z']:+.2f}", "(MGAS T3) {}. Its")
num("G X38 T3 core radius (.out)", f"{float(re.search(r'T3.: ([0-9.]+)', o38).group(1)):.2f}", "too wide ({} Mpc in the hottest")
nk = {f: 15 - len(x38["footings"][f]["clusters"]["fails"]) for f in ("canonical", "alt")}
num("G X38 keys passing (JSON)", f"{nk['canonical']} / 15 ({nk['alt']})", "{} 14 / 15")
x40b = JS("X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")
gz = (x40b["footings"]["canonical"]["X38_groups"]["Z"], x40b["footings"]["alt"]["X38_groups"]["Z"])
num("G X38 groups Z (X40b JSON)", f"{gz[0]:+.2f} / {gz[1]:+.2f}", "groups line (Z = {}, X40b)")
num("G X38 groups Z, table (X40b JSON)", f"{gz[0]:+.2f}", "groups Z {} +2.05")
# X39
o39 = outtxt("X39_baryonic_contraction", "x39_contraction.out")
m3 = re.search(r"G-MID-T3\s+meas \+([0-9.]+)\+-[0-9.]+ pred \+([0-9.]+) Z \+[0-9.]+ \(X38 \+([0-9.]+)", o39)
num("G X39 MID T3 1.05 -> 1.13 vs 2.13 (.out)", f"{float(m3.group(3)):.2f} to {float(m3.group(2)):.2f} against {float(m3.group(1)):.2f}", "MID T3 only from {}, and")
u39 = re.findall(r"SD \+ AC: rms [0-9.]+, median U ([0-9.]+) -> line FAIL", o39)
num("G X39 Upsilon (.out)", f"{float(u39[0]):.2f} / {float(u39[2]):.2f}", "median Υ falls to {} and fails")
check("G X39 verdict (JSON)", JS("X39_baryonic_contraction", "x39_contraction_results.json")["verdict"] == "SD + AC FAILS")
x40 = JS("X40_fixed_core_radius", "x40_fixed_core_results.json")
num("G X40 r_c (JSON)", f"{x40['r_c_kpc']:.2f}", "rc = {} kpc")
num("G X40 SPARC (JSON)", f"{x40['sparc']['A_c2b_refit']['rms']:.3f} at Υ {x40['sparc']['A_c2b_refit']['U_median']:.2f}", "gives rms {} (fails)")
check("G X40 verdict FC FAILS, clusters OVER (JSON)", x40["verdict"] == "FC FAILS" and all("OVER" in k for k in x40["footings"]["canonical"]["clusters"]["fails"]))
rd("G X40b rule A g_b (README)", readme("X40b_core_surface_density_scaling"), "They have 0.04–0.07 a₀", "cluster cores gb is only 0.04-0.07 a0")
num("G X40b rule B bound (JSON)", f"{x40b['ruleB_inputs']['bound_0_3']:.2f}", "at most a factor {}. With")
num("G X40b alpha best (JSON)", f"{x40b['footings']['canonical']['C']['alpha_best']:.2f} / {x40b['footings']['alt']['C']['alpha_best']:.2f}", "αbest = {}, i.e.")
rd("G X40b 3-5x (README)", readme("X40b_core_surface_density_scaling"), "cluster cores need roughly 3–5 × a₀/(2πG)", "cores at 3-5 times a0/(2πG)")
check("G X40b verdict (JSON)", x40b["verdict"] == "NO FRAMEWORK-NATIVE RULE CLOSES IT")
# X41
x41 = JS("X41_collapse_floor_sigma", "x41_collapse_floor_results.json")
tb = x41["sigma_coll_table"]
slope = math.log(tb["1e15"][0] / tb["1e13"][0]) / math.log(100)
num("G X41 slope (JSON table)", f"{slope:.2f}", "a slope of {} in mass")
num("G X41 amplitude (JSON)", f"{x41['footings']['canonical']['clusters']['ratio_median']:.2f} / {x41['footings']['alt']['clusters']['ratio_median']:.2f}", "only {} of a0/(2πG)")
en = (x41["footings"]["canonical"]["eta_needed"], x41["footings"]["alt"]["eta_needed"])
num("G X41 eta needed (JSON)", f"{en[0][0]:.1f}-{en[0][1]:.1f} / {en[1][0]:.1f}-{en[1][1]:.1f}", "factor η of {} is needed")
check("G X41 verdict CF INACTIVE (JSON)", x41["verdict"] == "CF INACTIVE")
x42 = JS("X42_core_rise_above_galaxies", "x42_core_rise_results.json")
cf42 = x42["footings"]["canonical"]["H1"]["conc_factor"]
num("G X42 conc factor (JSON)", f"{cf42['10000000000000.0']:.1f}-{cf42['1000000000000000.0']:.1f}", "factor of {} over the same")
num("G X42 groups out of sample (JSON)", f"{x42['footings']['canonical']['H1']['grades']['groups']['Z']:+.2f} / {x42['footings']['alt']['H1']['grades']['groups']['Z']:+.2f}",
    "out of sample (Z = {})")
check("G X42 verdict BOTH FAIL (JSON)", x42["verdict"] == "BOTH FAIL")
# X43
x43 = JS("X43_collapse_core_floor", "x43_collapse_core_results.json")
rd("G X43 eta 14.83, c_f external (README)", readme("X43_collapse_core_floor"), "η = (4/(3B(1))) c_f^{5/4} = 14.83   [c_f = 4 EXTERNAL]", "f = 14.83 [cf = 4 EXTERNAL]")
has("G X43 eta abstract", "η = 14.83 from self-similar infall")
rd("G X43 crossover (README)", readme("X43_collapse_core_floor"), "M ≈ 10^12.1 (canonical) / 10^12.4 (alt)", "M ≈ 1012.1 / 1012.4 M⊙")
s43 = {f: x43["footings"][f]["sparc"]["A_c2b_refit"] for f in ("canonical", "alt")}
num("G X43 SPARC (JSON)", f"{s43['canonical']['rms']:.4f} / {s43['alt']['rms']:.4f}, median Υ {s43['canonical']['U_median']:.2f} / {s43['alt']['U_median']:.2f}", "SPARC passes (rms {})")
num("G X43 SPARC table (JSON)", f"{s43['canonical']['rms']:.4f} / {s43['canonical']['U_median']:.2f}", "0.0795 / 0.77 {}")
gq = (x43["footings"]["canonical"]["groups"]["Z"], x43["footings"]["alt"]["groups"]["Z"])
check("G X43 groups Z +2.05 on both footings (JSON)", f"{gq[0]:+.2f}" == f"{gq[1]:+.2f}" and "groups at Z = +2.05 on both footings" in flat)
num("G X43 groups Z (JSON)", f"{gq[0]:+.2f}", "groups at Z = {} on both")
num("G X43 groups Z abstract (JSON)", f"{gq[0]:+.2f}", "groups (Z = {}) and")
c43 = x43["footings"]["canonical"]["clusters"]["cells"]["h0672"]
num("G X43 MID T3 (JSON)", f"{c43['G-MID-T3']['pred']:.2f}, Z = {c43['G-MID-T3']['Z']:+.2f}", "Z = +4.26 {}-")
num("G X43 MID T3 move (JSON)", f"{cc['canonical']['G-MID-T3']['Z']:+.2f} to {c43['G-MID-T3']['Z']:+.2f}", "MID T3 moves from Z = {}")
num("G X43 MID slope (JSON)", f"{c43['G-MID-b']['Z']:+.2f}", "+3.07 {} -")
num("G X43 MGAS all OUTER move (JSON)", f"{cc['canonical']['G-OUT-Mall']['Z']:+.2f} to {c43['G-OUT-Mall']['Z']:+.2f}", "OUTER band from {}. Two")
num("G X43 MGAS T3 OUTER (JSON)", f"{c43['G-OUT-M3']['pred']:.2f} against {c43['G-OUT-M3']['meas']:.2f} (Z = {c43['G-OUT-M3']['Z']:+.2f})", "OUTER band, {}.")
num("G X43 MGAS T3 OUTER abstract (JSON)", f"{c43['G-OUT-M3']['Z']:+.2f}", "outskirts (Z = {}).")
check("G X43 MGAS T3 OUTER Z equal on both footings (JSON)", f"{c43['G-OUT-M3']['Z']:.2f}" == f"{x43['footings']['alt']['clusters']['cells']['h0672']['G-OUT-M3']['Z']:.2f}")
num("G X43 table MGAS T3 (JSON)", f"{cc['canonical']['G-OUT-M3']['pred']:.2f}, Z = {cc['canonical']['G-OUT-M3']['Z']:+.2f} {c43['G-OUT-M3']['pred']:.2f}, Z = {c43['G-OUT-M3']['Z']:+.2f}", "OUTER {} fails")
num("G X38 table MID T3 (JSON)", f"{cc['canonical']['G-MID-T3']['pred']:.2f}, Z = {cc['canonical']['G-MID-T3']['Z']:+.2f}", "MID T3 {} 2.06")
ok43 = {f: sum(x43["footings"][f]["clusters"]["ok"].values()) for f in ("canonical", "alt")}
num("G X43 keys passing (JSON)", f"{ok43['canonical']} of 15", "passes SPARC and {} cluster keys")
check("G X43 14/15 on both footings (JSON)", ok43["canonical"] == ok43["alt"] == 14 and x43["footings"]["canonical"]["clusters"]["fails"] == ["G-OUT-M3 (UNDER)"])
check("G X43 verdict CC FAILS [c_f EXTERNAL] (JSON)", x43["verdict"] == "CC FAILS [c_f EXTERNAL]")
cf5 = x43["footings"]["canonical"]["reported"]["c_f 5"]
num("G X43 c_f=5 eta (JSON)", f"{cf5['eta']:.1f}", "cf = 5 (η = {}) passes")
num("G X43 c_f=5 groups (JSON)", f"{cf5['groups']['Z']:+.2f}", "passes the groups (Z = {})")
num("G X43 c_f=5 SPARC table (JSON)", f"{cf5['sparc']['rms']:.4f} / {cf5['sparc']['U']:.2f}", "0.0782 / 0.77 {}")
check("G X43 c_f=5 only MGAS T3 fails (JSON)", cf5["cluster_fails"] == ["G-OUT-M3 (UNDER)"] and cf5["groups"]["verdict"] == "CONSISTENT")
# X44
x44 = JS("X44_self_similar_cf", "x44_self_similar_cf_results.json")
check("G X44 c_f = 2^(8/9) (JSON)", abs(x44["c_f_SS"] - 2 ** (8 / 9)) < 1e-9 and "cf = 28/9 = 1.85" in flat)
num("G X44 c_f (JSON)", f"{x44['c_f_SS']:.2f}", "= 28/9 = {} (η")
num("G X44 eta (JSON)", f"{x44['eta']:.2f}", "(η = {}), which fails four keys")
x4c, x4a = x44["footings"]["canonical"], x44["footings"]["alt"]
check("G X44 four failing keys on both footings (JSON)", x4c["n_fail"] == 4 and x4a["n_fail"] == 4 and "which fails four keys: groups, MID T3, the MID slope and MGAS T3 OUTER" in flat)
num("G X44 groups (JSON)", f"{x4c['groups']['Z']:+.2f} ({x4a['groups']['Z']:+.2f})", "+1.82 {}")
num("G X44 MID T3 (JSON)", f"{x4c['MID_T3']['pred']:.2f}, Z = {x4c['MID_T3']['Z']:+.2f}", "+0.30-{}")
num("G X44 MID slope (JSON)", f"{x4c['MID_b']['Z']:+.2f}", "+1.70 - {}")
num("G X44 MGAS T3 OUTER (JSON)", f"{x4c['OUT_M3']['pred']:.2f}, Z = {x4c['OUT_M3']['Z']:+.2f}", "fails {}")
o44 = outtxt("X44_self_similar_cf", "x44_self_similar_cf.out")
cr = re.findall(r"groups reach Z = 2.0 at c_f ~ ([0-9.]+)", o44)
num("G X44 groups crossing (.out)", f"{float(cr[0]):.2f} / {float(cr[1]):.2f}", "at cf ≈ {}, and")
rd("G X44 3.3-4.6 (README)", readme("X44_self_similar_cf"), "c_f ≈ 3.3–4.6", "calibration gives 3.3-4.6")
rd("G X44 in the verdict (verdict)", VERD, "The data pin c_f ≈ 4–4.2", "The data pin cf ≈ 4-4.2")
rd("G X44 peak structure (verdict)", VERD, "it needs the structure of the initial peaks", "It needs the structure of the initial density peaks")
rd("G X44 in the spec (spec)", SPEC, "c_f is not derivable from self-similar infall alone", "cannot come from scale-free infall")
rd("G MGAS T3 data-side check (verdict)", VERD, "MGAS T3 OUTER should get a data-side check", "data-side check of that band")

# ---------------------------------------------------------------- H. the map (MAP1) and the figure
mp = json.load(open(os.path.join(RB, "MAP1_cosmic_river", "map1_cosmic_river.json")))
mo = outtxt("MAP1_cosmic_river", "map1_cosmic_river.out")
num("H MAP1 H (JSON)", f"{mp['H']:.2f}", "self-calibrates H = {} km")
num("H MAP1 groups (.out)", f"{int(re.search(r'^groups (\d+)', mo, re.M).group(1)):,}", "groups the {} Cosmicflows")
sl = [g for g in mp["groups"]]
num("H MAP1 slice groups (JSON)", f"{len(sl):,}", "The slice holds {} groups")
num("H MAP1 median v_pec error (JSON)", f"{float(sorted(g[3] for g in sl)[len(sl) // 2]) if len(sl) % 2 else 0.5 * (sorted(g[3] for g in sl)[len(sl) // 2 - 1] + sorted(g[3] for g in sl)[len(sl) // 2]):.0f}",
    "(median error {} km s-1)")
num("H MAP1 SPARC in slice (JSON)", f"{sum(abs(s[3]) < mp['slice']['sgz'] for s in mp['sparc'])}", "{} SPARC galaxies (at X33's")
num("H MAP1 clusters in slice (JSON)", f"{sum(abs(c[3]) < mp['slice']['sgz'] for c in mp['clusters'])} of the {len(mp['clusters'])}", "and {} eRASS1 clusters")
check("H MAP1 slice and kernel (JSON)", mp["slice"] == {"sgz": 25, "R": 160} and mp["grid"]["sigma"] == 10.0 and "|SGZ| < 25 Mpc, R < 160 Mpc" in flat and "(σ = 10 Mpc kernel" in flat)
check("H MAP1 Malmquist not corrected (commit 3f9b3ae361)", "inhomogeneous-Malmquist bias (not corrected)" in git("show", "-s", "--format=%B", "3f9b3ae361").stdout
      and "No inhomogeneous-Malmquist correction is applied" in flat)
check("H MAP1 eRASS1 western hemisphere (.out)", "western Galactic hemisphere only" in mo and "eRASS1 covers only the western Galactic hemisphere" in flat)
check("H MAP1 commit adds the lane", "rebuild_2026_10_22/MAP1_cosmic_river/map1_cosmic_river.json" in git("show", "--name-only", "--format=", "3f9b3ae361").stdout and "MAP1 (3f9b3ae361)" in flat)
check("H figure: illustrative, not evidence (caption)", "Illustrative only: the map is not evidence for the theory." in flat and "it tests nothing" in flat)
check("H figure: clip at 1000 in script and caption", "CLIP = 1000.0" in open(FIGPY).read() and "clipped at ± 1000" in flat)
check("H figure: script reads MAP1 JSON only", "map1_cosmic_river.json" in open(FIGPY).read() and "includegraphics[width=0.72\\textwidth]{PAPER62_fig_river.pdf}" in tex)
fld = [[None if v is None else v for v in row] for row in mp["grid"]["field"]]
check("H figure: field cells 4489 (JSON = .out)", sum(v is not None for row in fld for v in row) == int(re.search(r"cells with data (\d+)", mo).group(1)) == 4489)

# ---------------------------------------------------------------- I. pending and dated data
rd("I ALMA dates (verdict)", VERD, "| ALMA U4 / GS4 | 2026-11-06 / 11-28 |", "ALMA U4 (2026-11-06) and GS4 (2026-11-28)")
rd("I Gaia DR4 date (verdict)", VERD, "| Gaia DR4: wide binaries, MW | 2026-12-02 |", "Gaia DR4 wide binaries and the Milky Way (2026-12-02)")
rd("I L1 converged ladder (verdict)", VERD, "the converged ladder says ρ_NL ≈ −0.05: it does not restore growth", "the converged ladder says the nonlinear hold term does not restore growth")
L1D = "rebuild_2026_10_22/L1_khronon_pm"
tracked = git("ls-files", L1D).stdout.split()
prod = [f for f in tracked if re.search(r"(512|production|_verdict)", f, re.I)]
check("I L1 512^3 pending: no production result file tracked", prod == [], str(prod))

# ---------------------------------------------------------------- J. commits cited
COMMITS = {"P4_v3_galaxy_tiles": ["6c5e6161b9", "6c0249a8bc"], "X11_cross_shear_diagnosis": ["9a105431c9", "c1cd5455a5"], "X13_source_size_test": ["c4e5a5a064", "4eeeceba07"],
           "X21_cluster_switch_anatomy": ["a48f6d5e08", "3aa4f07b58"], "X20_hosted_dwarf_disequilibrium": ["87b6832e84", "bd736c128e"],
           "X24_dwarf_velocity_floor": ["7a79903c3f", "19d31a99d9"], "X25_dwarf_pericentre_tides": ["d4827bece5", "5a754eb2e2"], "X22_cosmic_dust_window": ["a2b532e3c6", "5c7114f508"],
           "X34_recombination_release": ["6c5d581400", "ab4a3a8e1a"], "X30_sheet_cluster_profile": ["c6be83f91c", "0f19b6759b"], "X32_bullet_cold_sector": ["57ff3e7df4", "975ccfbf49"],
           "X19_selector_rank_test": ["8960ea2285", "a9ec701f5b"], "X31_feedback_energy_selector": ["1aa11f9bcb", "358e3859ed"], "X23_late_heated_cold": ["b8d81770bb", "df896db507"],
           "X23_late_heating_graded": ["6ec6b89807", "9c54fae62e"], "X24b_vacuum_heated_cold": ["1d0f8c6967", "3492bcbeb4"], "X26_cold_sector_map": ["b10263968f", "c9112e3126"],
           "X35_a0_tracks_ede": ["02848d0330", "0eb84a459a"], "X37_orbit_conversion": ["204001f8ad", "538dc083c9"], "EM1_emergent_dust_law": ["1b0dbd6eef", "889d65276e"],
           "X36_efe_discriminator": ["d8651cafc3", "8d7df6a74d"], "X38_a0_surface_density_halos": ["9cc80516df", "3e28ca3027"], "X39_baryonic_contraction": ["b75acfc767", "54684fb62f"],
           "X40_fixed_core_radius": ["b37983a0f7", "5dc30a7c1a"], "X40b_core_surface_density_scaling": ["b09db13390", "ba368d2ba1"], "X41_collapse_floor_sigma": ["0ea05957ee", "e9c1b9abe4"],
           "X42_core_rise_above_galaxies": ["4a13086d02", "0d7d0d5686"], "X43_collapse_core_floor": ["00bc1a7950", "bf8cc9e7cf"], "X44_self_similar_cf": ["c8dd02f5aa", "66273956b2"],
           "MAP1_cosmic_river": ["3f9b3ae361"]}
for lane, hs in COMMITS.items():
    for h in hs:
        files = git("show", "--name-only", "--format=", h).stdout
        check(f"J {lane} commit {h} touches lane, cited", f"rebuild_2026_10_22/{lane}/" in files and h in flat)
check("J verdict commit 58a2d738f8 folds X44, cited", "covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md" in git("show", "--name-only", "--format=", "58a2d738f8").stdout
      and "X44" in git("show", "-s", "--format=%s", "58a2d738f8").stdout and "58a2d738f8" in flat)
check("J frozen hashes in JSON match cited criteria", x38["frozen"] == "9cc80516df" and x41["frozen"] == "0ea05957ee" and x42["frozen"] == "4a13086d02"
      and x43["frozen"] == "00bc1a7950" and x44["frozen"] == "c8dd02f5aa" and x40b["frozen"] == "b09db13390")

# ---------------------------------------------------------------- O. citations and metadata
bib = open(os.path.join(ROOT, "citations", "REFERENCES.bib"), encoding="utf-8").read()


def bibentry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
    return m.group(1) if m else ""


check("O SPARC Lelli 2016 (bib)", "152" in bibentry("Lelli2016a") and "157" in bibentry("Lelli2016a") and "AJ 152, 157 (2016)" in flat)
check("O Cosmicflows-4 Tully 2023 (bib)", "944" in bibentry("Tully2023") and "94" in bibentry("Tully2023") and "ApJ 944, 94 (2023)" in flat)
check("O eRASS1 Bulbul 2024 (bib)", "685" in bibentry("Bulbul2024") and "A106" in bibentry("Bulbul2024") and "A&A 685, A106 (2024)" in flat)
check("O Bertschinger 1985 (bib)", "58" in bibentry("Bertschinger1985") and "39" in bibentry("Bertschinger1985") and "ApJS 58, 39 (1985)" in flat)
check("O Fillmore & Goldreich 1984 (bib)", "281" in bibentry("Fillmore1984") and "ApJ 281, 1 (1984)" in flat)
check("O Burkert 1995 (bib)", "447" in bibentry("Burkert1995") and "ApJ 447, L25 (1995)" in flat)
check("O Watkins-Feldman 2015, Lacey-Cole 1993 not in bib (disclosed)", not bibentry("Watkins2015") and not bibentry("Lacey1993") and "are not in the record's bibliography" in flat)
rme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
check("O PAPER60 DOI (README)", "PAPER60, DOI 10.5281/zenodo.23601528" in rme and "PAPER60 (doi:10.5281/zenodo.23601528)" in flat)
z = json.load(open(ZJ))["metadata"]
ids = {r["identifier"] for r in z["related_identifiers"]}
check("O related identifiers (PAPER60)", "10.5281/zenodo.23601528" in ids)
check("O zenodo: working paper, CC-BY, fitted, not closed, external c_f, illustrative map, draft", z["publication_type"] == "workingpaper" and z["license"] == "cc-by-4.0"
      and "fitted" in z["description"] and "not closed" in z["description"] and "external" in z["description"] and "illustrative" in z["description"].lower()
      and json.load(open(ZJ)).get("draft_not_deposited") is True)
check("O no publish script for PAPER62", not any(f.startswith("PAPER62") and "publish" in f for f in os.listdir(HERE)))

# ---------------------------------------------------------------- Q. honesty, forbidden, names
for s in ("fitted", "the theory is not closed", "not peer reviewed", "never pooled", "AI-assisted", "Anthropic's Claude", "not a particle",
          "Not evidence for the framework", "The owner's programme", "No particle species is added", "It is not evidence for the theory", "EXTERNAL",
          "X43 is not a pass", "the framework does not derive it"):
    has(f"Q honesty '{s}'", s)
zl = z["description"].lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "breakthrough",
            "κ is derived", "kappa is derived", "c_f is derived", "/users/", "gmail", "dark matter particle", "dark-matter particle", "cold dark matter"):
    check(f"Q forbidden '{bad}' absent", bad not in low and bad not in tex.lower() and bad not in zl)
check("Q no 'derived' applied to kappa", not re.search(r"(κ|kappa)[^.]{0,30}\bis derived", low))
check("Q no home path in TeX or figure script", "/Users/" not in tex and "~/" not in tex and "/Users/" not in open(FIGPY).read())
gu = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split()
check("Q no personal name (repo user) in PDF, TeX or zenodo description", all(x.lower() not in low and x.lower() not in tex.lower() and x.lower() not in zl for x in gu if len(x) >= 3), f"{len(gu)} name parts checked")

if MUT:
    missed = [n for n, caught in NUM if not caught]
    for n in missed:
        print(f"  [NOT CAUGHT] {n}")
    print(f"\nPAPER62 core-note audit --mutate: {len(NUM) - len(missed)}/{len(NUM)} perturbed number checks FAIL as required")
    sys.exit(1 if missed else 0)
print(f"\nPAPER62 core-note audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
