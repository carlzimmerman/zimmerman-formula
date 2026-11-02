#!/usr/bin/env python3
"""FR1 read (FROZEN_CRITERIA.md): checks, label, joint chi^2, Z_tot, read-across. Caches only; M3A1's audit text read only. kappa = 1/2 FITTED, unused; not theory closed."""
import contextlib, io, json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CC = os.path.join(HERE, "cache_jobs"); HH = ("h0672", "h0686"); OUT = []; RES = {}; CK = {}
def P(s=""): print(s, flush=True); OUT.append(s)
LN = json.load(open(os.path.join(HERE, "fr1_line.json")))
def J(n): return json.load(open(os.path.join(CC, re.sub(r"\W", "_", n) + ".json")))
def cells(R):
    c = R["grader"]["canonical"]["clusters"]["cells"]; O = {}
    for h in HH:
        m = R["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
Z4 = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_results.json")))["runs"]; FS = ("0.034", "0.0615"); k1 = k1x = 0.0
for f in FS:
    O = cells(J(f"K1 one {f}")); C = Z4[f"f* {f}, gas +0.005"]; k1 = max(k1, max(abs(O[h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in O[h])); x = J(f"K1 one {f}")["footings"]["canonical"]; k1x = max(k1x, abs(x["mean"] - C["xcop"]["mean"]), abs(x["rms"] - C["xcop"]["rms"]))
CK["K1"] = k1 <= 1e-6 and k1x <= 1e-6; P(f"K1 f_ret 1 vs ZN4 +0.005, per key, X-COP, both f*: preds {k1:.1e}, X-COP {k1x:.1e}: {'PASS' if CK['K1'] else 'FAIL'}")
CK["K2"] = LN["K2"]; P(f"K2 line parser: {'PASS' if LN['K2'] else 'FAIL'} (fr1_line.out)")
R = J("H 0.034"); D = R["dump"]; A = sorted([v for v in D.values() if v["i"] is not None], key=lambda v: v["Mb200"]); M3 = A[-len(A) // 3:]; med = lambda a, k: float(np.median([v[k] for v in a]))
d3 = max(abs(math.log10(v["Y500_line"]) - math.log10((1 + 5.2715) * v["Mb5"] / 10 ** v["lgM500"])) for v in A if False) if False else None
k4 = abs(math.log10(med(M3, "Y500_model") / med(M3, "Y500_line"))); CK["K4"] = k4 <= .03; P(f"K4 closure M3, model's own M_b/M at its R500 vs the line, median: {med(M3, 'Y500_model'):.4f} vs {med(M3, 'Y500_line'):.4f}, {k4:.4f} dex: {'PASS' if CK['K4'] else 'FAIL'}; 1 %-99 % spread over all clusters {np.percentile([math.log10(v['Y500_model'] / v['Y500_line']) for v in A], [1, 99]).round(3).tolist()}")
HA = json.load(open(os.path.join(RB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]["A_c2b_refit"]["params"]["h"]; qq = .7 / HA
kh = max(abs(LN["H"]["a"] + LN["H"]["b"] * (v["lgM500"] - math.log10(qq) - 14.5) + math.log10(1.034) + 1.5 * math.log10(qq) - math.log10(v["Y500_line"])) for v in A); CK["K3"] = kh <= 1e-3; P(f"K3 solved M500 back through the line by hand, every cluster, grader's bg h {HA:.4f}: max |d lg Y| {kh:.1e}: {'PASS' if CK['K3'] else 'FAIL'}")
MU = {f: cells(J(f"MUT flip {f}")) for f in FS}; xm = J("MUT flip 0.034")["footings"]["canonical"]; CK["MUT"] = abs(xm["mean"]) > .05; P(f"MUTATE slope flip: X-COP {xm['mean']:+.3f} {xm['rms']:.3f}, no fair R200 {J('MUT flip 0.034')['zn1']['no_fs']}, M3 {MU['0.034']['h0672']['G-OUT-M3']['Z']:+.2f}: {'BITES' if CK['MUT'] else 'DOES NOT BITE'}")
ok = all(CK.values()); P(f"checks {'all pass' if ok else 'FAILED: ' + str(CK)}")
P(f"\nM3 ({len(M3)} by Mb200), primary H, f* 0.034: lg M500 {med(M3, 'lgM500'):.3f}, lg M200 {med(M3, 'lgM200'):.3f}, R500 {med(M3, 'R500') / 3.0857e22:.3f} Mpc, R200 {med(M3, 'R200') / 3.0857e22:.3f}, Y500 {med(M3, 'Y500_line'):.3f} (lg {math.log10(med(M3, 'Y500_line')):+.3f}), carry {med(M3, 'carry'):.3f} (lg {math.log10(med(M3, 'carry')):+.3f}), Y200 {med(M3, 'Y200'):.3f} (lg {math.log10(med(M3, 'Y200')):+.3f}), cold/baryon at R200 {med(M3, 'Mc200') / med(M3, 'Mb200'):.2f}, M_c(R200)/Mfair {np.median([v['Mc200'] / v['Mfair'] for v in M3]):.3f}, M_c(r_ta)/Mfair {np.median([v['Mcta'] / v['Mfair'] for v in M3]):.3f}")
P(f"   need, HM1: cold/baryon 7.4 to 9 at R200, i.e. lg Y200 {math.log10(6.2715 / 8.4):+.3f} to {math.log10(6.2715 / 10):+.3f} (Z 2, Z 0), total-mass convention")
RES["M3"] = {k: med(M3, k) for k in ("lgM500", "lgM200", "Y500_line", "Y200", "carry", "Mc200", "Mb200", "Mbt", "Mfair", "Mcta")}
T = open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_audit.py")).read(); T = T[:T.index("JR = {}")]; _l = T.split("\n"); assert _l[106].startswith("FC = os.environ") and _l[117].startswith('P("  C4b m'); T = "\n".join(_l[:106] + _l[118:]); M3D = os.path.join(RB, "M3A1_outer_key_audit"); ns = {"__file__": os.path.join(M3D, "m3a1_audit.py"), "__name__": "x"}; _a = sys.argv; sys.argv = ["m3a1_audit.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(T, "m3a1", "exec"), ns)
sys.argv = _a; M3R = json.load(open(os.path.join(M3D, "m3a1_results.json"))); RR = {}
for f, h in ns["CELLS"]:
    q = ns["C"][(f, h)]; Kb = ns["keys"](ns["WB_"], q, f, h); ks = list(Kb); RR[(f, h)] = (ks, np.corrcoef(np.array([Kb[k] for k in ks])))
kj = max(abs(ns["joint"](cells(J(f"K1 one {f}"))[h], RR[(f, h)][0], RR[(f, h)][1])[0] - M3R["joint"][f"{f}|{h}"]["chi2"]) for f in FS for h in HH); CK["Kj"] = kj <= 1e-3; P(f"Joint vs M3A1 on f_ret 1: {kj:.1e}: {'PASS' if CK['Kj'] else 'FAIL'}")
BASE = {("0.034", "h0672"): 4.41, ("0.034", "h0686"): 4.07, ("0.0615", "h0672"): 4.13, ("0.0615", "h0686"): 3.81}
def rowfor(lab, fs=FS, tot_extra=None):
    o = {}
    for f in fs:
        Rr = J(f"{lab} {f}"); O = cells(Rr); b = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); x = Rr["footings"]["canonical"]
        o[f] = dict(keys=15 - len(b), bad=b, xcop=(x["mean"], x["rms"]), xok=abs(x["mean"]) <= .05 and x["rms"] <= .10, by_x=x["by_x"], no_fs=Rr["zn1"]["no_fs"], cell={})
        for h in HH:
            v = O[h]["G-OUT-M3"]; ks, Rm = RR[(f, h)]; jj = ns["joint"](O[h], ks, Rm); zt = M3R["Ztot"][f"{f}|{h}"]; tot = math.sqrt(v["s"] ** 2 + sum(zt[t] ** 2 for t in ("gas", "slope", "seed", "m", "nz", "leak"))); o[f]["cell"][h] = dict(Z=v["Z"], pred=v["pred"], meas=v["meas"], s=v["s"], chi2=jj[0], p=jj[2], tot=tot, Ztot=(v["meas"] - v["pred"]) / tot, reach=(float(BASE[(f, h)]) - v["Z"]) / (float(BASE[(f, h)]) - 2))
    return o
def show(lab, name):
    r = rowfor(lab); RES[lab] = r; reach = [c["reach"] for f in r for c in r[f]["cell"].values()]; xs = [r[f]["xok"] for f in r]
    P(f"{name}: " + " | ".join(f"f* {f}: {r[f]['keys']}/15 {r[f]['bad'] if r[f]['keys'] < 15 else ''} M3 {r[f]['cell']['h0672']['Z']:+.2f},{r[f]['cell']['h0686']['Z']:+.2f} Ztot {r[f]['cell']['h0672']['Ztot']:+.2f},{r[f]['cell']['h0686']['Ztot']:+.2f} chi2 {r[f]['cell']['h0672']['chi2']:.1f},{r[f]['cell']['h0686']['chi2']:.1f} p {r[f]['cell']['h0672']['p']:.1e},{r[f]['cell']['h0686']['p']:.1e} X-COP {r[f]['xcop'][0]:+.3f},{r[f]['xcop'][1]:.3f} {'PASS' if r[f]['xok'] else 'FAIL'} no-fs {r[f]['no_fs']}" for f in r) + f" | reach {min(reach):.3f} to {max(reach):.3f}"); return r, reach, xs
def label(reach, r, F, xs):
    cl = all(r[f]["keys"] == 15 for f in r) and all(xs); return "RETENTION CLOSES CLUSTERS" if cl else ("PARTLY" if min(reach) >= 1 / 3 and not F else "NOT RETENTION")
P("\nGas +0.005, 15 keys; cells f* 0.034, 0.0615; h 0.672, 0.686; reach on G-OUT-M3")
lab = {}
for k, n in (("K1 one", "fair share (= ZN4)"), ("H", "H PRIMARY"), ("Hm1s", "H -1 sigma at lg M 14.2"), ("Hp1s", "H +1 sigma"), ("W", "W"), ("Hplusg", "H+g"), ("HgasX", "HG"), ("H noL20", "H without L20"), ("H noL15S09", "H without L15, S09")):
    r, re_, xs = show(k, n); lab[k] = label(re_, r, False, xs)
b = LN["H"]["b"]; sb = LN["H"]["sb"]; se3 = 0.0; c = LN["H"]["cov"]; d = med(M3, "lgM500") - math.log10(qq) - 14.5; se3 = math.sqrt(c[0][0] + 2 * d * c[0][1] + d * d * c[1][1]); P(f"\nSE of line H at M3's lg M500: {se3:.4f}; b {b:+.3f} +- {sb:.3f}; clusters below 14.3: {sum(1 for q in LN['CH'] if q['lgM'] < 14.3)}")
noind = se3 > .04 or sum(1 for q in LN["CH"] if q["lgM"] < 14.3) < 15; re_H = [c["reach"] for f in RES["H"] for c in RES["H"][f]["cell"].values()]; xsH = [RES["H"][f]["xok"] for f in FS]
V = "NO INDEPENDENT MEASUREMENT" if noind else ("NOT RETENTION" if b - sb <= 0 else label(re_H, RES["H"], False, xsH)); tags = []
if not all(xsH): tags.append("[X-COP LOST]")
if lab["W"] != V: tags.append("[MASS-METHOD-DEPENDENT]")
if lab["HgasX"] != V: tags.append("[HG-DEPENDENT]")
if lab["Hm1s"] != V or lab["Hp1s"] != V: tags.append("[ERROR-DEPENDENT]")
P(f"labels: {lab}"); P(f"VERDICT{'' if all(CK.values()) else ' NOT VALID, a check failed'}: {V} {' '.join(tags)}"); RES["verdict"] = V; RES["tags"] = tags; RES["checks"] = {k: bool(v) for k, v in CK.items()}
# line error into Z_tot
ep = cells(J("Hp1s 0.034")); em = cells(J("Hm1s 0.034")); e0 = cells(J("H 0.034")); dln = .5 * (ep["h0672"]["G-OUT-M3"]["pred"] - em["h0672"]["G-OUT-M3"]["pred"]); P(f"\nLine's own 1 sigma in pred {abs(dln):.4f}; Z_tot with it, f* 0.034 h 0.672: {(e0['h0672']['G-OUT-M3']['meas'] - e0['h0672']['G-OUT-M3']['pred']) / math.sqrt(RES['H']['0.034']['cell']['h0672']['tot'] ** 2 + dln ** 2):+.2f}")
o0 = cells(J("K1 one 0.034")); dp = e0["h0672"]["G-OUT-M3"]["pred"] - o0["h0672"]["G-OUT-M3"]["pred"]; fk = RES["M3"]["Mc200"] / RES["M3"]["Mfair"]; P(f"By hand, HM1's rate: pred {o0['h0672']['G-OUT-M3']['pred']:.3f} to {e0['h0672']['G-OUT-M3']['pred']:.3f}, +{dp:.3f}; M_c(R200)/Mfair H {fk:.3f} vs HM1's 0.297 (with h, M3 defined there by key): rate would give +{2.56 * (fk - .297):.3f}")
P("\nPost-result, reported, no label: G-OUT-M3 at f* 0.034, h 0.672, 0.686; keys; X-COP")
for k, n in (("post carry XCOP", "H, X-COP's measured carry +0.031 at R200 in place of GS1's slope + ZN4's shape"), ("post carry XCOP g", "same with H+g"), ("post s2676", "H, tail s 2.676"), ("post s3071", "H, tail s 3.071")):
    r = rowfor(k, ("0.034",)); RES[k] = r; q = r["0.034"]; P(f"  {n}: {q['keys']}/15 {q['bad']}, M3 {q['cell']['h0672']['Z']:+.2f},{q['cell']['h0686']['Z']:+.2f}, Ztot {q['cell']['h0672']['Ztot']:+.2f}, X-COP {q['xcop'][0]:+.3f},{q['xcop'][1]:.3f} by x {q['by_x']}")
for k in ("H 0.034",): P(f"  X-COP by x, H: {J(k)['footings']['canonical']['by_x']}")
P("\nH +0.111, reported only, a scale the data don't support: " + " | ".join(f"f* {f}: {15 - len({k for h in HH for k, v in cells(J(f'H +0.111 {f}'))[h].items() if abs(v['Z']) > 2})}/15, M3 {cells(J(f'H +0.111 {f}'))['h0672']['G-OUT-M3']['Z']:+.2f}" for f in FS))
XT = json.load(open(os.path.join(os.path.dirname(RB), "real_research", "data", "xcop", "xcop_r500_ettori2019.json"))); lmx = float(np.median([math.log10(v["M500"]) + 14 for v in XT.values()])); P(f"\nLine H, derived without X-COP, at X-COP's median lg M500 {lmx:.2f}, h 0.7, f* 0.034: lg Y500 {LN['H']['a'] + LN['H']['b'] * (lmx - 14.5) + math.log10(1.034):+.3f}; X-COP's own measured -0.042 (LF1). Same method, hydrostatic; out of sample in clusters only")
P("Binned H at M3's mass: lg M500 14-14.5 median gas-only lg Y -0.137 +- 0.043 (n 18), line at M3's h 0.7 mass {:+.3f}. dZ(M3)/d lg Y from the +/-1 sigma rows: {:.1f} per dex".format(LN["H"]["a"] + LN["H"]["b"] * (med(M3, "lgM500") - math.log10(qq) - 14.5), (ep["h0672"]["G-OUT-M3"]["Z"] - em["h0672"]["G-OUT-M3"]["Z"]) / (2 * se3)))
# read-across, report only
P("\nRead-across, report only. Y at R200. EM1: M200 total = cold/f_c with cold = 10^(11.18 + 0.90 (lg M_b - 10)). Line H at lg M500 = lg M200 - 0.15 (M3's), +f* 0.034, h 0.672, carry as M3's")
for lb in (10, 11, 12, 12.5, 13, 13.5, 14):
    lgc = 11.18 + .9 * (lb - 10); M2 = lgc - math.log10(5.2715 / 6.2715); y = 6.2715 * 10 ** lb / 10 ** M2; lm5 = M2 - .15; l5 = LN["H"]["a"] + LN["H"]["b"] * (lm5 - math.log10(qq) - 14.5) + math.log10(1.034) + 1.5 * math.log10(qq); P(f"  lg M_b {lb}: EM1 lg M200 {M2:.2f}, Y200 {y:.3f} (lg {math.log10(y):+.3f}); line H Y500 lg {l5:+.3f}, with M3's carry {l5 + math.log10(med(M3, 'carry')):+.3f}; difference line - EM1 {l5 + math.log10(med(M3, 'carry')) - math.log10(y):+.3f}; data at this mass: {'measured' if lm5 >= 13.19 else 'NONE, extrapolated'}")
P("\nOutside R200, M3, H: M_b(<R200) {:.2e}, missing (1 - Y200) f_b M200 = {:.2e}; at Y200 of HM1's Z=2 ({:.3f}): {:.2e}. Gas + stars the grader already has from R200 to r_ta: {:.2e}.".format(med(M3, "Mb200"), (1 - med(M3, "Y200")) * .15945 * 10 ** med(M3, "lgM200"), 6.2715 / 8.4, (1 - 6.2715 / 8.4) * .15945 * 10 ** med(M3, "lgM200"), med(M3, "Mbt") - med(M3, "Mb200")))
json.dump(RES, open(os.path.join(HERE, "fr1_results.json"), "w"), indent=0, default=float); open(os.path.join(HERE, "fr1.out"), "w").write("\n".join(OUT) + "\n")
