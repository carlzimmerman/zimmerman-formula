#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG306 (PAPER40 referee): independent trace of quoted numbers to their source files, and the list of numbers no script checks.

For each traced number: the value is re-derived here from the committed source (git HEAD; own code, not the audit's getters) or from this
lane's own recomputation (cfg306_physics_checks_results.json, which re-implements the chain), formatted as the paper prints it, and looked for
in the tex.  number_trace.csv records: id, tex block (the % AUDIT tag whose block holds it), the quoted literal, the source, the derivation,
the re-derived literal, match, whether PAPER40_audit.py carries a row for it, and a note.
Then every numeric token in every audited block that is NOT inside an audit literal of that block is listed (uncovered_numbers.csv).
"""
import os, re, json, csv, math, subprocess, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
PAP = "qwen_claude_field_theory/papers_2026/"
L1, L2, L4 = (CFG.split(REPO + "/")[1] + "/" + x + "/" for x in ("CFG301_mightee_hi_catalogue_width_chain", "CFG302_mightee_cube_raw_widths", "CFG304_mightee_flux_scale_alfalfa"))


def show(p):
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + p], capture_output=True)
    assert r.returncode == 0, p
    return r.stdout.decode()


J = lambda p: json.loads(show(p))["numbers"] if "numbers" in json.loads(show(p)) else json.loads(show(p))
A1, B1, CC2, SELF, M5, MU1, MU2 = (J(L1 + f) for f in ("cfg301_stageA_results.json", "cfg301_stageB_results.json", "cfg301_CC2_results.json", "cfg301_SELFTEST_results.json",
                                                      "cfg301_M5_results.json", "cfg301_stageB_MUTATE1_results.json", "cfg301_stageB_MUTATE2_results.json"))
W2 = J(L2 + "cfg302_raw_widths_results.json"); PH2 = J(L2 + "cfg302_posthoc_diagnostics_results.json")
F4 = J(L4 + "cfg304_flux_scale_alfalfa_results.json"); PH4 = J(L4 + "cfg304_posthoc_results.json")
P40 = json.loads(show(PAP + "PAPER40_figures_numbers.json"))
OWN = json.load(open(os.path.join(HERE, "cfg306_physics_checks_results.json")))["numbers"]
tex = show(PAP + "PAPER40_meerkat_a0_2026.tex")
A0C, A0A = 9.360324825027975e-11, 1.1312035414413022e-10
FP0 = json.loads(show("real_research/derivation_chain_2026/FP0_core_postulates_results.json"))["numbers"]

# audit module (rows only; its __main__ is not run)
os.environ["PAPER40_REPO"] = REPO
spec = importlib.util.spec_from_file_location("p40audit", os.path.join(REPO, PAP, "PAPER40_audit.py"))
AU = importlib.util.module_from_spec(spec); spec.loader.exec_module(AU)
blocks = AU.tex_blocks(tex)
audit_lits = {}
for (b, e, g, t, k) in AU.ROWS:
    audit_lits.setdefault(b, []).extend([AU.norm_tex(e), AU.norm_tex(t) if t else AU.norm_tex(e)])

f3 = lambda v: f"{v:.3f}"; s3 = lambda v: f"{v:+.3f}"; dex = lambda a, b: math.log10(a / b)
la = lambda ls: 10 ** ls * A0C / 1e-10
rows = []


def T(id_, lit, val, src, how, note=""):
    nl = AU.norm_tex(lit)
    blks = [b for b, txt in blocks.items() if nl in txt]
    covered = any(nl in L for b in blks for L in audit_lits.get(b, []))
    rows.append(dict(id=id_, blocks="+".join(blks) or "NOT FOUND", quoted=lit, source=src, derivation=how, rederived=val, match=(val == lit) and bool(blks),
                     audit_row=covered, note=note))


Bp = B1["pooled"]
T("N01", "1.046", f"{Bp['a0'] / 1e-10:.3f}", L1 + "cfg301_stageB_results.json", "pooled.a0 / 1e-10")
T("N02", "1.117", f3(Bp["s"]), L1 + "cfg301_stageB_results.json", "pooled.s")
T("N03", "1.012--1.145", f"{la(Bp['q'][1]):.3f}--{la(Bp['q'][2]):.3f}", L1 + "cfg301_stageB_results.json", "10^pooled.q[16,84] x a0_canonical")
T("N04", "0.936--1.311", f"{la(Bp['q'][0]):.3f}--{la(Bp['q'][3]):.3f}", L1 + "cfg301_stageB_results.json", "10^pooled.q[2.5,97.5] x a0_canonical")
T("N05", "0.143", f3(Bp["recipe_half"]), L1 + "cfg301_stageB_results.json", "pooled.recipe_half")
T("N06", "+0.048", s3(dex(Bp["a0"], FP0["a0_canonical"])), "FP0 + CFG301", "log10(a0/a0_canonical)")
T("N07", "-0.034", s3(dex(Bp["a0"], FP0["a0_rho_total"])), "FP0 + CFG301", "log10(a0/a0_alt)")
T("N08", "-0.060", s3(dex(Bp["a0"], 1.20e-10)), "CFG301", "log10(a0/1.20e-10)")
T("N09", "\\kappa=0.559", f"\\kappa={0.5 * Bp['a0'] / A0C:.3f}", "CFG301 + FP0", "a0/(2 a0_canonical)")
T("N10", "\\kappa=0.462", f"\\kappa={0.5 * Bp['a0'] / A0A:.3f}", "CFG301 + FP0", "a0/(2 a0_alt)")
for i, (s_, a_) in enumerate((("1.233", "1.154"), ("1.089", "1.019"), ("1.081", "1.012"))):
    r = B1["results"][f"W{i + 1}"]
    T(f"N1{i + 1}", f"{s_} & {a_}", f"{r['s']:.3f} & {r['a0'] / 1e-10:.3f}", L1 + "cfg301_stageB_results.json", f"results.W{i + 1}.s, .a0")
sel = A1["selection"]
T("N14", "293 to 202", f"{sel[0][1]} to {sel[1][1]}", L1 + "cfg301_stageA_results.json", "selection[0..1]; re-derived by my own cut in cfg306_physics_checks (P0)")
T("N15", "(122)", f"({sel[3][1]})", L1 + "cfg301_stageA_results.json", "selection[3]")
yq = OWN["P0_reproduction"]["y_quartiles"]
T("N16", "0.028, 0.033 and 0.042", f"{yq[0]:.3f}, {yq[1]:.3f} and {yq[2]:.3f}", "CFG306 own chain (P0)", "quartiles of g_bar/a0 at R over the 47")
T("N17", "0.084", f"{OWN['P0_reproduction']['y_max']:.3f}", "CFG306 own chain (P0)", "max y")
gf = [w["gas_frac_med"] for w in A1["windows"]]
T("N18", "0.70", "0.70", L1 + "README.md / stage A", "median gas fraction (README; window medians " + ", ".join(f"{x:.3f}" for x in gf) + ")", "pooled value is in the README only; not a JSON field")
bt = B1["btfr"]
T("N19", "1.251\\times10^{-10}", f"{bt['(i) all survivors']['median'] / 1e-10:.3f}\\times10^{{-10}}", L1 + "cfg301_stageB_results.json", "btfr.(i).median; own P1 k=1 BTFR "
  + f"{OWN['P1_frame']['k1']['btfr_median']:.4e}")
T("N20", "1.187\\times10^{-10}", f"{bt['(ii) gas-dominated (M_gas > M*)']['median'] / 1e-10:.3f}\\times10^{{-10}}", L1 + "cfg301_stageB_results.json", "btfr.(ii).median")
T("N21", "1.197", f"{bt['(i) all survivors']['kernel_factor']['s=1']:.3f}", L1 + "cfg301_stageB_results.json", "btfr.(i).kernel_factor.s=1; own P2 exp kernel "
  + f"{OWN['P2_kernels']['rows']['exp (nu_mono, MLS16; PAPER40 primary)']['kernel_factor_median']:.3f}")
T("N22", "s^*=1.304", f"s^*={CC2['s']:.3f}", L1 + "cfg301_CC2_results.json", "s; own re-run in P2 " + f"{OWN['P2_kernels']['cc2_check']['s']:.4f}")
T("N23", "+0.008", s3(CC2["offset_dex"]), L1 + "cfg301_CC2_results.json", "offset_dex")
T("N24", "1.324", f"{CC2['rhi_diag']['s_measured_RHI']:.3f}", L1 + "cfg301_CC2_results.json", "rhi_diag.s_measured_RHI")
T("N25", "-0.013", s3(SELF["selftest"]["bias"]), L1 + "cfg301_SELFTEST_results.json", "selftest.bias")
T("N26", "93 of 100", f"{SELF['selftest']['coverage']} of 100", L1 + "cfg301_SELFTEST_results.json", "selftest.coverage")
T("N27", "+0.322", s3(MU1["response"]), L1 + "cfg301_stageB_MUTATE1_results.json", "response")
T("N28", "+0.392", s3(MU2["response"]), L1 + "cfg301_stageB_MUTATE2_results.json", "response")
rr = B1["recipe"]["pooled"]["rows"]
T("N29", "0.106", f3(abs(rr["delta"]["log_s"][0] - Bp["log_s"])), L1 + "cfg301_stageB_results.json", "|recipe.rows.delta - pooled|")
T("N30", "0.036", f3(abs(rr["h0"]["log_s"][0] - Bp["log_s"])), L1 + "cfg301_stageB_results.json", "|recipe.rows.h0 - pooled|")
T("N31", "9.62\\times10^{-11}", f"{10 ** rr['h0']['log_s'][0] * A0C / 1e-11:.2f}\\times10^{{-11}}", L1 + "cfg301_stageB_results.json", "10^recipe.rows.h0 x a0")
T("N32", "-0.20", f"{B1['trend']['slope']:+.2f}", L1 + "cfg301_stageB_results.json", "trend.slope")
T("N33", "0.009", f3(B1["trend"]["rival_lever_W1_W3"]), L1 + "cfg301_stageB_results.json", "trend.rival_lever_W1_W3")
T("N34", "-0.022", s3(W2["widths"]["median"]), L2 + "cfg302_raw_widths_results.json", "widths.median")
T("N35", "0.039", f3(W2["widths"]["robust_scatter"]), L2 + "cfg302_raw_widths_results.json", "widths.robust_scatter")
T("N36", "4 of 58", f"{W2['widths']['n_pull_out']} of {W2['widths']['n']}", L2 + "cfg302_raw_widths_results.json", "widths.n_pull_out / n")
T("N37", "0.22", f"{W2['fluxes']['all_linear']['median']:.2f}", L2 + "cfg302_raw_widths_results.json", "fluxes.all_linear.median")
T("N38", "0.489", f3(W2["C_OFF"]["robust_std_win"]), L2 + "cfg302_raw_widths_results.json", "C_OFF.robust_std_win")
T("N39", "74.2--77.3", f"{min(W2['beam']['per_cube_median'].values()):.1f}--{max(W2['beam']['per_cube_median'].values()):.1f}", L2 + "cfg302_raw_widths_results.json",
  "beam.per_cube_median min-max", "the per-cube MEDIAN beams; the per-channel valid range in the same JSON is " + f"{W2['beam']['min_valid']:.1f}-{W2['beam']['max_valid']:.1f}")
T("N40", "-0.443", s3(P40["post_hoc_rows"]["cfg302_join"]["median_logratio_S_detected"]), PAP + "PAPER40_figures_numbers.json", "post_hoc_rows.cfg302_join")
C1 = F4["results"]["cat"]["C1"]["OPT"]
T("N41", "-0.195", s3(C1["median"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "results.cat.C1.OPT.median")
T("N42", "-0.250 to -0.156", f"{C1['p16']:+.3f} to {C1['p84']:+.3f}", L4 + "cfg304_flux_scale_alfalfa_results.json", "p16, p84")
T("N43", "-0.308", s3(F4["results"]["cube"]["C1"]["OPT"]["median"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "results.cube.C1.OPT.median")
T("N44", "-0.175", s3(F4["results"]["cat"]["CLEAN_C1"]["OPT"]["median"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "results.cat.CLEAN_C1")
T("N45", "-0.383", s3(F4["results"]["cube"]["CLEAN_C1"]["OPT"]["median"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "results.cube.CLEAN_C1", "N = 3 cube pairs")
T("N46", "+0.000", s3(F4["results"]["w50"]["C1"]["median"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "results.w50.C1.median",
  "median sits on an exact tie (3 of 23 pairs have identical integer W50); mean " + f"{F4['results']['w50']['C1']['mean']:+.3f}; 68% {F4['results']['w50']['C1']['p16']:+.3f} to {F4['results']['w50']['C1']['p84']:+.3f}")
T("N47", "0.275", f3(F4["shuffle"]["mean"]), L4 + "cfg304_flux_scale_alfalfa_results.json", "shuffle.mean")
T("N48", "5.97\\times10^{-11}", f"{F4['cfg301']['A']['central']['a0'] / 1e-11:.2f}\\times10^{{-11}}", L4 + "cfg304_flux_scale_alfalfa_results.json", "cfg301.A.central.a0")
T("N49", "4.98--6.76", f"{F4['cfg301']['A']['hi']['a0'] / 1e-11:.2f}--{F4['cfg301']['A']['lo']['a0'] / 1e-11:.2f}", L4 + "cfg304_flux_scale_alfalfa_results.json", "cfg301.A.hi/lo",
  "CFG304's README prints 4.99 (a README rounding slip; JSON 4.985)")
T("N50", "7.50\\times10^{-11}", f"{OWN['P3_flux_frame']['C1 code-1 (CFG304 primary) | k=1']['a0_gas'] / 1e-11:.2f}\\times10^{{-11}}", "CFG306 own chain (P3)", "gas-only shift by -R_cat, R follows")
T("N51", "6.06\\times10^{-11}", f"{OWN['P3_flux_frame']['C1 code-1 (CFG304 primary) | k=1']['a0_all'] / 1e-11:.2f}\\times10^{{-11}}", "CFG306 own chain (P3)", "all-baryon shift at fixed R")
T("N52", "1.31\\times10^{-10}", f"{OWN['P1_frame']['k0']['a0'] / 1e-10:.2f}\\times10^{{-10}}", "CFG306 own chain (P1)", "k = 0 pooled a0")
T("N53", "+0.098", s3(math.log10(OWN["P1_frame"]["k0"]["a0"] / OWN["P1_frame"]["k1"]["a0"])), "CFG306 own chain (P1)", "log10(a0 k=0 / a0 k=1)")
T("N54", "-0.137", s3(float(re.search(r"'z_ge_002': \[(-0\.\d+), 19\]", str(PH4["PH1"]["ALL"]) if isinstance(PH4["PH1"], dict) else str(PH4["PH1"])).group(1))), L4 + "cfg304_posthoc_results.json", "PH1.ALL.z_ge_002 (N 19)")
T("N55", "-0.157", s3(dex(Bp["a0"], 1.50e-10)), "CFG301 + V26 abstract", "log10(a0/1.50e-10)")
T("N56", "-0.056", s3(dex(Bp["a0"], 1.19e-10)), "CFG301 + D23 abstract", "log10(a0/1.19e-10)")
T("N57", "0.514 and 0.425", f"{0.5 * 10 ** rr['h0']['log_s'][0]:.3f} and {0.5 * 10 ** rr['h0']['log_s'][0] * A0C / A0A:.3f}", L1 + "cfg301_stageB_results.json", "kappa at H0 = 67.4")
T("N58", "0.32--0.40", f"{0.5 * OWN['P3_flux_frame']['C1 code-1 (CFG304 primary) | k=1']['a0_all'] / A0C:.2f}--{0.5 * OWN['P3_flux_frame']['C1 code-1 (CFG304 primary) | k=1']['a0_gas'] / A0C:.2f}",
  "CFG306 own chain (P3)", "kappa_rhoL on the single-dish scale (all-baryon to gas-only R follows)", "lower end uses CFG304's interpolated 5.97 in the paper (0.319); exact re-run 6.06 gives 0.32")
T("N59", "0.60", f"{F4['cfg301']['A']['central']['a0'] / 1e-10:.2f}", L4 + "cfg304_flux_scale_alfalfa_results.json", "Fig. 1 caption (A, 0.60)")
T("N60", "1.50\\pm0.05", "1.50\\pm0.05", "V26 arXiv:2608.03576 abstract + main.tex l.540", "verbatim", "V25 (19 galaxies) gives 1.69 +- 0.13 (V26 main.tex l.543); the delta-family fit gives 1.86 +- 0.06 (l.631)")

with open(os.path.join(HERE, "number_trace.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
nm = sum(r["match"] for r in rows); na = sum(r["audit_row"] for r in rows)
print(f"traced {len(rows)} numbers: {nm} match (value and printed), {len(rows) - nm} do not; {na} also carried by a PAPER40_audit.py row")
for r in rows:
    if not r["match"]:
        print("  MISMATCH", r["id"], r["quoted"], "->", r["rederived"], r["blocks"])

# uncovered numeric tokens per block
unc = []
numre = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\w])")
for b, txt in blocks.items():
    t = txt
    for L in sorted(set(audit_lits.get(b, [])), key=len, reverse=True):
        if L:
            t = t.replace(L, " ")
    t = re.sub(r"\\(begin|end)\{[^}]*\}|\\label\{[^}]*\}|\\ref\{[^}]*\}|\\includegraphics\[[^]]*\]\{[^}]*\}|\\fpath\{[^}]*\}|\[[A-Z]+\d*(, [A-Z]+\d*)*\]", " ", t)
    t = re.sub(r"10\^\{-?\d+\}|\^\{?-?\d\}?|_\{?\d\}?|\\tfrac12|\\frac\{[^}]*\}\{[^}]*\}", " ", t)
    toks = [m.group(0) for m in numre.finditer(t)]
    toks = [x for x in toks if not re.fullmatch(r"[-+]?[0-9]", x)]
    for x in toks:
        unc.append(dict(block=b, token=x))
with open(os.path.join(HERE, "uncovered_numbers.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["block", "token"]); w.writeheader(); [w.writerow(r) for r in unc]
print(f"numeric tokens (two or more characters) in audited blocks not inside any audit literal of their block: {len(unc)}")
bybl = {}
for r in unc:
    bybl.setdefault(r["block"], []).append(r["token"])
for b in sorted(bybl):
    print(f"  {b}: {' '.join(bybl[b])}")
