#!/usr/bin/env python3
"""B4.4 -- analysis of the line points: gate G-W (windowed estimator WW vs full-range flat-histogram production at L = 4, Amendment 2), gate G-K (pure adjoint SU(2)), G-B2 consistency,
finite-size extrapolation, segment fits, triple point (D-TP), 1/alpha, for SU(2) and SU(3).  Three variants of the input are analysed:
  win  = WW at every L;  mix = production at L = 4 and WW at L >= 6 (the pre-registered fallback if G-W fails);  prod = production at every L (only where available).
The PRIMARY variant is 'win' if G-W passes for the group, else 'mix' (Amendment 2); the other variants are printed.  Writes b4_tp_<grp>_weight.json (primary) and b4_tp_<grp>_weight_<variant>.json.
Run:    python3 b4_analysis.py                exit 0 iff the declared internal gates pass (G-W for each group with matched points, G-K); the physics RESULT is only reported
MUTATE: python3 b4_analysis.py MUTATE         the windowed values are given a +0.02 bias in beta_A (a wrong estimator): G-W must fail -> exit 1; exit 3 otherwise."""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np
import b4_tp as T

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []
PRIMARY_SEG = {"su2": [0.2, 0.3, 0.4, 0.6, 0.7, 0.8], "su3": [0.0, 0.4, 0.8, 1.2, 1.6]}


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def gate_W(grp):
    w = T.load_points(grp, "weight", "win")
    p = T.load_points(grp, "weight", "prod")
    rows = []
    for bF in sorted(w):
        if 4 in w[bF] and bF in p and 4 in p[bF]:
            bw, ew = w[bF][4][0] + (0.02 if MUT else 0.0), w[bF][4][1]
            bp, ep = p[bF][4][0], p[bF][4][1]
            rows.append((bF, bw, ew, bp, ep, (bw - bp) / math.hypot(ew, ep)))
    return rows


for grp in ("su2", "su3"):
    rows = gate_W(grp)
    print(f"\n=== {grp.upper()} ===")
    gw_ok = None
    sig_est = 0.003
    if rows:
        print("  G-W: windowed (WW) vs full-range flat-histogram production at L = 4:")
        for r in rows:
            print(f"     beta_F={r[0]:5.2f}: WW {r[1]:.5f} +- {r[2]:.5f}   production {r[3]:.5f} +- {r[4]:.5f}   diff {r[1] - r[3]:+.5f} ({r[5]:+.1f} sigma)")
        mx = max(abs(r[5]) for r in rows)
        md = float(np.mean([r[1] - r[3] for r in rows]))
        prim = [r for r in rows if r[0] in PRIMARY_SEG[grp]]
        rms = float(np.sqrt(np.mean([(r[1] - r[3]) ** 2 for r in prim]))) if prim else 0.003
        mdp = float(np.mean([r[1] - r[3] for r in prim])) if prim else float("nan")
        gw_ok = mx <= 3.5 and abs(md) <= 0.003
        chk(f"G-W {grp}: every matched L=4 point within 3.5 combined sigma and mean difference <= 0.003", gw_ok,
            f"(max {mx:.1f} sigma over {len(rows)} points; mean WW-production {md:+.5f}; on the primary-segment points only: mean {mdp:+.5f}, rms {rms:.5f}, n={len(prim)})")
        sig_est = max(rms, 0.001)   # Amendment 3 (post hoc): estimator systematic = rms difference over the primary-segment points
    else:
        print("  G-W: no matched points")
    if not MUT:
        w6 = T.load_points(grp, "weight", "win"); p6 = T.load_points(grp, "weight", "prod")
        m6 = [(bF, w6[bF][6], p6[bF][6]) for bF in sorted(p6) if 6 in p6[bF] and bF in w6 and 6 in w6[bF]]
        if m6:
            print("  L = 6 cross-check (non-gating, full-range production vs WW at the same beta_F):")
            for bF, w, p in m6:
                print(f"     beta_F={bF:5.2f}: WW {w[0]:.5f} +- {w[1]:.5f}   production {p[0]:.5f} +- {p[1]:.5f}   diff {w[0] - p[0]:+.5f} ({(w[0] - p[0]) / math.hypot(w[1], p[1]):+.1f} sigma)")
    if MUT:
        continue
    cshift = 0.0
    if grp == "su3":
        has6 = any(6 in v for v in T.load_points(grp, "weight", "win").values())
        cshift = 0.0 if has6 else 0.06   # SU(3): common finite-size shift of all line points assumed within +-0.06 when no L=6 point is used (about 1.5 x the relative SU(2) shift, measured c - x(L=4) = +0.015 at beta_A about 2.5); disclosed in Amendment 3
    res = {}
    for variant in ("win", "mix", "prod"):
        res[variant] = T.analyze(grp, "weight", src=variant, sig_est=sig_est, transfer=True, verbose=False, common_shift=cshift)
        res[variant]["variant"] = variant; res[variant]["sig_est"] = sig_est; res[variant]["gw_ok"] = gw_ok
    # primary: G-W failed -> the pre-registered fallback 'mix' if it can be formed (needs production values on both segments), else 'win' (flagged); G-W passed or unverifiable -> 'win'
    primary = "mix" if (gw_ok is False and res["mix"].get("status") == "IDENTIFIED") else "win"
    res[primary] = T.analyze(grp, "weight", src=primary, sig_est=sig_est, transfer=True, verbose=True, common_shift=cshift)
    res[primary]["variant"] = primary; res[primary]["sig_est"] = sig_est; res[primary]["gw_ok"] = gw_ok
    for variant in ("win", "mix", "prod"):
        r = res[variant]
        json.dump(r, open(os.path.join(HERE, f"b4_tp_{grp}_weight_{variant}.json"), "w"), indent=1, default=str)
        if variant == primary:
            json.dump(r, open(os.path.join(HERE, f"b4_tp_{grp}_weight.json"), "w"), indent=1, default=str)
            if r.get("G_K") is not None:
                chk("G-K pure-adjoint SU(2) beta_c in [2.40, 2.60] (literature about 2.5)", r["G_K"]["ok"], f"({r['G_K']['value']:.4f} +- {r['G_K']['sigma']:.4f})")
        if r.get("status") == "IDENTIFIED":
            print(f"  >>> variant {variant:4s}{' (PRIMARY)' if variant == primary else ''}: triple point ({r['bF']:.4f} +- {r['sF']:.4f}, {r['bA']:.4f} +- {r['sA']:.4f}); 1/alpha(M_P) = {r['inv_expo']:.2f} (not-exp {r['inv_not']:.2f}), lattice +- {r['s_lat']:.2f} ({100 * r['frac_lat']:.1f}%) [stat+FSS {r['s_stat']:.2f}, fit-range {r['s_fit']:.2f}]")
        else:
            print(f"  >>> variant {variant}: not identified ({r.get('why', r.get('status'))})")
if MUT:
    fired = any(t.startswith("G-W") for t in FAILED)
    print("\nMUTATE CONTROL: windowed values biased by +0.02 in beta_A ->", "G-W FAILS as required (exit 1, the control fires)" if fired else "G-W did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)
sys.exit(0 if not FAILED else 1)
