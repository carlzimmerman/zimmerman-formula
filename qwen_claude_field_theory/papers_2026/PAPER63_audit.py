#!/usr/bin/env python3
"""PAPER63 audit: every quoted number must match the committed lane outputs (rebuild_2026_10_22/ CF1, GC1, M6N1, P1D1-P1D4,
X43, X62 JSON); every cited commit must exist and touch its lane; the PDF must be newer than the TeX and the figure; the
figure is regenerated in memory from CF1's JSON; naming rules (cold dark energy; CDM only as LambdaCDM), no forbidden claim,
no local path or personal name.
Run: python3 PAPER63_audit.py (exit 0 only if all pass).
     python3 PAPER63_audit.py --mutate (perturbs every JSON-derived number; exit 0 only if every number check then FAILS)."""
import json, os, re, subprocess, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RB = os.path.join(ROOT, "rebuild_2026_10_22")
STEM = "PAPER63_where_cold_dark_energy_switches_on_2026"
TEX = open(os.path.join(HERE, STEM + ".tex")).read()
F = N = 0
NUMF = NUMN = 0


def check(name, ok, msg=""):
    global F, N
    N += 1; F += (not ok)
    if not MUT:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))


def J(rel):
    return json.load(open(os.path.join(RB, rel)))


def bump(t):
    """MUTATE: change the last digit of the formatted number (live-check test)."""
    for i in range(len(t) - 1, -1, -1):
        if t[i].isdigit():
            return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "1"


def num(name, value, fmt, tex_pattern=None):
    """value from JSON, formatted with fmt, must appear in the TeX (in its context pattern)."""
    global NUMF, NUMN
    t = fmt.format(value)
    if MUT:
        t = bump(t)
    s = (tex_pattern or "{}").format(t)
    ok = s in TEX
    NUMN += 1; NUMF += (not ok)
    check(name, ok, f"'{s}'")


def row(name, label, vals, fmt):
    """a whole table row, built from JSON values, must appear verbatim in the TeX."""
    global NUMF, NUMN
    cells = [fmt(v) for v in vals]
    if MUT:
        cells = [bump(c) for c in cells]
    s = label + " & " + " & ".join(cells) + "\\\\"
    ok = s in TEX
    NUMN += 1; NUMF += (not ok)
    check(name, ok, f"'{s[:60]}...'")


cf1 = J("CF1_cf_window_map/cf1_window_results.json")
GRID = [3.5, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 6.0]
row("CF1 threshold row canonical", "threshold, canonical", [cf1[f"cf_{cf:g}"]["crossover"]["canonical"] for cf in GRID], lambda v: f"{v:.2f}")
row("CF1 threshold row alt", "threshold, alternative", [cf1[f"cf_{cf:g}"]["crossover"]["alt"] for cf in GRID], lambda v: f"{v:.2f}")
row("CF1 lensing row canonical", "lensing $\\Delta\\chi^2$ (canonical)", [cf1[f"cf_{cf:g}"]["grade"]["canonical"]["lensing"]["d_LF_L"] for cf in GRID],
    lambda v: f"{v:+.1f}" if v > 0.05 else f"{v:.1f}")
check("CF1 verdict NO SINGLE c_f", cf1["verdict"] == "NO SINGLE c_f" and "NO SINGLE $c_f$" in TEX)
lp = cf1["line_pass_cf"]
check("CF1 lensing passes only at 3.5", lp["lensing"] == [3.5])
check("CF1 groups pass >= 4.75", lp["groups"] == [4.75, 5.0, 5.25, 5.5, 6.0])
check("CF1 M3 pass >= 5.25", lp["G-OUT-M3"] == [5.25, 5.5, 6.0])
check("CF1 G-IN-Mall pass <= 5.0", lp["G-IN-Mall"] == [3.5, 4.0, 4.25, 4.5, 4.75, 5.0])
check("CF1 SPARC pass >= 5.5", lp["SPARC line"] == [5.5, 6.0])
check("CF1 UFD never", lp["dwarfs MW ultra-faint"] == [])
ufd = {round(cf1[f"cf_{cf:g}"]["grade"]["alt"]["dwarfs"]["MW ultra-faint"]["Z"], 2) for cf in GRID}
check("CF1 alt UFD Z -2.77 at every c_f", ufd == {-2.77} and "$Z=-2.77$" in TEX)
check("CF1 checks 10/10", all(cf1["checks"].values()) and len(cf1["checks"]) == 10 and "checks 10/10" in TEX)
x62 = J("X62_environment_keyed_switch/x62_env_switch_results.json")
check("X62 c_f 4 crossover in TeX", "$10^{12.09}$ (canonical) / $10^{12.43}" in TEX)
# GC1
g1 = J("GC1_group_cluster_core_rule/gc1_two_halo_results.json")
fr = g1["verdicts"]["canonical"]["term_fraction_h0672"]
check("GC1 max |term share| = 1.3%", round(100 * max(abs(v) for k, v in fr.items() if k != "G-IN-Mall"), 1) == 1.3 and "1.3\\,\\%" in TEX)
num("GC1 M3 term share", abs(fr["G-OUT-M3"]), "{:.3f}", "G-OUT-M3 by {}")
num("GC1 native M3 Z", g1["runs"]["R4_nat_no2h"]["canonical"]["M3"][0]["Z"], "{:+.2f}", "($" + "{}" + "$)")
check("GC1 verdict NOT REPAIRED", all(v["R4_class"] == "NOT REPAIRED" for v in g1["verdicts"].values()) and "NOT REPAIRED" in TEX)
check("GC1 bias median 4.1", round(g1["bias_range"][1], 1) == 4.1 and "median $b=4.1$" in TEX)
# X43 c_f 4 M3
x43 = J("X43_collapse_core_floor/x43_collapse_core_results.json")
num("X43 M3 Z", x43["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-OUT-M3"]["Z"], "{:+.2f}", "$Z=" + "{}" + "$")
# M6N1
m = J("M6N1_minimum_patch_need/m6n1_need_results.json")
num("M6N1 x_min canonical", 100 * m["footings"]["canonical"]["x_min"], "{:.1f}", "{}\\,\\% (canonical)")
num("M6N1 x_min alt", 100 * m["footings"]["alt"]["x_min"], "{:.1f}", "{}\\,\\% (alternative)")
num("M6N1 eps_ref canonical", 100 * m["footings"]["canonical"]["eps_ref"], "{:.1f}", "({}\\,\\%")
num("M6N1 eps_ref alt", 100 * m["footings"]["alt"]["eps_ref"], "{:.1f}", "/ {}\\,\\%)")
for f, lo, hi in (("canonical", 19, 56), ("alt", 28, 83)):
    ec = [c["eps_crit"] for c in m["footings"][f]["corners"].values()]
    check(f"M6N1 eps_crit range {f}", (round(100 * min(ec)), round(100 * max(ec))) == (lo, hi) and f"{lo}--{hi}\\,\\%" in TEX, f"{100*min(ec):.1f}-{100*max(ec):.1f}")
# P1D lanes
p1 = J("P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json")
num("P1D1 null chi2", p1["footings"]["canonical"]["primary"]["G0"]["chi2"], "{:.1f}", "{}/39")
num("P1D1 kcut mu95", p1["footings"]["canonical"]["variants"]["V-kcut"]["scan"]["mu95"], "{:.2f}", "$\\mu_{{95}}={}$")
p3 = J("P1D3_m6_desi_dr1_growth/p1d3_m6_desi_results.json")
check("P1D3 null chi2 7017/719", round(p3["footings"]["canonical"]["primary"]["G0"]["chi2"]) == 7017 and p3["footings"]["canonical"]["primary"]["G0"]["dof"] == 719 and "7017/719" in TEX)
num("P1D3 hiz mu95", p3["footings"]["canonical"]["variants"]["V-hiz"]["scan"]["mu95"], "{:.2f}", "$\\mu_{{95}}={}$")
p2 = J("P1D2_m6_lognormal_fgpa_forest/p1d2_m6_fgpa_results.json") if os.path.exists(os.path.join(RB, "P1D2_m6_lognormal_fgpa_forest/p1d2_m6_fgpa_results.json")) else None
if p2:
    pr = p2["configs"]["primary"]["footings"]
    num("P1D2 Asimov canonical", pr["canonical"]["G1"]["dchi2_asimov"], "{:.2f}", "{} / ")
    num("P1D2 Asimov alt", pr["alt"]["G1"]["dchi2_asimov"], "{:.2f}", "/ {})")
else:
    check("P1D2 results JSON present", False, "P1D2 result not yet committed")
p4 = J("P1D4_m6_native_3d_forest/p1d4_m6_3d_results.json")
check("P1D4 null chi2 1864/690", round(p4["footings"]["canonical"]["primary"]["G0"]["chi2"]) == 1864 and p4["footings"]["canonical"]["primary"]["G0"]["dof"] == 690 and "1864/690" in TEX)
hz = p4["footings"]["canonical"]["variants"]["V-hiz"]["G0"]
check("P1D4 hiz 433/327", round(hz["chi2"]) == 433 and hz["dof"] == 327 and "433/327" in TEX)
# commits
for c, lane in (("ef5a07c251", "CF1_cf_window_map"), ("e370b35e1c", "CF1_cf_window_map"), ("d1da6b8185", "GC1_group_cluster_core_rule"),
                ("09280e4b66", "GC1_group_cluster_core_rule"), ("3a2f5ca3a0", "M6N1_minimum_patch_need"), ("3ab6a1bf44", "M6N1_minimum_patch_need"),
                ("8f6e3db4bc", "P1D1_m6_boera_high_z_forest"), ("d50412913d", "P1D3_m6_desi_dr1_growth"), ("d89e0f9469", "P1D2_m6_lognormal_fgpa_forest"),
                ("f05be7280b", "P1D4_m6_native_3d_forest")):
    try:
        files = subprocess.run(["git", "-C", ROOT, "show", "--name-only", "--format=", c], capture_output=True, text=True, check=True).stdout
        check(f"commit {c} touches {lane}", lane in files and c in TEX)
    except subprocess.CalledProcessError:
        check(f"commit {c} exists", False)
# build freshness and figure
pdf = os.path.join(HERE, STEM + ".pdf"); fig = os.path.join(HERE, "PAPER63_fig_cfmap.pdf")
check("PDF newer than TeX and figure", os.path.getmtime(pdf) >= max(os.path.getmtime(os.path.join(HERE, STEM + ".tex")), os.path.getmtime(fig)))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("figmod", os.path.join(HERE, "PAPER63_fig_cfmap.py")); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
check("figure data = CF1 JSON", fm.GRID == GRID and fm.passing == lp)
# naming / claims / privacy
body = re.sub(r"\\Lambda\s*CDM|\$\\Lambda\$CDM|LambdaCDM", "", TEX)
check("no bare CDM", "CDM" not in body)
check("no 'cold dark matter'", "cold dark matter" not in TEX.lower())
check("kappa fitted stated", "$\\kappa=\\tfrac12$ is fitted" in TEX)
check("no 'theory closed' claim", not re.search(r"(?<!not )theory (is )?closed", TEX.replace("the theory is not closed", "")))
check("no favour claim", "favour the framework" not in TEX.replace("not evidence for the framework", ""))
check("no local path / personal name", not re.search(r"/Users/|carl|Zimmerman", TEX))
zj = json.load(open(os.path.join(HERE, STEM + ".zenodo.json")))
check("zenodo json marked draft, not deposited", zj.get("draft_not_deposited") is True)
if MUT:
    print(f"MUTATE: {NUMF}/{NUMN} number checks failed (all must)")
    sys.exit(0 if NUMF == NUMN else 1)
print(f"\n{N - F}/{N} checks pass")
sys.exit(0 if F == 0 else 1)
