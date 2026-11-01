#!/usr/bin/env python3
"""DR3 reader: checks, frozen labels, effective response, LC1 read-across. FROZEN_CRITERIA.md ca7006d189. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*matmul.*")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); TG = ("A_c2b_refit", "B_cfg886_bg"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
R = json.load(open(os.path.join(HERE, "dr3_PRIMARY_results.json"))); M = json.load(open(os.path.join(HERE, "dr3_MUTATE_results.json"))); GI = json.load(open(os.path.join(HERE, "dr3_GASINV_results.json"))); N = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json"))); ok = True; run = R["runs"]; P("DR3: true disc monopole in SPARC's contraction, GB kept as force; kappa = 1/2 FITTED, unused; not theory closed")
def dS(a, b): return max(max(abs(a[t][k] - b[t][k]) for k in ("U", "rms", "tilt")) + 0 for t in TG), max(abs(a[t]["bins"][k] - b[t]["bins"][k]) for t in TG for k in a[t]["bins"])
k1 = [dS(run[a]["sparc"], N["runs"][b]["sparc"]) for a, b in (("EM1|off", "EM1|off"), ("OFF|blum", "EM1|blum"))]; v = max(max(x) for x in k1) <= 1e-6; ok &= v; P(f"K1 DR3 off vs NR3 MEDIAN: {k1}: {'PASS' if v else 'FAIL'}")
# K2, K3, Freeman
from scipy.special import i0e, i1e, k0e, k1e
x = np.array([1.0, 2.0, 5.0]); Rf = np.linspace(0.005, 12, 2400); sb = np.exp(-Rf); c = np.cumsum(np.r_[0.5 * sb[0] * Rf[0] ** 2, 0.5 * (sb[1:] * Rf[1:] + sb[:-1] * Rf[:-1]) * np.diff(Rf)]); T = 1 - (1 + x) * np.exp(-x); d = np.abs(np.interp(x, Rf, c) - T); v = d.max() <= 1e-3; ok &= v; P(f"K2 integrator on an exponential: |d| {d.max():.1e}: {'PASS' if v else 'FAIL'}")
xx = np.array([0.5, 1.0, 2.2, 5.0, 10.0]); y = xx / 2; rot = 2 * xx * y * y * (i0e(y) * k0e(y) - i1e(y) * k1e(y)); mono = 1 - (1 + xx) * np.exp(-xx); r_ = rot / mono; v = r_[0] < 1 and r_[2] > 1 and r_[3] > 1; ok &= v; P("K3 Freeman, GB r^2/G over monopole at x " + ", ".join(f"{a:g}: {b:.3f}" for a, b in zip(xx, r_)) + f": {'PASS' if v else 'FAIL'}")
v = abs(R["K4_L_ratio"] - 1) <= 0.15; ok &= v; P(f"K4 SB integrated over L[3.6], median {R['K4_L_ratio']:.3f} (16-84 {R['K4_L_ratio_16_84'][0]:.3f}, {R['K4_L_ratio_16_84'][1]:.3f}): {'PASS' if v else 'FAIL'}; gas: {R['gas_counts']}")
def clu(a, b):
    p = max(abs(a["keys"]["preds"][h][k] - b["keys"]["preds"][h][k]) for h in a["keys"]["preds"] for k in a["keys"]["preds"][h]); return max(p, abs(a["xcop"]["mean"] - b["xcop"]["mean"]), abs(a["groups"]["Z"] - b["groups"]["Z"]), abs(a["lt"][TG[0]] - b["lt"][TG[0]]))
k5 = [clu(run["DR3|blum"], run["OFF|blum"]), clu(run["DR3|gnedin"], run["OFF|gnedin"])]; v = max(k5) <= 1e-6; ok &= v; P(f"K5 preds, X-COP, groups, LT DR3 vs off: {k5}: {'PASS' if v else 'FAIL'}")
mu = M["runs"]["DR3|blum|MUT2"]["sparc"][TG[0]]; base = run["DR3|blum"]["sparc"][TG[0]]; v = abs(mu["U"] - base["U"]) >= 0.02; ok &= v; P(f"MUTATE monopole x 2: U {base['U']:.2f} -> {mu['U']:.2f}, bins {[round(a, 3) for a in mu['bins'].values()]}: {'BITES' if v else 'FAIL'}")
k6 = abs(GI["runs"]["DR3|blum"]["sparc"][TG[0]]["U"] - base["U"]) + abs(GI["runs"]["DR3|blum"]["sparc"][TG[0]]["rms"] - base["rms"]); v = k6 <= 1e-9; ok &= v; P(f"Rerun in the stress process, DR3|blum |d| {k6:.1e}: {'PASS' if v else 'FAIL'}")
def row(n, r):
    a, b = r["sparc"][TG[0]], r["sparc"][TG[1]]; P(f"{n:15s} U {a['U']:.2f}/{b['U']:.2f} rms {a['rms']:.4f}/{b['rms']:.4f} tilt {a['tilt']:+.2f}/{b['tilt']:+.2f} bins A {[round(x, 3) for x in a['bins'].values()]} B {[round(x, 3) for x in b['bins'].values()]} keys {r['keys']['n']} {r['keys']['bad']} groups {r['groups']['Z']:+.2f} X-COP {r['xcop']['mean']:+.3f},{r['xcop']['rms']:.3f} LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}")
P("\nRows, MEDIAN")
for n, r in run.items(): row(n, r)
for n in ("GASINV|blum", "GASINV|gnedin", "GASINVxFQ|blum"): row(n + " (stress)", GI["runs"][n])
P(f"stress inversion: median V^2 fit rms {GI['gasinv_fit_rms_median']:.4f}; gas M inverted over V_gas^2 r/G {GI['gasinv_ratio_to_vg2r']}")
PIN = ("150-200", "200-250")
def label(on, off):
    a, o = on["sparc"], off["sparc"]; half = all(a[t]["bins"][b] >= o[t]["bins"][b] + 0.5 * (0.50 - o[t]["bins"][b]) for t in TG for b in PIN); mv = max(abs(a[t]["bins"][b] - o[t]["bins"][b]) for t in TG for b in PIN); clr = all(a[t]["rms"] <= 0.110 and 0.5 <= a[t]["U"] <= 0.8 and abs(a[t]["tilt"]) <= 0.15 and abs(on["lt"][t]) <= 0.10 for t in TG) and on["groups"]["verdict"] == "CONSISTENT"
    return "SPARC SIDE CLEARS" if clr else "HALVED, STILL FAILS" if half else "NOT HALVED, MOVES" if mv >= 0.02 else "NO MOVE"
L = {m: label(run[f"DR3|{m}"], run[f"OFF|{m}"]) for m in ("blum", "gnedin")}; Ls = {m: label(GI["runs"][f"GASINV|{m}"], run[f"OFF|{m}"]) for m in ("blum", "gnedin")}; P(f"\nFROZEN LABELS: Blumenthal {L['blum']}; Gnedin {L['gnedin']}. Stress, measured gas: {Ls}")
P("\nEffective response, (Q_DR3 - 1)/(Q_off - 1) at r0, 2, 3, 4 R_d; M_b monopole over GB r^2/G; bg A, Y 0.5")
for k, a in R["eff"].items(): P(f"  {k} (n {a['n']}) ratio {[round(x, 2) for x in a['ratio']]} M_b {[round(x, 2) for x in a['mb']]}")
# LC1 read-across, same-seed particles
sys.argv = ["x"]; src = open(os.path.join(RB, "LC1_live_contraction", "lc1_read.py")).read(); src = src[:src.index('if __name__ == "__main__":')]; ns = {"__file__": os.path.join(RB, "LC1_live_contraction", "lc1_read.py"), "__name__": "lc1h"}; exec(compile(src, "lc1h", "exec"), ns); contract, cr = ns["contract"], ns["cr"]
LCJ = json.load(open(os.path.join(RB, "LC1_live_contraction", "lc1_results.json")))["pairs"]["0.00"]; ZN = ns.get("ZN1R") or os.path.join(RB, "ZN1_zooms_to_z0", "runs"); out = []; I = [1, 2, 3]; RDG = ns["RDG"]
for s, p in LCJ.items():
    B_ = np.load(os.path.join(ZN, s, "snap_z0.00.npz"), allow_pickle=False); m0 = float(B_["m"]); rB = cr(B_["x"], m0); Md, Ms = p["Md"], p["Msim"]; Rd = 3.565e-3; f = Md / Ms; rg = np.geomspace(1e-5, float(rB[-1]), 6000); M0 = (1 - f) * m0 * np.searchsorted(rB, rg); F = Md / (Ms - Md); rr = RDG * Rd; M0r = np.interp(np.log(rr), np.log(rg), M0)
    def Q(Mb): return np.interp(np.log(rr), np.log(rg), contract(rg, Mb, M0, F)[0]) / M0r
    QK = Q(Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2))); aa = Rd + 0.2 * Rd; QR = Q(np.maximum.accumulate(Md * rg ** 3 / (rg ** 2 + aa ** 2) ** 1.5)); xe = rg / Rd; QEm = Q(Md * (1 - (1 + xe) * np.exp(-xe))); ye = np.minimum(xe / 2, 300); QEr = Q(np.maximum.accumulate(2 * Md * xe * ye * ye * (i0e(ye) * k0e(ye) - i1e(ye) * k1e(ye)))); ql = np.array(p["Q"]); out.append(dict(dK=float(np.max(np.abs(QK[I] / np.array(p["QB"])[I] - 1))), f_mono=float(np.median((ql[I] - 1) / (QK[I] - 1))), f_rot=float(np.median((ql[I] - 1) / (QR[I] - 1))), mr=float(np.median((QK[I] - 1) / (QR[I] - 1))), er=float(np.median((QEm[I] - 1) / (QEr[I] - 1))), f_expm=float(np.median((ql[I] - 1) / (QEm[I] - 1)))))
dK = max(o["dK"] for o in out); P(f"\nLC1 read-across: {len(out)} seeds, Q_Blumenthal reproduced max |d| {dK:.1e} at 2,3,4 R_d")
RC = {}
if dK <= 0.05:
    g = lambda k: np.array([o[k] for o in out]); RC = {k: [float(np.median(g(k))), float(g(k).min()), float(g(k).max())] for k in ("f_mono", "f_rot", "mr", "er", "f_expm")}; P(f"  f_Q against the Kuzmin monopole (LC1's own) {RC['f_mono']}; live against v^2 r/G of the same disc {RC['f_rot']}; monopole over rotation-mass response, same disc, Kuzmin {RC['mr']}, exponential {RC['er']}; live against an exponential's monopole {RC['f_expm']}")
    sp = [R["eff"][b]["ratio"][1:] for b in ("150-200", "200-250", "250-400")]; dr = float(np.median(sp)); P(f"  DR3's ratio on SPARC, spirals at 2-4 R_d median {dr:.2f}. Inside LC1's live range against rotation mass [{RC['f_rot'][1]:.2f}, {RC['f_rot'][2]:.2f}]: {RC['f_rot'][1] <= dr <= RC['f_rot'][2]}"); RC["dr3_ratio"] = dr
V = "NOT DECIDED" if not ok else f"Blumenthal {L['blum']}; Gnedin {L['gnedin']}"; P(f"\nVERDICT: {V}"); json.dump(dict(verdict=V, labels=L, stress_labels=Ls, checks_ok=bool(ok), lc1=RC), open(os.path.join(HERE, "dr3_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "dr3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
