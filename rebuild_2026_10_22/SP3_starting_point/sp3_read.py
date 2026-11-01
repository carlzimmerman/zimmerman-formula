#!/usr/bin/env python3
"""SP3 reader: checks, grid, S4, verdict by the frozen rule. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, sys
import numpy as np
from scipy.stats import rankdata, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, HERE); from sp3_native import cell; OUT = []; TG = ("A_c2b_refit", "B_cfg886_bg")
def P(s): print(s, flush=True); OUT.append(s)
H = json.load(open(os.path.join(HERE, "sp3_hand_results.json")))["runs"]; W = json.load(open(os.path.join(HERE, "sp3_weigh.json"))); NR2 = json.load(open(os.path.join(RB, "NR2_low_mass_ng80", "NR2_MEDIAN_x74_results_fs0.034_nat_s2.7774.json")))["footings"]["canonical"]["sparc"]; NR3 = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]; R1 = json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_results.json")))["runs"]; R1p = json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_post_results.json")))["runs"]; O3 = json.load(open(os.path.join(RB, "OP3_contraction_on_native", "op3_results.json")))["runs"]
d = lambda a, b: max(max(abs(a[t]["U"] - b[t]["U_median"]), abs(a[t]["rms"] - b[t]["rms"])) for t in TG); dd = lambda a, b: max(max(abs(a[t]["U"] - b[t]["U"]), abs(a[t]["rms"] - b[t]["rms"])) for t in TG)
n = lambda mp, mn, f, m=1, dl=0.0: cell(mp, mn, f, m, dl)
k1a = d(H["EM1|off"]["sparc"], NR2); k1b = dd(H["EM1|blum"]["sparc"], NR3["EM1|blum"]["sparc"])
k2 = max(max(abs(n("EM1", "tot", f)["sparc"][t][q] - O3[l]["sparc"][t][q]) for t in TG for q in ("U_median", "rms")) for f, l in ((0.0, "K1 frozen f_Q 0"), (0.872, "PRIMARY frozen map f_Q 0.872")))
k3u = max(abs(H[a]["sparc"][t]["U"] - b["sparc"][t]["U"]) for a, b in (("E1|off", R1["E1|off"]), ("C1|off", R1p["C1|off"])) for t in TG); k3r = max(abs(H[a]["sparc"][t]["rms"] - b["sparc"][t]["rms"]) for a, b in (("E1|off", R1["E1|off"]), ("C1|off", R1p["C1|off"])) for t in TG)
A5 = n("AM1", "tot", 0.0); k5 = abs(A5["sparc"][TG[0]]["rms"] - 0.233); k5f = abs(n("AM1", "fc1", 0.0)["sparc"][TG[0]]["rms"] - 0.233)
e12 = float(re.search(r"eta\(M\) at 1e12/13/14/15: ([\d.]+)", open(os.path.join(HERE, "sp3_hand_run.log")).read()).group(1))
mu = n("EM1", "tot", 0.872, 2); b0 = n("EM1", "tot", 0.872); dmu = abs(mu["sparc"][TG[0]]["U_median"] - b0["sparc"][TG[0]]["U_median"])
C = dict(K1=max(k1a, k1b) <= 1e-6, K2=k2 <= 1e-6, K3=k3u <= 0.01 and k3r <= 0.002, K4=True, K5=min(k5, k5f) <= 0.03, K6=abs(e12 - 21.53) <= 0.01, MUT=dmu >= 0.02); P(f"Checks K1 {k1a:.1e} {k1b:.1e}; K2 {k2:.1e}; K3 dU {k3u:.3f} drms {k3r:.4f}; K4 asserted in sp3_weigh; K5 AM1 native off rms {A5['sparc'][TG[0]]['rms']:.3f}, {n('AM1','fc1',0.0)['sparc'][TG[0]]['rms']:.3f} vs ZN2 alt 0.233-0.253; K6 eta12 {e12:.3f}; MUTATE M_b x 2 dU {dmu:.2f}: {C}")
ok = all(C.values()); G = {}
def gates(U, rms, tilt, grp, lt, w):
    g = dict(line=all(0.5 <= U[i] <= 0.8 and rms[i] <= 0.11 for i in (0, 1)), tilt=all(abs(x) <= 0.15 for x in tilt), groups=abs(grp) <= 2, lt=all(abs(x) <= 0.10 for x in lt), dm=w["reached"], mw=w["cls"] == "FEASIBLE IN PRIORS"); return g
def row(lab, U, rms, tilt, grp, lt, bins, w):
    g = gates(U, rms, tilt, grp, lt, w); G[lab] = g; P(f"| {lab} | {U[0]:.2f}/{U[1]:.2f} | {rms[0]:.3f} | {tilt[0]:+.2f}/{tilt[1]:+.2f} | {grp:+.2f} | {lt[0]:+.3f}/{lt[1]:+.3f} | {w['r']:.3f} ({w['n']}) | {w['cls'].replace('FEASIBLE ', 'F ')} {w['n_all']} | {' '.join(f'{v:.2f}' for v in bins)} | {','.join(k for k, v in g.items() if not v) or 'NONE'} |")
P("\n| cell | U A/B | rms A | tilt | groups | LT | DiskMass r (n) | MW | U by V_flat, A | fails |\n|---|---|---|---|---|---|---|---|---|---|")
for ln in ("EM1", "E1", "C1", "AM1", "FAIR200"):
    for mo in ("off", "blum"):
        k = f"{ln}|{mo}"; r = H.get(k) or (R1.get(k) if ln == "E1" else R1p.get(k) if ln == "C1" else NR3.get(k))
        if r is None: continue
        s = r["sparc"]; row(f"hand {ln} {mo}", [s[t]["U"] for t in TG], [s[t]["rms"] for t in TG], [s[t]["tilt"] for t in TG], r["groups"]["Z"], [r["lt"][t] for t in TG], list(s[TG[0]]["bins"].values()), W[f"hand|{ln}|{mo}"])
    for mn in ("tot", "fc1"):
        for f, mo in ((0.0, "off"), (0.872, "fq")):
            r = n(ln, mn, f); s = r["sparc"]; x = r["sp3"]; row(f"native-{mn} {ln} {mo}", [s[t]["U_median"] for t in TG], [s[t]["rms"] for t in TG], [x["tilt"][t] for t in TG], r["groups"]["Z"], [x["lt"][t] for t in TG], list(x["binsU"][TG[0]].values()), W[f"native-{mn}|{ln}|{mo}"])
Fit = json.load(open(os.path.join(HERE, "sp3_refit.json"))); P("\nRefit, FITTED, EM1 + delta, native, f_Q 0.872, U 0.50 on both backgrounds; blue range (-0.10, +0.14)")
for mn, q in Fit.items():
    dl = q["delta"]; r = n("EM1", mn, 0.872, 1, dl); s = r["sparc"]; x = r["sp3"]; P(f"  {mn}: delta {dl:+.3f} {'PINCHED' if not -0.10 <= dl <= 0.14 else 'inside blue'}; U {s[TG[0]]['U_median']:.2f}/{s[TG[1]]['U_median']:.2f} rms {s[TG[0]]['rms']:.3f} tilt {x['tilt'][TG[0]]:+.2f} groups {r['groups']['Z']:+.2f} LT {x['lt'][TG[0]]:+.3f} bins {[round(v, 2) for v in x['binsU'][TG[0]].values()]}; trace {q['trace']}")
meas = {k: v for k, v in G.items() if k.endswith((" fq", " blum"))}; offc = {k: v for k, v in G.items() if k.endswith(" off")}; fitted = ()
RES = [k for k, v in meas.items() if all(v.values())]; PL = [k for k, v in meas.items() if v["line"] and not k.endswith(("FAIR200 x",))]; OF = [k for k, v in offc.items() if all(v.values())]
V = "NOT DECIDED, check failed" if not ok else (f"START RESOLVES {RES}" if RES else ("PARTLY" if (PL or OF) else "NOT THE START")); P(f"\nClear line with response: {PL}\nOff cells clearing all galaxy gates: {OF}\nVERDICT: {V}")
# S4 inclination, TP1's sample and partial Spearman
T = {}
for l in open(os.path.join(RB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) >= 18:
        try: T[p[0]] = dict(inc=float(p[5]), e=float(p[6]), vf=float(p[15]), Q=int(p[17]))
        except ValueError: pass
def pS(x, y, z):
    x, y, z = rankdata(x), rankdata(y), rankdata(z); rx = x - np.polyval(np.polyfit(z, x, 1), z); ry = y - np.polyval(np.polyfit(z, y, 1), z); return spearmanr(rx, ry)
P("\nS4 inclination, partial Spearman at fixed lg V_flat, 100-400 km/s, line p < 0.0071")
for k in ("EM1|off", "EM1|blum"):
    U = H[k]["Ugal"][TG[0]]; N = [a for a in U if a in T and T[a]["Q"] <= 2 and T[a]["inc"] >= 30 and 100 <= T[a]["vf"] < 400]; u = [U[a] for a in N]; r = pS([T[a]["inc"] for a in N], u, [math.log10(T[a]["vf"]) for a in N]); P(f"  {k}: n {len(N)} rho {r[0]:+.3f} p {r[1]:.3f}")
    tr = [a for a in N if 150 <= T[a]["vf"] < 250]; sh = [2 * math.radians(T[a]["e"]) / math.tan(math.radians(T[a]["inc"])) for a in tr]; i_ = np.array([T[a]["inc"] for a in tr]); uu = np.array([U[a] for a in tr]); P(f"    trough n {len(tr)}: median inc {np.median(i_):.0f}, median U below/above median inc {np.median(uu[i_ <= np.median(i_)]):.2f}/{np.median(uu[i_ > np.median(i_)]):.2f}; median 2 e_i cot i {np.median(sh):.3f}, i.e. V^2 by {100 * np.median(sh):.0f} % at 1 sigma, coherent")
json.dump(dict(verdict=V, checks=C, gates=G), open(os.path.join(HERE, "sp3_results.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "sp3.out"), "w").write("\n".join(OUT) + "\n")
