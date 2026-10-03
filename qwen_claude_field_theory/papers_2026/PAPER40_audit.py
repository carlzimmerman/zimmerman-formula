#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER40 audit: every number the paper quotes in an audited block is re-read from a COMMITTED file (git HEAD) and checked twice.

For each audited value the script checks that
  (1) the value, formatted as the paper prints it, follows from its source: a JSON field (read with `git show HEAD:<path>`, never the
      working tree), a regex capture over a committed text file, or a stated arithmetic on such values (a rounding, a ratio to a footing,
      kappa = a0 / (2 a0_footing)); and
  (2) the value is printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the non-comment lines since the previous tag).
Exit 0 only if every row matches.  Reports "N of N".

Sources
  * committed at HEAD: the CFG301, CFG302 and CFG304 outputs and READMEs, CFG279's and CFG281's files, the catalogue's provenance note and
    file, FP0's constants, the committed MNRAS v3 draft (for Desmond 2023's published a0) and PAPER39 (for Omega_c h^2).
  * the paper's own output PAPER40_figures_numbers.json (written by make_paper40_figures.py, committed WITH this paper; read from the
    working tree, like the .tex) for the rows labelled post hoc in the paper.  The script refuses to run if that file's reproduction gate
    (CFG301's committed values reproduced exactly) did not pass.
  * literature values (LIT rows) that no committed file carries: checked only for being printed in their block, against the values recorded
    here from the arXiv API abstracts read on 2026-10-02 (not re-fetched by this script); reported as a separate tally.
Coverage: only numbers carried by a row below are checked; the tex side is checked anywhere in the tagged block; numbers quoted only in
running text and the references' journal data are not checked.  Where a lane README and its script output differ, the output wins (one case:
CFG302's README prints the observed-frame width ratio as +0.003 dex; its JSON gives +0.00245, printed here as +0.002).

Usage:   python3 PAPER40_audit.py               # main run
         python3 PAPER40_audit.py --mutate      # alters ONE expected value (B01 pooled a0); must exit 1
         python3 PAPER40_audit.py --mutate-tex  # alters ONE tex literal in memory (same row); must exit 1
         python3 PAPER40_audit.py -v            # print every row
Environment: PAPER40_REPO (repo root; default = two levels above this file).
"""
import os, re, sys, json, math, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PAPER40_REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(HERE, "PAPER40_meerkat_a0_2026.tex")
P40 = os.path.join(HERE, "PAPER40_figures_numbers.json")
CFG = "campaign_fresh_gravity/"
L301 = CFG + "CFG301_mightee_hi_catalogue_width_chain/"
L302 = CFG + "CFG302_mightee_cube_raw_widths/"
L304 = CFG + "CFG304_mightee_flux_scale_alfalfa/"
SRC = {
    "A301": L301 + "cfg301_stageA_results.json",
    "B301": L301 + "cfg301_stageB_results.json",
    "OB301": L301 + "cfg301_stageB.out",
    "OA301": L301 + "cfg301_stageA.out",
    "CC2": L301 + "cfg301_CC2_results.json",
    "SELF": L301 + "cfg301_SELFTEST_results.json",
    "M5": L301 + "cfg301_M5_results.json",
    "MU1": L301 + "cfg301_stageB_MUTATE1_results.json",
    "MU2": L301 + "cfg301_stageB_MUTATE2_results.json",
    "R301": L301 + "README.md",
    "FC301": L301 + "FROZEN_CRITERIA.md",
    "S301": L301 + "cfg301_width_chain.py",
    "J302": L302 + "cfg302_raw_widths_results.json",
    "PH302": L302 + "cfg302_posthoc_diagnostics_results.json",
    "R302": L302 + "README.md",
    "J304": L304 + "cfg304_flux_scale_alfalfa_results.json",
    "PH304": L304 + "cfg304_posthoc_results.json",
    "R304": L304 + "README.md",
    "R279": CFG + "CFG279_mightee_published_values/README.md",
    "J281": CFG + "CFG281_budhies_local_control/cfg281_stageB_results.json",
    "DATA": "data_assembly/mightee_hi_catalogue_2026-10-02/README.md",
    "CSV": "data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv",
    "FP0": "real_research/derivation_chain_2026/FP0_core_postulates_results.json",
    "FP0S": "real_research/derivation_chain_2026/FP0_core_postulates.py",
    "MN3": "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/mnras_a0_lambda_v3.tex",
    "P39": "qwen_claude_field_theory/papers_2026/PAPER39_closure_map_2026.tex",
}
_cache = {}


def raw(key):
    """The file as committed at HEAD (bytes; never the working tree)."""
    if key not in _cache:
        r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + SRC[key]], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"cannot read {SRC[key]} at HEAD (not committed?): {r.stderr.decode()[:200]}")
        _cache[key] = r.stdout
    return _cache[key]


def S(key):
    """Parsed source: JSON for .json, text otherwise; 'P40' = the paper's own numbers (working tree)."""
    if key == "P40":
        if "P40" not in _cache:
            _cache["P40"] = json.load(open(P40))
        return _cache["P40"]
    b = raw(key)
    return json.loads(b) if SRC[key].endswith(".json") else b.decode("utf-8")


def rx(key, pattern, g=1):
    m = re.search(pattern, S(key), re.M)
    if not m:
        raise LookupError(f"pattern not found in {key}: {pattern}")
    return m.group(g)


def commit_exists(h):
    r = subprocess.run(["git", "-C", REPO, "rev-parse", "--verify", "--quiet", h + "^{commit}"], capture_output=True)
    return h if r.returncode == 0 else None


# ---------------------------------------------------------------- shorthands for committed values
def B(*path):
    d = S("B301")["numbers"]
    for p in path:
        d = d[p]
    return d


def J4(*path):
    d = S("J304")["numbers"]
    for p in path:
        d = d[p]
    return d


def P(*path):
    d = S("P40")
    for p in path:
        d = d[p]
    return d


A0C = lambda: S("FP0")["numbers"]["a0_canonical"]
A0A = lambda: S("FP0")["numbers"]["a0_rho_total"]
SPARC = lambda: float(rx("S301", r"SREF = (1\.20) / 0\.93603")) * 1e-10
DESM = lambda: float(rx("MN3", r"a_0=\((1\.19)\\pm0\.04\\pm0\.09\)")) * 1e-10
V26 = lambda: float(rx("R279", r"whole sample a₀ = (1\.50) ± 0\.05")) * 1e-10
POOL = lambda: B("pooled", "a0")
f = lambda n: (lambda v: f"{v:.{n}f}")
sg = lambda n: (lambda v: f"{v:+.{n}f}")
u10 = lambda v, n=3: f"{v / 1e-10:.{n}f}"
u11 = lambda v, n=2: f"{v / 1e-11:.{n}f}"
q2a = lambda lq, n=3: f"{10 ** lq * A0C() / 1e-10:.{n}f}"          # a log10 s* percentile as a0 in 1e-10 m s^-2
dex = lambda a, b: math.log10(a / b)

ROWS = []   # (block, expected literal, getter, tex literal or None, kind)


def R(b, expected, getter, tex=None, kind="src"):
    ROWS.append((b, expected, getter, tex, kind))


def LIT(b, value, tex=None):
    ROWS.append((b, value, (lambda v=value: v), tex, "lit"))


def row13(key, label):
    r = B("results", key); q = r["q"]
    zc = "---" if key == "pooled" else f"{r['z_med']:.3f}"
    dl = "---" if key == "pooled" else f"{r['DL_med']:.0f}"
    return (f"{label} & {r['n']} & {zc} & {dl} & {r['s']:.3f} & {u10(r['a0'])} & {q2a(q[1])}--{q2a(q[2])} & {q2a(q[0])}--{q2a(q[3])} & {r['recipe_half']:.3f}")


def kap(a0, foot, n=3):
    return f"{0.5 * a0 / foot:.{n}f}"


# ================================================================ B01 abstract
R("B01", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
R("B01", "1.1312\\times10^{-10}", lambda: f"{A0A() / 1e-10:.4f}\\times10^{{-10}}")
R("B01", "293", lambda: str(S("A301")["numbers"]["selection"][0][1]), "catalogue (293 H")
R("B01", "47", lambda: str(S("A301")["numbers"]["N"]), "47 golden discs")
R("B01", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "g_{\\rm bar}/a_0\\le0.084")
R("B01", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "and 37 gas-dominated")
R("B01", "+0.008", lambda: sg(3)(S("CC2")["numbers"]["offset_dex"]))
R("B01", "1.046\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B01", "1.01--1.15", lambda: f"{q2a(B('pooled', 'q')[1], 2)}--{q2a(B('pooled', 'q')[2], 2)}")
R("B01", "0.143", lambda: f(3)(B("pooled", "recipe_half")), "\\pm0.143")
R("B01", "+0.048", lambda: sg(3)(dex(POOL(), A0C())))
R("B01", "-0.034", lambda: sg(3)(dex(POOL(), A0A())))
R("B01", "-0.060", lambda: sg(3)(dex(POOL(), SPARC())), "-0.060 dex from SPARC's 1.20")
R("B01", "0.56", lambda: kap(POOL(), A0C(), 2), "\\kappa=0.56")
R("B01", "0.46", lambda: kap(POOL(), A0A(), 2), "or 0.46")
R("B01", "1.25\\times10^{-10}", lambda: f"{u10(B('btfr', '(i) all survivors', 'median'), 2)}\\times10^{{-10}}")
R("B01", "1.19", lambda: u10(B("btfr", "(ii) gas-dominated (M_gas > M*)", "median"), 2), "(1.19 for the gas-dominated discs)")
R("B01", "+0.078", lambda: sg(3)(math.log10(B("btfr", "(i) all survivors", "kernel_factor", "s=1"))))
R("B01", "-0.022", lambda: sg(3)(S("J302")["numbers"]["widths"]["median"]))
R("B01", "0.039", lambda: f(3)(S("J302")["numbers"]["widths"]["robust_scatter"]), "scatter 0.039")
R("B01", "15", lambda: str(J4("results", "sets_n", "C1")), "for 15 overlapping galaxies")
R("B01", "0.195", lambda: f(3)(-J4("results", "cat", "C1", "OPT", "median")), "by 0.195")
R("B01", "0.64", lambda: f(2)(10 ** J4("results", "cat", "C1", "OPT", "median")), "holds 0.64")
R("B01", "0.6--0.75", lambda: f"{J4('cfg301', 'A', 'central', 'a0') / 1e-10:.1f}--{P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0') / 1e-10:.2f}")
R("B01", "1.05\\times10^{-10}", lambda: f"{u10(POOL(), 2)}\\times10^{{-10}}", "and 1.05\\times10^{-10}")
R("B01", "+0.098", lambda: sg(3)(P("post_hoc_rows", "frame_k0", "dlog_vs_primary")))
R("B01", "0.009", lambda: f(3)(B("trend", "rival_lever_W1_W3")), "lever is 0.009")
R("B01", "0.093", lambda: f(3)(S("A301")["numbers"]["windows"][2]["z_max"]), "z\\le0.093")
R("B01", "0.12", lambda: rx("P39", r"\\Omega_ch\^2\\approx(0\.12)"), "\\Omega_ch^2\\approx0.12")
# ================================================================ B02 relation and scale
R("B02", "1.20\\times10^{-10}", lambda: f"{SPARC() / 1e-10:.2f}\\times10^{{-10}}", "g_\\dagger=1.20\\times10^{-10}")
R("B02", "1.19", lambda: f"{DESM() / 1e-10:.2f}", "a_0=(1.19\\pm0.04")
R("B02", "0.04", lambda: rx("MN3", r"a_0=\(1\.19\\pm(0\.04)\\pm0\.09\)"), "\\pm0.04 {\\rm(stat)}")
R("B02", "0.09", lambda: rx("MN3", r"a_0=\(1\.19\\pm0\.04\\pm(0\.09)\)"), "\\pm0.09 {\\rm(sys)}")
LIT("B02", "2693"); LIT("B02", "153")
# ================================================================ B03 MeerKAT
R("B03", "1.50\\pm0.05", lambda: rx("R279", r"whole sample a₀ = (1\.50 ± 0\.05)").replace(" ± ", "\\pm"), "a_0=(1.50\\pm0.05)")
R("B03", "293", lambda: rx("DATA", r"the catalogue is \*\*(293) HI sources"), "lists 293 sources")
R("B03", "0.004<z<0.093", lambda: rx("DATA", r"293 HI sources in COSMOS, (0\.004 < z < 0\.093)").replace(" ", ""))
LIT("B03", "67 galaxies"); LIT("B03", "0\\le z\\le0.081"); LIT("B03", "204 galaxies"); LIT("B03", "slope 0.501"); LIT("B03", "intercept -3.252")
LIT("B03", "19 H"); LIT("B03", "z=0.08"); LIT("B03", "130 resolved")
# ================================================================ B04 framework
R("B04", "67.4", lambda: rx("FP0S", r"H0_KMS, OM_L, OM_M = (67\.4), 0\.6847"), "H_0=67.4")
R("B04", "0.6847", lambda: rx("FP0S", r"H0_KMS, OM_L, OM_M = 67\.4, (0\.6847)"), "\\Omega_\\Lambda=0.6847")
R("B04", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
R("B04", "1.1312\\times10^{-10}", lambda: f"{A0A() / 1e-10:.4f}\\times10^{{-10}}")
R("B04", "2.54", lambda: rx("R279", r"agree to 2\.1×10⁻⁴ relative for y ≤ (2\.54)"), "g_{\\rm bar}/a_0=2.54")
R("B04", "2\\times10^{-4}", lambda: f"{round(float(rx('R279', r'agree to (2\.1)×10⁻⁴ relative'))):d}\\times10^{{-4}}", "to 2\\times10^{-4}")
R("B04", "0.12", lambda: rx("P39", r"\\Omega_ch\^2\\approx(0\.12)"), "\\Omega_ch^2\\approx0.12")
# ================================================================ B05 catalogue
R("B05", "H_0=70", lambda: "H_0=" + rx("DATA", r"distances from LCDM H0 = (70)"), "H_0=70, \\Omega_M=0.3")
R("B05", "q_0=0.2", lambda: "q_0=" + rx("DATA", r"g-band isophotes with q0 = (0\.2)"), "thickness q_0=0.2")
R("B05", "0.45\\%", lambda: f"{S('A301')['numbers']['controls_numbers']['dl_max_rel'] * 100:.2f}\\%")
R("B05", "0.8", lambda: f(1)(P("post_hoc_rows", "q0_check_max_dev_deg")), "to 0.8^\\circ")
# ================================================================ B06 cut and windows
SEL = lambda i: str(S("A301")["numbers"]["selection"][i][1])
R("B06", "293 to 202", lambda: f"{SEL(0)} to {SEL(1)}", "(293 to 202 sources)")
R("B06", "188", lambda: SEL(2), "(188;")
R("B06", "122", lambda: SEL(3), "(122)")
R("B06", "78", lambda: SEL(4), "(78)")
R("B06", "70", lambda: SEL(5), "(70)")
R("B06", "47", lambda: SEL(6), "\\ge8 (47)")
R("B06", "47", lambda: SEL(7), "finite inputs (47)")
for i, tmpl in enumerate(("{} galaxies", "({},", "({},")):
    R("B06", tmpl.format((16, 16, 15)[i]), (lambda i=i, tmpl=tmpl: tmpl.format(S("A301")["numbers"]["windows"][i]["n"])))
for i in range(3):
    w = lambda i=i: S("A301")["numbers"]["windows"][i]
    R("B06", ["0.0266--0.0476", "0.0506--0.0756", "0.0773--0.0930"][i], (lambda w=w: f"{w()['z_min']:.4f}--{w()['z_max']:.4f}"))
    R("B06", ["median 0.042", "median 0.067", "median 0.081"][i], (lambda w=w: f"median {w()['z_med']:.3f}"))
    R("B06", ["185 Mpc", "300 Mpc", "368 Mpc"][i], (lambda w=w: f"{w()['DL_med']:.0f} Mpc"))
R("B06", "0.70", lambda: rx("OA301", r"pooled: N 47; .*?gas fraction median (0\.70)"), "gas fraction is 0.70")
# ================================================================ B07 chain
R("B07", "0.506", lambda: rx("S301", r"D_HI = 10\^\((0\.506) log M_HI - 3\.293\)"), "=0.506\\log_{10}")
R("B07", "-3.293", lambda: "-" + rx("S301", r"D_HI = 10\^\(0\.506 log M_HI - (3\.293)\)"))
R("B07", "1.33", lambda: rx("FC301", r"M_gas = (1\.33) M_HI"), "M_b=1.33")
R("B07", "11", lambda: rx("FC301", r"knob δ = (11) km s⁻¹"), "\\delta=11 km")
# ================================================================ B08 estimator
R("B08", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}", "s^*\\times9.3603\\times10^{-11}")
R("B08", "7\\times10^{-17}", lambda: f"{round(float(rx('OB301', r'\|d log10 a0\| = ([0-9.]+)e-17'))):d}\\times10^{{-17}}")
R("B08", "4{,}000", lambda: "{:,}".format(int(rx("FC301", r"bootstrap over galaxies \(B = (4),000\)") + "000")).replace(",", "{,}"))
# ================================================================ B09 recipe
R("B09", "\\delta=11", lambda: "\\delta=" + rx("FC301", r"knob δ = (11) km s⁻¹"), "\\delta=11 km s^{-1}; M_\\star")
R("B09", "0.25", lambda: rx("FC301", r"knob: ± (0\.25) dex on M\\\*"), "M_\\star\\pm0.25")
R("B09", "0.15", lambda: rx("FC301", r"knob ± (0\.15) dex\)"), "\\pm0.15 dex; and")
R("B09", "67.4", lambda: rx("FC301", r"H₀ = (67\.4) distance variant"), "to 67.4")
R("B09", "0.5", lambda: rx("FC301", r"y = g_bar/a₀ < (0\.5) at R"), "(y<0.5)")
# ================================================================ B10 calibration controls
R("B10", "1.282", lambda: f(3)(SPARC() / A0C()), "=1.282")
R("B10", "1.449", lambda: f(3)(S("J281")["numbers"]["out"]["LC"]["s"]), "s^*=1.449")
R("B10", "1.233", lambda: f(3)(B("results", "W1", "s")), "W1 gives s^*=1.233")
R("B10", "-0.017", lambda: sg(3)(B("calibration", "offset_sparc")))
R("B10", "-0.070", lambda: sg(3)(B("calibration", "offset_281")))
R("B10", "0.136", lambda: f(3)(B("calibration", "w1_recipe_half")), "half-width 0.136")
R("B10", "123", lambda: str(S("CC2")["numbers"]["n"]), "applied to 123 SPARC")
R("B10", "1.304", lambda: f(3)(S("CC2")["numbers"]["s"]))
R("B10", "+0.008", lambda: sg(3)(S("CC2")["numbers"]["offset_dex"]))
R("B10", "1.324", lambda: f(3)(S("CC2")["numbers"]["rhi_diag"]["s_measured_RHI"]))
R("B10", "-0.002", lambda: sg(3)(S("CC2")["numbers"]["rhi_diag"]["median_log_R_ratio"]))
R("B10", "-0.057", lambda: sg(3)(B("calibration", "drift")))
R("B10", "0.136", lambda: f(3)(B("trend", "rho", "W3", "sd_stat")), "width of the drift is 0.136")
R("B10", "-0.013", lambda: sg(3)(S("SELF")["numbers"]["selftest"]["bias"]))
R("B10", "0.023", lambda: rx("FC301", r"stated bias \(CFG281: −(0\.023) dex\)"), "tolerance 0.023")
R("B10", "93 of 100", lambda: f"{S('SELF')['numbers']['selftest']['coverage']} of 100")
# ================================================================ B11 reactivity
R("B11", "1.1892", lambda: rx("FC301", r"widths × (1\.1892)"))
R("B11", "+0.322", lambda: sg(3)(S("MU1")["numbers"]["response"]))
R("B11", "0.30\\pm0.05", lambda: rx("FC301", r"must rise by (0\.30 ± 0\.05) dex").replace(" ± ", "\\pm"))
R("B11", "+0.392", lambda: sg(3)(S("MU2")["numbers"]["response"]))
R("B11", "0.37\\pm0.06", lambda: rx("FC301", r"CFG281: \+(0\.37 ± 0\.06)").replace(" ± ", "\\pm"))
R("B11", "1.332408", lambda: f(6)(S("M5")["numbers"]["LU"]["mine"]))
R("B11", "1.449173", lambda: f(6)(S("M5")["numbers"]["LC"]["mine"]))
R("B11", "six", lambda: {6: "six"}.get(sum(int(v) for v in list(S("A301")["numbers"]["hand_estimates"].values()) + list(S("CC2")["numbers"]["hand_estimates"].values())
                                             + list(B("hand_estimates").values())), "?"), "All six frozen hand estimates hit")
# ================================================================ B12 disclosures
R("B12", "8/3/2/2", lambda: "/".join(str(x) for x in S("A301")["numbers"]["matching"]["W1"]["win_counts"]))
R("B12", "9.605", lambda: f(3)(S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "(9.605)")
R("B12", "9.76", lambda: f(2)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2]), "W3's (9.76)")
R("B12", "0.155", lambda: f(3)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2] - S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "is 0.155 dex below")
# ================================================================ B13 results table (whole rows)
for key, lab in (("W1", "W1"), ("W2", "W2"), ("W3", "W3"), ("pooled", "pooled")):
    R("B13", {"W1": "W1 & 16 & 0.042 & 185 & 1.233 & 1.154 & 1.045--1.312 & 0.964--1.910 & 0.136",
              "W2": "W2 & 16 & 0.067 & 300 & 1.089 & 1.019 & 0.931--1.153 & 0.768--1.311 & 0.139",
              "W3": "W3 & 15 & 0.081 & 368 & 1.081 & 1.012 & 0.780--1.336 & 0.467--1.424 & 0.135",
              "pooled": "pooled & 47 & --- & --- & 1.117 & 1.046 & 1.012--1.145 & 0.936--1.311 & 0.143"}[key], (lambda key=key, lab=lab: row13(key, lab)))
R("B13", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
# ================================================================ B14 level
R("B14", "1.046\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B14", "1.117", lambda: f(3)(B("pooled", "s")), "s^*=1.117")
R("B14", "1.012--1.145", lambda: f"{q2a(B('pooled', 'q')[1])}--{q2a(B('pooled', 'q')[2])}")
R("B14", "0.936--1.311", lambda: f"{q2a(B('pooled', 'q')[0])}--{q2a(B('pooled', 'q')[3])}")
R("B14", "0.143", lambda: f(3)(B("pooled", "recipe_half")), "half-width of 0.143")
R("B14", "+0.048", lambda: sg(3)(dex(POOL(), A0C())))
R("B14", "-0.034", lambda: sg(3)(dex(POOL(), A0A())))
R("B14", "-0.060", lambda: sg(3)(dex(POOL(), SPARC())))
RK = lambda k: B("recipe", "pooled", "rows", k, "half")
R("B14", "0.106", lambda: f(3)(RK("delta")), "0.106 (\\delta)")
R("B14", "0.086", lambda: f(3)(RK("tau_ms")), "0.086 (M_\\star)")
R("B14", "0.026", lambda: f(3)(RK("rdex")), "0.026 (D_{\\rm HI})")
R("B14", "0.036", lambda: f(3)(RK("h0")), "0.036 dex (H_0)")
R("B14", "0.026", lambda: f(3)(RK("sini")), "sensitivity is 0.026")
R("B14", "0.146", lambda: f(3)(B("pooled", "recipe_half_with_sin60")), "(0.146 with it")
R("B14", "0.028, 0.033 and 0.042", lambda: ", ".join(f"{v:.3f}" for v in B("pooled", "y_q")[:2]) + f" and {B('pooled', 'y_q')[2]:.3f}")
R("B14", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "maximum of 0.084")
# ================================================================ B15 windows and drift
R("B15", "1.154, 1.019 and 1.012", lambda: f"{u10(B('results', 'W1', 'a0'))}, {u10(B('results', 'W2', 'a0'))} and {u10(B('results', 'W3', 'a0'))}")
R("B15", "-0.20", lambda: sg(2)(B("trend", "slope")), "is -0.20 per dex")
R("B15", "-0.67 to +0.08", lambda: f"{B('trend', 'slope_q')[1]:+.2f} to {B('trend', 'slope_q')[2]:+.2f}")
R("B15", "-1.25 to +0.35", lambda: f"{B('trend', 'slope_q')[0]:+.2f} to {B('trend', 'slope_q')[3]:+.2f}")
R("B15", "0.877", lambda: f(3)(B("trend", "rho", "W3", "rho")))
R("B15", "-0.057\\pm0.136", lambda: f"{B('trend', 'rho', 'W3', 'log_rho'):+.3f}\\pm{B('trend', 'rho', 'W3', 'sd_stat'):.3f}")
R("B15", "0.105", lambda: f(3)(-B("trend", "cfg281", "change")), "falls by 0.105")
R("B15", "+0.009", lambda: sg(3)(B("trend", "rival_lever_W1_W3")))
# ================================================================ B16 BTFR
BT = lambda k, *p: B("btfr", {"i": "(i) all survivors", "ii": "(ii) gas-dominated (M_gas > M*)"}[k], *p)
R("B16", "1.251\\times10^{-10}", lambda: f"{u10(BT('i', 'median'))}\\times10^{{-10}}")
R("B16", "1.187--1.348", lambda: f"{u10(BT('i', 'q')[1])}--{u10(BT('i', 'q')[2])}")
R("B16", "+0.126", lambda: sg(3)(BT("i", "dex_canonical")))
R("B16", "+0.044", lambda: sg(3)(BT("i", "dex_alt")))
R("B16", "0.123", lambda: f(3)(BT("i", "recipe_half")), "recipe 0.123")
R("B16", "1.187\\times10^{-10}", lambda: f"{u10(BT('ii', 'median'))}\\times10^{{-10}}")
R("B16", "1.109--1.251", lambda: f"{u10(BT('ii', 'q')[1])}--{u10(BT('ii', 'q')[2])}")
R("B16", "+0.103", lambda: sg(3)(BT("ii", "dex_canonical")))
R("B16", "+0.021", lambda: sg(3)(BT("ii", "dex_alt")))
R("B16", "0.128", lambda: f(3)(BT("ii", "recipe_half")), "recipe 0.128")
R("B16", "1.197", lambda: f(3)(BT("i", "kernel_factor", "s=1")))
R("B16", "+0.078", lambda: sg(3)(math.log10(BT("i", "kernel_factor", "s=1"))))
R("B16", "1.172", lambda: f(3)(BT("i", "kernel_factor", "s=1.282")))
R("B16", "1.183", lambda: f(3)(BT("ii", "kernel_factor", "s=1")))
R("B16", "-0.023", lambda: sg(3)(B("gas_minus_deep")))
R("B16", "1.526\\times10^{-10}", lambda: f"{u10(S('CC2')['numbers']['btfr_sparc']['median'])}\\times10^{{-10}}")
# ================================================================ B17 kappa
QP = lambda i: 10 ** B("pooled", "q")[i] * A0C()
HALF = lambda: B("pooled", "recipe_half")
R("B17", "0.559", lambda: kap(POOL(), A0C()), "\\kappa=0.559")
R("B17", "0.540--0.612", lambda: f"{kap(QP(1), A0C())}--{kap(QP(2), A0C())}")
R("B17", "0.500--0.701", lambda: f"{kap(QP(0), A0C())}--{kap(QP(3), A0C())}")
R("B17", "0.143", lambda: f(3)(HALF()), "10^{\\pm0.143}")
R("B17", "0.40--0.78", lambda: f"{kap(POOL() * 10 ** -HALF(), A0C(), 2)}--{kap(POOL() * 10 ** HALF(), A0C(), 2)}")
R("B17", "0.462", lambda: kap(POOL(), A0A()), "\\kappa=0.462")
R("B17", "0.447--0.506", lambda: f"{kap(QP(1), A0A())}--{kap(QP(2), A0A())}")
R("B17", "0.414--0.580", lambda: f"{kap(QP(0), A0A())}--{kap(QP(3), A0A())}")
R("B17", "0.33--0.64", lambda: f"{kap(POOL() * 10 ** -HALF(), A0A(), 2)}--{kap(POOL() * 10 ** HALF(), A0A(), 2)}")
R("B17", "0.036", lambda: f(3)(-(B("recipe", "pooled", "rows", "h0", "log_s")[0] - B("pooled", "log_s"))), "falls by 0.036")
R("B17", "0.514", lambda: kap(10 ** B("recipe", "pooled", "rows", "h0", "log_s")[0] * A0C(), A0C()))
R("B17", "0.425", lambda: kap(10 ** B("recipe", "pooled", "rows", "h0", "log_s")[0] * A0C(), A0A()))
# ================================================================ B18 other determinations
R("B18", "-0.056", lambda: sg(3)(dex(POOL(), DESM())))
R("B18", "1.19", lambda: f"{DESM() / 1e-10:.2f}", "[D23] (1.19)")
R("B18", "-0.157", lambda: sg(3)(dex(POOL(), V26())))
R("B18", "1.50", lambda: f"{V26() / 1e-10:.2f}", "[V26] (1.50)")
R("B18", "1.31--1.80", lambda: rx("R279", r"sub-samples span (1\.31–1\.80)").replace("–", "--"))
# ================================================================ B19 Figure 1 caption
CA = lambda k, t: J4("cfg301", k, t, "a0")
R("B19", "0.60", lambda: u10(CA("A", "central"), 2), "(A, 0.60;")
R("B19", "0.50--0.68", lambda: f"{u10(CA('A', 'hi'), 2)}--{u10(CA('A', 'lo'), 2)}")
R("B19", "0.70", lambda: u10(CA("B", "central"), 2), "(B, 0.70;")
R("B19", "0.61--0.76", lambda: f"{u10(CA('B', 'hi'), 2)}--{u10(CA('B', 'lo'), 2)}")
R("B19", "+0.078", lambda: sg(3)(math.log10(BT("i", "kernel_factor", "s=1"))))
R("B19", "0.936", lambda: u10(A0C()), "canonical (0.936)")
R("B19", "1.131", lambda: u10(A0A()), "alternative (1.131)")
R("B19", "1.20", lambda: f"{SPARC() / 1e-10:.2f}", "g_\\dagger (1.20)")
R("B19", "1.50", lambda: f"{V26() / 1e-10:.2f}", "modelling (1.50)")
# ================================================================ B20 Figure 2 caption
R("B20", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "(filled, 37)")
R("B20", "10", lambda: str(S("A301")["numbers"]["N"] - S("A301")["numbers"]["pooled"]["n_gas_dom"]), "(open, 10)")
R("B20", "1.25\\times10^{-10}", lambda: f"{u10(BT('i', 'median'), 2)}\\times10^{{-10}}")
# ================================================================ B21 systematics table
RC = lambda: J4("results", "cat", "C1", "OPT", "median")
PH2 = lambda k: S("PH304")["numbers"]["PH2"]["consequence"][k]["central"]["a0"]
R("B21", "-0.195", lambda: sg(3)(RC()), "catalogue/ALFALFA -0.195")
R("B21", "-0.243", lambda: sg(3)(dex(CA("A", "central"), POOL())))
R("B21", "0.70", lambda: f(2)(J4("cfg301", "f_gas")), "gas fraction 0.70")
R("B21", "-0.174", lambda: sg(3)(dex(CA("B", "central"), POOL())))
R("B21", "-0.237", lambda: sg(3)(P("flux_translation_post_hoc", "A_all_baryons_R_fixed", "dlog_vs_primary")))
R("B21", "-0.144", lambda: sg(3)(P("flux_translation_post_hoc", "B_gas_only_R_follows", "dlog_vs_primary")))
R("B21", "-0.159", lambda: sg(3)(S("PH304")["numbers"]["PH2"]["any_code"]["R_cat"]), "(-0.159 dex)")
R("B21", "-0.193 / -0.141", lambda: f"{dex(PH2('A'), POOL()):+.3f} / {dex(PH2('B'), POOL()):+.3f}")
R("B21", "+0.098", lambda: sg(3)(P("post_hoc_rows", "frame_k0", "dlog_vs_primary")))
R("B21", "+0.025 / -0.055", lambda: f"{P('post_hoc_rows', 'q0_0.10', 'dlog_vs_primary'):+.3f} / {P('post_hoc_rows', 'q0_0.30', 'dlog_vs_primary'):+.3f}")
R("B21", "+0.026", lambda: sg(3)(B("recipe", "pooled", "rows", "sini", "log_s")[0] - B("pooled", "log_s")))
R("B21", "-0.106", lambda: sg(3)(B("recipe", "pooled", "rows", "delta", "log_s")[0] - B("pooled", "log_s")))
R("B21", "-0.090 / +0.082", lambda: f"{B('recipe', 'pooled', 'rows', 'tau_ms', 'log_s')[1] - B('pooled', 'log_s'):+.3f} / {B('recipe', 'pooled', 'rows', 'tau_ms', 'log_s')[0] - B('pooled', 'log_s'):+.3f}")
R("B21", "+0.021 / -0.031", lambda: f"{B('recipe', 'pooled', 'rows', 'rdex', 'log_s')[1] - B('pooled', 'log_s'):+.3f} / {B('recipe', 'pooled', 'rows', 'rdex', 'log_s')[0] - B('pooled', 'log_s'):+.3f}")
R("B21", "-0.001", lambda: sg(3)(P("post_hoc_rows", "size_rajohnson2022", "dlog_vs_primary")))
R("B21", "-0.036", lambda: sg(3)(B("recipe", "pooled", "rows", "h0", "log_s")[0] - B("pooled", "log_s")))
R("B21", "1.046\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
# ================================================================ B22 CFG302
def N302(*p):
    d = S("J302")["numbers"]
    for k in p:
        d = d[k]
    return d

R("B22", "188", lambda: str(N302("counts", "n_sample")), "the 188 golden")
R("B22", "74.2--77.3", lambda: rx("R302", r"circular, \*\*(74\.2–77\.3)″").replace("–", "--"))
R("B22", "179", lambda: str(N302("counts", "n_primary")), "Of the 179")
R("B22", "58", lambda: str(N302("detection", "n_detected")), "58 reach")
R("B22", "-0.022", lambda: sg(3)(N302("widths", "median")))
R("B22", "0.039", lambda: f(3)(N302("widths", "robust_scatter")), "scatter of 0.039")
R("B22", "4 of 58", lambda: f"{N302('widths', 'n_pull_out')} of {N302('widths', 'n')}")
R("B22", "0.22", lambda: f(2)(N302("fluxes", "all_linear", "median")), "all 179 is 0.22")
R("B22", "-0.30", lambda: sg(2)(N302("fluxes", "detected_log", "median")), "is -0.30 dex")
R("B22", "0.50", lambda: f(2)(10 ** N302("fluxes", "detected_log", "median")), "a ratio of 0.50")
R("B22", "0.24", lambda: f(2)(N302("fluxes", "detected_log", "robust_scatter")), "scatter 0.24")
R("B22", "46 of 58", lambda: f"{N302('fluxes', 'n_pull_out')} of {N302('fluxes', 'detected_log', 'n')}")
R("B22", "1.002", lambda: f(3)(S("PH302")["numbers"]["PH4"]["median_ratio_to_1p5"]["2.5"]))
R("B22", "0.60\\pm0.05", lambda: f"{S('PH302')['numbers']['PH5']['line_mean']:.2f}\\pm" + rx("R302", r"holds \*\*0\.60 ± (0\.05)\*\*"))
R("B22", "0.489", lambda: f(3)(N302("C_OFF", "robust_std_win")))
R("B22", "45", lambda: str(P("post_hoc_rows", "cfg302_join", "n_primary")), "45 are in")
R("B22", "20", lambda: str(P("post_hoc_rows", "cfg302_join", "n_detected")), "and 20 reach")
R("B22", "-0.443", lambda: sg(3)(P("post_hoc_rows", "cfg302_join", "median_logratio_S_detected")))
R("B22", "-0.017", lambda: sg(3)(P("post_hoc_rows", "cfg302_join", "median_logratio_W50_detected")))
# ================================================================ B23 CFG304
R("B23", "23", lambda: str(J4("results", "n_pairs")), "23 matches")
R("B23", "15", lambda: str(J4("results", "sets_n", "C1")), "15 of them")
R("B23", "+0.000", lambda: sg(3)(J4("results", "w50", "C1", "median")))
R("B23", "0.037", lambda: f(3)(J4("results", "w50", "C1", "robust_scatter")), "scatter 0.037")
R("B23", "0.275", lambda: f(3)(J4("shuffle", "mean")))
R("B23", "-0.195", lambda: sg(3)(RC()), "flux is -0.195")
R("B23", "-0.250 to -0.156", lambda: f"{J4('results', 'cat', 'C1', 'OPT', 'p16'):+.3f} to {J4('results', 'cat', 'C1', 'OPT', 'p84'):+.3f}")
R("B23", "0.64", lambda: f(2)(10 ** RC()), "about 0.64")
R("B23", "7", lambda: str(J4("results", "csets_n", "C1")), "for the 7 of them")
R("B23", "-0.308", lambda: sg(3)(J4("results", "cube", "C1", "OPT", "median")))
R("B23", "-0.175", lambda: sg(3)(J4("results", "decisions", "CLEAN_C1_OPT", "R_cat")))
R("B23", "-0.383", lambda: sg(3)(J4("results", "decisions", "CLEAN_C1_OPT", "R_cube")))
R("B23", "0.22", lambda: f(2)(-S("PH304")["numbers"]["PH4"]["C1"]["dlogM"][0]), "sit 0.22 dex below")
R("B23", "-0.137", lambda: sg(3)(S("PH304")["numbers"]["PH1"]["ALL"]["z_ge_002"][0]))
R("B23", "19", lambda: str(S("PH304")["numbers"]["PH1"]["ALL"]["z_ge_002"][1]), "over 19 pairs")
R("B23", "neither", lambda: J4("results", "decisions", "C1_OPT", "decision"), "``neither''")
# ================================================================ B24 the flux scale and a0
R("B24", "5.97\\times10^{-11}", lambda: f"{u11(CA('A', 'central'))}\\times10^{{-11}}")
R("B24", "4.98--6.76", lambda: f"{u11(CA('A', 'hi'))}--{u11(CA('A', 'lo'))}")
R("B24", "7.00\\times10^{-11}", lambda: f"{u11(CA('B', 'central'))}\\times10^{{-11}}")
R("B24", "0.70", lambda: f(2)(J4("cfg301", "f_gas")), "gas fraction of 0.70")
R("B24", "6.08--7.60", lambda: f"{u11(CA('B', 'hi'))}--{u11(CA('B', 'lo'))}")
R("B24", "6.06\\times10^{-11}", lambda: f"{u11(P('flux_translation_post_hoc', 'A_all_baryons_R_fixed', 'a0'))}\\times10^{{-11}}")
R("B24", "7.50\\times10^{-11}", lambda: f"{u11(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'))}\\times10^{{-11}}")
R("B24", "7.11", lambda: u11(P("flux_translation_post_hoc", "B_gas_only_R_fixed", "a0")), "7.11 at fixed R")
R("B24", "-0.159", lambda: sg(3)(S("PH304")["numbers"]["PH2"]["any_code"]["R_cat"]))
R("B24", "6.7", lambda: u11(PH2("A"), 1), "gives 6.7 and")
R("B24", "7.6", lambda: u11(PH2("B"), 1), "7.6\\times10^{-11}")
R("B24", "23", lambda: str(J4("results", "n_pairs")), "the 23 H")
R("B24", "0.047", lambda: rx("R304", r"the 23 HI-brightest COSMOS sources at z ≤ (0\.047)"), "z\\le0.047")
R("B24", "0.093", lambda: rx("R304", r"CFG301's 47 galaxies reach z = (0\.093)"), "z=0.093")
R("B24", "1.05\\times10^{-10}", lambda: f"{u10(POOL(), 2)}\\times10^{{-10}}")
R("B24", "0.32--0.40", lambda: f"{kap(CA('A', 'central'), A0C(), 2)}--{kap(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), A0C(), 2)}")
R("B24", "0.26--0.33", lambda: f"{kap(CA('A', 'central'), A0A(), 2)}--{kap(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), A0A(), 2)}")
R("B24", "0.20--0.30", lambda: f"{-dex(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), SPARC()):.2f}--{-dex(CA('A', 'central'), SPARC()):.2f}")
# ================================================================ B25 velocity frame
R("B25", "+0.002", lambda: sg(3)(N302("widths", "obsframe_median")), "reading to +0.002")
R("B25", "-0.022", lambda: sg(3)(N302("widths", "median")))
R("B25", "0.025", lambda: rx("R302", r"velocity convention is not decided \(± (0\.025) dex\)"), "\\pm0.025")
R("B25", "0.098", lambda: f(3)(P("post_hoc_rows", "frame_k0", "dlog_vs_primary")), "rise by 0.098")
R("B25", "1.31\\times10^{-10}", lambda: f"{u10(P('post_hoc_rows', 'frame_k0', 'a0'), 2)}\\times10^{{-10}}")
R("B25", "0.065", lambda: f(3)(P("post_hoc_rows", "frame_k0", "z_median")), "z=0.065")
# ================================================================ B26 inclinations etc.
R("B26", "+0.025", lambda: sg(3)(P("post_hoc_rows", "q0_0.10", "dlog_vs_primary")))
R("B26", "-0.055", lambda: sg(3)(P("post_hoc_rows", "q0_0.30", "dlog_vs_primary")))
R("B26", "+0.026", lambda: sg(3)(B("recipe", "pooled", "rows", "sini", "log_s")[0] - B("pooled", "log_s")))
R("B26", "0.106", lambda: f(3)(RK("delta")), "by 0.106")
R("B26", "37 of the 47", lambda: f"{S('A301')['numbers']['pooled']['n_gas_dom']} of the {S('A301')['numbers']['N']}")
R("B26", "-0.090 / +0.082", lambda: f"{B('recipe', 'pooled', 'rows', 'tau_ms', 'log_s')[1] - B('pooled', 'log_s'):+.3f} / {B('recipe', 'pooled', 'rows', 'tau_ms', 'log_s')[0] - B('pooled', 'log_s'):+.3f}")
R("B26", "0.026", lambda: f(3)(RK("rdex")), "by 0.026 dex (half-width)")
R("B26", "-0.001", lambda: sg(3)(P("post_hoc_rows", "size_rajohnson2022", "dlog_vs_primary")))
R("B26", "0.008", lambda: f(3)(-P("post_hoc_rows", "size_rajohnson2022", "dlogD_at_median")), "smaller by 0.008")
R("B26", "9.73", lambda: f(2)(P("post_hoc_rows", "size_rajohnson2022", "median_logMHI")), "=9.73")
# ================================================================ B27 distances
R("B27", "0.036", lambda: f(3)(RK("h0")), "by 0.036")
R("B27", "9.62\\times10^{-11}", lambda: f"{u11(10 ** B('recipe', 'pooled', 'rows', 'h0', 'log_s')[0] * A0C())}\\times10^{{-11}}")
R("B27", "1.028", lambda: f(3)(10 ** B("recipe", "pooled", "rows", "h0", "log_s")[0]), "s^*=1.028")
# ================================================================ B28 matching and N
R("B28", "0.155", lambda: f(3)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2] - S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "is 0.155 dex lower")
R("B28", "15--16", lambda: f"{min(w['n'] for w in S('A301')['numbers']['windows'])}--{max(w['n'] for w in S('A301')['numbers']['windows'])}", "With 15--16 galaxies")
# ================================================================ B29 what it can say
R("B29", "1.046\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B29", "-0.060", lambda: sg(3)(dex(POOL(), SPARC())))
R("B29", "0.082", lambda: f(3)(dex(A0A(), A0C())), "differ by 0.082")
R("B29", "+0.048", lambda: sg(3)(dex(POOL(), A0C())))
R("B29", "-0.034", lambda: sg(3)(dex(POOL(), A0A())))
R("B29", "0.143", lambda: f(3)(HALF()), "half-width of 0.143")
SD = lambda: [dex(CA("A", "central"), POOL()), dex(CA("B", "central"), POOL()), P("flux_translation_post_hoc", "A_all_baryons_R_fixed", "dlog_vs_primary"),
              P("flux_translation_post_hoc", "B_gas_only_R_follows", "dlog_vs_primary"), dex(PH2("A"), POOL()), dex(PH2("B"), POOL())]
R("B29", "-0.14 to -0.24", lambda: f"{max(SD()):+.2f} to {min(SD()):+.2f}")
R("B29", "0.009", lambda: f(3)(B("trend", "rival_lever_W1_W3")), "constant by 0.009")
R("B29", "0.136", lambda: f(3)(B("trend", "rho", "W3", "sd_stat")), "width of 0.136")
R("B29", "0.60--0.75", lambda: f"{u10(CA('A', 'central'), 2)}--{u10(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), 2)}")
R("B29", "0.20--0.30", lambda: f"{-dex(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), SPARC()):.2f}--{-dex(CA('A', 'central'), SPARC()):.2f}")
R("B29", "+0.008", lambda: sg(3)(S("CC2")["numbers"]["offset_dex"]))
# ================================================================ B30 conclusions
R("B30", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "y\\le0.084")
R("B30", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "37 of them")
R("B30", "1.046\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B30", "1.01--1.15", lambda: f"{q2a(B('pooled', 'q')[1], 2)}--{q2a(B('pooled', 'q')[2], 2)}")
R("B30", "0.143", lambda: f(3)(HALF()), "\\pm0.143")
R("B30", "0.56", lambda: kap(POOL(), A0C(), 2), "\\kappa=0.56")
R("B30", "0.46", lambda: kap(POOL(), A0A(), 2), "or 0.46")
R("B30", "15", lambda: str(J4("results", "sets_n", "C1")), "for 15 bright")
R("B30", "0.195", lambda: f(3)(-RC()), "by 0.195")
R("B30", "0.60--0.75", lambda: f"{u10(CA('A', 'central'), 2)}--{u10(P('flux_translation_post_hoc', 'B_gas_only_R_follows', 'a0'), 2)}")
R("B30", "+0.098", lambda: sg(3)(P("post_hoc_rows", "frame_k0", "dlog_vs_primary")))
# ================================================================ B31 data availability (commits, provenance, the catalogue's bytes)
for h in ("2555ab142", "6b10c01c0", "7d317dd4f", "a89ba33b9", "336b36f8f", "34e40dac6", "19adffd49"):
    R("B31", h, (lambda h=h: commit_exists(h)))
R("B31", "eb247d5de07eb30e", lambda: rx("DATA", r"sha256 prefix (eb247d5de07eb30e)"))
R("B31", "75,999", lambda: "{:,}".format(len(raw("CSV"))), "(75,999 bytes")
R("B31", "bcf9e8558bc5644805b9acb288372c17daffac76d8be6c89d7db9843af9fbf23", lambda: hashlib.sha256(raw("CSV")).hexdigest())
R("B31", "10.48479/jkc0-g916", lambda: rx("DATA", r"SARAO DOI (10\.48479/jkc0-g916)"))


# ---------------------------------------------------------------- machinery
def norm_tex(s):
    s = s.replace("$", "").replace("\\,", " ").replace("~", " ")
    s = re.sub(r"\s*/\s*", "/", s)
    return re.sub(r"\s+", " ", s)


def tex_blocks(text):
    blocks, cur = {}, []
    for line in text.split("\n"):
        m = re.match(r"% AUDIT: (B\d\d)\s*$", line)
        if m:
            if m.group(1) in blocks:
                raise SystemExit(f"duplicate AUDIT tag {m.group(1)} in the tex")
            blocks[m.group(1)] = norm_tex("\n".join(cur))
            cur = []
        elif not line.lstrip().startswith("%"):
            cur.append(line)
    return blocks


MUTATE_KEY = ("B01", "1.046\\times10^{-10}")


def run(mode=None):
    p40 = S("P40")
    if not p40.get("reproduction_ok"):
        raise SystemExit("PAPER40_figures_numbers.json: the reproduction gate did not pass -- re-run make_paper40_figures.py")
    blocks = tex_blocks(open(TEX, encoding="utf-8").read())
    mi = next(i for i, r in enumerate(ROWS) if (r[0], r[1]) == MUTATE_KEY)
    results, used = [], set()
    for i, (b, expected, getter, tex, kind) in enumerate(ROWS):
        used.add(b)
        try:
            got = getter()
        except Exception as e:                      # a missing key or pattern is a failed row, not a crash
            got = f"<error: {e}>"
        exp = expected
        lit = norm_tex(tex if tex is not None else expected)
        label = f"[{b}] {kind}: {expected}"
        if i == mi and mode == "value":
            exp = exp.replace("1.046", "1.047"); label += "  (MUTATED expected value)"
        if i == mi and mode == "tex":
            lit = lit.replace("1.046", "1.047"); label += "  (MUTATED tex literal)"
        src_ok = (got == exp) if kind == "src" else True
        tex_ok = lit in blocks.get(b, "")
        results.append((label, kind, got, src_ok, tex_ok, lit))
    orphan = sorted(set(blocks) - used)
    missing = sorted(used - set(blocks))
    return results, orphan, missing


if __name__ == "__main__":
    mode = "value" if "--mutate" in sys.argv else "tex" if "--mutate-tex" in sys.argv else None
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()
    print(f"PAPER40 audit against committed files at HEAD {head} (paper's own numbers: PAPER40_figures_numbers.json, working tree)"
          + (f"   [MUTATE: {mode}]" if mode else ""))
    results, orphan, missing = run(mode)
    bad = {"src": 0, "lit": 0}; n = {"src": 0, "lit": 0}
    for label, kind, got, s_ok, t_ok, lit in results:
        ok = s_ok and t_ok
        n[kind] += 1; bad[kind] += (not ok)
        if not ok or "-v" in sys.argv:
            why = ("source gives %r" % got if not s_ok else "") + ("; not printed in its tex block as %r" % lit if not t_ok else "")
            print(f"  [{'ok ' if ok else 'BAD'}] {label:60s} {why}")
    if orphan:
        print("  note: tex blocks with no audit rows:", ", ".join(orphan))
    if missing:
        print("  BAD: audit rows name blocks absent from the tex:", ", ".join(missing))
        bad["src"] += len(missing)
    print(f"\n{n['src'] - bad['src']} of {n['src']} quoted values match their committed sources and their tex blocks")
    print(f"{n['lit'] - bad['lit']} of {n['lit']} literature values (LIT; from the arXiv abstracts read 2026-10-02, not in a committed file) are printed in their blocks")
    tot = bad["src"] + bad["lit"]
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if tot else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if tot else 0)
