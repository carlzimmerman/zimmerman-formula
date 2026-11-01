#!/usr/bin/env python3
"""ER1 read, FROZEN_CRITERIA.md. eps FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "er1_results.json"))); O3 = json.load(open(os.path.join(H, "..", "OP3_contraction_on_native", "op3_results.json")))["runs"]; A, B = "A_c2b_refit", "B_cfg886_bg"; OUT = []
def P(s): print(s); OUT.append(s)
F = [0, .1, .2, .3, .4, .5, .6, .7, .872, 1.0]; BN = list(R["f0"]["bins3"])
def line(r): return all(r["sparc"][t]["line"] for t in (A, B))
P("Part 1, f grid: f U_A/U_B rms tilt | U by bin")
for f in F:
    r = R[f"f{f}"]; P(f"  {f:5} {r['sparc'][A]['U_median']:.2f}/{r['sparc'][B]['U_median']:.2f} {r['sparc'][A]['rms']:.4f} {r['tilt']:+.2f} | " + " ".join(f"{r['bins3'][b]['U']:.2f}" for b in BN) + " | dV " + " ".join(f"{r['bins3'][b]['dV']:+.0f}" for b in BN))
def freq(b, U):
    u = [R[f"f{f}"]["bins3"][b]["U"] for f in F]; 
    if u[0] < U: return None
    for i in range(len(F) - 1, -1, -1):
        if u[i] >= U:
            if i == len(F) - 1: return 1.0
            return F[i] + (u[i] - U) / (u[i] - u[i + 1]) * (F[i + 1] - F[i])
E = R["f0"]["er1E"]; TF = F; ER = {}
for U in (0.50, 0.65):
    P(f"\nPart 2, target U {U}: bin f_req, eps_req SN, eps_req SN+BH (median, 84 %), undone fraction from 0.872")
    for b in BN:
        lo, hi = map(float, b.split("-")); f = freq(b, U); G = [g for g in E.values() if g["ok"] and lo <= g["vf"] <= hi]
        if f is None: P(f"  {b}: f 0 still below"); f = 0.0
        ff = min(f, .872); es = np.array([np.interp(ff, TF, g["E"]) / g["SN"] for g in G]); eb = np.array([np.interp(ff, TF, g["E"]) / (g["SN"] + g["BH"]) for g in G]); ER[(b, U)] = (float(np.median(es)), float(np.median(eb))); P(f"  {b}: f_req {f:.2f}; SN {np.median(es):.4f} (84% {np.percentile(es, 84):.4f}, max {es.max():.4f}); SN+BH {np.median(eb):.5f}; full undo SN {np.median([g['E'][0] / g['SN'] for g in G]):.4f}; n {len(G)}")
short = any(v[1] > 1 for v in ER.values()); P(f"BUDGET SHORT: {short}; SN alone short at U 0.50: {any(ER[(b, .5)][0] > 1 for b in BN)}")
nz = [ER[(b, .5)][0] for b in BN if ER[(b, .5)][0] > 0]; P(f"eps_req SN, U 0.50, spread max/min where > 0: {max(nz) / min(nz):.1f}")
P("\nPart 3, forward: eps U_A/U_B rms tilt line | U by bin")
ok = []
for bu in ("SN", "SNBH"):
    for e in (.001, .003, .01, .03, .1, .3, 1.0, 1e3, 1e-12):
        r = R[f"{bu}_e{e}"]; L = line(r); T = abs(r["tilt"]) <= .15; ok += [(bu, e)] if L and T and e not in (1e3, 1e-12) else []; P(f"  {bu:5} {e:<7} {r['sparc'][A]['U_median']:.2f}/{r['sparc'][B]['U_median']:.2f} {r['sparc'][A]['rms']:.4f} {r['tilt']:+.2f} {L} | " + " ".join(f"{r['bins3'][b]['U']:.2f}" for b in BN))
d = lambda a, b: max(abs(a["sparc"][t][k] - b["sparc"][t][k]) for t in (A, B) for k in ("U_median", "rms"))
P(f"\nK1 f0 vs OP3 {d(R['f0'], O3['K1 frozen f_Q 0']):.4f}; f.872 vs OP3 {d(R['f0.872'], O3['PRIMARY frozen map f_Q 0.872']):.4f}; K2 E(.872) max {max(g['E'][8] for g in E.values()):.1e}; K3 eps 0 vs f.872 {d(R['SN_e1e-12'], R['f0.872']):.4f}; K4 eps 1e3 vs f0 {d(R['SN_e1000.0'], R['f0']):.4f}; MUTATE budget x .01 U {R['MUT_SNBH_e0.1']['sparc'][A]['U_median']:.2f} vs {R['SNBH_e0.1']['sparc'][A]['U_median']:.2f}")
P("LABEL: " + ("BUDGET SHORT" if short else f"ENERGY RULE HOLDS AT ONE FITTED eps {ok}" if ok else "WRONG SHAPE"))
open(os.path.join(H, "er1.out"), "w").write("\n".join(OUT) + "\n")
