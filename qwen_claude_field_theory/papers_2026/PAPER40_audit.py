#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER40 v1.2 audit: every number the paper quotes in an audited block is re-read from a COMMITTED file (git HEAD) and checked.

For each audited value the script checks that
  (1) the value, formatted as the paper prints it, follows from its source: a JSON field (read with `git show HEAD:<path>`, never the
      working tree), a regex capture over a committed text file, or a stated arithmetic on such values (a rounding, a ratio to a footing,
      kappa = a0 / (2 a0_footing));
  (2) the value is printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the non-comment lines since the previous tag);
      short literals are matched with their surrounding words, so a bare "0.01" cannot match by accident;
  (3) for rows whose value is a plain number, the number is also present in the text of the built PDF (pdftotext), so the PDF and the
      tex cannot drift apart.
Exit 0 only if every row matches.  Reports "N of N" per check.

Sources
  * committed at HEAD: the CFG301, CFG302, CFG304, CFG306 and CFG309 outputs and READMEs, CFG279's and CFG281's files, the catalogue's
    provenance note and file, FP0's constants, CFG1's README (SPARC's systematic), the committed MNRAS v3 draft (Desmond 2023's published
    a0) and PAPER39 (Omega_c h^2).
  * v1.1 primary (catalogue W50 rest-frame, k = 0): CFG309's re-run of CFG301's committed chain
    (cfg309_cfg301chain_stageB_FRAME_results.json and _summary.json).  CFG301's own k = 1 JSON is the disclosed version 1.0 variant.
  * the paper's own output PAPER40_figures_numbers.json (written by make_paper40_figures.py, committed WITH this paper; read from the
    working tree, like the .tex and the PDF) for the rows labelled post hoc in the paper.  The script refuses to run if that file's
    reproduction gate (CFG301, CFG309 and CFG306 committed values reproduced) did not pass.
  * literature values (LIT rows) that no committed file carries: checked only for being printed in their block, against the values recorded
    here from the arXiv abstract pages read on 2026-10-02/03 and the V26 e-print source (arXiv:2608.03576, sha256 a79e2a67...); a
    separate tally.
Coverage: only numbers carried by a row below are checked; numbers quoted only in running text and the references' journal data are not.
Where a lane README and its script output differ, the output wins (CFG302's beam range is read from its results JSON, not its README).

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
PDF = os.path.join(HERE, "PAPER40_meerkat_a0_2026.pdf")
P40 = os.path.join(HERE, "PAPER40_figures_numbers.json")
CFG = "campaign_fresh_gravity/"
L301 = CFG + "CFG301_mightee_hi_catalogue_width_chain/"
L302 = CFG + "CFG302_mightee_cube_raw_widths/"
L304 = CFG + "CFG304_mightee_flux_scale_alfalfa/"
L306 = CFG + "CFG306_paper40_referee/"
L309 = CFG + "CFG309_mightee_width_frame/"
SRC = {
    "A301": L301 + "cfg301_stageA_results.json",
    "B301": L301 + "cfg301_stageB_results.json",
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
    "P306": L306 + "cfg306_physics_checks_results.json",
    "FS306": L306 + "cfg306_flux_scale_results.json",
    "VF306": L306 + "cfg306_velocity_frame_results.json",
    "REF306": L306 + "REFEREE_REPORT.md",
    "F309": L309 + "cfg309_cfg301chain_stageB_FRAME_results.json",
    "S309": L309 + "cfg309_cfg301chain_FRAME_summary.json",
    "OF309": L309 + "cfg309_cfg301chain_stageB_FRAME.out",
    "W309": L309 + "cfg309_width_frame_results.json",
    "R279": CFG + "CFG279_mightee_published_values/README.md",
    "O279": CFG + "CFG279_mightee_published_values/cfg279.out",
    "J281": CFG + "CFG281_budhies_local_control/cfg281_stageB_results.json",
    "R1": CFG + "CFG1_README.md",
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


def dig(d, path):
    for p in path:
        d = d[p]
    return d


# ---------------------------------------------------------------- shorthands for committed values
B = lambda *p: dig(S("B301")["numbers"], p)          # CFG301, k = 1 (version 1.0 frame)
F = lambda *p: dig(S("F309")["numbers"], p)          # CFG309 FRAME, k = 0 (v1.1 primary)
J4 = lambda *p: dig(S("J304")["numbers"], p)
P6 = lambda *p: dig(S("P306")["numbers"], p)
P = lambda *p: dig(S("P40"), p)                      # this paper's post hoc numbers
A0C = lambda: S("FP0")["numbers"]["a0_canonical"]
A0A = lambda: S("FP0")["numbers"]["a0_rho_total"]
SPARC = lambda: float(rx("S301", r"SREF = (1\.20) / 0\.93603")) * 1e-10
SPSYS = lambda: float(rx("R1", r"g† = 1\.20 ± 0\.02 ± (0\.24) \(sys\)"))
DESM = lambda: float(rx("MN3", r"a_0=\((1\.19)\\pm0\.04\\pm0\.09\)")) * 1e-10
V26 = lambda: float(rx("R279", r"whole sample a₀ = (1\.50) ± 0\.05")) * 1e-10
POOL = lambda: F("pooled", "a0")
POOL1 = lambda: B("pooled", "a0")
HALF = lambda: F("pooled", "recipe_half")
f = lambda n: (lambda v: f"{v:.{n}f}")
sg = lambda n: (lambda v: f"{v:+.{n}f}")
u10 = lambda v, n=3: f"{v / 1e-10:.{n}f}"
q2a = lambda lq, n=3: f"{10 ** lq * A0C() / 1e-10:.{n}f}"          # a log10 s* percentile as a0 in 1e-10 m s^-2
dex = lambda a, b: math.log10(a / b)
PM = lambda s: s.replace(" +- ", "\\pm").replace(" ± ", "\\pm")
# CFG306 P3 (flux scale x frame): the gas-only reading at k = 0 for each ratio
G3 = lambda lab: P6("P3_flux_frame", f"{lab} | k=0", "a0_gas")
SNRX, PAIR7, ZX = "CFG306 S2: code-1 trend in SNR_3D extrapolated to the 47", "CFG301-like 7 pairs (CFG304 PH2)", "CFG306 S2: code-1 trend in z extrapolated to the 47"
C1R, ZGE, ZCL = "C1 code-1 (CFG304 primary)", "z >= 0.02, codes 1+2 (CFG304 PH1)", "z >= 0.02, confusion-clean (CFG304 PH1)"
FLUXLABS = (C1R, PAIR7, ZGE, ZCL, SNRX, ZX)
# CFG306 P2 (kernels): a0 at k = 0 / k = 1
K2 = lambda name, k="a0_k0": P6("P2_kernels", "rows", name, k)
KEXP, KCF = "exp (nu_mono, MLS16; PAPER40 primary)", "framework closed form sqrt(1+1/y)"
KSTD, KSIM, KDEL = "standard (n=2)", "simple (alpha=1)", "delta-family delta=4.1 (V26 best fit)"
KD = lambda name: dex(K2(name), K2(KEXP))
KUP = lambda: [KD(KSTD), KD(KCF), KD(KDEL)]
RF = lambda k, i=0: F("recipe", "pooled", "rows", k, "log_s")[i] - F("pooled", "log_s")
SEL = lambda k: P("post_hoc_rows", "selection_snr", k)
COR = lambda k: P("post_hoc_rows", "residuals_k0", "spearman", k)
JF = lambda k: P("post_hoc_rows", "residuals_k0", "joint_fit", k)

EC = lambda conv, *k: P("post_hoc_rows", "errors_and_conventions_k0", conv, *k)
SD_ = lambda *k: P("post_hoc_rows", "single_dish_range", *k)
ROWS = []   # (block, expected literal, getter, tex literal or None, kind)


def R(b, expected, getter, tex=None, kind="src"):
    ROWS.append((b, expected, getter, tex, kind))


def LIT(b, value, tex=None):
    ROWS.append((b, value, (lambda v=value: v), tex, "lit"))


def kap(a0, foot, n=3):
    return f"{0.5 * a0 / foot:.{n}f}"


def row15(key, label):
    r = F("results", key); q = r["q"]
    zc = "---" if key == "pooled" else f"{r['z_med']:.3f}"
    dl = "---" if key == "pooled" else f"{r['DL_med']:.0f}"
    return (f"{label} & {r['n']} & {zc} & {dl} & {r['s']:.3f} & {u10(r['a0'])} & {q2a(q[1])}--{q2a(q[2])} & {q2a(q[0])}--{q2a(q[3])} & {r['recipe_half']:.3f}")


# ================================================================ B01 abstract
R("B01", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
R("B01", "1.1312\\times10^{-10}", lambda: f"{A0A() / 1e-10:.4f}\\times10^{{-10}}")
R("B01", "Forty-seven", lambda: {47: "Forty-seven"}.get(S("A301")["numbers"]["N"], "?"), "Forty-seven golden discs")
R("B01", "0.027", lambda: f(3)(S("A301")["numbers"]["windows"][0]["z_min"]), "at 0.027\\le z\\le0.093")
R("B01", "0.093", lambda: f(3)(S("A301")["numbers"]["windows"][2]["z_max"]), "z\\le0.093 survive")
R("B01", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "g_{\\rm bar}/a_0\\le0.084")
R("B01", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "37 gas-dominated")
R("B01", "1.31\\times10^{-10}", lambda: f"{u10(POOL(), 2)}\\times10^{{-10}}", "a_0=1.31\\times10^{-10} m s^{-2}")
R("B01", "0.034", lambda: f(3)(F("pooled", "sd")), "statistical \\pm0.034 or")
R("B01", "0.128", lambda: f(3)(HALF()), "recipe \\pm0.128 dex")
R("B01", "0.70", lambda: kap(POOL(), A0C(), 2), "\\kappa=0.70 or")
R("B01", "0.58", lambda: kap(POOL(), A0A(), 2), "or 0.58:")
R("B01", "0.048", lambda: f(3)(EC("H0=70", "se_median")), "or \\pm0.048 dex, by bootstrap or per-galaxy spread")
R("B01", "0.019", lambda: f(3)(dex(POOL(), A0C()) - HALF()), "canonical footing 0.019 dex outside")
R("B01", "1.21\\times10^{-10}", lambda: f"{u10(H0A(), 2)}\\times10^{{-10}}", "a_0=1.21\\times10^{-10}")
R("B01", "0.111", lambda: f(3)(EC("H0=67.4", "dex_canonical")), "(0.111 dex away)")
R("B01", "0.90--1.13", lambda: f"{u10(SD_('lo'), 2)}--{u10(SD_('hi'), 2)}", "give 0.90--1.13\\times10^{-10}")
R("B01", "0.90", lambda: u10(G3(C1R), 2), "(0.90 for the frozen pairs")
R("B01", "1.07", lambda: u10(G3(SNRX), 2), "1.07 for a post hoc extrapolation)")
R("B01", "0.08", lambda: f(2)(SEL("0")["dlog_vs_primary"]), "S/N cut, by 0.08 dex")
R("B01", "0.10", lambda: f(2)(-RF("delta")), "by up to 0.10 dex")
R("B01", "0.06--0.07", lambda: f"{min(KUP()):.2f}--{max(KUP()):.2f}", "by 0.06--0.07 dex")
R("B01", "0.009", lambda: f(3)(F("trend", "rival_lever_W1_W3")), "lever of 0.009 dex")
R("B01", "0.12", lambda: rx("P39", r"\\Omega_ch\^2\\approx(0\.12)"), "\\Omega_ch^2\\approx0.12")
# ================================================================ B02 relation and scale
R("B02", "1.20\\times10^{-10}", lambda: f"{SPARC() / 1e-10:.2f}\\times10^{{-10}}", "g_\\dagger=1.20\\times10^{-10}")
R("B02", "0.24", lambda: f(2)(SPSYS()), "\\pm0.24 in the same units")
R("B02", "0.08", lambda: f(2)(math.log10((1.20 + SPSYS()) / 1.20)), "units, 0.08 dex")
R("B02", "1.19", lambda: f"{DESM() / 1e-10:.2f}", "a_0=(1.19\\pm0.04")
R("B02", "0.04", lambda: rx("MN3", r"a_0=\(1\.19\\pm(0\.04)\\pm0\.09\)"), "\\pm0.04 {\\rm(stat)}")
R("B02", "0.09", lambda: rx("MN3", r"a_0=\(1\.19\\pm0\.04\\pm(0\.09)\)"), "\\pm0.09 {\\rm(sys)}")
LIT("B02", "2693 points"); LIT("B02", "153 SPARC"); LIT("B02", "a_0=1.3\\pm0.3")
# ================================================================ B03 MeerKAT, V25/V26, line widths
R("B03", "1.69\\pm0.13", lambda: PM(rx("O279", r"COSMOS reference, Sersic N=19 (1\.69 \+- 0\.13)")), "a_0=(1.69\\pm0.13)")
R("B03", "1.50\\pm0.05", lambda: PM(rx("R279", r"whole sample a₀ = (1\.50 ± 0\.05)")), "a_0=(1.50\\pm0.05)")
R("B03", "1.48\\pm0.04", lambda: PM(rx("O279", r"Sersic photometry N=130 (1\.48 \+- 0\.04)")), "(1.48\\pm0.04)")
R("B03", "1.86\\pm0.06", lambda: PM(rx("O279", r"a0 = (1\.86 \+- 0\.06) \(delta")), "(1.86\\pm0.06)")
R("B03", "-1.60\\pm2.33", lambda: PM(rx("O279", r"varying\s+RAR\s+a1 =\s+(-1\.60 \+- 2\.33)")), "a_1=(-1.60\\pm2.33)")
R("B03", "5.0", lambda: rx("O279", r"a1/sigma 4\.981 \((5\.0)\)"), "formal 5.0\\sigma rise")
R("B03", "293", lambda: rx("DATA", r"the catalogue is \*\*(293) HI sources"), "lists 293 sources")
R("B03", "0.004<z<0.093", lambda: rx("DATA", r"293 HI sources in COSMOS, (0\.004 < z < 0\.093)").replace(" ", ""))
R("B03", "-4.80\\pm0.76", lambda: PM(rx("O279", r"MIGHTEE\+LADUMA\+SPARC\s+constant 0\.6\s+RAR\s+a1 =\s+(-4\.80 \+- 0\.76)")), "a_1=(-4.80\\pm0.76)")
R("B03", "6.3", lambda: f"{abs(float(rx('O279', r'MIGHTEE\+LADUMA\+SPARC\s+constant 0\.6\s+RAR\s+a1 =\s+-4\.80 \+- 0\.76\s+\(a1/sigma = (-6\.32)\)'))):.1f}", "formal 6.3\\sigma fall")
LIT("B03", "67 early-science"); LIT("B03", "0\\le z\\le0.081"); LIT("B03", "(slope 3.66)"); LIT("B03", "204 galaxies"); LIT("B03", "slope 0.501")
LIT("B03", "intercept -3.252"); LIT("B03", "19 H"); LIT("B03", "z=0.08"); LIT("B03", "130 resolved"); LIT("B03", "3.75\\pm0.11")
# ================================================================ B04 framework
R("B04", "67.4", lambda: rx("FP0S", r"H0_KMS, OM_L, OM_M = (67\.4), 0\.6847"), "H_0=67.4")
R("B04", "0.6847", lambda: rx("FP0S", r"H0_KMS, OM_L, OM_M = 67\.4, (0\.6847)"), "\\Omega_\\Lambda=0.6847")
R("B04", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
R("B04", "1.1312\\times10^{-10}", lambda: f"{A0A() / 1e-10:.4f}\\times10^{{-10}}")
R("B04", "2.54", lambda: rx("R279", r"agree to 2\.1×10⁻⁴ relative for y ≤ (2\.54)"), "g_{\\rm bar}/a_0=2.54")
R("B04", "2\\times10^{-4}", lambda: f"{round(float(rx('R279', r'agree to (2\.1)×10⁻⁴ relative'))):d}\\times10^{{-4}}", "to 2\\times10^{-4}")
R("B04", "0.12", lambda: rx("P39", r"\\Omega_ch\^2\\approx(0\.12)"), "\\Omega_ch^2\\approx0.12")
# ================================================================ B05 this paper / version note
R("B05", "0.098", lambda: f(3)(dex(POOL(), POOL1())), "by 0.098 dex")
# ================================================================ B06 catalogue
R("B06", "H_0=70", lambda: "H_0=" + rx("DATA", r"distances from LCDM H0 = (70)"), "H_0=70, \\Omega_M=0.3")
R("B06", "q_0=0.2", lambda: "q_0=" + rx("DATA", r"g-band isophotes with q0 = (0\.2)"), "thickness q_0=0.2")
R("B06", "0.45\\%", lambda: f"{S('A301')['numbers']['controls_numbers']['dl_max_rel'] * 100:.2f}\\%")
R("B06", "0.8", lambda: f(1)(P("post_hoc_rows", "q0_check_max_dev_deg")), "to 0.8^\\circ")
# ================================================================ B07 cut and windows
SL = lambda i: str(S("A301")["numbers"]["selection"][i][1])
R("B07", "293 to 202", lambda: f"{SL(0)} to {SL(1)}", "(293 to 202 sources)")
R("B07", "188", lambda: SL(2), "(188;")
R("B07", "122", lambda: SL(3), "(122)")
R("B07", "78", lambda: SL(4), "(78)")
R("B07", "70", lambda: SL(5), "(70)")
R("B07", "47", lambda: SL(6), "\\ge8 (47)")
R("B07", "47", lambda: SL(7), "finite inputs (47)")
for i, tmpl in enumerate(("W1 ({} galaxies", "W2 ({},", "W3 ({},")):
    R("B07", tmpl.format((16, 16, 15)[i]), (lambda i=i, tmpl=tmpl: tmpl.format(S("A301")["numbers"]["windows"][i]["n"])))
for i in range(3):
    w = lambda i=i: S("A301")["numbers"]["windows"][i]
    R("B07", ["0.0266--0.0476", "0.0506--0.0756", "0.0773--0.0930"][i], (lambda w=w: f"{w()['z_min']:.4f}--{w()['z_max']:.4f}"))
    R("B07", ["median 0.042", "median 0.067", "median 0.081"][i], (lambda w=w: f"median {w()['z_med']:.3f}"))
    R("B07", ["185 Mpc", "300 Mpc", "368 Mpc"][i], (lambda w=w: f"{w()['DL_med']:.0f} Mpc"))
R("B07", "0.70", lambda: rx("OA301", r"pooled: N 47; .*?gas fraction median (0\.70)"), "gas fraction is 0.70")
# ================================================================ B08 chain
R("B08", "0.506", lambda: rx("S301", r"D_HI = 10\^\((0\.506) log M_HI - 3\.293\)"), "=0.506\\log_{10}")
R("B08", "-3.293", lambda: "-" + rx("S301", r"D_HI = 10\^\(0\.506 log M_HI - (3\.293)\)"))
R("B08", "1.33", lambda: rx("FC301", r"M_gas = (1\.33) M_HI"), "M_b=1.33")
R("B08", "11", lambda: rx("FC301", r"knob δ = (11) km s⁻¹"), "\\delta=11 km")
LIT("B08", "scatter (0.06 dex)")
# ================================================================ B09 estimator
R("B09", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}", "s^*\\times9.3603\\times10^{-11}")
R("B09", "3\\times10^{-17}", lambda: f"{round(float(rx('OF309', r'\|d log10 a0\| = ([0-9.]+)e-17'))):d}\\times10^{{-17}}")
R("B09", "4{,}000", lambda: "{:,}".format(int(rx("FC301", r"bootstrap over galaxies \(B = (4),000\)") + "000")).replace(",", "{,}"))
# ================================================================ B10 recipe
R("B10", "\\delta=11", lambda: "\\delta=" + rx("FC301", r"knob δ = (11) km s⁻¹"), "\\delta=11 km s^{-1}; M_\\star")
R("B10", "0.25", lambda: rx("FC301", r"knob: ± (0\.25) dex on M\\\*"), "M_\\star\\pm0.25")
R("B10", "0.15", lambda: rx("FC301", r"knob ± (0\.15) dex\)"), "\\pm0.15 dex; and")
R("B10", "67.4", lambda: rx("FC301", r"H₀ = (67\.4) distance variant"), "to 67.4")
R("B10", "0.5", lambda: rx("FC301", r"y = g_bar/a₀ < (0\.5) at R"), "(y<0.5)")
# ================================================================ B11 calibration controls (k = 0, CFG309)
R("B11", "1.282", lambda: f(3)(SPARC() / A0C()), "=1.282")
R("B11", "1.449", lambda: f(3)(S("J281")["numbers"]["out"]["LC"]["s"]), "s^*=1.449")
R("B11", "1.440", lambda: f(3)(F("results", "W1", "s")), "W1 gives s^*=1.440")
R("B11", "+0.050", lambda: sg(3)(F("calibration", "offset_sparc")))
R("B11", "-0.003", lambda: sg(3)(F("calibration", "offset_281")))
R("B11", "0.135", lambda: f(3)(F("calibration", "w1_recipe_half")), "half-width 0.135")
R("B11", "9", lambda: rx("REF306", r"uses δ = (9) km s⁻¹"), "\\delta=9 km")
R("B11", "0.082", lambda: f(3)(dex(A0A(), A0C())), "the 0.082 dex between")
R("B11", "123", lambda: str(S("CC2")["numbers"]["n"]), "applied to 123 SPARC")
R("B11", "1.304", lambda: f(3)(S("CC2")["numbers"]["s"]))
R("B11", "+0.008", lambda: sg(3)(S("CC2")["numbers"]["offset_dex"]))
R("B11", "1.324", lambda: f(3)(S("CC2")["numbers"]["rhi_diag"]["s_measured_RHI"]))
R("B11", "-0.002", lambda: sg(3)(S("CC2")["numbers"]["rhi_diag"]["median_log_R_ratio"]))
R("B11", "+0.022", lambda: sg(3)(F("calibration", "drift")), "drift is +0.022")
R("B11", "0.141", lambda: f(3)(F("trend", "rho", "W3", "sd_stat")), "width of the drift is 0.141")
R("B11", "-0.013", lambda: sg(3)(S("SELF")["numbers"]["selftest"]["bias"]))
R("B11", "0.023", lambda: rx("FC301", r"stated bias \(CFG281: −(0\.023) dex\)"), "tolerance 0.023")
R("B11", "93 of 100", lambda: f"{S('SELF')['numbers']['selftest']['coverage']} of 100")
R("B11", "all four", lambda: "all four" if all(S("B301")["numbers"]["calibration"][k] for k in ("cc1", "cc2", "cc3", "cc4")) and
  all(F("calibration", k) for k in ("cc1", "cc2", "cc3", "cc4")) else "?", "all four also pass")
# ================================================================ B12 the width side on SPARC (CFG306 P6)
R("B12", "22", lambda: str(P6("P6_sparc_alfalfa", "n_sel")), "On 22 SPARC")
R("B12", "+0.026", lambda: sg(3)(P6("P6_sparc_alfalfa", "median_dlogV")), "by +0.026 dex")
R("B12", "+0.022 to +0.032", lambda: " to ".join(f"{v:+.3f}" for v in P6("P6_sparc_alfalfa", "dlogV_boot68")))
R("B12", "+0.10", lambda: sg(2)(4 * P6("P6_sparc_alfalfa", "median_dlogV")), "is +0.10 dex in a_0")
R("B12", "+0.184", lambda: sg(3)(P6("P6_sparc_alfalfa", "dlog_s_w50_minus_vflat")))
R("B12", "+0.071", lambda: sg(3)(P6("P6_sparc_alfalfa", "dlog_s_w50d11_minus_vflat")))
R("B12", "0.044", lambda: f(3)(-P("post_hoc_rows", "delta5", "dlog_vs_primary")), "by 0.044 dex")
R("B12", "4\\times0.026", lambda: f"4\\times{P6('P6_sparc_alfalfa', 'median_dlogV'):.3f}")
R("B12", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "all at y\\le0.084")
# ================================================================ B13 reactivity and reproduction
R("B13", "1.1892", lambda: rx("FC301", r"widths × (1\.1892)"))
R("B13", "+0.322", lambda: sg(3)(S("MU1")["numbers"]["response"]))
R("B13", "0.30\\pm0.05", lambda: PM(rx("FC301", r"must rise by (0\.30 ± 0\.05) dex")))
R("B13", "+0.392", lambda: sg(3)(S("MU2")["numbers"]["response"]))
R("B13", "0.37\\pm0.06", lambda: PM(rx("FC301", r"CFG281: \+(0\.37 ± 0\.06)")))
R("B13", "1.332408", lambda: f(6)(S("M5")["numbers"]["LU"]["mine"]))
R("B13", "1.449173", lambda: f(6)(S("M5")["numbers"]["LC"]["mine"]))
R("B13", "six", lambda: {6: "six"}.get(sum(int(v) for v in list(S("A301")["numbers"]["hand_estimates"].values()) + list(S("CC2")["numbers"]["hand_estimates"].values())
                                             + list(B("hand_estimates").values())), "?"), "All six frozen hand estimates hit")
R("B13", "2\\times10^{-16}", lambda: f"{round(abs(S('S309')['cons_dex']) / 1e-16):d}\\times10^{{-16}}" if S("S309")["id_max_diff"] == 0.0 else "?")
# ================================================================ B14 disclosures
R("B14", "8/3/2/2", lambda: "/".join(str(x) for x in S("A301")["numbers"]["matching"]["W1"]["win_counts"]))
R("B14", "9.605", lambda: f(3)(S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "(9.605)")
R("B14", "9.76", lambda: f(2)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2]), "W3's (9.76)")
R("B14", "0.155", lambda: f(3)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2] - S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "is 0.155 dex below")
# ================================================================ B15 results table (whole rows, k = 0)
for key in ("W1", "W2", "W3", "pooled"):
    R("B15", {"W1": "W1 & 16 & 0.042 & 185 & 1.440 & 1.348 & 1.254--1.597 & 1.093--2.317 & 0.135",
              "W2": "W2 & 16 & 0.067 & 300 & 1.394 & 1.305 & 1.233--1.506 & 1.038--1.696 & 0.136",
              "W3": "W3 & 15 & 0.081 & 368 & 1.513 & 1.416 & 1.130--1.965 & 0.655--1.967 & 0.132",
              "pooled": "pooled & 47 & --- & --- & 1.401 & 1.311 & 1.273--1.418 & 1.206--1.669 & 0.128"}[key], (lambda key=key: row15(key, key)))
R("B15", "9.3603\\times10^{-11}", lambda: f"{A0C() / 1e-11:.4f}\\times10^{{-11}}")
# ================================================================ B16 level
R("B16", "1.311\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B16", "1.401", lambda: f(3)(F("pooled", "s")), "s^*=1.401")
R("B16", "1.273--1.418", lambda: f"{q2a(F('pooled', 'q')[1])}--{q2a(F('pooled', 'q')[2])}")
R("B16", "1.206--1.669", lambda: f"{q2a(F('pooled', 'q')[0])}--{q2a(F('pooled', 'q')[3])}")
R("B16", "0.034", lambda: f(3)(F("pooled", "sd")), "deviation of 0.034 dex")
R("B16", "0.128", lambda: f(3)(HALF()), "half-width of 0.128")
R("B16", "+0.146", lambda: sg(3)(dex(POOL(), A0C())))
R("B16", "+0.064", lambda: sg(3)(dex(POOL(), A0A())))
R("B16", "+0.038", lambda: sg(3)(dex(POOL(), SPARC())))
R("B16", "0.08", lambda: f(2)(math.log10((1.20 + SPSYS()) / 1.20)), "own 0.08 dex systematic")
R("B16", "0.019", lambda: f(3)(dex(POOL(), A0C()) - HALF()), "outside by 0.019 dex")
R("B16", "0.261", lambda: f(3)(EC("H0=70", "per_gal_robust_sd")), "robust spread of 0.261 dex")
R("B16", "0.048", lambda: f(3)(EC("H0=70", "se_median")), "median of 0.048 dex")
R("B16", "1.057--1.626", lambda: f"{u10(EC('H0=70', 'se95_a0')[0])}--{u10(EC('H0=70', 'se95_a0')[1])}")
R("B16", "outside-outside-inside", lambda: "-".join(("inside" if EC("H0=70", k_) else "outside") for k_ in ("canonical_in_se95", "alt_in_boot95", "alt_in_se95")), "the alternative footing lies outside the bootstrap interval but inside the wider one")
R("B16", "inside-inside-inside", lambda: "-".join(("inside" if EC("H0=67.4", k_) else "outside") for k_ in ("canonical_in_recipe", "alt_in_boot95", "alt_in_se95")), "canonical footing is inside the recipe width and the alternative footing inside both statistical intervals")
RKF = lambda k: F("recipe", "pooled", "rows", k, "half")
R("B16", "0.098", lambda: f(3)(RKF("delta")), "0.098 (\\delta)")
R("B16", "0.069", lambda: f(3)(RKF("tau_ms")), "0.069 (M_\\star)")
R("B16", "0.026", lambda: f(3)(RKF("rdex")), "0.026 (D_{\\rm HI})")
R("B16", "0.036", lambda: f(3)(RKF("h0")), "0.036 dex (H_0)")
R("B16", "0.035", lambda: f(3)(RKF("sini")), "sensitivity is 0.035")
R("B16", "0.132", lambda: f(3)(F("pooled", "recipe_half_with_sin60")), "(0.132 with it")
R("B16", "0.028, 0.033 and 0.042", lambda: ", ".join(f"{v:.3f}" for v in F("pooled", "y_q")[:2]) + f" and {F('pooled', 'y_q')[2]:.3f}")
R("B16", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "maximum of 0.084")
R("B16", "1.046\\times10^{-10}", lambda: f"{u10(POOL1())}\\times10^{{-10}}")
R("B16", "-0.098", lambda: sg(3)(dex(POOL1(), POOL())), "(-0.098 dex)")
# ================================================================ B17 windows, drift, joint fit
R("B17", "1.348, 1.305 and 1.416", lambda: f"{u10(F('results', 'W1', 'a0'))}, {u10(F('results', 'W2', 'a0'))} and {u10(F('results', 'W3', 'a0'))}")
R("B17", "+0.05", lambda: sg(2)(F("trend", "slope")), "is +0.05 per dex")
R("B17", "-0.44 to +0.35", lambda: f"{F('trend', 'slope_q')[1]:+.2f} to {F('trend', 'slope_q')[2]:+.2f}")
R("B17", "-1.03 to +0.64", lambda: f"{F('trend', 'slope_q')[0]:+.2f} to {F('trend', 'slope_q')[3]:+.2f}")
R("B17", "1.051", lambda: f(3)(F("trend", "rho", "W3", "rho")))
R("B17", "+0.022\\pm0.141", lambda: f"{F('trend', 'rho', 'W3', 'log_rho'):+.3f}\\pm{F('trend', 'rho', 'W3', 'sd_stat'):.3f}")
R("B17", "+0.009", lambda: sg(3)(F("trend", "rival_lever_W1_W3")))
R("B17", "-2.6", lambda: sg(1)(JF("b_z")), "gives -2.6 per unit z")
R("B17", "-8.0 to +1.5", lambda: " to ".join(f"{v:+.1f}" for v in JF("b_z_95")))
R("B17", "-5.2 to -0.5", lambda: " to ".join(f"{v:+.1f}" for v in JF("b_z_68")), "(68\\% -5.2 to -0.5;")
R("B17", "+0.09", lambda: sg(2)(JF("b_mhi")), "and +0.09 per dex")
R("B17", "-0.23 to +0.49", lambda: " to ".join(f"{v:+.2f}" for v in JF("b_mhi_95")))
# ================================================================ B18 BTFR
BT = lambda k, *p: F("btfr", {"i": "(i) all survivors", "ii": "(ii) gas-dominated (M_gas > M*)"}[k], *p)
R("B18", "1.530\\times10^{-10}", lambda: f"{u10(BT('i', 'median'))}\\times10^{{-10}}")
R("B18", "1.460--1.725", lambda: f"{u10(BT('i', 'q')[1])}--{u10(BT('i', 'q')[2])}")
R("B18", "+0.213", lambda: sg(3)(BT("i", "dex_canonical")))
R("B18", "+0.131", lambda: sg(3)(BT("i", "dex_alt")))
R("B18", "0.111", lambda: f(3)(BT("i", "recipe_half")), "recipe 0.111")
R("B18", "1.464\\times10^{-10}", lambda: f"{u10(BT('ii', 'median'))}\\times10^{{-10}}")
R("B18", "1.457--1.530", lambda: f"{u10(BT('ii', 'q')[1])}--{u10(BT('ii', 'q')[2])}")
R("B18", "+0.194", lambda: sg(3)(BT("ii", "dex_canonical")))
R("B18", "+0.112", lambda: sg(3)(BT("ii", "dex_alt")))
R("B18", "0.120", lambda: f(3)(BT("ii", "recipe_half")), "recipe 0.120")
R("B18", "1.197", lambda: f(3)(BT("i", "kernel_factor", "s=1")))
R("B18", "+0.078", lambda: sg(3)(math.log10(BT("i", "kernel_factor", "s=1"))))
R("B18", "1.172", lambda: f(3)(BT("i", "kernel_factor", "s=1.282")))
R("B18", "1.183", lambda: f(3)(BT("ii", "kernel_factor", "s=1")))
R("B18", "-0.019", lambda: sg(3)(F("gas_minus_deep")))
R("B18", "3.43", lambda: f(2)(P("post_hoc_rows", "btfr_slope_k0", "inverse")), "47 is 3.43")
R("B18", "3.11--3.79", lambda: "--".join(f"{v:.2f}" for v in P("post_hoc_rows", "btfr_slope_k0", "inverse_68")))
LIT("B18", "against 3.66"); LIT("B18", "forward-equivalent 3.73")
R("B18", "1.526\\times10^{-10}", lambda: f"{u10(S('CC2')['numbers']['btfr_sparc']['median'])}\\times10^{{-10}}")
# ================================================================ B19 kappa (k = 0)
QP = lambda i: 10 ** F("pooled", "q")[i] * A0C()
R("B19", "0.700", lambda: kap(POOL(), A0C()), "\\kappa=0.700")
R("B19", "0.680--0.758", lambda: f"{kap(QP(1), A0C())}--{kap(QP(2), A0C())}")
R("B19", "0.644--0.892", lambda: f"{kap(QP(0), A0C())}--{kap(QP(3), A0C())}")
R("B19", "0.128", lambda: f(3)(HALF()), "10^{\\pm0.128}")
R("B19", "0.52--0.94", lambda: f"{kap(POOL() * 10 ** -HALF(), A0C(), 2)}--{kap(POOL() * 10 ** HALF(), A0C(), 2)}")
R("B19", "0.580", lambda: kap(POOL(), A0A()), "\\kappa=0.580")
R("B19", "0.563--0.627", lambda: f"{kap(QP(1), A0A())}--{kap(QP(2), A0A())}")
R("B19", "0.533--0.738", lambda: f"{kap(QP(0), A0A())}--{kap(QP(3), A0A())}")
R("B19", "0.43--0.78", lambda: f"{kap(POOL() * 10 ** -HALF(), A0A(), 2)}--{kap(POOL() * 10 ** HALF(), A0A(), 2)}")
H0A = lambda: 10 ** F("recipe", "pooled", "rows", "h0", "log_s")[0] * A0C()
R("B19", "1.208\\times10^{-10}", lambda: f"{u10(H0A())}\\times10^{{-10}}")
R("B19", "0.645", lambda: kap(H0A(), A0C()))
R("B19", "0.534", lambda: kap(H0A(), A0A()))
R("B19", "0.565--0.868", lambda: "--".join(f"{v:.3f}" for v in EC("H0=70", "kappa_canonical_se95")))
R("B19", "0.467--0.719", lambda: "--".join(f"{v:.3f}" for v in EC("H0=70", "kappa_alt_se95")))
R("B19", "0.594--0.823", lambda: "--".join(f"{v:.3f}" for v in EC("H0=67.4", "kappa_canonical_boot95")))
R("B19", "0.520--0.800", lambda: "--".join(f"{v:.3f}" for v in EC("H0=67.4", "kappa_canonical_se95")))
# ================================================================ B20 other determinations
R("B20", "+0.042", lambda: sg(3)(dex(POOL(), DESM())))
R("B20", "1.19", lambda: f"{DESM() / 1e-10:.2f}", "[D23] (1.19)")
R("B20", "-0.058", lambda: sg(3)(dex(POOL(), V26())))
R("B20", "1.50", lambda: f"{V26() / 1e-10:.2f}", "[V26] (1.50)")
R("B20", "1.31--1.80", lambda: rx("R279", r"sub-samples span (1\.31–1\.80)").replace("–", "--"))
R("B20", "1.69", lambda: rx("O279", r"COSMOS reference, Sersic N=19 (1\.69) \+-"), "gave 1.69")
LIT("B20", "at most 28 of V26's 130"); LIT("B20", "V25's 19 and 9"); LIT("B20", "smoothed 3\\sigma")
# ================================================================ B21 Figure 1 caption
R("B21", "1.05", lambda: u10(POOL1(), 2), "frame (1.05)")
R("B21", "1.07", lambda: u10(G3(SNRX), 2), "S\\!N_{\\rm 3D} (1.07)")
R("B21", "0.90--1.13", lambda: f"{u10(SD_('lo'), 2)}--{u10(SD_('hi'), 2)}", "its bar, 0.90--1.13")
R("B21", "+0.078", lambda: sg(3)(math.log10(BT("i", "kernel_factor", "s=1"))))
R("B21", "0.936", lambda: u10(A0C()), "canonical (0.936)")
R("B21", "1.131", lambda: u10(A0A()), "alternative (1.131)")
R("B21", "1.20", lambda: f"{SPARC() / 1e-10:.2f}", "g_\\dagger (1.20)")
R("B21", "1.50", lambda: f"{V26() / 1e-10:.2f}", "resolved fit (1.50)")
# ================================================================ B22 Figure 2 caption
R("B22", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "(filled, 37)")
R("B22", "10", lambda: str(S("A301")["numbers"]["N"] - S("A301")["numbers"]["pooled"]["n_gas_dom"]), "(open, 10)")
R("B22", "1.53\\times10^{-10}", lambda: f"{u10(BT('i', 'median'), 2)}\\times10^{{-10}}")
# ================================================================ B23 systematics table (relative to the k = 0 pooled a0)
GD = lambda lab: dex(G3(lab), POOL())
R("B23", "-0.115", lambda: sg(3)(P6("P3_flux_frame", f"{SNRX} | k=0", "R")), "(-0.115 dex)")
R("B23", "-0.089", lambda: sg(3)(GD(SNRX)), "& -0.089 &")
R("B23", "-0.159", lambda: sg(3)(P6("P3_flux_frame", f"{PAIR7} | k=0", "R")), "cut (-0.159)")
R("B23", "-0.087", lambda: sg(3)(P6("P3_flux_frame", f"{ZX} | k=0", "R")), "in z (-0.087)")
R("B23", "-0.132 / -0.064", lambda: f"{GD(PAIR7):+.3f} / {GD(ZX):+.3f}")
R("B23", "-0.195", lambda: sg(3)(J4("results", "cat", "C1", "OPT", "median")), "unadjusted (-0.195)")
R("B23", "-0.163", lambda: sg(3)(GD(C1R)), "& -0.163 &")
R("B23", "-0.098", lambda: sg(3)(dex(POOL1(), POOL())), "& -0.098 & CFG301")
R("B23", "-0.044 / -0.098", lambda: f"{P('post_hoc_rows', 'delta5', 'dlog_vs_primary'):+.3f} / {RF('delta'):+.3f}")
R("B23", "-0.001 / +0.063", lambda: f"{KD(KSIM):+.3f} / {KD(KSTD):+.3f}")
R("B23", "+0.058 / +0.067", lambda: f"{KD(KCF):+.3f} / {KD(KDEL):+.3f}")
R("B23", "+0.034 / +0.006 / +0.034", lambda: " / ".join(f"{SEL(k)['dlog_vs_primary']:+.3f}" for k in ("6", "10", "12")))
R("B23", "+0.084", lambda: sg(3)(SEL("0")["dlog_vs_primary"]), "(70 discs) & +0.084")
R("B23", "-0.025 / -0.073", lambda: f"{P('post_hoc_rows', 'h2_0.1', 'dlog_vs_primary'):+.3f} / {P('post_hoc_rows', 'h2_0.3', 'dlog_vs_primary'):+.3f}")
R("B23", "+0.029 / -0.050", lambda: f"{P('post_hoc_rows', 'q0_0.10', 'dlog_vs_primary'):+.3f} / {P('post_hoc_rows', 'q0_0.30', 'dlog_vs_primary'):+.3f}")
R("B23", "+0.035", lambda: sg(3)(RF("sini")), "& +0.035 & CFG309")
R("B23", "-0.076 / +0.063", lambda: f"{RF('tau_ms', 1):+.3f} / {RF('tau_ms', 0):+.3f}")
R("B23", "+0.021 / -0.030", lambda: f"{RF('rdex', 1):+.3f} / {RF('rdex', 0):+.3f}")
R("B23", "-0.001", lambda: sg(3)(P("post_hoc_rows", "size_rajohnson2022", "dlog_vs_primary")), "[R22] & -0.001")
R("B23", "-0.036", lambda: sg(3)(RF("h0")), "& -0.036 & CFG309")
R("B23", "1.311\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
# ================================================================ B24 velocity frame (CFG309)
T2 = lambda: S("W309")["numbers"]["T2"]
R("B24", "26.126", lambda: f(3)(T2()["channel_width_Hz"] / 1e3), "26.126 kHz")
R("B24", "+0.066 to +0.068", lambda: f"{min(r['dev']['REST'] for r in T2()['rows']) * 100:+.3f} to {max(r['dev']['REST'] for r in T2()['rows']) * 100:+.3f}")
R("B24", "1.4\\times10^{-5}", lambda: f"{T2()['spread'] / 1e-5:.1f}\\times10^{{-5}}")
R("B24", "Four", lambda: {4: "Four"}.get(T2()["link_counts"]["1"], "?"), "Four of the five")
R("B24", "237.858", lambda: f"{T2()['rows'][0]['X_kms']:.3f}")
R("B24", "223", lambda: f"{T2()['rows'][0]['W50_cat_compared']:.0f}", "223 catalogued")
R("B24", "0.012", lambda: f(3)(S("W309")["numbers"]["T3"]["median_x"]), "lever of 0.012")
R("B24", "-0.017", lambda: sg(3)(S("W309")["numbers"]["T4"]["primary"]["mR"]), "offset -0.017 dex")
R("B24", "13 of 20", lambda: f"{S('W309')['numbers']['T4']['INJ']['votes']['REST']['REST']} of 20")
R("B24", "-0.022", lambda: sg(3)(S("J302")["numbers"]["widths"]["median"]), "catalogue's to -0.022")
R("B24", "+0.002", lambda: sg(3)(S("J302")["numbers"]["widths"]["obsframe_median"]), "agree to +0.002")
R("B24", "+0.002", lambda: sg(3)(S("J302")["numbers"]["widths"]["obsframe_median"]), "raw widths (+0.002 against -0.022 dex)")
R("B24", "-0.012", lambda: sg(3)(S("VF306")["numbers"]["F3"]["code 1"]["expected_if_rest"]), "against -0.012 dex for the rest frame")
R("B24", "1.046\\times10^{-10}", lambda: f"{u10(POOL1())}\\times10^{{-10}}")
# ================================================================ B25 CFG302
N302 = lambda *p: dig(S("J302")["numbers"], p)
R("B25", "188", lambda: str(N302("counts", "n_sample")), "the 188 golden")
R("B25", "62.2--77.3", lambda: f"{N302('beam', 'min_valid'):.1f}--{N302('beam', 'max_valid'):.1f}")
R("B25", "75.9", lambda: f(1)(N302("beam", "median_valid")), "median 75.9")
R("B25", "74.7--77.3", lambda: f"{min(N302('beam', 'per_cube_median').values()):.1f}--{max(N302('beam', 'per_cube_median').values()):.1f}")
R("B25", "179", lambda: str(N302("counts", "n_primary")), "Of the 179")
R("B25", "58", lambda: str(N302("detection", "n_detected")), "58 reach")
R("B25", "-0.022", lambda: sg(3)(N302("widths", "median")))
R("B25", "0.039", lambda: f(3)(N302("widths", "robust_scatter")), "scatter of 0.039")
R("B25", "4 of 58", lambda: f"{N302('widths', 'n_pull_out')} of {N302('widths', 'n')}")
R("B25", "0.22", lambda: f(2)(N302("fluxes", "all_linear", "median")), "all 179 is 0.22")
R("B25", "-0.30", lambda: sg(2)(N302("fluxes", "detected_log", "median")), "is -0.30 dex")
R("B25", "0.50", lambda: f(2)(10 ** N302("fluxes", "detected_log", "median")), "a ratio of 0.50")
R("B25", "0.24", lambda: f(2)(N302("fluxes", "detected_log", "robust_scatter")), "scatter 0.24")
R("B25", "46 of 58", lambda: f"{N302('fluxes', 'n_pull_out')} of {N302('fluxes', 'detected_log', 'n')}")
R("B25", "1.002", lambda: f(3)(S("PH302")["numbers"]["PH4"]["median_ratio_to_1p5"]["2.5"]))
R("B25", "0.60\\pm0.05", lambda: f"{S('PH302')['numbers']['PH5']['line_mean']:.2f}\\pm" + rx("R302", r"holds \*\*0\.60 ± (0\.05)\*\*"))
R("B25", "0.489", lambda: f(3)(N302("C_OFF", "robust_std_win")))
R("B25", "45", lambda: str(P("post_hoc_rows", "cfg302_join", "n_primary")), "45 are in")
R("B25", "20", lambda: str(P("post_hoc_rows", "cfg302_join", "n_detected")), "and 20 reach")
R("B25", "-0.443", lambda: sg(3)(P("post_hoc_rows", "cfg302_join", "median_logratio_S_detected")))
R("B25", "-0.017", lambda: sg(3)(P("post_hoc_rows", "cfg302_join", "median_logratio_W50_detected")))
# ================================================================ B26 CFG304
RC = lambda: J4("results", "cat", "C1", "OPT", "median")
R("B26", "23", lambda: str(J4("results", "n_pairs")), "23 matches")
R("B26", "15", lambda: str(J4("results", "sets_n", "C1")), "15 of them")
R("B26", "0.275", lambda: f(3)(J4("shuffle", "mean")))
R("B26", "+0.000", lambda: sg(3)(J4("results", "w50", "C1", "median")))
R("B26", "-0.025 to 0.000", lambda: f"{J4('results', 'w50', 'C1', 'p16'):+.3f} to {J4('results', 'w50', 'C1', 'p84'):.3f}")
R("B26", "-0.012", lambda: sg(3)(S("VF306")["numbers"]["F3"]["code 1"]["expected_if_rest"]), "predicts -0.012 dex")
R("B26", "-0.195", lambda: sg(3)(RC()), "flux is -0.195")
R("B26", "-0.250 to -0.156", lambda: f"{J4('results', 'cat', 'C1', 'OPT', 'p16'):+.3f} to {J4('results', 'cat', 'C1', 'OPT', 'p84'):+.3f}")
R("B26", "0.64", lambda: f(2)(10 ** RC()), "about 0.64")
R("B26", "7", lambda: str(J4("results", "csets_n", "C1")), "for the 7 of them")
R("B26", "-0.308", lambda: sg(3)(J4("results", "cube", "C1", "OPT", "median")))
R("B26", "-0.175", lambda: sg(3)(J4("results", "decisions", "CLEAN_C1_OPT", "R_cat")))
R("B26", "-0.383", lambda: sg(3)(J4("results", "decisions", "CLEAN_C1_OPT", "R_cube")))
R("B26", "0.22", lambda: f(2)(-S("PH304")["numbers"]["PH4"]["C1"]["dlogM"][0]), "sit 0.22 dex below")
R("B26", "neither", lambda: J4("results", "decisions", "C1_OPT", "decision"), "``neither''")
# ================================================================ B27 how far the offset carries (CFG306 S1/S2/P6, CFG304 PH1)
FS = lambda *p: dig(S("FS306")["numbers"], p)
R("B27", "0.028", lambda: f(3)(FS("S1", "props", "z", "code1 15")[0]), "median z 0.028")
R("B27", "0.065", lambda: f(3)(FS("S1", "props", "z", "47")[0]), "(ours 0.065)")
R("B27", "18.7", lambda: f(1)(FS("S1", "props", "SNR_3D", "code1 15")[0]), "S\\!N_{\\rm 3D} 18.7")
R("B27", "12.4", lambda: f(1)(FS("S1", "props", "SNR_3D", "47")[0]), "(ours 12.4)")
R("B27", "66", lambda: f(0)(FS("S1", "props", "theta_HI arcsec", "code1 15")[0]), "diameter 66''")
R("B27", "40", lambda: f(0)(FS("S1", "props", "theta_HI arcsec", "47")[0]), "(ours 40'')")
R("B27", "30", lambda: f(0)(100 * FS("S1", "frac47_inside_pairs_range", "z")), "only 30\\% of")
R("B27", "7 of the 47", lambda: f"{FS('S1', 'n47_with_alfalfa_pair')} of the 47")
R("B27", "-0.62", lambda: sg(2)(FS("S2", "code 1 (15) | log SNR_3D", "rho")), "(Spearman -0.62")
R("B27", "0.01", lambda: f(2)(FS("S2", "code 1 (15) | log SNR_3D", "p")), "-0.62, p 0.01)")
R("B27", "-0.115", lambda: sg(3)(FS("S2", "code 1 (15) | extrapolated to the 47's median log SNR_3D", "at_median47")), "give -0.115 (in")
R("B27", "-0.087", lambda: sg(3)(FS("S2", "all 23 | extrapolated to the 47's median z", "at_median47")), "and -0.087 (in z, all 23 pairs)")
R("B27", "-0.137", lambda: sg(3)(S("PH304")["numbers"]["PH1"]["ALL"]["z_ge_002"][0]), "give -0.137 (19")
R("B27", "19", lambda: str(S("PH304")["numbers"]["PH1"]["ALL"]["z_ge_002"][1]), "(19 pairs)")
R("B27", "-0.120", lambda: sg(3)(S("PH304")["numbers"]["PH1"]["ALL_clean"]["z_ge_002"][0]), "and -0.120 (confusion-clean)")
R("B27", "+0.053", lambda: sg(3)(P6("P6_sparc_alfalfa", "median_dlogMHI_all")), "sit +0.053 dex above")
R("B27", "35", lambda: str(P6("P6_sparc_alfalfa", "n_matched")), "for 35 common")
R("B27", "0.25", lambda: f(2)(-RC() + P6("P6_sparc_alfalfa", "median_dlogMHI_all")), "about 0.25 dex below")
R("B27", "500", lambda: rx("REF306", r"would need about (500) times"), "about 500 times")
R("B27", "29", lambda: rx("REF306", r"MeerKAT's (29) m shortest baseline"), "29 m shortest")
R("B27", "25", lambda: rx("REF306", r"recovers scales of about (25)′"), "about 25'")
# ================================================================ B28 the flux scale and a0
R("B28", "0.90\\times10^{-10}", lambda: f"{u10(G3(C1R), 2)}\\times10^{{-10}}", "gives a_0=0.90\\times10^{-10}")
R("B28", "0.97", lambda: u10(G3(PAIR7), 2), "cut give 0.97")
R("B28", "1.02 and 1.06", lambda: f"{u10(G3(ZGE), 2)} and {u10(G3(ZCL), 2)}")
R("B28", "1.07", lambda: u10(G3(SNRX), 2), "S\\!N_{\\rm 3D} 1.07")
R("B28", "1.13", lambda: u10(G3(ZX), 2), "extrapolation 1.13")
R("B28", "0.90--1.13", lambda: f"{u10(SD_('lo'), 2)}--{u10(SD_('hi'), 2)}", "We take 0.90--1.13")
R("B28", "0.481", lambda: kap(G3(C1R), A0C()), "0.90 \\kappa is 0.481")
R("B28", "0.398", lambda: kap(G3(C1R), A0A()), "or 0.398")
R("B28", "-0.016", lambda: sg(3)(SD_("lo_vs_canonical")), "canonical footing -0.016 dex")
R("B28", "-0.099", lambda: sg(3)(SD_("lo_vs_alt")), "alternative -0.099 dex")
R("B28", "0.571", lambda: kap(G3(SNRX), A0C()), "is 0.571")
R("B28", "0.472", lambda: kap(G3(SNRX), A0A()), "or 0.472, with")
R("B28", "inside", lambda: "inside" if max(abs(SD_(k_)) for k_ in ("lo_vs_canonical", "lo_vs_alt", "hi_vs_canonical", "hi_vs_alt")) <= HALF() else "outside", "both footings are inside the recipe width")
R("B28", "+0.058", lambda: sg(3)(dex(G3(SNRX), A0C())), "canonical footing +0.058 dex")
R("B28", "-0.025", lambda: sg(3)(dex(G3(SNRX), A0A())), "alternative -0.025 dex")
R("B28", "0.60--0.75", lambda: f"{u10(J4('cfg301', 'A', 'central', 'a0'), 2)}--{u10(P6('P3_flux_frame', C1R + ' | k=1', 'a0_gas'), 2)}")
R("B28", "0.9", lambda: f(1)(SD_("lo") / 1e-10), "about 0.9 to 1.31\\times10^{-10}")
R("B28", "1.31", lambda: u10(POOL(), 2), "0.9 to 1.31\\times10^{-10}")
# ================================================================ B29 kernel
R("B29", "-0.001", lambda: sg(3)(KD(KSIM)), "agree (-0.001")
R("B29", "+0.06 to +0.07", lambda: f"{min(KUP()):+.2f} to {max(KUP()):+.2f}")
R("B29", "1.50", lambda: u10(K2(KCF), 2), "to 1.50 with")
R("B29", "1.22", lambda: u10(K2(KCF, "a0_k1"), 2), "(1.22 in")
R("B29", "0.082", lambda: f(3)(dex(A0A(), A0C())), "the 0.082 dex")
R("B29", "+0.001 and +0.032", lambda: (lambda v: f"{min(v):+.3f} and {max(v):+.3f}")([r["mightee_minus_cc2_k0"] for r in P6("P2_kernels", "rows").values()]))
R("B29", "1.50 against 1.86", lambda: f"{V26() / 1e-10:.2f} against " + rx("O279", r"a0 = (1\.86) \+- 0\.06 \(delta"))
# ================================================================ B30 width, inclination, M*, H2, size
R("B30", "0.098", lambda: f(3)(-RF("delta")), "by 0.098 dex,")
R("B30", "+0.029 or -0.050", lambda: f"{P('post_hoc_rows', 'q0_0.10', 'dlog_vs_primary'):+.3f} or {P('post_hoc_rows', 'q0_0.30', 'dlog_vs_primary'):+.3f}")
R("B30", "+0.035", lambda: sg(3)(RF("sini")), "by +0.035 dex")
R("B30", "-0.08", lambda: sg(2)(COR("incl_deg")["rho"]), "(Spearman -0.08)")
R("B30", "+0.09", lambda: sg(2)(COR("axis_ratio")["rho"]), "ratio (+0.09)")
R("B30", "-0.076 / +0.063", lambda: f"{RF('tau_ms', 1):+.3f} / {RF('tau_ms', 0):+.3f}")
R("B30", "0.025 or 0.073", lambda: f"{-P('post_hoc_rows', 'h2_0.1', 'dlog_vs_primary'):.3f} or {-P('post_hoc_rows', 'h2_0.3', 'dlog_vs_primary'):.3f}")
R("B30", "0.026", lambda: f(3)(RKF("rdex")), "by 0.026 dex (half-width)")
R("B30", "-0.001", lambda: sg(3)(P("post_hoc_rows", "size_rajohnson2022", "dlog_vs_primary")), "[R22] by -0.001")
R("B30", "0.008", lambda: f(3)(-P("post_hoc_rows", "size_rajohnson2022", "dlogD_at_median")), "smaller by 0.008")
R("B30", "9.73", lambda: f(2)(P("post_hoc_rows", "size_rajohnson2022", "median_logMHI")), "=9.73")
# ================================================================ B31 selection
R("B31", "23 of 70", lambda: f"{SEL('removed_by_8')['n']} of {SEL('0')['n']}")
R("B31", "2.23\\times10^{-10}", lambda: f"{u10(SEL('removed_by_8')['a0'], 2)}\\times10^{{-10}}")
R("B31", "1.59\\times10^{-10}", lambda: f"{u10(SEL('0')['a0'], 2)}\\times10^{{-10}}")
R("B31", "+0.084", lambda: sg(3)(SEL("0")["dlog_vs_primary"]), "(+0.084 dex")
R("B31", "1.72 and 1.23", lambda: f"{u10(P6('P4_selection', '23 removed by SNR_3D >= 8', 'a0'), 2)} and {u10(P6('P4_selection', '70 (before SNR cut)', 'a0'), 2)}")
R("B31", "-0.009 to +0.034", lambda: (lambda v: f"{min(v):+.3f} to {max(v):+.3f}")([SEL(k)["dlog_vs_primary"] for k in ("6", "7", "9", "10", "12")]))
R("B31", "-0.50", lambda: sg(2)(P6("P4_selection", "snr_fit_70", "coef_logW50")), "W_{50}^{-0.50}")
R("B31", "+0.63", lambda: sg(2)(COR("W50")["rho"]), "(Spearman +0.63)")
R("B31", "-0.45", lambda: sg(2)(COR("gas_fraction")["rho"]), "(-0.45, p")
R("B31", "0.002", lambda: f(3)(COR("gas_fraction")["p"]), "p 0.002)")
R("B31", "+0.36", lambda: sg(2)(COR("log_Mstar")["rho"]), "(+0.36, p")
R("B31", "0.01", lambda: f(2)(COR("log_Mstar")["p"]), "+0.36, p 0.01)")
R("B31", "-0.11", lambda: sg(2)(COR("z")["rho"]), "z (-0.11)")
R("B31", "+0.04", lambda: sg(2)(COR("log_MHI")["rho"]), "M_{\\rm HI} (+0.04)")
R("B31", "-11.4\\pm1.3", lambda: (lambda m: f"{float(m.group(1)):.1f}\\pm{float(m.group(2)):.1f}")(re.search(r"bTFR direct\s+a1 =\s+(-[0-9.]+) \+- ([0-9.]+)", S("O279"))))
R("B31", "-8.1\\pm2.4", lambda: (lambda m: f"{float(m.group(1)):.1f}\\pm{float(m.group(2)):.1f}")(re.search(r"bTFR inverse\s+a1 =\s+(-[0-9.]+) \+- ([0-9.]+)", S("O279"))))
# ================================================================ B32 distances
R("B32", "0.036", lambda: f(3)(RKF("h0")), "by 0.036")
R("B32", "1.208\\times10^{-10}", lambda: f"{u10(H0A())}\\times10^{{-10}}")
R("B32", "1.290", lambda: f(3)(10 ** F("recipe", "pooled", "rows", "h0", "log_s")[0]), "s^*=1.290")
R("B32", "+0.111", lambda: sg(3)(EC("H0=67.4", "dex_canonical")), "is +0.111 dex away")
R("B32", "0.128", lambda: f(3)(EC("H0=67.4", "recipe_half_with_h0")), "is kept (0.128 dex)")
R("B32", "0.123", lambda: f(3)(EC("H0=67.4", "recipe_half")), "correction (0.123 dex)")
R("B32", "inside", lambda: "inside" if EC("H0=67.4", "canonical_in_recipe") and EC("H0=67.4", "canonical_in_recipe_with_h0") else "outside", "inside the recipe width whether")
R("B32", "+0.028", lambda: sg(3)(EC("H0=67.4", "dex_alt")), "is +0.028 dex away")
R("B32", "1.112--1.540", lambda: f"{u10(EC('H0=67.4', 'boot95_a0')[0])}--{u10(EC('H0=67.4', 'boot95_a0')[1])}")
R("B32", "0.974--1.498", lambda: f"{u10(EC('H0=67.4', 'se95_a0')[0])}--{u10(EC('H0=67.4', 'se95_a0')[1])}")
R("B32", "outside", lambda: "outside" if not (EC("H0=67.4", "canonical_in_boot95") or EC("H0=67.4", "canonical_in_se95")) else "inside", "the canonical footing stays outside both statistical intervals")
# ================================================================ B33 matching and N
R("B33", "0.155", lambda: f(3)(S("A301")["numbers"]["windows"][2]["lmhi_q"][2] - S("A301")["numbers"]["windows"][0]["lmhi_q"][2]), "is 0.155 dex lower")
R("B33", "15--16", lambda: f"{min(w['n'] for w in S('A301')['numbers']['windows'])}--{max(w['n'] for w in S('A301')['numbers']['windows'])}", "With 15--16 galaxies")
# ================================================================ B34 what it can say
R("B34", "1.311\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B34", "1.208\\times10^{-10}", lambda: f"{u10(H0A())}\\times10^{{-10}}")
R("B34", "0.90--1.13", lambda: f"{u10(SD_('lo'), 2)}--{u10(SD_('hi'), 2)}", "and 0.90--1.13\\times10^{-10}")
R("B34", "+0.111", lambda: sg(3)(EC("H0=67.4", "dex_canonical")), "(+0.111 dex)")
R("B34", "+0.038", lambda: sg(3)(dex(POOL(), SPARC())), "SPARC (+0.038 dex)")
R("B34", "+0.064", lambda: sg(3)(dex(POOL(), A0A())), "footing (+0.064 dex")
R("B34", "0.128", lambda: f(3)(HALF()), "half-width of 0.128")
R("B34", "+0.146", lambda: sg(3)(dex(POOL(), A0C())), "(+0.146 dex)")
R("B34", "0.082", lambda: f(3)(dex(A0A(), A0C())), "differ by 0.082")
R("B34", "-0.06 to -0.16", lambda: (lambda v: f"{max(v):+.2f} to {min(v):+.2f}")([GD(l) for l in FLUXLABS]))
R("B34", "-0.10", lambda: sg(2)(RF("delta")), "up to -0.10 dex")
R("B34", "+0.07", lambda: sg(2)(max(KUP())), "up to +0.07 dex")
R("B34", "0.009", lambda: f(3)(F("trend", "rival_lever_W1_W3")), "constant by 0.009")
R("B34", "0.141", lambda: f(3)(F("trend", "rho", "W3", "sd_stat")), "width of 0.141")
# ================================================================ B35 conclusions
R("B35", "0.084", lambda: rx("R301", r"a maximum of (0\.084)"), "y\\le0.084")
R("B35", "37", lambda: str(S("A301")["numbers"]["pooled"]["n_gas_dom"]), "37 of them")
R("B35", "1.311\\times10^{-10}", lambda: f"{u10(POOL())}\\times10^{{-10}}")
R("B35", "0.034", lambda: f(3)(F("pooled", "sd")), "statistical \\pm0.034")
R("B35", "0.128", lambda: f(3)(HALF()), "recipe \\pm0.128")
R("B35", "0.70", lambda: kap(POOL(), A0C(), 2), "\\kappa=0.70")
R("B35", "0.58", lambda: kap(POOL(), A0A(), 2), "or 0.58")
R("B35", "0.048", lambda: f(3)(EC("H0=70", "se_median")), "\\pm0.048 dex from")
R("B35", "1.208\\times10^{-10}", lambda: f"{u10(H0A())}\\times10^{{-10}}")
R("B35", "0.90--1.13", lambda: f"{u10(SD_('lo'), 2)}--{u10(SD_('hi'), 2)}", "in 0.90--1.13\\times10^{-10}")
R("B35", "0.084", lambda: f(3)(SEL("0")["dlog_vs_primary"]), "by 0.084 dex")
R("B35", "0.10", lambda: f(2)(-RF("delta")), "by up to 0.10 dex")
R("B35", "0.06--0.07", lambda: f"{min(KUP()):.2f}--{max(KUP()):.2f}", "by 0.06--0.07 dex")
# ================================================================ B36 data availability (commits, provenance, the catalogue's bytes)
for h in ("2555ab142", "6b10c01c0", "7d317dd4f", "a89ba33b9", "336b36f8f", "34e40dac6", "45c41e887", "ec54de4ac", "53f8fa937", "19adffd49"):
    R("B36", h, (lambda h=h: commit_exists(h)))
R("B36", "eb247d5de07eb30e", lambda: rx("DATA", r"sha256 prefix (eb247d5de07eb30e)"))
R("B36", "75,999", lambda: "{:,}".format(len(raw("CSV"))), "(75,999 bytes")
R("B36", "bcf9e8558bc5644805b9acb288372c17daffac76d8be6c89d7db9843af9fbf23", lambda: hashlib.sha256(raw("CSV")).hexdigest())
R("B36", "10.48479/jkc0-g916", lambda: rx("DATA", r"SARAO DOI (10\.48479/jkc0-g916)"))


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


def pdf_text():
    """The built PDF's text (pdftotext), with the typographic minus normalised; None if it cannot be read."""
    r = subprocess.run(["pdftotext", "-raw", PDF, "-"], capture_output=True)
    if r.returncode != 0:
        return None
    return re.sub(r"\s+", " ", r.stdout.decode("utf-8").replace("\u2212", "-"))


PLAIN = re.compile(r"^[+-]?\d+(\.\d+)?$")
MUTATE_KEY = ("B01", "1.31\\times10^{-10}")


def run(mode=None):
    p40 = S("P40")
    if not p40.get("reproduction_ok"):
        raise SystemExit("PAPER40_figures_numbers.json: the reproduction gate did not pass -- re-run make_paper40_figures.py")
    blocks = tex_blocks(open(TEX, encoding="utf-8").read())
    ptxt = pdf_text()
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
            exp = exp.replace("1.31", "1.32"); label += "  (MUTATED expected value)"
        if i == mi and mode == "tex":
            lit = lit.replace("1.31", "1.32"); label += "  (MUTATED tex literal)"
        src_ok = (got == exp) if kind == "src" else True
        tex_ok = lit in blocks.get(b, "")
        pdf_ok = None
        if PLAIN.match(expected):
            sign, num = (expected[0], expected[1:]) if expected[0] in "+-" else ("", expected)
            pat = r"(?<![\d.])" + (re.escape(sign) + r"\s?" if sign else "") + re.escape(num) + r"(?![\d])"
            pdf_ok = bool(ptxt) and re.search(pat, ptxt) is not None
        results.append((label, kind, got, src_ok, tex_ok, pdf_ok, lit))
    orphan = sorted(set(blocks) - used)
    missing = sorted(used - set(blocks))
    return results, orphan, missing


if __name__ == "__main__":
    mode = "value" if "--mutate" in sys.argv else "tex" if "--mutate-tex" in sys.argv else None
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()
    print(f"PAPER40 v1.2 audit against committed files at HEAD {head} (paper's own numbers: PAPER40_figures_numbers.json, working tree)"
          + (f"   [MUTATE: {mode}]" if mode else ""))
    results, orphan, missing = run(mode)
    bad = {"src": 0, "lit": 0}; n = {"src": 0, "lit": 0}; npdf = bpdf = 0
    for label, kind, got, s_ok, t_ok, p_ok, lit in results:
        ok = s_ok and t_ok
        n[kind] += 1; bad[kind] += (not ok)
        if p_ok is not None:
            npdf += 1; bpdf += (not p_ok)
        if not ok or p_ok is False or "-v" in sys.argv:
            why = ("source gives %r" % got if not s_ok else "") + ("; not printed in its tex block as %r" % lit if not t_ok else "") \
                  + ("; not in the PDF text" if p_ok is False else "")
            print(f"  [{'ok ' if ok and p_ok is not False else 'BAD'}] {label:60s} {why}")
    if orphan:
        print("  note: tex blocks with no audit rows:", ", ".join(orphan))
    if missing:
        print("  BAD: audit rows name blocks absent from the tex:", ", ".join(missing))
        bad["src"] += len(missing)
    print(f"\n{n['src'] - bad['src']} of {n['src']} quoted values match their committed sources and their tex blocks")
    print(f"{n['lit'] - bad['lit']} of {n['lit']} literature values (LIT; arXiv abstracts and the V26 e-print, not in a committed file) are printed in their blocks")
    print(f"{npdf - bpdf} of {npdf} plain-number rows are present in the text of the built PDF")
    tot = bad["src"] + bad["lit"] + bpdf
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if tot else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if tot else 0)
