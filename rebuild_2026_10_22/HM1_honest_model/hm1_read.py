#!/usr/bin/env python3
"""HM1 read (FROZEN_CRITERIA.md): checks, C5's scorecard, joint chi^2, Z_tot, the puzzle. Reads caches only, M3A1's audit read only. Rerun byte-identical. kappa = 1/2 FITTED, unused; not theory closed."""
import contextlib, io, json, os, sys
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CC = os.path.join(HERE, "cache_cells"); CG = os.path.join(HERE, "cache_gal"); HH = ("h0672", "h0686"); TG = ("A_c2b_refit", "B_cfg886_bg"); OUT = []; RES = {}; CK = {}
def P(s=""): print(s, flush=True); OUT.append(s)
L = lambda n: json.load(open(os.path.join(CC, n + ".json"))); G_ = lambda n: json.load(open(os.path.join(CG, n + ".json")))
def row(r): bad = sorted({k for h in HH for k, v in r["cells"][h].items() if abs(v["Z"]) > 2}); return bad
xok = lambda r: abs(r["xcop"]["mean"]) <= 0.05 and r["xcop"]["rms"] <= 0.10
P("HM1 honest model: native shape, measured response, fair share. kappa = 1/2 FITTED, unused; no a0; not theory closed. Not blind.")
# ---- K1
Z4 = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_results.json")))["runs"]; k1 = 0.0; k1x = 0.0; k3 = 0.0
for g, zl in (("0.005", "gas +0.005"), ("0.111", "X-COP's gas")):
    for fs in ("0.034", "0.0615"):
        d = L(f"N_{g}_{fs}"); c = d["hm1"]["off|none"]; z = Z4[f"f* {fs}, {zl}"]; k1 = max(k1, max(abs(c["cells"][h][k]["pred"] - z["cells"][h][k]["pred"]) for h in HH for k in z["cells"][h])); k1x = max(k1x, max(abs(c["xcop"][q] - z["xcop"][q]) for q in ("mean", "rms"))); k3 = max(k3, d["K3"])
CK["K1"] = k1 <= 1e-6 and k1x <= 1e-6; CK["K3"] = k3 <= 1e-6; P(f"K1 f 0, BCG none vs ZN4 per key, 4 cells: preds {k1:.1e}, X-COP {k1x:.1e}: {'PASS' if CK['K1'] else 'FAIL'}"); P(f"K3 identity no baryons on native shapes: {k3:.1e}: {'PASS' if CK['K3'] else 'FAIL'}")
# ---- K2
k2 = 0.0
for tag, c in (("tot_off", "EM1_tot_f0_m1_d+0.0000"), ("tot_fq", "EM1_tot_f0.872_m1_d+0.0000"), ("fc1_off", "EM1_fc1_f0_m1_d+0.0000"), ("fc1_fq", "EM1_fc1_f0.872_m1_d+0.0000")):
    a = G_(tag); b = json.load(open(os.path.join(RB, "SP3_starting_point", "cells", c + ".json"))); ds = [abs(a["groups"]["Z"] - b["groups"]["Z"])] + [abs(a["sparc"][t][q] - b["sparc"][t][q]) for t in TG for q in ("U_median", "rms")] + [abs(a["sp3"]["tilt"][t] - b["sp3"]["tilt"][t]) for t in TG] + [abs(a["sp3"]["lt"][t] - b["sp3"]["lt"][t]) for t in TG]; k2 = max(k2, max(ds))
CK["K2"] = k2 <= 1e-6; P(f"K2 SP3's native rows, EM1, both maps, f 0 and 0.872: {k2:.1e}: {'PASS' if CK['K2'] else 'FAIL'}")
# ---- K4
A = L("N_0.005_0.034")["hm1"]; p = A["fq|bcg"]; KD = L("K4diag"); p["K4d"] = KD["hm1"]["fq|bcg"]["K4d"]; d4 = np.array([v[2] for v in p["K4d"]]); CK["K4"] = p["K4n"] == 0; P(f"K4 M_c(r_ta) after/before, Blumenthal f_Q, BCG, f* 0.034, gas +0.005: max |d| {p['K4']:.3f}; over 1e-3 in {p['K4n']} of 652 cluster-h cells: {'PASS' if CK['K4'] else 'FAIL'}")
if len(d4):
    P(f"   measured one grid step past r_ta instead: max |d| {KD['hm1']['fq|bcg']['K4b'][0]:.3f} in {KD['hm1']['fq|bcg']['K4b'][1]} cells")
    P(f"   those cells: d median {np.median(d4):+.4f}, range {d4.min():+.4f} to {d4.max():+.4f}; F = Mb(r_ta)/M0(r_ta) median {np.median([v[3] for v in p['K4d']]):.3f}; M0(r_ta)/Mfair median {np.median([v[4] for v in p['K4d']]):.3f}; r_ta median {np.median([v[5] for v in p['K4d']]):.2f} Mpc; by M tercile {[int(sum(v[6] == t for v in p['K4d'])) for t in range(3)]}")
a1 = L("A1_0.005_0.034")["hm1"]["fq|bcg|A1"]; dzz = max(abs(a1["cells"][h][k]["Z"] - p["cells"][h][k]["Z"]) for h in HH for k in p["cells"][h]); P(f"   AMENDMENT A1, post-result: mass pushed past r_ta returned as a shell at r_ta. Max |dZ| over 15 keys, both h, against the frozen row: {dzz:.3f}; X-COP |d| {abs(a1['xcop']['mean'] - p['xcop']['mean']):.1e}. Same failing keys: {row(a1) == row(p)}. A1 doesn't restore a verdict.")
RES["K4"] = dict(max=p["K4"], n=p["K4n"], A1_dZ=dzz)
g4 = A["gn|bcg"]; P(f"   Gnedin drift at r_ta (not conserved by construction): max {g4['K4']:.3f}, over 1e-3 in {g4['K4n']}")
# ---- K5
N3 = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]; S0 = L("S_erass_0.034")["hm1"]["S|off|none"]; S1 = L("S_cn1F_erass")["hm1"]["S|blum|bcg|cn1F"]; S1o = L("S_erass_0.034")["hm1"]["S|blum|bcg"]; f5 = lambda c, r: max(abs(c["cells"][h][k]["pred"] - r["keys"]["preds"][h][k]) for h in HH for k in r["keys"]["preds"][h]); k5a, k5b, k5c = f5(S0, N3["EM1|off"]), f5(S1, N3["EM1|blum"]), f5(S1o, N3["EM1|blum"]); CK["K5"] = k5a <= 1e-6 and k5b <= 1e-6; P(f"K5 S-core rebuild vs NR3 MEDIAN preds: off {k5a:.1e}; Blumenthal with CN1's F and no clip {k5b:.1e}: {'PASS' if CK['K5'] else 'FAIL'}; with this lane's F (M0's own, Mb clipped at r_ta) {k5c:.1e}, X-COP off |d| {abs(S0['xcop']['mean'] - N3['EM1|off']['xcop']['mean']):.1e}")
# ---- K6
K0 = json.load(open(os.path.join(HERE, "kn1_grade_hm1_off.json"))); KR = json.load(open(os.path.join(RB, "KN1_kids_native_halos", "kn1_grade_em1.json"))); dk = abs(K0["footings"]["canonical"]["all"]["dchi2"] - KR["footings"]["canonical"]["all"]["dchi2"]); LG = json.load(open(os.path.join(HERE, "hm1_op1.json"))); CK["K6"] = dk <= 0.1 and LG["K6_op1"] <= 1e-3; P(f"K6 f 0 through KN1's path: dchi2 |d| {dk:.1e}; through OP1's: {LG['K6_op1']:.1e}: {'PASS' if CK['K6'] else 'FAIL'}")
# ---- K7
P("K7 sign, M_c after/before, median, f_Q + BCG, clusters at 0.05, 0.15, 0.3, 0.46, 1, 2 Mpc: " + ", ".join(f"{v:.3f}" for v in p["flip"]) + ". All outward at every radius here; SPARC inward at r0 per OP3 and UR1 (Y falls from 0.84 to 0.44).")
CK["K7"] = p["flip"][0] < 1
# ---- MUTATE
m = A["MUTATE fq05|bcg"]; dm = max(abs(m["cells"][h][k]["pred"] - p["cells"][h][k]["pred"]) for h in HH for k in p["cells"][h]); gf, gm = G_("tot_fq"), G_("tot_MUTATE05"); du = abs(gm["sparc"][TG[0]]["U_median"] - gf["sparc"][TG[0]]["U_median"]); CK["MUTATE"] = dm > 0.01 and du > 0.02; P(f"MUTATE f x 0.5: key pred moves up to {dm:.3f}, G-OUT-M3 {p['cells']['h0672']['G-OUT-M3']['Z']:+.2f} > {m['cells']['h0672']['G-OUT-M3']['Z']:+.2f}, X-COP {p['xcop']['mean']:+.3f} > {m['xcop']['mean']:+.3f}; Y {gf['sparc'][TG[0]]['U_median']:.2f} > {gm['sparc'][TG[0]]['U_median']:.2f}: {'BITES' if CK['MUTATE'] else 'UNDECIDED'}")
# ---- clusters
P("\nClusters, canonical. keys passing, failing, G-OUT-M3 both h, X-COP mean rms")
TAB = {}
for g in ("0.005", "0.111"):
    for fs in ("0.034", "0.0615"):
        J = L(f"N_{g}_{fs}")["hm1"]
        if g == "0.005" and fs == "0.034": J = dict(J); J["fq|bcg|cn1F"] = L("cn1F_0.005")["hm1"]["fq|bcg|cn1F"]
        for n, r in J.items():
            if n.startswith("MUTATE"): continue
            b = row(r); c = r["cells"]; TAB[f"{g}|{fs}|{n}"] = dict(n=15 - len(b), bad=b, M3=[c[h]["G-OUT-M3"]["Z"] for h in HH], x=[r["xcop"]["mean"], r["xcop"]["rms"]], xok=xok(r)); P(f"  gas +{g} f* {fs} {n:14s}: {15 - len(b):2d}/15 {b} M3 {c['h0672']['G-OUT-M3']['Z']:+.2f}, {c['h0686']['G-OUT-M3']['Z']:+.2f}; G-IN-Mall {c['h0672']['G-IN-Mall']['Z']:+.2f}; G-MID-T3 {c['h0672']['G-MID-T3']['Z']:+.2f}; X-COP {r['xcop']['mean']:+.4f}, {r['xcop']['rms']:.3f} {'PASS' if xok(r) else 'FAIL'}")
RES["clusters"] = TAB; P(f"  X-COP by x, primary: {p['xcop']['by_x']}; alt template failing keys, primary: {sorted({k for h in p['alt'] for k, v in p['alt'][h].items() if abs(v['Z']) > 2})}")
P(f"  M0(r_ta)/Mfair, native, all clusters 16, 50, 84: {[round(v, 3) for v in p['ratio']]}")
# ---- joint, Z_tot
M3D = os.path.join(RB, "M3A1_outer_key_audit"); T = open(os.path.join(M3D, "m3a1_audit.py")).read(); T = T[:T.index("JR = {}")]; _l = T.split("\n"); assert _l[106].startswith("FC = os.environ") and _l[117].startswith('P("  C4b m'); T = "\n".join(_l[:106] + _l[118:]);   # drops only the C4c n(z) block, which needs a KiDS column path and isn't used by R; K_j below checks R against M3A1
ns = {"__file__": os.path.join(M3D, "m3a1_audit.py"), "__name__": "x"}; _a = sys.argv; sys.argv = ["m3a1_audit.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(T, "m3a1", "exec"), ns)
sys.argv = _a; M3R = json.load(open(os.path.join(M3D, "m3a1_results.json"))); JP = {}; kj = 0.0
P("\nJoint chi^2, BA1's line, M3A1's R (from the f 0 row's per-cluster vectors; applied to the response rows, disclosed), and Z_tot for G-OUT-M3 by M3A1's quadrature")
for f, h in ns["CELLS"]:
    q = ns["C"][(f, h)]; Kb = ns["keys"](ns["WB_"], q, f, h); ks = list(Kb); Rb = np.corrcoef(np.array([Kb[k] for k in ks])); j0 = ns["joint"](L(f"N_0.005_{f}")["hm1"]["off|none"]["cells"][h], ks, Rb); kj = max(kj, abs(j0[0] - M3R["joint"][f"{f}|{h}"]["chi2"])); zt = M3R["Ztot"][f"{f}|{h}"]
    for n in ("off|none", "fq|bcg", "fq|none", "blum|bcg", "gn|bcg"):
        c = L(f"N_0.005_{f}")["hm1"][n]["cells"][h]; a = ns["joint"](c, ks, Rb); v = c["G-OUT-M3"]; tot = np.sqrt(v["s"] ** 2 + sum(zt[t] ** 2 for t in ("gas", "slope", "seed", "m", "nz", "leak"))); Zt = (v["meas"] - v["pred"]) / tot; JP[f"{f}|{h}|{n}"] = dict(chi2=a[0], dof=a[1], p=a[2], Ztot=Zt); P(f"  f* {f} {h} {n:9s}: chi^2 {a[0]:.1f}/{a[1]}, p {a[2]:.1e} {'JOINT PASS' if a[2] >= 0.05 else 'JOINT FAIL' if a[2] < 0.01 else 'MARGINAL'}; Z_tot {Zt:+.2f}")
CK["Kj"] = kj <= 1e-9; P(f"  check: f 0 row against M3A1's joint, |d chi^2| {kj:.1e}: {'PASS' if CK['Kj'] else 'FAIL'}"); RES["joint"] = JP
# ---- galaxies
P("\nGalaxies, EM1's fitted line, native reads no eta. Y A/B, rms A/B, tilt A/B, LT A/B, groups, IC 1613 E (Z)")
NDr = json.load(open(os.path.join(RB, "ND1_native_dwarfs", "nd1_ab_results.json"))); import re; _m = re.search(r"IC 1613 ([-+\d.]+) \(([-+\d.]+),", open(os.path.join(RB, "ND1_native_dwarfs", "nd1_ab.out")).read()); SE = float(_m.group(1)) / float(_m.group(2))
for tg in ("tot_off", "tot_fq", "fc1_off", "fc1_fq", "tot_blum", "tot_gn", "tot_fq_ng80proxy"):
    r = G_(tg); s = r["sparc"]; x = r["sp3"]; ic = x.get("ltE", {}).get(TG[0], {}).get("IC 1613"); RES["gal_" + tg] = dict(U=[s[t]["U_median"] for t in TG], rms=[s[t]["rms"] for t in TG], tilt=[x["tilt"][t] for t in TG], lt=[x["lt"][t] for t in TG], groups=r["groups"]["Z"], gv=r["groups"].get("verdict"), ic=ic, bins=x["binsU"][TG[0]]); P(f"  {tg:18s} {s[TG[0]]['U_median']:.2f}/{s[TG[1]]['U_median']:.2f} {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} {x['tilt'][TG[0]]:+.2f}/{x['tilt'][TG[1]]:+.2f} {x['lt'][TG[0]]:+.3f}/{x['lt'][TG[1]]:+.3f} G {r['groups']['Z']:+.2f} {r['groups'].get('verdict')} IC {ic:+.3f} ({ic / SE:+.1f}); bins {[round(v, 2) for v in x['binsU'][TG[0]].values()]}")
W = json.load(open(os.path.join(HERE, "hm1_weigh.json"))); P("Direct weighing, SP3's path, rerun: " + "; ".join(f"{k.split('|')[0]} {k.split('|')[2]} r {v['r']:.3f} n {v['n']} {v['cls']} {v['n_all']}" for k, v in W.items()))
P("\nKiDS, KN1's path (all; primary), canonical, alt: dchi2(H2H - L2H)")
for t in ("off", "fq", "fqfc1", "MUT05"):
    k = json.load(open(os.path.join(HERE, f"kn1_grade_hm1_{t}.json"))); RES["kids_" + t] = k["footings"]["canonical"]["all"]["dchi2"]; P(f"  {t:6s}: {k['footings']['canonical']['all']['dchi2']:+.1f} ({k['footings']['canonical']['primary']['dchi2']:+.1f}), alt {k['footings']['alt']['all']['dchi2']:+.1f}, H2H {k['footings']['canonical']['all']['H2H']:.1f}, class {k['verdict']}")
P("\nLocal Group, OP1's P1, EM1, 1e10 tag, E (Z)")
for ft in ("canonical", "alt"):
    for n in ("frozen|off", "frozen|fq", "frozen|blum", "FC1|fq"): P(f"  {ft} {n:12s}: " + "; ".join(f"{c} {v['E']:+.3f} ({v['Z']:+.2f})" for c, v in LG[ft][n].items()))
# ---- puzzle
Q = L("P_0.005")["hm1"]; RR = [0.05, 0.1, 0.2, 0.3, 0.46, 0.7, 1.0, 1.42, 2.06, 3.0, 4.5]; arr = lambda n, k: np.array([c[k] for c in Q[n]["dump"]["clusters"]]); MS, MN, RS, RN, MB = arr("S|off|none", "Mc"), arr("off|none", "Mc"), arr("S|off|none", "rho"), arr("off|none", "rho"), arr("off|none", "Mb"); R2 = arr("off|none", "R200"); MF = arr("off|none", "Mfair")
P("\nPUZZLE. M3, 109 clusters, f* 0.034, h 0.672, gas +0.005, both paths through one grader. Medians")
P("  r Mpc:      " + " ".join(f"{r:7.2f}" for r in RR)); P("  r/R200:     " + " ".join(f"{r / np.median(R2):7.2f}" for r in RR)); P("  M_c N 1e13: " + " ".join(f"{v:7.2f}" for v in np.median(MN, 0) / 1e13)); P("  M_c S 1e13: " + " ".join(f"{v:7.2f}" for v in np.median(MS, 0) / 1e13)); P("  Mb 1e13:    " + " ".join(f"{v:7.2f}" for v in np.median(MB, 0) / 1e13)); P("  M S/N:      " + " ".join(f"{v:7.3f}" for v in np.median(MS / MN, 0))); P("  16 %:       " + " ".join(f"{v:7.3f}" for v in np.percentile(MS / MN, 16, 0))); P("  84 %:       " + " ".join(f"{v:7.3f}" for v in np.percentile(MS / MN, 84, 0))); P("  rho S/N:    " + " ".join(f"{v:7.3f}" for v in np.median(RS / RN, 0)))
for n in ("S|off|none", "off|none"):
    a, b = arr(n, "M200_c") / MF, arr(n, "Mrta") / MF; P(f"  {n}: M_c(R200)/Mfair {np.median(a):.3f}; M_c(r_ta)/Mfair {np.median(b):.3f} [{np.percentile(b, 16):.3f}, {np.percentile(b, 84):.3f}]")
P(f"  R200 {np.median(R2):.3f} Mpc, r_ta {np.median(arr('off|none', 'rta')):.2f} Mpc, Mfair {np.median(MF) / 1e13:.1f}e13")
P("  G-OUT-M3 pred split, OE1's telescoping chain: piece, S, N, S - N")
sp, sn = Q["S|off|none"]["dump"]["shares"], Q["off|none"]["dump"]["shares"]; ts = sum(v["OUTER"] for v in sp.values()); tn = sum(v["OUTER"] for v in sn.values())
for k in sp: P(f"    {k:14s} {sp[k]['OUTER']:+.3f} {sn[k]['OUTER']:+.3f} {sp[k]['OUTER'] - sn[k]['OUTER']:+.3f}")
P(f"    total          {ts:+.3f} {tn:+.3f} {ts - tn:+.3f}; grader's {Q['S|off|none']['cells']['h0672']['G-OUT-M3']['pred']:.3f}, {Q['off|none']['cells']['h0672']['G-OUT-M3']['pred']:.3f}, meas {Q['off|none']['cells']['h0672']['G-OUT-M3']['meas']:.3f}, s {Q['off|none']['cells']['h0672']['G-OUT-M3']['s']:.3f}")
rw = lambda n: Q[n]["xcop"]["rows"]; P("  X-COP, x: r kpc, M_c N, M_c S 1e13, resid N, resid S: " + "; ".join(f"{x}: {np.median([v['r'] for v in rw('off|none') if v['x'] == x]):.0f}, {np.median([v['Mh'] for v in rw('off|none') if v['x'] == x]) / 1e13:.1f}, {np.median([v['Mh'] for v in rw('S|off|none') if v['x'] == x]) / 1e13:.1f}, {np.mean([v['d'] for v in rw('off|none') if v['x'] == x]):+.3f}, {np.mean([v['d'] for v in rw('S|off|none') if v['x'] == x]):+.3f}" for x in (0.1, 0.2, 0.3, 0.5, 0.7)))
v3 = Q["off|none"]["cells"]["h0672"]["G-OUT-M3"]; rate = sn["c<R200"]["OUTER"] / np.median(arr("off|none", "M200_c") / MF); nZ2 = v3["meas"] - 2 * v3["s"] - v3["pred"]; nZ0 = v3["meas"] - v3["pred"]; dM2, dM0 = nZ2 / rate, nZ0 / rate; miss = 1 - np.median(arr("off|none", "Mrta") / MF); fair = np.median(arr("off|none", "M200_c") / MF)
P(f"  Requirement, arithmetic on the two curves: pred per unit M_c(<R200)/Mfair {rate:.2f}. To Z = 2: pred +{nZ2:.3f}, M_c inside about 1.4 Mpc +{dM2:.3f} Mfair ({dM2 * np.median(MF) / 1e13:.1f}e13). To Z = 0: +{nZ0:.3f}, +{dM0:.3f} Mfair ({dM0 * np.median(MF) / 1e13:.1f}e13). Native holds {miss:.3f} Mfair outside r_ta, so that is {dM2 / miss:.0%} to {dM0 / miss:.0%} of it. M_c(<R200) x {1 + dM2 / fair:.2f} to x {1 + dM0 / fair:.2f}, cold over baryons at R200 {5.36 * (1 + dM2 / fair):.1f} to {5.36 * (1 + dM0 / fair):.1f}, against fair share's 5.36")
x1 = KD["x1"]; P("  X-COP's x = 1 row (R500), outside the frozen 0.75 cut, post-result, no grade: resid mean native " + f"{np.mean([v['N'] for v in x1]):+.3f}, S-core {np.mean([v['S'] for v in x1]):+.3f}, n {len(x1)}, r median {np.median([v['r'] for v in x1]):.0f} kpc; M_c/Mfair there native {np.median([v['MnF'] for v in x1]):.3f}, S-core {np.median([v['MsF'] for v in x1]):.3f}. Per cluster native: " + ", ".join(f"{v['c']} {v['N']:+.2f}" for v in x1)); RES["x1"] = dict(N=float(np.mean([v["N"] for v in x1])), S=float(np.mean([v["S"] for v in x1])))
H = L("S_0.005_0.034")["hm1"]; hy = H["hybrid"]; hf = H["hybrid|fq|bcg"]; h3 = Q["hybrid"]["hyb_M3"]; P(f"  Diagnostic, NOT A RULE: native inside 0.75 R500, max(native, S-core) outside. {15 - len(row(hy))}/15, failing {row(hy)}, G-OUT-M3 {hy['cells']['h0672']['G-OUT-M3']['Z']:+.2f}, {hy['cells']['h0686']['G-OUT-M3']['Z']:+.2f}; X-COP {hy['xcop']['mean']:+.3f}, {hy['xcop']['rms']:.3f}, unchanged by construction, since it tests only inside the join. Join in M3 {h3['rx'][1]:.3f} Mpc [{h3['rx'][0]:.3f}, {h3['rx'][2]:.3f}], step in M_c at the join {h3['step'][1]:.3f} Mfair [{h3['step'][0]:.3f}, {h3['step'][2]:.3f}]. With f_Q + BCG on top: {15 - len(row(hf))}/15, M3 {hf['cells']['h0672']['G-OUT-M3']['Z']:+.2f}, X-COP {hf['xcop']['mean']:+.3f}, {hf['xcop']['rms']:.3f}")
RES["puzzle"] = dict(R=RR, S_over_N=np.median(MS / MN, 0).tolist(), dM2=dM2, dM0=dM0, miss=miss, split={k: [sp[k]["OUTER"], sn[k]["OUTER"]] for k in sp}, hybrid=dict(n=15 - len(row(hy)), M3=hy["cells"]["h0672"]["G-OUT-M3"]["Z"], M3_join=h3))
# ---- verdict
P("\nFG1 lines for C5, canonical, primary"); gp = RES["gal_tot_fq"]; lo = lambda v, l: all(abs(x) <= l for x in v)
S_ok = all(0.5 <= u <= 0.8 for u in gp["U"]) and all(x <= 0.11 for x in gp["rms"]); Tl = lo(gp["tilt"], 0.15); LT = lo(gp["lt"], 0.10); Gr = gp["groups"] < 2 and gp["groups"] > -2; K_ = len(row(p)) == 0; X_ = xok(p); kd = json.load(open(os.path.join(HERE, "kn1_grade_hm1_fq.json"))); Ln = kd["verdict"]["canonical"] != "LAW" and kd["verdict"]["alt"] != "LAW"; DW = {c: v["Z"] for c, v in LG["canonical"]["frozen|fq"].items()}; Dw = all(abs(v) < 2 for v in DW.values()); wt = W["native-tot|EM1|fq"]; MW = wt["cls"] == "FEASIBLE IN PRIORS"; DM = 0.9 <= wt["r"] <= 1.1 and wt["n"] >= 27; IC = abs(gp["ic"] / SE) < 2
LN = dict(S=S_ok, Tl=Tl, LT=LT, G=Gr, K=K_, X=X_, Ln=Ln, Dw=Dw, MW=MW, DM=DM, IC=IC); ST = {"S": f"U {gp['U'][0]:.2f}/{gp['U'][1]:.2f}, rms {gp['rms'][0]:.4f} [HM1, = SP3]", "Tl": f"{gp['tilt'][0]:+.2f}/{gp['tilt'][1]:+.2f} [HM1, = SP3]", "LT": f"{gp['lt'][0]:+.3f}/{gp['lt'][1]:+.3f} [HM1, = SP3]", "G": f"Z {gp['groups']:+.2f}, not contracted as OP3 [HM1, = SP3]", "K": f"{15 - len(row(p))} of 15, {row(p)} [HM1]", "X": f"{p['xcop']['mean']:+.3f}, {p['xcop']['rms']:.3f} [HM1]", "Ln": f"class {kd['verdict']['canonical']}, dchi2 {kd['footings']['canonical']['all']['dchi2']:+.1f} [HM1]", "Dw": "; ".join(f"{c} {v:+.2f}" for c, v in DW.items()) + " [HM1]", "MW": f"{wt['cls']}, {wt['n_all']} cells [HM1, = SP3]", "DM": f"r {wt['r']:.3f}, n {wt['n']} [HM1, = SP3]; CFG577's Jeans 5-7 % would take it to about 1.14, as SP3", "IC": f"E {gp['ic']:+.3f}, Z {gp['ic'] / SE:+.1f} [HM1]"}
for k in LN: P(f"  {k:3s} {'PASS' if LN[k] else 'FAIL'}: {ST[k]}")
fl = [k for k in LN if not LN[k]]; ok = all(v for k, v in CK.items()); RES["lines"] = LN; RES["checks"] = CK; g111 = len(row(L("N_0.111_0.034")["hm1"]["fq|bcg"])) == 0; RES["reading"] = "FAILS: " + ", ".join(fl)
V = ("NO VERDICT AS FROZEN (" + ", ".join(k for k, v in CK.items() if not v) + " failed). " if not ok else "") + "FAILS: " + ", ".join(fl) + (" [GAS-CONDITIONAL]" if g111 else "") + (" [RESPONSE-DEPENDENT]" if len({xok(L("N_0.005_0.0615")["hm1"][n_]) for n_ in ("fq|bcg", "blum|bcg", "gn|bcg")}) > 1 else ""); P(f"\nChecks {CK}\nLABEL: {V}"); RES["label"] = V
json.dump(RES, open(os.path.join(HERE, "hm1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hm1.out"), "w").write("\n".join(OUT) + "\n")
