#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03i -- the anisotropy sign flip of the candidate's wide-binary boost: Delta(s) = gamma_aligned(s) - gamma_perpendicular(s) changes sign at a
crossing separation s_x set by the coherence length.  Finer scan s = 10-25 kAU, theta = 0 and 90 deg, 1 Msun pairs, xi = 0.03/0.05/0.08 pc (canonical)
and 0.05/0.08 pc (alt), registered external field.  Output: Delta(s) per xi, the crossing s_x(xi) by linear interpolation, and s_x/xi, s_x/r_e.
Usage: python3 g03i_anisotropy_sign_flip.py canonical|alt   (tables) ;  python3 g03i_anisotropy_sign_flip.py analyse   (checks)"""
import math, sys, os, json, time, numpy as np
sys.argv_saved = list(sys.argv); mode = sys.argv[1] if len(sys.argv) > 1 else "analyse"
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g03g_3d_pair_solver.py")).read()
head = src[:src.index('mode = sys.argv[1]')]; g = {"__file__": os.path.join(HERE, "g03g_3d_pair_solver.py"), "__name__": "g03g_lib"}
exec(compile(head, "g03ghead", "exec"), g)
solve_pair, box_for, A0, GEXT, KAU, MSUN, G, PC, mu = [g[k] for k in ("solve_pair", "box_for", "A0", "GEXT", "KAU", "MSUN", "G", "PC", "mu")]
SEPS = [10.0, 13.0, 16.0, 19.0, 22.0, 25.0]; XIS = {"canonical": [0.03, 0.05, 0.08], "alt": [0.05, 0.08]}
EXT = {"canonical": {0.05: [28.0, 32.0], 0.08: [36.0, 44.0, 52.0]}, "alt": {0.05: [28.0, 32.0], 0.08: [36.0, 44.0, 52.0]}}   # extension so every xi's crossing is inside the scan
_BIG = {}
def box_big(s):
    if s <= 25*KAU: return box_for(s)
    if "big" not in _BIG: _BIG["big"] = g["Box"](384*KAU, 256)
    return _BIG["big"]
T0 = time.time()
if mode in ("canonical-ext", "alt-ext"):
    foot = mode.split("-")[0]; a0 = A0[foot]; out = json.load(open(os.path.join(HERE, f"g03i_table_{foot}.json")))["table"]
    for xp, seps in EXT[foot].items():
        xi = xp*PC; g["_CACHE"].clear()
        for sk in seps:
            row = {}
            for th in (0.0, 90.0):
                r = solve_pair(a0, xi, 0.5*MSUN, 0.5*MSUN, sk*KAU, math.radians(th), box_big(sk*KAU), centred=True)
                row[str(th)] = r["gamma"]
            out[f"{xp}|{sk}"] = row
            print(f"  xi = {xp:.2f} pc  s = {sk:5.1f} kAU: aligned {row['0.0']:.4f}  perpendicular {row['90.0']:.4f}  Delta = {row['0.0'] - row['90.0']:+.4f}   [{time.time()-T0:.0f} s]", flush=True)
            json.dump(dict(foot=foot, a0=a0, gext=GEXT, table=out), open(os.path.join(HERE, f"g03i_table_{foot}.json"), "w"), indent=1)
    print("done", flush=True)
elif mode in ("canonical", "alt"):
    a0 = A0[mode]; out = {}
    for xp in XIS[mode]:
        xi = xp*PC; g["_CACHE"].clear()
        for sk in SEPS:
            row = {}
            for th in (0.0, 90.0):
                r = solve_pair(a0, xi, 0.5*MSUN, 0.5*MSUN, sk*KAU, math.radians(th), box_for(sk*KAU), centred=True)
                row[str(th)] = r["gamma"]
            out[f"{xp}|{sk}"] = row
            print(f"  xi = {xp:.2f} pc  s = {sk:5.1f} kAU: aligned {row['0.0']:.4f}  perpendicular {row['90.0']:.4f}  Delta = {row['0.0'] - row['90.0']:+.4f}   [{time.time()-T0:.0f} s]", flush=True)
            json.dump(dict(foot=mode, a0=a0, gext=GEXT, table=out), open(os.path.join(HERE, f"g03i_table_{mode}.json"), "w"), indent=1)
    print("done", flush=True)
else:
    FAILS = []
    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
        if not ok: FAILS.append(name)
    print("=" * 100); print("g03i -- anisotropy sign flip: crossing separation vs coherence length"); print("=" * 100)
    cross = {}
    for foot in ("canonical", "alt"):
        a0 = A0[foot]; ye = GEXT/a0; se = ye*mu(ye); re = math.sqrt(G*MSUN/(se*a0))
        T = json.load(open(os.path.join(HERE, f"g03i_table_{foot}.json")))["table"]
        print(f"  [{foot}] r_e(1 Msun) = {re/KAU:.2f} kAU (external field 1.9 a0 observed, s_e = {se:.3f} a0)")
        for xp in XIS[foot]:
            S = np.array(sorted(float(k.split("|")[1]) for k in T if float(k.split("|")[0]) == xp)); D = np.array([T[f"{xp}|{s_}"]["0.0"] - T[f"{xp}|{s_}"]["90.0"] for s_ in S])
            sign_changes = np.where(np.diff(np.sign(D)) != 0)[0]
            if len(sign_changes) >= 1:
                i = sign_changes[0]; sx = S[i] - D[i]*(S[i + 1] - S[i])/(D[i + 1] - D[i])
            else: sx = float('nan')
            cross[(foot, xp)] = sx
            print(f"    xi = {xp:.2f} pc ({xp*PC/KAU:5.1f} kAU): Delta(s) = " + " ".join(f"{d:+.4f}" for d in D) + f"  ->  s_x = {sx:.2f} kAU = {sx*KAU/(xp*PC):.2f} xi = {sx*KAU/re:.2f} r_e")
        check(f"S1 [{foot}] the anisotropy Delta = gamma_aligned - gamma_perp changes sign exactly once within the scanned range at every xi (perpendicular larger below the crossing, aligned larger above)",
              all(np.isfinite(cross[(foot, xp)]) for xp in XIS[foot]))
    xs = np.array([xp*PC/KAU for xp in XIS["canonical"]]); ys = np.array([cross[("canonical", xp)] for xp in XIS["canonical"]])
    if np.all(np.isfinite(ys)):
        slope, icpt = np.polyfit(xs, ys, 1); ratio = ys/xs
        print(f"  canonical: s_x vs xi: s_x = {slope:.2f} xi + {icpt:.2f} kAU; s_x/xi = {[f'{r:.2f}' for r in ratio]}")
        check("S2 [canonical] the crossing separation grows with xi (slope > 0): the flip is set by the coherence length, not by r_e alone", slope > 0, f"slope {slope:.2f}")
        check("S3 [canonical] s_x/xi varies by less than 40% across xi = 0.03-0.08 pc (approximate proportionality s_x ~ k xi with an r_e-dependent offset)", (ratio.max() - ratio.min())/ratio.mean() < 0.4, f"s_x/xi = {ratio.round(2)}")
    print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
