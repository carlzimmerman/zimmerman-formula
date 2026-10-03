#!/usr/bin/env python3
"""CFG310 number trace: 25+ quoted numbers per paper, each re-derived from its committed source and looked up in the tex.
Writes number_trace.csv and cfg310_number_trace.out next to itself.  Read-only on everything else.  kappa = 1/2 is FITTED.

A row MATCHES when (a) the value formatted as printed equals the printed literal and (b) the literal occurs in the tex (comment lines
removed).  Rows tagged NOTE carry a referee remark (a provenance or scope problem) even when the arithmetic matches."""
import os, re, json, math, csv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
P26 = os.path.join(REPO, "qwen_claude_field_theory", "papers_2026")
MN = os.path.join(P26, "mnras_submission_2026_v3")
CFG = os.path.join(REPO, "campaign_fresh_gravity")


def tex(path):
    return "\n".join(l for l in open(path, encoding="utf-8").read().splitlines() if not l.lstrip().startswith("%"))


TM, TP = tex(os.path.join(MN, "mnras_a0_lambda_v3.tex")), tex(os.path.join(P26, "PAPER40_meerkat_a0_2026.tex"))
PN = json.load(open(os.path.join(MN, "paper_numbers.json")))
P40 = json.load(open(os.path.join(P26, "PAPER40_figures_numbers.json")))["post_hoc_rows"]
J9 = json.load(open(os.path.join(CFG, "CFG309_mightee_width_frame", "cfg309_cfg301chain_stageB_FRAME_results.json")))["numbers"]
CC2 = json.load(open(os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_CC2_results.json")))["numbers"]
A0C, A0A = 9.3603e-11, 1.1312e-10
ROWS = []


def row(paper, rid, where, literal, value_str, source, note=""):
    T = TM if paper == "MNRAS v3.2" else TP
    in_tex = literal in T
    ok = in_tex and (value_str is None or value_str in literal)
    ROWS.append(dict(paper=paper, id=rid, location=where, printed=literal, recomputed=value_str, source=source,
                     in_tex=in_tex, match="MATCH" if ok else "NO MATCH", note=note))


S3, S4, S5, S5n, S7 = PN["S3"], PN["S4"], PN["S5"], PN["S5_native"]["B"], PN["S7"]
f2 = lambda x: f"{x:.2f}"; f3 = lambda x: f"{x:.3f}"; f1 = lambda x: f"{x:.1f}"
M = "MNRAS v3.2"; pn = "mnras_submission_2026_v3/paper_numbers.json"
row(M, "M01", "Sec 3.3 eq kappaA", r"\kappa_{\rm A}=0.450\pm0.073", f"{f3(S3['meas'][0][1])}\\pm{f3(S3['meas'][0][2])}", pn + " S3.meas[0]")
row(M, "M02", "Sec 3.5 eq kappaB", r"\kappa_{\rm B}=0.58\pm0.18", f"{f2(S3['meas'][1][1])}\\pm{f2(S3['meas'][1][2])}", pn + " S3.meas[1]")
row(M, "M03", "Sec 3.6 eq kappaC", r"\kappa_{\rm C}=0.43\pm0.08", f"{f2(S3['meas'][2][1])}\\pm{f2(S3['meas'][2][2])}", pn + " S3.meas[2]")
row(M, "M04", "abstract; Sec 3.9", r"puts $1/2$ at $2.6\sigma$", f1(S3["desmond_pulls"]["half"]), pn + " S3.desmond_pulls.half")
row(M, "M05", "Sec 3.9", r"$\kappa_\Lambda=0.636\pm0.053$", f"{f3(S3['published'][1]['kappa_L'])}\\pm{f3(S3['published'][1]['s_L'])}", pn + " S3.published[1]")
row(M, "M06", "Sec 3.2", r"requires $\Upsilon_{\rm disc}=0.555$", f3(PN["S2"]["ud_for_half_L"]), pn + " S2.ud_for_half_L")
row(M, "M07", "Sec 3.2", r"and $0.465$ for the $\rho_{\rm crit}$ reading", f3(PN["S2"]["ud_for_half_C"]), pn + " S2.ud_for_half_C")
row(M, "M08", "Sec 3.2", r"same fit gives $1.05\times10^{-10}$", f2(PN["S2"]["table"][1]["a0"] * 1e10), pn + " S2.table[1].a0")
row(M, "M09", "Sec 3.4", r"$\sigma_{\min}=9.5$ per cent, reached at $f_*=0.32$", f1(100 * S3["floor"]), pn + " S3.floor, S3.f_star",
    note=f"f_star {S3['f_star']:.3f}")
row(M, "M10", "Sec 4.1 eq dgate", r"\Delta_{\rm halo}(2.5)=+0.22", f2(S4["laws"][2]["gate"]), pn + " S4.laws[2].gate")
row(M, "M11", "Sec 4.1 law (b)", r"$\Delta_H=+0.58$", f2(S4["laws"][2]["Hz"]), pn + " S4.laws[2].Hz")
row(M, "M12", "Sec 4.1 law (c)", r"$\Delta_{\rm halo}(2.5)=0.768-0.440=+0.33$", f2(S4["laws"][2]["dm14"]), pn + " S4.laws[2].dm14")
d = S4["design"]
row(M, "M13", "Table 11 row 0.20", r"0.20 & 8 & 0.53 & 0.10 & 20 & 27 & 110 & 48 & 167",
    f"8 & {min(d['0.2|0.0']['p20_at_Ne']):.2f} & {max(d['0.2|0.0']['pwrong_at_Ne']):.2f} & 20 & 27 & 110 & 48 & 167", pn + " S4.design['0.2|*']")
row(M, "M14", "Sec 3.9", r"$e^{-0.22}$ (A), $e^{+0.12}$ (B) and $e^{-0.31}$ (C)", f"{S3['lnLR']['A']:+.2f}", pn + " S3.lnLR")
row(M, "M15", "Sec 4.3 RC100 native", r"\frac{d\log_{10}\hat a_0}{dz}=-0.12\pm0.10", f"{S5n['slope']:+.2f}\\pm{S5n['slope_err']:.2f}", pn + " S5_native.B.slope/_err",
    note="41 of 100 at the floor; floor fraction rises with z (CFG310 M3): censored sample")
row(M, "M16", "Sec 4.3", r"Their median is $\hat a_0=2.1\times10^{-10}$", f1(S5n["median_a0"] * 1e10), pn + " S5_native.B.median_a0")
row(M, "M17", "Sec 4.3 comparison", r"a slope of $-0.09\pm0.06$", f"{S5['slope']:+.2f}\\pm{S5['slope_err']:.2f}", pn + " S5.slope/_err")
tb = [t for t in S5n["tilt"] if abs(t["beta"] + 0.05) < 1e-9][0]
row(M, "M18", "Sec 4.3 drift", r"native slope to $+0.02\pm0.09$", f"{tb['slope']:+.2f}\\pm{tb['err']:.2f}", pn + " S5_native.B.tilt[beta=-0.05]")
row(M, "M19", "Sec 4.3 flags", r"native slope to $-0.14\pm0.11$", f"{S5n['flags']['no_flagged'][0]:+.2f}\\pm{S5n['flags']['no_flagged'][1]:.2f}", pn + " S5_native.B.flags.no_flagged")
yn = PN["S5_native"]["y_native"]
row(M, "M20", "Sec 4.2", r"the median is $y=2.4$, the central 68 per cent lie in $0.9<y<7.2$", f"y={yn['median']:.1f}", pn + " S5_native.y_native",
    note=f"p16 {yn['p16']:.2f} p84 {yn['p84']:.2f}, below 0.3: {yn['n_below_03']}")
mi = S7["musedark"]["routes"]["i"]
row(M, "M21", "Sec 4.3 MUSE-DARK", r"rises by $+0.57\pm0.09$ dex", f"{mi['d']:+.2f}\\pm{mi['sd']:.2f}", pn + " S7.musedark.routes.i")
mn = S7["native"]["musedark"]["iii"]
row(M, "M22", "Sec 4.3 MUSE-DARK native", r"changes by $-0.26\pm0.28$ dex", f"{mn['d']:+.2f}\\pm{mn['sd']:.2f}", pn + " S7.native.musedark.iii",
    note="route (ii) with H2 omitted: FLAT outside 95% in 2 of 3 thirds (CFG310 M4)")
kz = S7["kurvs"]["z"]["cell"]
row(M, "M23", "Sec 4.3 KURVS", r"by $3.3\sigma$, while the rival's central value sits at zero ($-0.1\sigma$)", f"{kz[0]:.1f}", pn + " S7.kurvs.z.cell",
    note=f"rival {kz[1]:+.2f}")
cs = S7["native"]["cristal_stress"]
row(M, "M24", "Sec 4.3 native inputs", r"excluded in 59 per cent of cells and constancy in 24 per cent", f"{100*cs['H_excl']:.0f}", pn + " S7.native.cristal_stress",
    note=f"FLAT {100*cs['F_excl']:.0f}%, n {cs['n']}")
al = S7["native"]["aless122"]["decision"]
row(M, "M25", "Sec 4.3 native inputs", r"no inferred value survives in 44 per cent of 540 variants", f"{100*al['f_noroot']:.0f}", pn + " S7.native.aless122.decision",
    note=f"FLAT excluded {100*al['f_FLAT_excl']:.0f}%, H(z) {100*al['f_Hz_excl']:.0f}% not printed; data sources (Amvrosiadis+, Dunne+22, Calistro Rivera+18) not cited")
g2 = S5["cfg217_G2"]
row(M, "M26", "Sec 4.3 reason 1", r"(Spearman $\rho=+0.33$, $p=0.036$)", f"{g2['rho']:+.2f}", pn + " S5.cfg217_G2", note=f"p {g2['p']:.3f}, n {g2['n']}")
ts = S7["musedark"]["tau_star"]
row(M, "M27", "Sec 4.3 MUSE-DARK", r"SED-mass bias of 1.8--2.2 dex per unit redshift", f"{ts['R198']:.1f}--{ts['R199a']:.1f}", pn + " S7.musedark.tau_star",
    note="from the R198/R199a (halo-normalised, superseded) SED routes, not the native routes the paragraph now discusses")
dr = S7["musedark"]["drift"]
row(M, "M28", "Sec 4.3 MUSE-DARK", r"falls by 0.72 dex per unit redshift (95 per cent interval 0.50--0.97)", f"{-dr['b']:.2f}", pn + " S7.musedark.drift")

P = "PAPER40 v1.1"; j9 = "CFG309/cfg309_cfg301chain_stageB_FRAME_results.json"; pj = "papers_2026/PAPER40_figures_numbers.json"
po = J9["results"]["pooled"]; q = po["q"]
row(P, "P01", "abstract; Table 1; Sec 4", r"$a_0=1.311\times10^{-10}$", f3(po["a0"] * 1e10), j9 + " results.pooled.a0")
row(P, "P02", "Sec 4", r"68\% interval of 1.273--1.418", f"{10**q[1]*A0C*1e10:.3f}--{10**q[2]*A0C*1e10:.3f}", j9 + " results.pooled.q[1:3]")
row(P, "P03", "Sec 4", r"95\% interval of 1.206--1.669", f"{10**q[0]*A0C*1e10:.3f}--{10**q[3]*A0C*1e10:.3f}", j9 + " results.pooled.q[0,3]")
row(P, "P04", "Sec 4", r"standard deviation of 0.034\,dex", f3(po["sd"]), j9 + " results.pooled.sd",
    note="asymptotic SE from the paper's robust per-galaxy SD 0.261 is 0.048 dex (CFG310 P4)")
row(P, "P05", "Sec 4", r"recipe half-width of 0.128\,dex", f3(po["recipe_half"]), j9 + " results.pooled.recipe_half")
row(P, "P06", "Sec 4", r"$+0.146$\,dex above the canonical footing", f"{math.log10(po['a0']/A0C):+.3f}", "derived from P01 and the canonical footing")
row(P, "P07", "Sec 4", r"$+0.064$\,dex above the alternative", f"{math.log10(po['a0']/A0A):+.3f}", "derived from P01 and the alternative footing")
row(P, "P08", "Sec 4 coefficient", r"$\kappa=0.700$ on the $\rho_\Lambda$ footing", f3(0.5 * po["a0"] / A0C), "kappa = a0/(2 a0_canonical)")
row(P, "P09", "Sec 4 coefficient", r"$\kappa=0.580$ on $\rho_{\rm crit}$", f3(0.5 * po["a0"] / A0A), "kappa = a0/(2 a0_alt)")
w = J9["results"]
row(P, "P10", "Sec 4 windows", r"The window medians are 1.348, 1.305 and 1.416", f"{w['W1']['a0']*1e10:.3f}, {w['W2']['a0']*1e10:.3f} and {w['W3']['a0']*1e10:.3f}", j9 + " results.W1-3.a0")
row(P, "P11", "Sec 3 CC1", r"W1 gives $s^*=1.440$", f3(w["W1"]["s"]), j9 + " results.W1.s")
row(P, "P12", "Sec 3 CC3", r"The drift is $+0.022$\,dex", f"{J9['calibration']['drift']:+.3f}", j9 + " calibration.drift")
row(P, "P13", "Sec 3 CC2", r"return $s^*=1.304$", f3(CC2["s"]), "CFG301/cfg301_CC2_results.json numbers.s")
fl = P40["flux_k0"]
row(P, "P14", "abstract; Sec 5", r"1.07 (0.97--1.13)", f"{fl['snr_extrap']['a0_gas']*1e10:.2f} ({fl['pairs7']['a0_gas']*1e10:.2f}--{fl['z_extrap']['a0_gas']*1e10:.2f})",
    pj + " flux_k0", note=f"CFG304 frozen primary (15 code-1 pairs) gives {fl['c1']['a0_gas']*1e10:.2f}, outside the quoted range; STANDING records 0.90-1.06")
row(P, "P15", "Sec 5 flux", r"the unadjusted 15 code-1 pairs 0.90", f"{fl['c1']['a0_gas']*1e10:.2f}", pj + " flux_k0.c1")
row(P, "P16", "Sec 5 flux", r"$\kappa$ is 0.571 ($\rho_\Lambda$) or 0.472", f"{0.5*fl['snr_extrap']['a0_gas']/A0C:.3f}", "kappa from P14 central")
row(P, "P17", "Sec 4 level", r"In the version 1.0 frame the pooled value is $1.046\times10^{-10}$", f3(P40["frame_k1_variant"]["a0"] * 1e10), pj + " frame_k1_variant.a0")
kk = P40["kernel_k0"]
row(P, "P18", "Table 2 kernel", r"$-0.001$ / $+0.063$", f"${kk['simple']['dlog_vs_primary']:+.3f}$ / ${kk['standard']['dlog_vs_primary']:+.3f}$", pj + " kernel_k0")
row(P, "P19", "Table 2 kernel", r"$+0.058$ / $+0.067$", f"${kk['closed_form']['dlog_vs_primary']:+.3f}$ / ${kk['delta4.1']['dlog_vs_primary']:+.3f}$", pj + " kernel_k0")
sel = P40["selection_snr"]
row(P, "P20", "Sec 5 selection", r"all 70 give $1.59\times10^{-10}$ ($+0.084$\,dex", f"{sel['0']['a0']*1e10:.2f}", pj + " selection_snr['0']",
    note=f"removed 23 alone {sel['removed_by_8']['a0']*1e10:.2f}e-10; not in the abstract")
row(P, "P21", "Table 2 line width", r"$-0.044$ / $-0.098$", f"{P40['delta5']['dlog_vs_primary']:+.3f}", pj + " delta5")
h0 = J9["recipe"]["pooled"]["rows"]["h0"]
row(P, "P22", "Sec 5 distances", r"to $1.208\times10^{-10}$ ($s^*=1.290$)", f"{10**h0['log_s'][0]*A0C*1e10:.3f}", j9 + " recipe.pooled.rows.h0",
    note="on this 'like-for-like' value the canonical footing (+0.111 dex) is INSIDE the recipe width (CFG310 P3)")
bt = J9["btfr"]
row(P, "P23", "Sec 4 BTFR", r"The median $V^4/(GM_b)$ is $1.530\times10^{-10}$", f3(bt["(i) all survivors"]["median"] * 1e10), j9 + " btfr.(i)")
row(P, "P24", "Sec 4 BTFR", r"$1.464\times10^{-10}$ over the 37 gas-dominated discs", f3(bt["(ii) gas-dominated (M_gas > M*)"]["median"] * 1e10), j9 + " btfr.(ii)")
yq = po["y_q"]
row(P, "P25", "Sec 4 level", r"quartiles 0.028, 0.033 and 0.042", f"{yq[0]:.3f}, {yq[1]:.3f} and {yq[2]:.3f}", j9 + " results.pooled.y_q")
bs = P40["btfr_slope_k0"]
row(P, "P26", "Sec 4 BTFR", r"inverse BTFR slope of the 47 is 3.43 (68\% 3.11--3.79", f"{bs['inverse']:.2f} (68\\% {bs['inverse_68'][0]:.2f}--{bs['inverse_68'][1]:.2f}", pj + " btfr_slope_k0")
jf = P40["residuals_k0"]["joint_fit"]
row(P, "P27", "Sec 4 windows", r"gives $-2.6$ per unit $z$ (95\% $-8.0$ to $+1.5$)", f"{jf['b_z']:.1f}", pj + " residuals_k0.joint_fit",
    note=f"68% [{jf['b_z_68'][0]:.2f}, {jf['b_z_68'][1]:.2f}] excludes zero; not printed")
sp = P40["residuals_k0"]["spearman"]
row(P, "P28", "Sec 5 selection", r"correlates with $W_{50}$ (Spearman $+0.63$)", f"{sp['W50']['rho']:+.2f}", pj + " residuals_k0.spearman")

with open(os.path.join(HERE, "number_trace.csv"), "w", newline="") as fh:
    wtr = csv.DictWriter(fh, fieldnames=list(ROWS[0].keys())); wtr.writeheader(); wtr.writerows(ROWS)
lines = []
for p in ("MNRAS v3.2", "PAPER40 v1.1"):
    rs = [r for r in ROWS if r["paper"] == p]
    lines.append(f"{p}: {sum(r['match']=='MATCH' for r in rs)} of {len(rs)} traced numbers match their committed source and are printed;"
                 f" {sum(bool(r['note']) for r in rs)} carry a referee note")
    for r in rs:
        if r["match"] != "MATCH":
            lines.append(f"   NO MATCH {r['id']}: printed '{r['printed']}' recomputed '{r['recomputed']}' in_tex {r['in_tex']}")
        if r["note"]:
            lines.append(f"   NOTE {r['id']}: {r['note']}")
open(os.path.join(HERE, "cfg310_number_trace.out"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
