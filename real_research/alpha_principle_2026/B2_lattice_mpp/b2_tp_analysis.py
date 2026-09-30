#!/usr/bin/env python3
"""B2 D-TP analysis: from the stage-2 scan results (b2_2_results.json for SU(2), and the hysteresis maps for SU(3)) locate the lowest first-order line at each beta_F, fit its two
segments (S1: the nearly horizontal one below the kink; S2: the falling one above it), intersect them (definition D-TP of the pre-registration: the triple point is where the single
line splits / where the two segments meet), extrapolate in L, and write b2_2_tp.json / b2_3_tp.json for b2_4.
usage: python3 b2_tp_analysis.py su2|su3      (reads existing files only; no simulation)
Line-position estimators fixed BEFORE looking at the stage-2 numbers:
  W  : if >= 2 runs of the scan are mixed (both phases occupied, 5-95%), the WHAM susceptibility maximum (largest non-edge chi maximum) with its block-jackknife error;
  H  : otherwise the hysteresis bracket [lowest beta_A at which some run is in the high phase, highest beta_A at which some run is in the low phase]; estimate = midpoint, error = half the width (conservative).
The intersection error is a Monte Carlo over Gaussian draws of the line positions (2000 draws).  Segment fits are weighted straight lines.  S2 uses the three points nearest the kink;
alternative S2 = the two points nearest the kink is reported as an extrapolation systematic.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
grp = sys.argv[1] if len(sys.argv) > 1 else "su2"
rng = np.random.default_rng(12345)


def estimate(r):
    """returns (x, err, method) for one scan_line result dict"""
    occ = r["occ"]      # Amendment 8: the W estimator is disabled (WHAM maxima sit on grid points; mixed runs are decaying metastable states)
    xs = sorted(set(o[0] for o in occ))
    high = [o[0] for o in occ if o[2] > 0.5]
    low = [o[0] for o in occ if o[2] <= 0.5]
    if not high or not low:
        return None
    a = min(high)      # cold high phase persists down to here
    b = max(low)       # hot low phase persists up to here
    if b < a:
        a, b = b, a
    return 0.5 * (a + b), max(0.5 * (b - a), 0.5 * (xs[1] - xs[0]) if len(xs) > 1 else 0.01), f"H bracket [{a:.3f}, {b:.3f}]"


def wfit(x, y, s):
    x, y, s = map(np.asarray, (x, y, s))
    A = np.vstack([np.ones_like(x), x]).T
    W = np.diag(1 / s ** 2)
    cov = np.linalg.inv(A.T @ W @ A)
    p = cov @ A.T @ W @ y
    return p


def intersect(S1, S2, ndraw=2000):
    """S1, S2: lists of (bF, x, err).  returns central (bF*, bA*), samples"""
    def one(P1, P2):
        p1 = wfit([p[0] for p in P1], [p[1] for p in P1], [p[2] for p in P1])
        p2 = wfit([p[0] for p in P2], [p[1] for p in P2], [p[2] for p in P2])
        if abs(p1[1] - p2[1]) < 1e-9:
            return None
        bf = (p2[0] - p1[0]) / (p1[1] - p2[1])
        return bf, p1[0] + p1[1] * bf
    c = one(S1, S2)
    smp = []
    for _ in range(ndraw):
        P1 = [(p[0], p[1] + p[2] * rng.normal(), p[2]) for p in S1]
        P2 = [(p[0], p[1] + p[2] * rng.normal(), p[2]) for p in S2]
        o = one(P1, P2)
        if o is not None:
            smp.append(o)
    smp = np.array(smp)
    return c, smp


out = {}
CFG = {"su2": dict(res="b2_2_results.json", S1=(0.0, 0.2, 0.4), S2=(0.6, 0.7, 0.8), S2alt=2, S1alt=(0.0, 0.2), out="b2_2_tp_raw.json"),
       "su3": dict(res="b2_3_results.json", S1=(0.0, 0.4, 0.8), S2=(1.2, 1.6), S2alt=2, S1alt=(0.0, 0.4), out="b2_3_tp_raw.json")}[grp]
res = json.load(open(os.path.join(HERE, CFG["res"])))["stage2"]
S1F, S2F = CFG["S1"], CFG["S2"]
perL = {}
for key, r in res.items():
    kind, L, fixed = key.split("_")[:3]
    prev = perL.setdefault(int(L), {}).get(float(fixed))
    if prev is not None:        # a refined scan of the same line is POOLED with the earlier one (its own window would clip the bracket)
        r = dict(r); r["occ"] = prev[1]["occ"] + r["occ"]; r["nmixed"] = prev[1]["nmixed"] + r["nmixed"]; r["nruns"] = prev[1]["nruns"] + r["nruns"]
    est = estimate(r)
    perL[int(L)][float(fixed)] = (est, r)
for L in sorted(perL):
    print(f"L={L}: line positions")
    for bF in sorted(perL[L]):
        est, r = perL[L][bF]
        print(f"   beta_F={bF:4.2f}: " + (f"beta_A = {est[0]:.4f} +- {est[1]:.4f} [{est[2]}]  (mixed runs {r['nmixed']}/{r['nruns']}, threshold X_A={r['thr']:.3f}, tau_int max {r['tau_max']:.0f}; WHAM maxima {[round(m['x'], 3) for m in r['maxima']]})" if est else "not located"))
if grp == "su3":
    # L=6 line positions from the coarse hysteresis map (step 0.25), same H estimator (Amendment 8): high phase if X_A > 0.4
    mp = json.load(open(os.path.join(HERE, "b2_3_stage1H_L6.json")))["stage1"]
    perL.setdefault(6, {})
    for bF, rows in mp.items():
        occ = []
        for bA, v in rows.items():
            occ.append((float(bA), 1, 1.0 if v[0] > 0.4 else 0.0))     # cold start
            occ.append((float(bA), 2, 1.0 if v[2] > 0.4 else 0.0))     # hot start
        est = estimate(dict(occ=occ, nmixed=0, maxima=[]))
        perL[6][float(bF)] = (est, dict(nmixed=0, nruns=len(occ), thr=0.4, tau_max=0.0, maxima=[]))
tp = {}
for L in sorted(perL):
    S1 = [(bF, *perL[L][bF][0][:2]) for bF in S1F if bF in perL[L] and perL[L][bF][0]]
    S2 = [(bF, *perL[L][bF][0][:2]) for bF in S2F if bF in perL[L] and perL[L][bF][0]]
    if len(S1) < 2 or len(S2) < 2:
        print(f"L={L}: too few points for the two segments (S1 {len(S1)}, S2 {len(S2)}): no intersection")
        continue
    c, smp = intersect(S1, S2)
    S2b = sorted(S2)[:CFG["S2alt"]]
    S1b = [p for p in S1 if p[0] in CFG["S1alt"]]
    c2, _ = intersect(S1, S2b)
    c3, _ = intersect(S1b, S2) if len(S1b) >= 2 else (c, None)
    tp[L] = dict(bF=c[0], bA=c[1], sF=float(0.5 * (np.percentile(smp[:, 0], 84) - np.percentile(smp[:, 0], 16))), sA=float(0.5 * (np.percentile(smp[:, 1], 84) - np.percentile(smp[:, 1], 16))), alt_S2_bF=c2[0], alt_S2_bA=c2[1], alt_S1_bF=c3[0], alt_S1_bA=c3[1], nS1=len(S1), nS2=len(S2))
    print(f"L={L}: triple point (intersection of the S1 and S2 fits) = ({c[0]:.3f} +- {0.5 * (np.percentile(smp[:, 0], 84) - np.percentile(smp[:, 0], 16)):.3f}, {c[1]:.3f} +- {0.5 * (np.percentile(smp[:, 1], 84) - np.percentile(smp[:, 1], 16)):.3f});  alt S2 (two nearest points): ({c2[0]:.3f}, {c2[1]:.3f});  alt S1 ({CFG['S1alt']}): ({c3[0]:.3f}, {c3[1]:.3f})")
out["perL"] = tp
json.dump(out, open(os.path.join(HERE, CFG["out"]), "w"), indent=1)

# ---------------------------------------------------------------------------------------------------------- finite-size treatment and final file
Ls = sorted(tp)
if len(Ls) >= 2:
    La, Lb = Ls[-2], Ls[-1]
    f4 = lambda a, b: b + (b - a) * (1.0 / Lb ** 4) / (1.0 / La ** 4 - 1.0 / Lb ** 4)
    f2 = lambda a, b: b + (b - a) * (1.0 / Lb ** 2) / (1.0 / La ** 2 - 1.0 / Lb ** 2)
    k4 = (1.0 / Lb ** 4) / (1.0 / La ** 4 - 1.0 / Lb ** 4)
    fin = {}
    for name, s_key in (("bF", "sF"), ("bA", "sA")):
        a, b = tp[La][name], tp[Lb][name]
        x4, x2 = f4(a, b), f2(a, b)
        stat = math.hypot((1 + k4) * tp[Lb][s_key], k4 * tp[La][s_key])
        ext = max(abs(x4 - x2), abs(b - a) / 2)
        fin[name] = (x4, stat, ext)
    print(f"\nFinite-size treatment from L={La}, {Lb} (x + b/L^4; alternative x + b/L^2; sigma_ext = max(|diff|, |x_Lb - x_La|/2)):")
    for name in ("bF", "bA"):
        print(f"   {name}: infinity = {fin[name][0]:.4f}   stat {fin[name][1]:.4f}   ext {fin[name][2]:.4f}   total {math.hypot(fin[name][1], fin[name][2]):.4f}   (L={La}: {tp[La][name]:.4f}, L={Lb}: {tp[Lb][name]:.4f})")
    ident = all(tp[L]["nS1"] >= 2 and tp[L]["nS2"] >= 2 for L in (La, Lb))
    res_out = dict(status="IDENTIFIED" if ident else "UNDECIDED", bF=fin["bF"][0], bA=fin["bA"][0], sF=math.hypot(fin["bF"][1], fin["bF"][2]), sA=math.hypot(fin["bA"][1], fin["bA"][2]),
                   perL=tp, Ls=[La, Lb], why="" if ident else "too few points")
    json.dump(res_out, open(os.path.join(HERE, "b2_%s_tp.json" % ("2" if grp == "su2" else "3")), "w"), indent=1)
    print("   written; status", res_out["status"])
