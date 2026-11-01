#!/usr/bin/env python3
"""MH1: read rows, checks, labels. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "mh1_RUN_results.json"))); M = json.load(open(os.path.join(H, "mh1_MUTATE_results.json"))); N = json.load(open(os.path.join(H, "..", "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]; T1 = json.load(open(os.path.join(H, "mh1_t1.json"))); TG = ("A_c2b_refit", "B_cfg886_bg"); O = []
def P(s): print(s); O.append(s)
def gates(r):
    s = r["sparc"]; g = []
    if not all(s[t]["rms"] <= .11 and .5 <= s[t]["U"] <= .8 for t in TG): g.append("line")
    if not all(abs(s[t]["tilt"]) <= .15 for t in TG): g.append("tilt")
    if abs(r["groups"]["Z"]) > 2: g.append("groups")
    if not all(abs(r["lt"][t]) <= .10 for t in TG): g.append("LT")
    return g
k1 = max(max(abs(R["rows"][a]["sparc"][t][k] - N[b]["sparc"][t][k]) for t in TG for k in ("U", "rms", "tilt")) for a, b in (("off", "EM1|off"), ("blum", "EM1|blum"))); k1b = max(abs(R["rows"][a]["lt"][t] - N[b]["lt"][t]) for t in TG for a, b in (("off", "EM1|off"), ("blum", "EM1|blum"))); k1c = max(abs(R["rows"][a]["groups"]["Z"] - N[b]["groups"]["Z"]) for a, b in (("off", "EM1|off"), ("blum", "EM1|blum")))
k2 = max(abs(R["rows"]["K2_none"]["sparc"][t][k] - R["rows"]["blum"]["sparc"][t][k]) for t in TG for k in ("U", "rms", "tilt")); k4 = all(v["K4"][0] < 1e-6 and v["K4"][1] for v in R["pred"].values()); mb = abs(M["rows"]["MUT_MB_x2"]["sparc"][TG[0]]["U"] - R["rows"]["MB"]["sparc"][TG[0]]["U"]); mv = abs(M["rows"]["MUT_VDI_invert"]["sparc"][TG[0]]["U"] - R["rows"]["VDI0"]["sparc"][TG[0]]["U"])
ok = max(k1, k1b, k1c, k2) <= 1e-6 and k4 and mb > .02 and mv > .05
P(f"MH1; kappa = 1/2 FITTED, unused; not theory closed\nK1 vs NR3 MEDIAN {max(k1, k1b, k1c):.1e}; K2 {k2:.1e}; K3 by the same path (F_c 0 is the 'blum' row); K4 {k4}; MUTATE MB x2 dU {mb:.2f}, VDI inverted dU {mv:.2f}: {'PASS' if ok else 'FAIL'}")
L = {}
for k, r in R["rows"].items():
    if k.startswith("K2"): continue
    s = r["sparc"]; g = gates(r); L[k] = "SPARC SIDE CLEARS" if not g else "FAILS " + ",".join(g); c = R["clusters"].get(k); P(f"{k}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f} groups {r['groups']['Z']:+.2f} LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f} bins {[round(v, 2) for v in s[TG[0]]['bins'].values()]}: {L[k]}" + (f"; keys {c['n']} {c['bad']} X-COP {c['xcop']['mean']:+.3f}, {c['xcop']['rms']:.3f}" if c else ""))
g = R["gal"]["VDI0"]; TB = {}
for l in open(os.path.join(H, "..", "..", "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: TB[p[0]] = (float(p[15]), int(p[17]), float(p[5]))
    except ValueError: pass
U = R["rows"]["VDI0"]["sparc"][TG[0]]["per"]; P("VDI0 by V_flat: n, selected share, sigma_crit med km/s, D med, M_T/M med, bulge/M med, U selected / not")
for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
    n = [k for k in g if k in TB and TB[k][1] <= 2 and TB[k][2] >= 30 and lo <= TB[k][0] < hi]; se = [k for k in n if g[k]["sel"]]; un = [k for k in n if not g[k]["sel"]]; md = lambda a: float(np.median(a)) if len(a) else float("nan"); P(f"  {lo}-{hi}: {len(n)}, {len(se) / len(n):.2f}, {md([g[k]['sc'] for k in n]):.1f}, {md([g[k]['D'] for k in n]):.2f}, {md([g[k]['MT_over_M'] for k in n]):.3f}, {md([g[k]['Bfrac'] for k in n]):.3f}, {md([U[k] for k in se]):.2f} / {md([U[k] for k in un]):.2f}; bulge-free {sum(g[k]['Bfrac'] <= 0 for k in n)}")
for k, v in R["pred"].items(): P(f"pred {k}: M200 {v['M200']:.3g} F_obs {v['F_obs']:.3f} F_c {v['F_c']:.3f}; M_c(<{v['r_kpc']:g} kpc) no response {v['M0']:.3g}, Blumenthal {v['blum']:.3g}, MB {v['MB']:.3g}, MB/Blum {v['MB'] / v['blum']:.3f}")
for k, v in T1.items():
    if isinstance(v, dict): P(f"T1 {k}: Q(3Rd) " + " ".join(f"{h} {v['Q'][h][1]:.2f}" for h in "LPIC") + " rho " + " ".join(f"{a} {b:.3f}" for a, b in v["rho"].items()))
P(f"T1 K-T1 Q_L-1 {T1['K_T1']:.2f} vs LC1 0.94, line 25 %: FAIL; MUTATE {T1['MUTATE']:+.1%}; frozen label {T1['label']}")
json.dump(dict(ok=ok, labels=L, t1=T1["label"]), open(os.path.join(H, "mh1_verdict.json"), "w"), indent=1); open(os.path.join(H, "mh1.out"), "w").write("\n".join(O) + "\n")
