#!/usr/bin/env python3
"""PAPER66 tables, generated from the committed AC1 results and the seals. Run: python3 PAPER66_build_tables.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
D = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions", "ac1_results.json"))); A, B = D["A"], D["B"]
CA, AL = "canon 9.36e-11", "alt 1.13e-10"
f2 = lambda x: "FLOOR" if x is None else f"{x:.2f}"
out = []
def table(cap, lab, cols, rows):
    out.append("\\begin{table}[h]\\centering\\small\\caption{" + cap + "}\\label{" + lab + "}\\begin{tabular}{" + cols + "}\\toprule")
    out.extend(rows); out.append("\\bottomrule\\end{tabular}\\end{table}")
# T2
rows = ["case & $V_c$ & $n{=}1$ F-DESI & $n{=}1$ F-flat & $\\nu_{\\rm mono}$ F-DESI & $n{=}2$ F-DESI & $n{=}1$ R-H & route N \\\\ \\midrule"]
for cs, V in A["cases"].items():
    r = A["req"][cs]; g = lambda k, m: f"{f2(r[k][CA + '|' + m]['logMgas_Rg=Rd'])} / {f2(r[k][AL + '|' + m]['logMgas_Rg=Rd'])}"
    N = r["route N (added after criteria, information)"]["12.5"]
    rows.append(f"{cs.replace('/0.72', '$/0.72$')} & {V:.0f} & {g('n=1', 'F-DESI')} & {g('n=1', 'F-flat')} & {g('nu_mono', 'F-DESI')} & {g('n=2', 'F-DESI')} & {g('n=1', 'R-H')} & {f2(N)} \\\\")
table("U4\\_27928: required total $\\log M_{\\rm gas}$ at the sealed $R=8.27$\\,kpc, $R_g=R_d$, canonical / alt, at the H$\\alpha$ speed. FLOOR: the stars alone already exceed the requirement. Route N: lg $M_{200}$ 12.5, added after the criteria, information only.", "t:u4a", "lrcccccc", rows)
# T3
rows = ["lg $M_\\star$, shape, $\\alpha_{\\rm CO}$ & Newton & $n{=}1$ F-flat & $n{=}1$ F-DESI & $n{=}1$ R-H & route N 12.5 \\\\ \\midrule"]
for lms in (11.31, 11.11):
    for sh in ("S1", "S2"):
        for a in (4.36, 1.0):
            d = B["forward"][f"lgM*{lms}|{sh}|alpha{a}"]; t = lambda k: "/".join(f"{d[k][i]:.0f}" for i in (1, 2, 3))
            rows.append(f"{lms}, {sh}, {a:g} & {t('Newton')} & {t('n=1|' + CA + '|F-flat')} & {t('n=1|' + CA + '|F-DESI')} & {t('n=1|' + CA + '|R-H')} & {t('route N|12.5')} \\\\")
table("U4\\_28473: predicted $V_c$ in km\\,s$^{-1}$ at $R=2/3/4$\\,kpc from the published CO flux, canonical footing. S1: stellar $R_e$ 1.37\\,kpc; S2: 3.16\\,kpc. Gas $R_e$ 1.56\\,kpc.", "t:fw", "lccccc", rows)
# T4
rows = ["$V_c$ & \\multicolumn{3}{c}{lg $M_\\star$ 11.31, S2} & \\multicolumn{3}{c}{lg $M_\\star$ 11.11, S2} & \\multicolumn{3}{c}{lg $M_\\star$ 11.11, S1} \\\\ & flat & F-DESI & R-H & flat & F-DESI & R-H & flat & F-DESI & R-H \\\\ \\midrule"]
for V in (350, 400, 450, 500, 550, 600):
    c = []
    for b in ("lgM*11.31|S2", "lgM*11.11|S2", "lgM*11.11|S1"):
        for m in ("F-flat", "F-DESI", "R-H"):
            x = B["inverse"][b][f"3|{V}"][f"n=1|{CA}|{m}"]["alpha"]; c.append("F" if x is None else f"{x:.2f}")
    rows.append(f"{V} & " + " & ".join(c) + " \\\\")
table("U4\\_28473: $\\alpha_{\\rm CO,req}$ at $R=3$\\,kpc for a measured $V_c$, $n=1$, canonical. F = FLOOR, stars alone exceed the requirement. The primary statistic of the scoring plan.", "t:inv", "lccccccccc", rows)
# T5
d = B["forward"]["lgM*11.11|S2|alpha1.0"]; rows = ["reading & canonical & alt \\\\ \\midrule", f"Newton & \\multicolumn{{2}}{{c}}{{{d['Newton'][2]:.0f}}} \\\\"]
for kn, lb in (("n=1", "$n=1$"), ("nu_mono", "$\\nu_{\\rm mono}$"), ("n=2", "$n=2$")):
    for m, ml in (("F-flat", "flat"), ("F-DESI", "F-DESI"), ("band low 0.325", "band 0.325"), ("band high 1.212", "band 1.212"), ("R-H", "R-H"), ("L-fb(RAR-eq)", "L-fb")):
        if kn != "n=1" and m not in ("F-flat", "F-DESI"): continue
        rows.append(f"{lb}, {ml} & {d[f'{kn}|{CA}|{m}'][2]:.0f} & {d[f'{kn}|{AL}|{m}'][2]:.0f} \\\\")
for l in ("12.0", "12.5", "13.0"): rows.append(f"route N, lg $M_{{200}}$ {l} & \\multicolumn{{2}}{{c}}{{{d['route N|' + l][2]:.0f}}} \\\\")
table("U4\\_28473: $V_c(3\\,{\\rm kpc})$ in km\\,s$^{-1}$ for one input branch (lg $M_\\star$ 11.11, S2, $\\alpha_{\\rm CO}=1$), every reading.", "t:read", "lcc", rows)
# T6 GS4
N1 = json.load(open(os.path.join(ROOT, "argon_push", "AG4e_n1_alma_seal", "SEALED_N1.json")))["GS4_24110"]; V3 = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "S3_v3_mw_seals", "SEALED_V3_ALMA_AQUAL.json")))["GS4_24110"]
C5 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]
rows = ["lg $M_\\star$ & model & $\\nu_{\\rm mono}$ & $n=1$ & v3 AQUAL disc \\\\ \\midrule"]
for lm in ("10.89", "10.76"):
    for m in ("F-DESI", "F-flat", "R-H"):
        g = lambda S: f"{f2(S[lm][CA + '|' + m]['logMgas_Rg=Rd'])} / {f2(S[lm][AL + '|' + m]['logMgas_Rg=Rd'])}"
        rows.append(f"{lm} & {m} & {g(C5)} & {g(N1)} & {g(V3)} \\\\")
table("GS4\\_24110 (public 2026-11-28), sealed before this note, unchanged: required $\\log M_{\\rm gas}$ at $R_e$, $V_c$ 206\\,km\\,s$^{-1}$, $R_g=R_d$, canonical / alt.", "t:gs4", "llccc", rows)
open(os.path.join(HERE, "PAPER66_tables.tex"), "w").write("\n".join(out) + "\n")
